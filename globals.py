#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Global Objects and Variables

Authors: Julius Susanto and Tom Walker
Last edited: January 2014
"""

import numpy as np
import simplejson as json
import sys

def init():
    global no_sections
    global sections
    global tower_data
    global pipe_data
    global network_data
    
    no_sections = 10
    sections = np.array([[200.0, 50.0, 1.0, 100.0], 
                        [250.0, 50.0, -1.0, 100.0],
                        [200.0, 50.0, -1.0, 100.0],
                        [200.0, 70.0, -1.0, 100.0],
                        [200.0, 75.0, -1.0, 100.0],
                        [200.0, 80.0, -1.0, 100.0],
                        [200.0, 70.0, -1.0, 100.0],
                        [200.0, 90.0, -1.0, 100.0],
                        [200.0, 110.0, -1.0, 100.0],
                        [200.0, 150.0, 1.0, 100.0]])
    
    
    tower_data = {
        "L_ab"              : 4.0,
        "L_ac"              : 1.0,
        "L_aw"              : 2.0,
        "H_a"               : 15.0,
        "H_b"               : 18.0,
        "H_c"               : 21.0,
        "H_w"               : 25.0,
        "Z_w"                : 0.2741 + 0.2406j
        }
    
    pipe_data = {
        "diameter"          : 0.5,
        "pipe_rho"          : 0.00000018,
        "pipe_mu"           : 300.0,
        "soil_rho"          : 100.0,
        "coat_thickness"    : 0.0013,
        "coat_rho"          : 50000000.0,
        "coat_mu"           : 5.0
        }
        
    network_data = {
        "freq"              : 50.0,
        "current_a"         : 100.0,     
        "angle_a"           : 0.0,
        "current_b"         : 100.0,     
        "angle_b"           : 120.0,
        "current_c"         : 100.0,     
        "angle_c"           : -120.0,
        "fault_current"     : 20.0,
        "split_factor"      : 0.7,
        "shield_factor"     : 0.8
        }


    global filename   
    filename = ""    
    


def write_project_to_file(fname, data = False, readable = True):
    """Write project settings and data to file.  Uses simplejson library.
    
    File is stored in human readable(ish) format.  We can make this compact by removing whitespace from
    indent and separators.  This is an option in case we start getting huge file sizes.
    
    :param fname: String of file (name and path) to write to.
    :type fname: String
    :param data: Optional argument.  Dictionary of data to write to file.  If not supplied the function will read from globals.
    :param type: Dictionary
    :param readable: Optional argument.  True if output should be formatted to be more easily readable.
    :type readable: Boolean
    :returns: True if the write was successful."""    
    global filename
    global no_sections    
    if not data:    
        data = dict()    
        if no_sections != len(sections):
            no_sections = len(sections)
        data['no_sections'] = no_sections
        data['sections'] = sections
        data['tower_data'] = tower_data
        data['pipe_data'] = pipe_data
        data['network_data'] = network_data         
    try:
        fp = open(fname, mode = 'w')
        if readable:
            json.dump(data, fp, cls=NumpyJSONEncoder, indent = "  ", separators=(',', ': '), sort_keys = True)
        else:
            json.dump(data, fp, cls=NumpyJSONEncoder, indent = 2, separators=(',',':'))
        fp.close()
        filename = fname
    except:
        return False
    return True
    


def load_project_from_file(fname, populate = True):
    """Load project settings and data from file.  Uses simplejson library.
    Global variables will be populated from data in file unless otherwise directed.
    
    Checks that input data is numerical however does not ensure it is within standard boundaries.
    
    :param fname: String of file (name and path) to read from.
    :type fname: String
    :param populate: Boolean indicating if read data should be populated into global variables.
    :type populate: Boolean
    :returns: Dictionary of data if read was successful, otherwise returns False.
    """
    global no_sections
    global sections
    global tower_data
    global pipe_data
    global network_data
    global filename
    try:
        fp = open(fname, mode = 'r')
        data = json.load(fp, object_hook = NumpyJSONDecoder)
        fp.close    
        filename = fname
        if populate:
            no_sections = data['no_sections']
            sections = data['sections']
            tower_data = data['tower_data']
            pipe_data = data['pipe_data']
            network_data = data['network_data']
            if no_sections != len(sections):
                no_sections = len(sections)
    except:
        print(sys.exc_info()[0], sys.exc_info()[1])
        return False
    return data
    

class NumpyJSONEncoder(json.JSONEncoder):
    """JSON encoder to support encoding of Numpy arrays and complex numbers."""
    def default(self, obj):
        """Default is called by JSONEncoder for serialisation of data.
           Passes back to core default method if not Numpy data."""
        if isinstance(obj, np.complex):
            return dict(__npcomplex__=True, real=obj.real, imag=obj.imag)            
        if isinstance(obj, np.ndarray):
            return dict(__nparray__=True, data=obj.tolist())
        return json.JSONEncoder.default(self, obj)

def NumpyJSONDecoder(dct):
    """Decoder function to support Numpy data encoded by NumpyJSONEncoder."""
    if '__npcomplex__' in dct:
        return np.complex(dct['real'], dct['imag'])
    if '__nparray__' in dct:
        return np.array(dct['data'])
    return dct
