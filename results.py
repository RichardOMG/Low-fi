#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Results Tab

Author: Julius Susanto
Last edited: January 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globals
import numpy
import os, sys
                      
class results_ui(QtGui.QVBoxLayout): 
    
    def setup(self):
        
        label1 = QtGui.QLabel('Select study:')
        label1.setFixedWidth(80)
        
        combo = QtGui.QComboBox()
        combo.addItem("Load LFI")
        combo.addItem("Fault LFI")
        
        calc_button = QtGui.QPushButton("Calculate")
        calc_button.setFixedWidth(80)
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label1)
        hbox.addWidget(combo)
        hbox.addWidget(calc_button)
        hbox.setAlignment(Qt.AlignLeft)
        
        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.addLayout(hbox)
        
        self.addLayout(vbox)
        calc_button.clicked.connect(self.calculate)
        
    def calculate(self, tableWidget):
      
        print globals.pipe_data["pipe_rho"]
        print globals.network_data["freq"]
        print globals.network_data["angle_c"]
        print globals.tower_data["Z_w"]
        
        print globals.sections
