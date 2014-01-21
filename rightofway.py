#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Right of Way Tab

Author: Julius Susanto
Last edited: January 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy
import globals
                      
class rightofway_ui(QtGui.QVBoxLayout): 
    
    def setup(self):
        
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
        
        update_button.clicked.connect(self.buttonClicked)
        self.tableWidget.itemChanged.connect(self.update_data)
    
    # Update number of sections in right of way
    def buttonClicked(self, tableWidget):
      
        globals.no_sections = int(self.le.text())
        self.tableWidget.setRowCount(globals.no_sections)
        globals.sections.resize((globals.no_sections,3))
    
    # Update sections matrix whenever table data is changed
    def update_data(self, tableWidgetItem):
        
        globals.sections[tableWidgetItem.row(), tableWidgetItem.column()] = float(tableWidgetItem.text())
        
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

            
        