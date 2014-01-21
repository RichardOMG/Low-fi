# -*- coding: utf-8 -*-
"""
Tests for AS4853 module

Tests are based on sample calculations given in AS4853 appendices.  
Values are rounded for print purposes.  In some cases this has required tolerances to be increased for tests to pass.

@author: Tom Walker
@lastupdate: 2013-12-31
"""


from AS4853 import *
from test_harness import *
import cmath

name = "Earth return current depth calculation"
description = "Example as per AS4853:2012 Appendix C2 (pg 77, De calculation)"
test_case(earth_return_current_depth,[100.0,50.0],931.08,eps = 1e-2, number = 1, name = name, description = description)

name = "Mutual impedance equation - single values"
description = "Example as per AS4853:2012 Appendix C2 (pg 77, Z1p calculation)"
test_case(mutual_impedance,[931.08,23.15],complex(0.04935,0.2321),eps = 1e-3, number = 2, name = name, description = description)

name = "Load LFI Mutual Impedance calculation - no overhead earthwire"
description = "Example as per AS4853:2012 Appendix B2 (pg 71, Zap, Zbp, Zcp calculations)"
arguments = [[[12, 12, 12]],
             [[23, 15, 7]],
             [],
             [],
             [],
             [],
             100.0,
             50.0]
expected_results = [[complex(0.04935,0.225), complex(0.04935,0.2438), complex(0.04935,0.2642)]]
test_case(mutual_impedances_load_LFI, arguments, expected_results, eps = 1e-3, number = 3, name = name, description = description)

name = "Load LFI Induced Voltage per unit length calculation - no overhead earthwire"
description = "Example as per AS4853:2012 Appendix B2 (pg 71, Vp calculation)"
arguments = [[[complex(0.04935,0.225), complex(0.04935,0.2438), complex(0.04935,0.2642)]],
             [[500 * complex(1,0), 500 * complex(math.cos(math.radians(-120)), math.sin(math.radians(-120))), 500 * complex(math.cos(math.radians(120)), math.sin(math.radians(120)))]],
             1.0]
expected_results = [16.9 * complex(math.cos(math.radians(-121.4)), math.sin(math.radians(-121.4)))]
test_case(induced_voltage_load_LFI_per_length, arguments, expected_results, eps = 1e-1, number = 4, name = name, description = description)

name = "Load LFI Induced Voltage calculation - no overhead earthwire"
description = "Example as per AS4853:2012 Appendix B2 (pg 71, Vp calculation)"
arguments = [[[complex(0.04935,0.225), complex(0.04935,0.2438), complex(0.04935,0.2642)]],
             [[500 * complex(1,0), 500 * complex(math.cos(math.radians(-120)), math.sin(math.radians(-120))), 500 * complex(math.cos(math.radians(120)), math.sin(math.radians(120)))]],
             10,             
             1.0]
expected_results = [169 * complex(math.cos(math.radians(-121.4)), math.sin(math.radians(-121.4)))]
test_case(induced_voltage_load_LFI, arguments, expected_results, eps = 1, number = 5, name = name, description = description)

# Test xx: Pending test data for Load LFI with overhead earth wire.


name = "Fault LFI Mutual Impedance calculation - two overhead earthwires"
description = "Example as per AS4853:2012 Appendix C2 (pg 77, 78)"
arguments = [[[12, 13, 12]],
             [[12.5, 20, 27.5]],
             [25, 25],
             [13.5, 26.5],
             0.912 * complex(math.cos(math.radians(-7.4)), math.sin(math.radians(-7.4))),
             100.0,
             50.0]
expected_results = [complex(0.04935, 0.2321), 0.917 * complex(math.cos(math.radians(-6.59)), math.sin(math.radians(-6.59)))]
test_case(mutual_impedance_fault_LFI, arguments, expected_results, eps = 1e-3, number = 6, name = name, description = description)

name = "Fault LFI Induced Voltage per unit length calculation - two overhead earthwires"
description = "Example as per AS4853:2012 Appendix C2 (pg 77, 78)"
arguments = [complex(0.04935, 0.2321),
             1500,
             0.917 * complex(math.cos(math.radians(-6.59)), math.sin(math.radians(-6.59)))]
expected_results = [326.4 * complex(math.cos(math.radians(78 - 6.59)), math.sin(math.radians(78 - 6.59)))]
test_case(induced_voltage_fault_LFI_per_length, arguments, expected_results, eps = 1e-1, number = 7, name = name, description = description)

name = "Fault LFI Induced Voltage calculation - two overhead earthwires"
description = "Example as per AS4853:2012 Appendix C2 (pg 77, 78)"
arguments = [complex(0.04935, 0.2321),
             1500,
             10,
             0.917 * complex(math.cos(math.radians(-6.59)), math.sin(math.radians(-6.59)))]
expected_results = [3264 * complex(math.cos(math.radians(78 - 6.59)), math.sin(math.radians(78 - 6.59)))]
test_case(induced_voltage_fault_LFI, arguments, expected_results, eps = 1, number = 8, name = name, description = description)
