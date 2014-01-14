# -*- coding: utf-8 -*-
"""
Test harness module

Helper functions for batch testing.

@author: Tom Walker
@lastupdate: 2014-01-01
"""

import numpy as np
import sys

def equivalent(a, b, eps = 1e-4):
    "Equivalence test. Check if a and b are within epsilon tolerance."    
    return abs(a-b) <= eps

def test_case(function, inputs, outputs, eps = 1e-4, verbose = False, number = 0, name = "", description = ""):
    """Test the result of a function for a given set of inputs and expected set of outputs.
    
    Outputs are flattened to a 1-D array prior to calculating difference for success checking.
    Verbose output will not display flattened arrays.
    
    :param function: function to test
    :type function: function
    :param inputs: inputs to pass to function
    :type inputs: list of inputs
    :param outputs: expected result of function
    :type outputs: list
    :param eps: maximum tolerance for successful test (optional)
    :type eps: float
    :param verbose: provide more detail of text results (optional)
    :type verbose: boolean
    
    :returns: results of call to test function
    :rtype: numpy array containing results of function call
    """   
    if number:
        print("TEST ", number, ": ", name, sep = '')
    else:
        print("TEST:", name)
    if verbose and len(description) > 0:
        print(description)       
        print("Calling",function,"with inputs",inputs)
    success = False
    try:
        result = np.array(function(*inputs))
        outputs = np.array(outputs)
        if verbose:
            print("Expected output", outputs)
            print("Received output", result)
            print("Tolerable difference",eps)
        if np.prod(result.shape) != np.prod(outputs.shape):
            if verbose:
                print("Result differs from length of expected output.")
        else:
            if verbose:
                print("Actual difference",abs(result - outputs))
            result = result.flatten()
            outputs = outputs.flatten()                        
            success = [equivalent(result[j], outputs[j], eps) for j in range(len(result))]           
    except:
        if verbose:        
            print("Test resulted in error: ", sys.exc_info()[0], sys.exc_info()[1])        
    status = "TEST "
    if number:
        status = status + str(number) + " "
    if all(success):        
        status = status + "PASSED."
    else:
        status = status + "FAILED."
    print(status)
    return result

