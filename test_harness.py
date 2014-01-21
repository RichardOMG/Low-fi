# -*- coding: utf-8 -*-
"""
Test harness module

Helper functions for batch testing.

@author: Tom Walker
@lastupdate: 2014-01-21
"""

import numpy as np
import sys

def equivalent(a, b, eps = 1e-4):
    "Equivalence test. Check if a and b are within epsilon tolerance."     
    return abs(a-b) <= eps

def test_case(function, inputs, outputs, eps = 1e-4, verbose = False, number = 0, name = "", description = ""):
    """Test the result of a function for a given set of inputs and expected set of outputs.
    Test function valid for numerical data only.
    
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
    :param number: test number to be output
    :type number: integer
    :param name: name to identify test by
    :type name: string
    :param description: description of test
    :type description: string
    
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

def test_case_two_stage(function1, function2, inputs, outputs, verbose = False, number = 0, name = "", description = ""):
    """Tests the results of function2(function1(inputs)).
    
    If extra arguments are required for function1 and function2 it is recommended to call them from a wrapper function.
    
    :param function1: first function to call
    :type function1: function
    :param inputs: inputs to pass to first function
    :type inputs: dictionary
    :param outputs: expected result of function
    :type outputs: dictionary
    :param verbose: provide more detail of text results (optional)
    :type verbose: boolean
    :param number: test number to be output
    :type number: integer
    :param name: name to identify test by
    :type name: string
    :param description: description of test
    :type description: string
    
    :returns: results of two successive function calls
    :rtype: dictionary containing results of function call
    """   
    if number:
        print("TEST ", number, ": ", name, sep = '')
    else:
        print("TEST:", name)
    
    if verbose and len(description) > 0:
        print(description)               
    success = [False]
    result = False
    try:
        if verbose:
            print("Calling", function1, "with inputs", inputs)
        result = function1(inputs)
        if verbose:
            print("Output of first step",result)
            print("Calling", function2, "with inputs", result)
        result = function2(result)
        if verbose:                        
            print("Expected output of second step", outputs)
            print("Received output of second step", result)
        if result.keys() != outputs.keys():
            if verbose:
                print("Dictionary keys differ between results and expected output.")
        else:
            success = [result[k] == outputs[k] for k in outputs.keys()]
            if verbose:
                print("Actual difference between results and expected output:", success)
    except:
        if verbose:        
            print("Test resulted in error: ", sys.exc_info()[0], sys.exc_info()[1])        
    status = "TEST "
    if number:
        status = status + str(number) + " "    
    if truth_test(success):
        status = status + "PASSED."
    else:
        status = status + "FAILED."
    print(status)
    return result

def truth_test(result):
    """Helper function to determine if an iterable of arbitrary dimension contains all True values.
    At present a 0 length array is 'True'.
    
    :param result: iterable to test
    :type result: iterable
    :returns: True if iterable contains only True values.
    """
    if isinstance(result, str):
        return False
    if hasattr(result, '__iter__'):
        return all([truth_test(r) for r in result])
    return result