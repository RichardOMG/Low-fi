# -*- coding: utf-8 -*-
"""
Low-fi: Low frequency induction simulation

Utility functions

Authors: Julius Susanto and Tom Walker
Last edited: January 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np

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



class LowFiTable(QtGui.QTableWidget): 
    """Overloaded version of the QTableWidget which adds Copy/Paste functionality to the table."""

    def __init__(self, main_window, data = [], headings = [], allowCopy = True, allowPaste = True, readOnly = False, alternatingRowColors = False):
        """Constructor which will set up Copy & Paste actions and populate table headings and data."""
        super(QtGui.QTableWidget, self).__init__()                
        self.setup(main_window, allowCopy, allowPaste)
        if len(data) > 0:
            self.fill_table(data, readOnly)
        if len(headings) > 0:
            self.setColumnCount(len(headings))            
            self.setHorizontalHeaderLabels(headings)
        self.setAlternatingRowColors(alternatingRowColors)
    
    def setup(self, main_window, allowCopy = True, allowPaste = True):
        """Set up table."""
        self.main_window = main_window
        
        if allowCopy:
            copyAction = QtGui.QAction('&Copy', self)
            copyAction.setShortcut('Ctrl+C')
            copyAction.setStatusTip('Copy')
            copyAction.triggered.connect(self.copy_fn)        
            self.addAction(copyAction)            

        if allowPaste:                
            pasteAction = QtGui.QAction('&Paste', self)
            pasteAction.setShortcut('Ctrl+V')
            pasteAction.setStatusTip('Paste')
            pasteAction.triggered.connect(self.paste_fn)       
            self.addAction(pasteAction)

        if allowCopy or allowPaste:                
            self.setContextMenuPolicy(Qt.ActionsContextMenu)
            self.setSelectionMode(QAbstractItemView.ContiguousSelection)

            
    def copy_fn(self):
        """Function for the Copy action."""
        # get active element
        # find selected text in element
        # load into clipboard
        if len(self.selectedRanges()) > 1:
            self.main_window.show_status_message("Copy command cannot be used with multiple ranges selected.", error = True, beep = True)
            return
        rows = self.selectedRanges()[0].rowCount()
        columns = self.selectedRanges()[0].columnCount()
        # For some reason the selectedIndexes output is transposed, so we have to transpose it
        data = np.array([ index.data() for index in self.selectedIndexes() ])
        data.resize((columns, rows))
        data = np.transpose(data).flatten()        
        delimiters = ([ "\t" for c in range(columns - 1) ] + ["\n"]) * rows        
        copy = [char for pair in zip(data, delimiters) for char in pair]
        copy = ''.join(copy)
        QApplication.clipboard().setText(copy)
        pass

    def paste_fn(self):
        """Function for the Paste action."""
        # There might be a more elegant way of doing this..
        try:
            data = QApplication.clipboard().text()
            data = [ [ float(val) for val in line.split('\t') if len(val) > 0 ] for line in data.split('\n') if len(line) > 0 ]        
            if len(self.selectedIndexes()) > 0 and len(data) > 0:
                data_rows = len(data)
                data_columns = len(data[0])
                table_rows = self.rowCount()
                table_columns = self.columnCount()
                active_row = self.selectedIndexes()[0].row()
                active_column = self.selectedIndexes()[0].column()
                selection = QtGui.QItemSelection(self.model().index(active_row, active_column), self.model().index(active_row + data_rows - 1, active_column + data_columns - 1))
                self.selectionModel().select(selection, QItemSelectionModel.ClearAndSelect)
                if active_row + data_rows > table_rows or active_column + data_columns > table_columns:
                    self.main_window.show_status_message("Clipboard data too large.", error = True, beep = True)
                else:                    
                    for r in range(data_rows):
                        for c in range(data_columns):
                            self.item(r + active_row, c + active_column).setText(str(data[r][c]))                                
        except:
            self.main_window.show_status_message("Clipboard data invalid.", error = True, beep = True)    
    
    def fill_table(self, data, readOnly = False):
        """Fill table from 2D list or numpy array."""
        if len(data) > 0:
            data_rows = len(data)
            data_columns = len(data[0])
            if data_columns > 0:
                self.setRowCount(data_rows)
                self.setColumnCount(data_columns)
                for r in range(0, data_rows):
                    for c in range(0, data_columns):
                        item = QTableWidgetItem()
                        item.setText(str(data[r][c]))
                        if readOnly:
                            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                        self.setItem(r, c, item)                        