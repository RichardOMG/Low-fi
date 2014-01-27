# -*- coding: utf-8 -*-
"""
Low-fi: Low frequency induction simulation

Utility functions

Authors: Julius Susanto and Tom Walker
Last edited: January 2014
"""

#from PyQt4 import QtCore, QtGui
#from PyQt4.QtCore import *
#from PyQt4.QtGui import *

def validate(input_value, lower_bound, upper_bound, l_inclusive = True, u_inclusive = True):
    """Check if value is within allowable range.
    
    :param input_value: Input value to validate
    :type input_value: String
    :param lower_bound: Lowest acceptable value.
    :type lower_bound: Float
    :param upper_bound: Highest acceptable value.
    :type upper_bound: Float
    :param l_inclusive: True if range includes lower bound.
    :type l_inclusive: Boolean
    :param u_inclusive: True if range includes upper bound.
    :type u_inclusive: Boolean
    :returns: Float of value if acceptable, False otherwise.
    """    
    try:
        value = float(input_value)
    except:
        value = lower_bound - 1         
    if ((u_inclusive and value <= upper_bound) or (not u_inclusive and value < upper_bound)) and ((l_inclusive and value >= lower_bound) or (not l_inclusive and value > lower_bound)):
        return value
    return False

def create_validation_hook(gui, text_field, description, lower_bound, upper_bound, l_inclusive = True, u_inclusive = True, update_data = True, refresh_data = True):
    """Wrapper to create a function which will validate value input into a QLineEdit. For floating point numbers.

    :param gui: Reference to main window
    :type gui: Window
    :param text_field: Text field to validate input of
    :type text_field: QLineEdit
    :param description: Description of text field for display in status line.
    :type description: String
    :param lower_bound: Lowest acceptable value.
    :type lower_bound: Float
    :param upper_bound: Highest acceptable value.
    :type upper_bound: Float
    :param l_inclusive: Optional. True if range includes lower bound.
    :type l_inclusive: Boolean
    :param u_inclusive: Optional. True if range includes upper bound.
    :type u_inclusive: Boolean
    :param update_data: Optional. True if update_data function should be called on gui object.
    :type update_data: Boolean
    :param refresh_data: Optional. True if refresh_data function should be called on gui object.
    :type refresh_data: Boolean
    :returns: Reference to function which will perform validation calls.
    """        
    def validation_hook():
        if validate(text_field.text(), lower_bound, upper_bound, l_inclusive, u_inclusive) is False:
            gui.main_window.show_status_message(description + ": Input value '" + text_field.text() + "' out of bounds (" + str(lower_bound) + " to " + str(upper_bound) + "). Value not set.", error = True, beep = True)
            if refresh_data:
                gui.refresh_data()
        else:
            if update_data:
                gui.update_data()
            gui.main_window.show_status_message("", error = False, beep = False)
            if refresh_data:
                gui.refresh_data()            
    return validation_hook



# validate data
# if successful, update text field
# if failed, update status message
