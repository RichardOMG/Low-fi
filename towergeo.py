#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Tower Tab

Authors: Julius Susanto and Tom Walker
Last edited: January 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globals
import utility
                      
class towergeo_ui(QtGui.QVBoxLayout): 
    
    def setup(self, window):
        
        self.main_window = window        
        
        img1 = QtGui.QLabel()
        img1.setPixmap(QtGui.QPixmap('images\Tower_Geo.png'))
        
        label1 = QtGui.QLabel('L_ab')
        label1.setFixedWidth(50)
        
        self.le1 = QtGui.QLineEdit()
        self.le1.setFixedWidth(50)
        self.le1.setText(str(globals.tower_data["L_ab"]))
        
        label1a = QtGui.QLabel('m')
        label1a.setFixedWidth(10)
        
        label2 = QtGui.QLabel('L_ac')
        label2.setFixedWidth(50)
        
        self.le2 = QtGui.QLineEdit()
        self.le2.setFixedWidth(50)
        self.le2.setText(str(globals.tower_data["L_ac"]))
        
        label2a = QtGui.QLabel('m')
        label2a.setFixedWidth(10)
        
        label3 = QtGui.QLabel('L_aw')
        label3.setFixedWidth(50)
        
        self.le3 = QtGui.QLineEdit()
        self.le3.setFixedWidth(50)
        self.le3.setText(str(globals.tower_data["L_aw"]))
        
        label3a = QtGui.QLabel('m')
        label3a.setFixedWidth(10)
        
        label4 = QtGui.QLabel('H_a')
        label4.setFixedWidth(50)
        
        self.le4 = QtGui.QLineEdit()
        self.le4.setFixedWidth(50)
        self.le4.setText(str(globals.tower_data["H_a"]))
        
        label4a = QtGui.QLabel('m')
        label4a.setFixedWidth(10)
        
        label5 = QtGui.QLabel('H_b')
        label5.setFixedWidth(50)
        
        self.le5 = QtGui.QLineEdit()
        self.le5.setFixedWidth(50)
        self.le5.setText(str(globals.tower_data["H_b"]))
        
        label5a = QtGui.QLabel('m')
        label5a.setFixedWidth(10)
        
        label6 = QtGui.QLabel('H_c')
        label6.setFixedWidth(50)
        
        self.le6 = QtGui.QLineEdit()
        self.le6.setFixedWidth(50)
        self.le6.setText(str(globals.tower_data["H_c"]))
        
        label6a = QtGui.QLabel('m')
        label6a.setFixedWidth(10)
        
        label7 = QtGui.QLabel('H_w')
        label7.setFixedWidth(50)
        
        self.le7 = QtGui.QLineEdit()
        self.le7.setFixedWidth(50)
        self.le7.setText(str(globals.tower_data["H_w"]))
        
        label7a = QtGui.QLabel('m')
        label7a.setFixedWidth(10)
        
        label8 = QtGui.QLabel('Z_w')
        label8.setFixedWidth(50)
        
        self.le8a = QtGui.QLineEdit()
        self.le8a.setFixedWidth(50)
        self.le8a.setText(str(globals.tower_data["Z_w"].real))
        
        label8a = QtGui.QLabel('+ j')
        label8a.setFixedWidth(15)
        
        self.le8b = QtGui.QLineEdit()
        self.le8b.setFixedWidth(50)
        self.le8b.setText(str(globals.tower_data["Z_w"].imag))
        
        label8b = QtGui.QLabel('Ohm')
        label8b.setFixedWidth(25)
        
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
        
        inner_grid.addWidget(label8, 7, 0)
        inner_grid.addWidget(self.le8a, 7, 1)
        inner_grid.addWidget(label8a, 7, 2)
        inner_grid.addWidget(self.le8b, 7, 3)
        inner_grid.addWidget(label8b, 7, 4)
        
        grid.addLayout(inner_grid, 0, 1)
        
        self.addLayout(grid)        
                
        self.le1.editingFinished.connect(utility.create_validation_hook(self, self.le1, "L_ab", 0, float("inf")))
        self.le2.editingFinished.connect(utility.create_validation_hook(self, self.le2, "L_ac", 0, float("inf")))
        self.le3.editingFinished.connect(utility.create_validation_hook(self, self.le3, "L_aw", 0, float("inf")))
        self.le4.editingFinished.connect(utility.create_validation_hook(self, self.le4, "H_a", 0, float("inf")))
        self.le5.editingFinished.connect(utility.create_validation_hook(self, self.le5, "H_b", 0, float("inf")))
        self.le6.editingFinished.connect(utility.create_validation_hook(self, self.le6, "H_c", 0, float("inf")))
        self.le7.editingFinished.connect(utility.create_validation_hook(self, self.le7, "H_w", 0, float("inf")))
        self.le8a.editingFinished.connect(utility.create_validation_hook(self, self.le8a, "Z_w (real component)", 0, float("inf")))
        self.le8b.editingFinished.connect(utility.create_validation_hook(self, self.le8b, "Z_w (real component)", 0, float("inf")))

    # Update global tower object on change event
    def update_data(self):
        globals.tower_data["L_ab"] = float(self.le1.text())
        globals.tower_data["L_ac"] = float(self.le2.text())
        globals.tower_data["L_aw"] = float(self.le3.text())
        globals.tower_data["H_a"] = float(self.le4.text())
        globals.tower_data["H_b"] = float(self.le5.text())
        globals.tower_data["H_c"] = float(self.le6.text())
        globals.tower_data["H_w"] = float(self.le7.text())
        globals.tower_data["Z_w"] = complex(float(self.le8a.text()), float(self.le8b.text()))
        
    def refresh_data(self):
        """Update text fields to match global variables."""   
        self.le1.setText(str(globals.tower_data["L_ab"]))
        self.le2.setText(str(globals.tower_data["L_ac"]))
        self.le3.setText(str(globals.tower_data["L_aw"]))
        self.le4.setText(str(globals.tower_data["H_a"]))
        self.le5.setText(str(globals.tower_data["H_b"]))
        self.le6.setText(str(globals.tower_data["H_c"]))
        self.le7.setText(str(globals.tower_data["H_w"]))
        self.le8a.setText(str(globals.tower_data["Z_w"].real))
        self.le8b.setText(str(globals.tower_data["Z_w"].imag))
         
