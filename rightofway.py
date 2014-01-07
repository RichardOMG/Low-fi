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
import os, sys
                      
class rightofway_ui(QtGui.QVBoxLayout): 
    
    def setup(self):
        
        label1 = QtGui.QLabel('No. of Sections:')
        label1.setFixedWidth(100)
        
        update_button = QtGui.QPushButton("Update")
        update_button.setFixedWidth(80)
        
        self.le = QtGui.QLineEdit()
        self.le.setFixedWidth(50)
        self.le.setText('20')
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label1)
        hbox.addWidget(self.le)
        hbox.addWidget(update_button)
        hbox.setAlignment(Qt.AlignLeft)
        
        self.tableWidget = QTableWidget(20,4)
        self.tableWidget.setHorizontalHeaderLabels(['Start (m)', 'End (m)', 'Separation (m)', 'Earth (Ohms)'])
        
        self.addLayout(hbox) 
        self.addWidget(self.tableWidget)
        update_button.clicked.connect(self.buttonClicked)
        
    def buttonClicked(self, tableWidget):
      
        noRows = int(self.le.text())
        self.tableWidget.setRowCount(noRows)
        