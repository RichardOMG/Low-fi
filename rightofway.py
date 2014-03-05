#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Right of Way Tab

Authors: Julius Susanto and Tom Walker
Last edited: January 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import globals
import utility
                      
class rightofway_ui(QtGui.QVBoxLayout): 
    
    def setup(self, window):   
        
        self.main_window = window        
        
        label1 = QtGui.QLabel('No. of Sections:')
        label1.setFixedWidth(100)
        
        update_button = QtGui.QPushButton("Update")
        update_button.setFixedWidth(80)
        
        self.le = QtGui.QLineEdit()
        self.le.setFixedWidth(50)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label1)
        hbox.addWidget(self.le)
        hbox.addWidget(update_button)
        hbox.setAlignment(Qt.AlignLeft)
        
        headings = ['Section Length (m)', 'Separation (m)', 'Earth (Ohms)', 'Soil rho (Ohm.m)', 'Phasing']
        self.tableWidget = RightOfWayTable(window, headings = headings, alternatingRowColors = True)

        self.addLayout(hbox) 
        self.addWidget(self.tableWidget)

        self.le.editingFinished.connect(utility.create_validation_hook(self, self.le, "Number of sections", 1, 100000, l_inclusive = True, u_inclusive = True, refresh_data = False))
        
        update_button.clicked.connect(self.buttonClicked)
        self.tableWidget.itemChanged.connect(self.update_data_matrix)

        self.refresh_data()

    
    # Update number of sections in right of way
    def buttonClicked(self, tableWidget):      
        globals.sections.resize((globals.no_sections,6))
        for row in range(self.tableWidget.rowCount(), globals.no_sections):
            globals.sections[row, 0] = 1.0                            
            globals.sections[row, 1] = 1.0                            
            globals.sections[row, 2] = 1.0
            globals.sections[row, 3] = 0.0
            globals.sections[row, 4] = 100.0
            globals.sections[row, 5] = 0             
        self.refresh_data()        
        
    
    def update_data(self):
        globals.no_sections = int(float(self.le.text()))
        self.le.setText(str(globals.no_sections))
    
    # Update sections matrix whenever table data is changed
    def update_data_matrix(self, tableWidgetItem): 
        lower_bound = 0.0
        upper_bound = float("inf")
        value = 0.0
        if tableWidgetItem.column() == 0:
            element = "length"
            value = utility.validate(tableWidgetItem.text(), lower_bound, upper_bound, l_inclusive = False, u_inclusive = False)
        elif tableWidgetItem.column() == 1:
            element = "separation"
            lower_bound = -1.0 * float("inf")
            value = utility.validate(tableWidgetItem.text(), lower_bound, upper_bound, l_inclusive = False, u_inclusive = False)
        elif tableWidgetItem.column() == 2:
            element = "earth impedance"
            try:
                # explicit string conversion required for Python 2.7
                value = np.complex(str(tableWidgetItem.text()))
            except:
                value = False
        elif tableWidgetItem.column() == 3:
            element = "soil resistivity"
            value = utility.validate(tableWidgetItem.text(), lower_bound, upper_bound, l_inclusive = False, u_inclusive = False)
        if not value is False:   
            columns = [0,1,2,4,5]            
            column = columns[tableWidgetItem.column()]
            update_mapping = (globals.sections[tableWidgetItem.row(), column] != value)
            if isinstance(value, np.complex):
                globals.sections[tableWidgetItem.row(), column] = np.real(value)
                globals.sections[tableWidgetItem.row(), column + 1] = np.imag(value)
                if np.imag(value) == 0.0:
                    tableWidgetItem.setText(str(np.real(value)))
                else:
                    tableWidgetItem.setText(str(value))
            else:            
                globals.sections[tableWidgetItem.row(), column] = value
                #tableWidgetItem.setText(str(value))
            if update_mapping:
                self.main_window.refresh_mapping()
        else:
            self.main_window.show_status_message("Section " + str(tableWidgetItem.row() + 1) + " " + element +  ": Input value '" + tableWidgetItem.text() + "' out of bounds. (" + str(lower_bound) + " to " + str(upper_bound) + "). Value not set.", error = True, beep = True)
            self.tableWidget.itemChanged.disconnect()
            self.refresh_data()          
            self.tableWidget.itemChanged.connect(self.update_data_matrix)            
        
        ##############
        # TODO - Apply dynamic criteria to separation distance (based on soli resistivity)
        ##############
        
    def refresh_data(self):
        """Update text fields to match global variables."""
        self.tableWidget.setRowCount(globals.no_sections)
        self.le.setText(str(globals.no_sections))
        self.tableWidget.fill_table(globals.sections)

            
class RightOfWayTable(utility.LowFiTable): 
    """Modified version of LowFi table specifically for the Right Of Way tab."""

    def signal_mapping(signal_mapper):
        self.signal_mapper = signal_mapper

    def fill_table(self, data):
        """Fill table from 2D list or numpy array."""
        if len(data) > 0:
            if isinstance(data, np.ndarray):
                data = data.tolist()
            data_rows = len(data)
            data_columns = len(data[0])
            if data_columns > 0:
                self.setRowCount(data_rows)
                # We hide the imag part of the complex impedance
                self.setColumnCount(data_columns - 1)
                for r in range(0, data_rows):
                    # Update real columns
                    for c, realc in [(0, 0), (1, 1), (3, 4)]:
                        item = QTableWidgetItem()                        
                        item.setText(str(data[r][realc]))      
                        self.setItem(r, c, item)
                    # Earth resistance has a hidden column which can have an imaginary number
                    if data[r][3] != 0.0:
                        # show complex impedance
                        item = QTableWidgetItem()               
                        item.setText(str(np.complex(data[r][2], data[r][3])))
                        self.setItem(r, 2, item)
                    else:
                        # show real impedance
                        item = QTableWidgetItem()
                        item.setText(str(data[r][2]))                    
                        self.setItem(r, 2, item)
                    # Last Column is a QComboBox to select phasing
                    phasing = QComboBox()
                    phasing.addItems(["Normal","120 degree shift", "240 degree shift"])
                    phasing.setCurrentIndex(np.real(data[r][5]))
                    phasing.currentIndexChanged.connect(self.phasing_signal(phasing, r, 5))
                    self.setCellWidget(r, 4, phasing)                      
                    
    def phasing_signal(self, phasing, r, c):
        """Function will update phasing in globals.  Connect to combobox index changed event."""
        def signal():
            value = phasing.currentIndex()
            if value >= 0 and value <= 2:
                globals.sections[r, c] = value
        return signal