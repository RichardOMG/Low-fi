#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Pipeline Tab

Author: Julius Susanto
Last edited: January 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import globals
                      
class pipeline_ui(QtGui.QVBoxLayout): 
    
    def setup(self):
                
        label1 = QtGui.QLabel('Pipe diameter')
        label1.setFixedWidth(150)
        
        self.le1 = QtGui.QLineEdit()
        self.le1.setFixedWidth(80)
        self.le1.setText(str(globals.pipe_data["diameter"]))
        
        label1a = QtGui.QLabel('m')
        label1a.setFixedWidth(40)
        
        label2 = QtGui.QLabel('Pipe resistivity')
        label2.setFixedWidth(150)
        
        self.le2 = QtGui.QLineEdit()
        self.le2.setFixedWidth(80)
        self.le2.setText(str(globals.pipe_data["pipe_rho"]))
        
        label2a = QtGui.QLabel('Ohm.m')
        label2a.setFixedWidth(40)
        
        label3 = QtGui.QLabel('Pipe relative permeability')
        label3.setFixedWidth(150)
        
        self.le3 = QtGui.QLineEdit()
        self.le3.setFixedWidth(80)
        self.le3.setText(str(globals.pipe_data["pipe_mu"]))
        
        label3a = QtGui.QLabel('')
        label3a.setFixedWidth(40)
        
        label4 = QtGui.QLabel('Soil resistivity')
        label4.setFixedWidth(150)
        
        self.le4 = QtGui.QLineEdit()
        self.le4.setFixedWidth(80)
        self.le4.setText(str(globals.pipe_data["soil_rho"]))
        
        label4a = QtGui.QLabel('Ohm.m')
        label4a.setFixedWidth(40)
        
        label5 = QtGui.QLabel('Coating thickness')
        label5.setFixedWidth(150)
        
        self.le5 = QtGui.QLineEdit()
        self.le5.setFixedWidth(80)
        self.le5.setText(str(globals.pipe_data["coat_thickness"]))
        
        label5a = QtGui.QLabel('m')
        label5a.setFixedWidth(40)
        
        label6 = QtGui.QLabel('Coating resistivity')
        label6.setFixedWidth(150)
        
        self.le6 = QtGui.QLineEdit()
        self.le6.setFixedWidth(80)
        self.le6.setText(str(globals.pipe_data["coat_rho"]))
        
        label6a = QtGui.QLabel('m')
        label6a.setFixedWidth(40)
        
        label7 = QtGui.QLabel('Coating relative permeability')
        label7.setFixedWidth(150)
        
        self.le7 = QtGui.QLineEdit()
        self.le7.setFixedWidth(80)
        self.le7.setText(str(globals.pipe_data["coat_mu"]))
        
        label7a = QtGui.QLabel('')
        label7a.setFixedWidth(40)
        
        grid = QtGui.QGridLayout()
        
        grid.addWidget(label1, 0, 0)
        grid.addWidget(self.le1, 0, 1)
        grid.addWidget(label1a, 0, 2)
        grid.addWidget(label2, 1, 0)
        grid.addWidget(self.le2, 1, 1)
        grid.addWidget(label2a, 1, 2)
        grid.addWidget(label3, 2, 0)
        grid.addWidget(self.le3, 2, 1)
        grid.addWidget(label3a, 2, 2)
        grid.addWidget(label4, 3, 0)
        grid.addWidget(self.le4, 3, 1)
        grid.addWidget(label4a, 3, 2)
        grid.addWidget(label5, 4, 0)
        grid.addWidget(self.le5, 4, 1)
        grid.addWidget(label5a, 4, 2)
        grid.addWidget(label6, 5, 0)
        grid.addWidget(self.le6, 5, 1)
        grid.addWidget(label6a, 5, 2)
        grid.addWidget(label7, 6, 0)
        grid.addWidget(self.le7, 6, 1)
        grid.addWidget(label7a, 6, 2)
        
        grid.setAlignment(Qt.AlignTop)
        self.addLayout(grid)
        
        self.le1.editingFinished.connect(self.update_data)
        self.le2.editingFinished.connect(self.update_data)
        self.le3.editingFinished.connect(self.update_data)
        self.le4.editingFinished.connect(self.update_data)
        self.le5.editingFinished.connect(self.update_data)
        self.le6.editingFinished.connect(self.update_data)
        self.le7.editingFinished.connect(self.update_data)

    def update_data(self):
        globals.pipe_data["diameter"] = float(self.le1.text())
        globals.pipe_data["pipe_rho"] = float(self.le2.text())
        globals.pipe_data["pipe_mu"] = float(self.le3.text())
        globals.pipe_data["soil_rho"] = float(self.le4.text())
        globals.pipe_data["coat_thickness"] = float(self.le5.text())
        globals.pipe_data["coat_rho"] = float(self.le6.text())
        globals.pipe_data["coat_mu"] = float(self.le7.text())
        
    def refresh_data(self):
        """Update text fields to match global variables."""
        self.le1.setText(str(globals.pipe_data["diameter"]))
        self.le2.setText(str(globals.pipe_data["pipe_rho"]))
        self.le3.setText(str(globals.pipe_data["pipe_mu"]))
        self.le4.setText(str(globals.pipe_data["soil_rho"]))
        self.le5.setText(str(globals.pipe_data["coat_thickness"]))
        self.le6.setText(str(globals.pipe_data["coat_rho"]))
        self.le7.setText(str(globals.pipe_data["coat_mu"]))
