# -*- coding: utf-8 -*-
"""
Tests for Save/Load functions

@author: Tom Walker
@lastupdate: 2014-01-21
"""


from globals import *
from test_harness import *

init()

name = "Test encode/decode of default global values"
description = "Tests simplejson serialisation (using custom encoder NumpyJSONEncoder) and decoding (custom object hook NumpyJSONDecoder) of global variables.  Serialisation performed to string only."
data = dict()    
data['no_sections'] = no_sections
data['sections'] = sections
data['tower_data'] = tower_data
data['pipe_data'] = pipe_data
data['network_data'] = network_data
def function11(data):
    return json.dumps(data, cls=NumpyJSONEncoder)
def function12(data):
    return json.loads(data, object_hook=NumpyJSONDecoder)    
test_case_two_stage(function11, function12, data, data, verbose = False, number = 1, name = name, description = description)


name = "Test save and load of data set."
description = "Tests writing and loading from disk.  Uses provided data only and does not touch global variables."
filename = '.\data.txt'
data = dict()    
data['no_sections'] = no_sections
data['sections'] = sections
data['tower_data'] = tower_data
data['pipe_data'] = pipe_data
data['network_data'] = network_data
def function21(junk):
    return write_project_to_file(filename, data = data)
def function22(junk):
    return load_project_from_file(filename, populate = False)    
test_case_two_stage(function21, function22, data, data, verbose = False, number = 2, name = name, description = description)

name = "Test save and load of data set (from memory)."
description = "Tests writing and loading from disk.  This time uses global variables.  Only uses supplied data for testing output."
filename = '.\data.txt'
data = dict()    
data['no_sections'] = no_sections
data['sections'] = sections
data['tower_data'] = tower_data
data['pipe_data'] = pipe_data
data['network_data'] = network_data
def function31(junk):
    return write_project_to_file(filename)
def function32(junk):
    return load_project_from_file(filename)    
test_case_two_stage(function31, function32, False, data, verbose = False, number = 3, name = name, description = description)
