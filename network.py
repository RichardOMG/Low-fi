#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Network Tab

Authors: Julius Susanto and Tom Walker
Last edited: January 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globals
import utility
                      
class network_ui(QtGui.QVBoxLayout): 
    
    def setup(self, window):
        
        self.main_window = window   
        
        heading_font = QtGui.QFont()
        heading_font.setPointSize(10)
        heading_font.setBold(True)
        
        label1 = QtGui.QLabel('System frequency')
        label1.setFixedWidth(150)
        
        self.le1 = QtGui.QLineEdit()
        self.le1.setFixedWidth(80)
        
        label1a = QtGui.QLabel('Hz')
        label1a.setFixedWidth(40)
        
        label2 = QtGui.QLabel('Load Current')
        label2.setFixedWidth(150)
        label2.setFont(heading_font)
        
        label3 = QtGui.QLabel('Phase A current')
        label3.setFixedWidth(150)
        
        self.le3a = QtGui.QLineEdit()
        self.le3a.setFixedWidth(50)
        
        label3a = QtGui.QLabel('A')
        label3a.setFixedWidth(10)
        
        self.le3b = QtGui.QLineEdit()
        self.le3b.setFixedWidth(50)
        
        label3b = QtGui.QLabel('deg')
        label3b.setFixedWidth(20)
        
        label4 = QtGui.QLabel('Phase B current')
        label4.setFixedWidth(150)
        
        self.le4a = QtGui.QLineEdit()
        self.le4a.setFixedWidth(50)
        
        label4a = QtGui.QLabel('A')
        label4a.setFixedWidth(10)
        
        self.le4b = QtGui.QLineEdit()
        self.le4b.setFixedWidth(50)
        
        label4b = QtGui.QLabel('deg')
        label4b.setFixedWidth(20)
        
        label5 = QtGui.QLabel('Phase C current')
        label5.setFixedWidth(150)
        
        self.le5a = QtGui.QLineEdit()
        self.le5a.setFixedWidth(50)
        
        label5a = QtGui.QLabel('A')
        label5a.setFixedWidth(10)
        
        self.le5b = QtGui.QLineEdit()
        self.le5b.setFixedWidth(50)
        
        label5b = QtGui.QLabel('deg')
        label5b.setFixedWidth(20)
        
        label6 = QtGui.QLabel('Fault Current')
        label6.setFixedWidth(150)
        label6.setFont(heading_font)
        
        label7 = QtGui.QLabel('Maximum earth fault current')
        label7.setFixedWidth(150)
        
        self.le7 = QtGui.QLineEdit()
        self.le7.setFixedWidth(50)
        
        label7a = QtGui.QLabel('kA')
        label7a.setFixedWidth(15)

        label8 = QtGui.QLabel('Earth fault split factor')
        label8.setFixedWidth(150)
        
        self.le8 = QtGui.QLineEdit()
        self.le8.setFixedWidth(50)
        
        label9 = QtGui.QLabel('Shielding factor')
        label9.setFixedWidth(150)
        
        self.le9 = QtGui.QLineEdit()
        self.le9.setFixedWidth(50)
        
        grid = QtGui.QGridLayout()
        
        grid.addWidget(label1, 0, 0)
        grid.addWidget(self.le1, 0, 1)
        grid.addWidget(label1a, 0, 2)
        grid.addWidget(label2, 2, 0)
        grid.addWidget(label3, 3, 0)
        grid.addWidget(self.le3a, 3, 1)
        grid.addWidget(label3a, 3, 2)
        grid.addWidget(self.le3b, 3, 3)
        grid.addWidget(label3b, 3, 4)
        grid.addWidget(label4, 4, 0)
        grid.addWidget(self.le4a, 4, 1)
        grid.addWidget(label4a, 4, 2)
        grid.addWidget(self.le4b, 4, 3)
        grid.addWidget(label4b, 4, 4)
        grid.addWidget(label5, 5, 0)
        grid.addWidget(self.le5a, 5, 1)
        grid.addWidget(label5a, 5, 2)
        grid.addWidget(self.le5b, 5, 3)
        grid.addWidget(label5b, 5, 4)
        grid.addWidget(label6, 6, 0)
        grid.addWidget(label7, 7, 0)
        grid.addWidget(self.le7, 7, 2)
        grid.addWidget(label7a, 7, 3)
        grid.addWidget(label8, 8, 0)
        grid.addWidget(self.le8, 8, 2)
        grid.addWidget(label9, 1, 0)
        grid.addWidget(self.le9, 1, 1)
        
        grid.setAlignment(Qt.AlignTop)
        self.addLayout(grid)
        
        self.refresh_data()        
        
        self.le1.editingFinished.connect(utility.create_validation_hook(self, self.le1, "System frequency", 0.0, float("inf")))
        self.le3a.editingFinished.connect(utility.create_validation_hook(self, self.le3a, "Phase A current", 0.0, float("inf")))
        self.le3b.editingFinished.connect(utility.create_validation_hook(self, self.le3b, "Phase A angle", -180.0, 180.0))
        self.le4a.editingFinished.connect(utility.create_validation_hook(self, self.le4a, "Phase B current", 0.0, float("inf")))
        self.le4b.editingFinished.connect(utility.create_validation_hook(self, self.le4b, "Phase B angle", -180.0, 180.0))
        self.le5a.editingFinished.connect(utility.create_validation_hook(self, self.le5a, "Phase C current", 0.0, float("inf")))
        self.le5b.editingFinished.connect(utility.create_validation_hook(self, self.le5b, "Phase C angle", -180.0, 180.0))
        self.le7.editingFinished.connect(utility.create_validation_hook(self, self.le7, "Maximum earth fault current", 0.0, float("inf")))
        self.le8.editingFinished.connect(utility.create_validation_hook(self, self.le8, "Earth fault split factor", 0.0, 1.0, l_inclusive = True, u_inclusive = True))
        self.le9.editingFinished.connect(utility.create_validation_hook(self, self.le9, "Shielding factor", 0.0, 1.0, l_inclusive = True, u_inclusive = True))

    def update_data(self):
        globals.network_data["freq"] = float(self.le1.text())
        globals.network_data["current_a"] = float(self.le3a.text())
        globals.network_data["angle_a"] = float(self.le3b.text())
        globals.network_data["current_b"] = float(self.le4a.text())
        globals.network_data["angle_b"] = float(self.le4b.text())
        globals.network_data["current_c"] = float(self.le5a.text())
        globals.network_data["angle_c" ] = float(self.le5b.text())
        globals.network_data["fault_current"] = float(self.le7.text())
        globals.network_data["split_factor"] = float(self.le8.text())
        globals.network_data["shield_factor"] = float(self.le9.text())

    def refresh_data(self):
        """Update text fields to match global variables."""
        self.le1.setText(str(globals.network_data["freq"]))
        self.le3a.setText(str(globals.network_data["current_a"]))
        self.le3b.setText(str(globals.network_data["angle_a"]))
        self.le4a.setText(str(globals.network_data["current_b"]))
        self.le4b.setText(str(globals.network_data["angle_b"]))
        self.le5a.setText(str(globals.network_data["current_c"]))
        self.le5b.setText(str(globals.network_data["angle_c" ]))
        self.le7.setText(str(globals.network_data["fault_current"]))
        self.le8.setText(str(globals.network_data["split_factor"]))
        self.le9.setText(str(globals.network_data["shield_factor"]))
