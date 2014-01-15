#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Global Objects and Variables

Author: Julius Susanto
Last edited: January 2014
"""

import numpy as np

def init():
    global no_sections
    global sections
    global tower_data
    global pipe_data
    global network_data
    
    no_sections = 10
    sections = np.array([[200.0, 50.0, 1.0], 
                        [250.0, 50.0, -1.0],
                        [200.0, 50.0, -1.0],
                        [200.0, 70.0, -1.0],
                        [200.0, 75.0, -1.0],
                        [200.0, 80.0, -1.0],
                        [200.0, 70.0, -1.0],
                        [200.0, 90.0, -1.0],
                        [200.0, 110.0, -1.0],
                        [200.0, 150.0, 1.0]])
    
    
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
    