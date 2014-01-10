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
    sections = np.array([[200, 50, 1], 
                        [250, 50, -1],
                        [200, 50, -1],
                        [200, 70, -1],
                        [200, 75, -1],
                        [200, 80, -1],
                        [200, 70, -1],
                        [200, 90, -1],
                        [200, 110, -1],
                        [200, 150, 1]])
    
    
    tower_data = {
        "L_ab"              : 4,
        "L_ac"              : 1,
        "L_aw"              : 2,
        "H_a"               : 15,
        "H_b"               : 18,
        "H_c"               : 21,
        "H_w"               : 25,
        "Z_w"                : 0.2741 + 0.2406j
        }
    
    pipe_data = {
        "diameter"          : 0.5,
        "pipe_rho"          : 0.00000018,
        "pipe_mu"           : 300,
        "soil_rho"          : 100,
        "coat_thickness"    : 0.0013,
        "coat_rho"          : 50000000,
        "coat_mu"           : 5
        }
        
    network_data = {
        "freq"              : 50,
        "current_a"         : 100,     
        "angle_a"           : 0,
        "current_b"         : 100,     
        "angle_b"           : 120,
        "current_c"         : 100,     
        "angle_c"           : -120,
        "fault_current"     : 20,
        "split_factor"      : 0.7,
        "shield_factor"     : 0.8
        }
    