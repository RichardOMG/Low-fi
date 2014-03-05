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

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
                      
class results_ui(QtGui.QVBoxLayout): 
    
    def setup(self, window):
        
        self.main_window = window   
        
        label1 = QtGui.QLabel('Select study:')
        label1.setFixedWidth(80)
        
        self.combo = QtGui.QComboBox()
        self.combo.addItem("Load LFI")
        self.combo.addItem("Fault LFI")

        label2 = QtGui.QLabel('Select mutual impedance formula:')
        label1.setFixedWidth(80)
        
        self.mutual_impedance_selection = QtGui.QComboBox()
        self.mutual_impedance_selection.addItem("Carson-Clem (AS4853)")
        self.mutual_impedance_selection.addItem("Ametani approximation")
        self.mutual_impedance_selection.addItem("Lucca approximation")
        
        calc_button = QtGui.QPushButton("Calculate")
        calc_button.setFixedWidth(80)       
        
        self.export_button = QtGui.QPushButton("Export")
        self.export_button.setFixedWidth(80)       
        self.export_button.hide()        
        
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(label2)
        hbox.addWidget(self.mutual_impedance_selection)
        hbox.addWidget(label1)
        hbox.addWidget(self.combo)
        hbox.addWidget(calc_button)
        hbox.addWidget(self.export_button)
        hbox.setAlignment(Qt.AlignLeft)
        
        vbox = QtGui.QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.addLayout(hbox)
        
        self.addLayout(vbox)
        calc_button.clicked.connect(self.calculate)
        self.export_button.clicked.connect(self.export_fn)
        
        self.results_table = utility.LowFiTable(self.main_window, headings = ["Distance along pipeline (m)", "Pipeline-to-earth touch voltage (V)"], allowPaste = False, alternatingRowColors = True)                        
        self.results_table.hide()
        self.results_table.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        
        vbox.addWidget(self.results_table)                
             
        self.plot = None
        
    
    # Calculate load and fault LFI voltages on the pipeline
    def calculate(self, tableWidget):
       
        loadLFI = self.combo.currentText() == "Load LFI"
       
        # launch calculation
        [ pipe_distance, Vp_final, diagnostics ] = calc.calculate(loadLFI, mutual_impedance_formula = self.mutual_impedance_selection.currentIndex())
                
        # clear diagnostics log and refresh with matrices from latest calculation
        self.main_window.diagnostics_clear()
        for (title, data) in diagnostics:
            self.main_window.diagnostics_matrix(title = title, data = data)
        
        # Populate table of results in calc
        if loadLFI:
            data = np.transpose(np.array([pipe_distance, Vp_final]))
        else:
            # Convert kV to V for fault LFI cases
            data = np.transpose(np.array([pipe_distance, Vp_final * 1000]))
        self.results_table.fill_table(data, readOnly = True)
        self.results_table.show()
        
        # Unhide export button
        self.export_button.show()   
        
        # Plot results  
        if loadLFI:
            ylabel = "Pipeline-to-earth touch voltage (V)"
            title = "Load LFI Voltages"
        else:
            ylabel = "Pipeline-to-earth touch voltage (kV)"
            title = "Fault LFI Voltages"        

        if self.plot is not None:
            self.plot.close()

        self.plot = PlotWindow(pipe_distance, Vp_final, "Distance along pipeline (m)", ylabel, title)
        self.plot.show()
        
    
    def export_fn(self):
        """Function for the Export action."""
        fname = QtGui.QFileDialog.getSaveFileName(self.main_window, "Export Data As", "", "Comma separate values (*.csv)")
        if fname:            
            if utility.write_table_to_csv_file(fname, self.results_table):
                self.main_window.show_status_message("Export to file " + fname + " successful.")
            else:
                self.main_window.show_status_message("Failed to export to " + fname + ".", error = True, beep = True)
        else:
            self.main_window.show_status_message("Export cancelled.")                   
    
class PlotWindow(QMainWindow):
    """Separate window for plot."""
    def __init__(self, x, y, xlabel, ylabel, title):
        QtGui.QMainWindow.__init__(self)
        self.setWindowTitle("Figure - " + title)
        self.main_widget = QtGui.QWidget(self)
        vbox = QtGui.QVBoxLayout(self.main_widget)
        figure = PlotCanvas(self.main_widget, x, y, xlabel, ylabel, title)
        toolbar = NavigationToolbar(figure, self.main_widget)
        vbox.addWidget(figure) 
        vbox.addWidget(toolbar)
        self.main_widget.setFocus() 
        self.setCentralWidget(self.main_widget) 
        
    
class PlotCanvas(FigureCanvas):
    """Implements matplotlib figure window to avoid clashes between PyQt and matplotlib."""

    def __init__(self, parent, x, y, xlabel, ylabel, title):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.x = x
        self.y = y
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)
        self.axes.set_xlim([0, max(x)])
        self.axes.set_xlabel(xlabel)
        self.axes.grid(color = '0.75', linestyle='--', linewidth=1)
        self.axes.plot(self.x, self.y)
        FigureCanvas.__init__(self, self.fig)
        
        self.setParent(parent)
    
