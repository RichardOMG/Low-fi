#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Tower Geometry Tab

Author: Julius Susanto
Last edited: January 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy
import os, sys
                      
class towergeo_ui(QtGui.QVBoxLayout): 
    
    def setup(self):
        
        img1 = QtGui.QLabel()
        img1.setPixmap(QtGui.QPixmap('images\Tower_Geo.png'))
        
        label1 = QtGui.QLabel('L_ab')
        label1.setFixedWidth(50)
        
        self.le1 = QtGui.QLineEdit()
        self.le1.setFixedWidth(50)
        self.le1.setText('4')
        
        label1a = QtGui.QLabel('m')
        label1a.setFixedWidth(10)
        
        label2 = QtGui.QLabel('L_ac')
        label2.setFixedWidth(50)
        
        self.le2 = QtGui.QLineEdit()
        self.le2.setFixedWidth(50)
        self.le2.setText('1')
        
        label2a = QtGui.QLabel('m')
        label2a.setFixedWidth(10)
        
        label3 = QtGui.QLabel('L_aw')
        label3.setFixedWidth(50)
        
        self.le3 = QtGui.QLineEdit()
        self.le3.setFixedWidth(50)
        self.le3.setText('2')
        
        label3a = QtGui.QLabel('m')
        label3a.setFixedWidth(10)
        
        label4 = QtGui.QLabel('H_a')
        label4.setFixedWidth(50)
        
        self.le4 = QtGui.QLineEdit()
        self.le4.setFixedWidth(50)
        self.le4.setText('15')
        
        label4a = QtGui.QLabel('m')
        label4a.setFixedWidth(10)
        
        label5 = QtGui.QLabel('H_b')
        label5.setFixedWidth(50)
        
        self.le5 = QtGui.QLineEdit()
        self.le5.setFixedWidth(50)
        self.le5.setText('18')
        
        label5a = QtGui.QLabel('m')
        label5a.setFixedWidth(10)
        
        label6 = QtGui.QLabel('H_c')
        label6.setFixedWidth(50)
        
        self.le6 = QtGui.QLineEdit()
        self.le6.setFixedWidth(50)
        self.le6.setText('21')
        
        label6a = QtGui.QLabel('m')
        label6a.setFixedWidth(10)
        
        label7 = QtGui.QLabel('H_w')
        label7.setFixedWidth(50)
        
        self.le7 = QtGui.QLineEdit()
        self.le7.setFixedWidth(50)
        self.le7.setText('25')
        
        label7a = QtGui.QLabel('m')
        label7a.setFixedWidth(10)
        
        grid = QtGui.QGridLayout()
        inner_grid = QtGui.QGridLayout()
        
        grid.addWidget(img1, 0, 0)
        inner_grid.addWidget(label1, 0, 0)
        inner_grid.addWidget(self.le1, 0, 1)
        inner_grid.addWidget(label1a, 0, 2)
        inner_grid.addWidget(label2, 1, 0)
        inner_grid.addWidget(self.le2, 1, 1)
        inner_grid.addWidget(label2a, 1, 2)
        inner_grid.addWidget(label3, 2, 0)
        inner_grid.addWidget(self.le3, 2, 1)
        inner_grid.addWidget(label3a, 2, 2)
        inner_grid.addWidget(label4, 3, 0)
        inner_grid.addWidget(self.le4, 3, 1)
        inner_grid.addWidget(label4a, 3, 2)
        inner_grid.addWidget(label5, 4, 0)
        inner_grid.addWidget(self.le5, 4, 1)
        inner_grid.addWidget(label5a, 4, 2)
        inner_grid.addWidget(label6, 5, 0)
        inner_grid.addWidget(self.le6, 5, 1)
        inner_grid.addWidget(label6a, 5, 2)
        inner_grid.addWidget(label7, 6, 0)
        inner_grid.addWidget(self.le7, 6, 1)
        inner_grid.addWidget(label7a, 6, 2)
        grid.addLayout(inner_grid, 0, 1)
        
        self.addLayout(grid)
