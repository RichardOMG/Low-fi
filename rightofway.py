#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Right of Way Tab

Author: Julius Susanto
Last edited: November 2013
"""

import os, sys
from PyQt4 import QtGui, QtCore

class rightofway_ui(QtGui.QVBoxLayout): 
    
    def setup(self):
        
        button1 = QtGui.QPushButton("button1")
        self.le = QtGui.QLineEdit()
        self.addWidget(button1) 
        self.addWidget(self.le)
        button1.clicked.connect(self.buttonClicked)
        
    def buttonClicked(self):
      
        sender = self.sender()
        self.le.setText(str(sender.text() + ' was pressed'))

"""
class line_sections():

    def __init__(self):
"""