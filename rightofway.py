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
import numpy
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
        self.le.setText(str(globals.no_sections))
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label1)
        hbox.addWidget(self.le)
        hbox.addWidget(update_button)
        hbox.setAlignment(Qt.AlignLeft)
        
        self.tableWidget = QTableWidget(globals.no_sections,3)
        self.tableWidget.setHorizontalHeaderLabels(['Section Length (m)', 'Separation (m)', 'Earth (Ohms)'])
        
        # Populate tableWidget based on (global) section data
        for row in range(0,self.tableWidget.rowCount()):
            item1 = QTableWidgetItem()
            item2 = QTableWidgetItem()
            item3 = QTableWidgetItem()
            item1.setText(str(globals.sections[row,0]))
            self.tableWidget.setItem(row, 0, item1)
            item2.setText(str(globals.sections[row,1]))
            self.tableWidget.setItem(row, 1, item2)
            item3.setText(str(globals.sections[row,2]))
            self.tableWidget.setItem(row, 2, item3)
                    
        self.addLayout(hbox) 
        self.addWidget(self.tableWidget)

        self.le.editingFinished.connect(utility.create_validation_hook(self, self.le, "Number of sections", 1, 100000, l_inclusive = True, u_inclusive = True, refresh_data = False))
        
        update_button.clicked.connect(self.buttonClicked)
        self.tableWidget.itemChanged.connect(self.update_data_matrix)
    
    # Update number of sections in right of way
    def buttonClicked(self, tableWidget):      
        #self.tableWidget.setRowCount(globals.no_sections)        
        globals.sections.resize((globals.no_sections,3))
        for row in range(self.tableWidget.rowCount(), globals.no_sections):
            globals.sections[row, 0] = 1.0                            
            globals.sections[row, 1] = 1.0                            
            globals.sections[row, 2] = 1.0      
        self.refresh_data()        
        
    
    def update_data(self):
        globals.no_sections = int(self.le.text())
    
    # Update sections matrix whenever table data is changed
    def update_data_matrix(self, tableWidgetItem):                        
        lower_bound = 0.0
        upper_bound = float("inf")
        value = 0.0
        if tableWidgetItem.column() == 0:
            element = "Length"
            value = utility.validate(tableWidgetItem.text(), lower_bound, upper_bound, l_inclusive = False, u_inclusive = False)
        elif tableWidgetItem.column() == 1:
            element = "Separation"
            value = utility.validate(tableWidgetItem.text(), lower_bound, upper_bound, l_inclusive = True, u_inclusive = False)
        elif tableWidgetItem.column() == 2:
            element = "Earth"
            lower_bound = -1.0 * float("inf")
            value = utility.validate(tableWidgetItem.text(), lower_bound, upper_bound, l_inclusive = False, u_inclusive = False)
        if not value is False:        
            globals.sections[tableWidgetItem.row(), tableWidgetItem.column()] = float(tableWidgetItem.text())            
        else:
            self.main_window.show_status_message("Section " + str(tableWidgetItem.row() + 1) + " " + element +  ": Input value '" + tableWidgetItem.text() + "' out of bounds. (" + str(lower_bound) + " to " + str(upper_bound) + "). Value not set.", error = True, beep = True)
            self.refresh_data()
        ##############
        # TODO - Apply dynamic criteria to separation distance (based on soli resistivity)
        ##############

        # Diagnostics
        # print globals.sections
        
    def refresh_data(self):
        """Update text fields to match global variables."""
        self.tableWidget.setRowCount(globals.no_sections)
        self.le.setText(str(globals.no_sections))
        for row in range(0, self.tableWidget.rowCount()):
            for col in range(0,3):
                item = QTableWidgetItem()
                item.setText(str(globals.sections[row, col]))
                self.tableWidget.setItem(row, col, item)

            
        