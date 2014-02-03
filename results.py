#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Results Tab

Authors: Julius Susanto and Tom Walker
Last edited: February 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, sys
import globals
import utility
import calc
import numpy as np
import dateutil, pyparsing
import matplotlib.pyplot as plt

                      
class results_ui(QtGui.QVBoxLayout): 
    
    def setup(self, window):
        
        self.main_window = window   
        
        label1 = QtGui.QLabel('Select study:')
        label1.setFixedWidth(80)
        
        self.combo = QtGui.QComboBox()
        self.combo.addItem("Load LFI")
        self.combo.addItem("Fault LFI")
        
        calc_button = QtGui.QPushButton("Calculate")
        calc_button.setFixedWidth(80)       
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label1)
        hbox.addWidget(self.combo)
        hbox.addWidget(calc_button)
        hbox.setAlignment(Qt.AlignLeft)
        
        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.addLayout(hbox)
        
        self.addLayout(vbox)
        calc_button.clicked.connect(self.calculate)
        
        # Scrolling groupbox - commented out, might remove this in favour of not showing individual calc steps
        # Note: this won't actually do anything until widgets are in the layout as 
        # QTableWidgets appear to have their own scroll behaviour
        #groupbox = QtGui.QGroupBox()
        #groupbox.setTitle("Calculation Results")
        #self.scrollarea = QtGui.QScrollArea()
        #self.scrollarea.setWidget(groupbox)               
        #self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        #self.scrollarea.setWidgetResizable(True)
        #self.scrollarea.setFixedHeight(500)      
        #self.results_layout = QtGui.QVBoxLayout()
        #self.results_layout.setAlignment(Qt.AlignTop)       
        #groupbox.setLayout(self.results_layout)  
        #self.scrollarea.hide()       
        #vbox.addWidget(self.scrollarea)

        self.results_table = utility.LowFiTable(self.main_window, headings = ["Distance along pipeline (m)", "Pipeline-to-earth touch voltage (V)"], allowPaste = False, alternatingRowColors = True)                        
        self.results_table.hide()
        self.results_table.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        
        vbox.addWidget(self.results_table)                
        
       
       
        
    
    # Calculate load and fault LFI voltages on the pipeline
    def calculate(self, tableWidget):
       
        loadLFI = self.combo.currentText() == "Load LFI"
       
        # launch calculation
        [ pipe_distance, Vp_final ] = calc.calculate(loadLFI)
        
        # Plot results        
        plt.plot(pipe_distance, Vp_final)
        plt.xlim([0, pipe_distance[globals.no_sections]])
        plt.xlabel("Distance along pipeline (m)")
        
        if self.combo.currentText() == "Load LFI":
            plt.ylabel("Pipeline-to-earth touch voltage (V)")
            plt.title("Load LFI Voltages")
        else:
            plt.ylabel("Pipeline-to-earth touch voltage (kV)")
            plt.title("Fault LFI Voltages")
        
        plt.grid(color = '0.75', linestyle='--', linewidth=1)
        plt.show()
        
        # Populate table of results in calc
        data = np.transpose(np.array([pipe_distance, Vp_final]))
        self.results_table.fill_table(data, readOnly = True)
        self.results_table.show()
        
        ##############
        # Diagnostics
        ##############
        
        #print pipe_distance
        #print Vp_final
        #print V_p
        

    def refresh_data(self):
        """Update text fields to match global variables."""
        # This is probably not needed.
        pass
        