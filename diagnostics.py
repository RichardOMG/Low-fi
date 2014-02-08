# -*- coding: utf-8 -*-
"""
Low-fi: Low frequency induction simulation

GUI window which displays tables of debug information.

Authors: Julius Susanto and Tom Walker
Last edited: February 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
import globals
import utility

                     
class diagnostics_ui(QtGui.QVBoxLayout): 
    """Window for logging matrix data as it is calculated."""
    
    def setup(self, window):          
        """Initialise debug UI."""
        self.main_window = window

        self.export_button = QtGui.QPushButton("Export")
        self.export_button.setFixedWidth(80)       
        self.addWidget(self.export_button)
        self.export_button.clicked.connect(self.export_fn)

        # Scrolling groupbox
        groupbox = QtGui.QGroupBox()
        scrollarea = QtGui.QScrollArea()
        scrollarea.setWidget(groupbox)               
        scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scrollarea.setWidgetResizable(True)
        self.results_layout = QtGui.QVBoxLayout()
        self.results_layout.setAlignment(Qt.AlignTop)
        groupbox.setLayout(self.results_layout)
        self.addWidget(scrollarea)    

    def clear(self):
        """Clear debug layout of matrices."""        
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            item.widget().deleteLater()        


    def log(self, title = "", data = [[]]):
        """Log a matrix to the diagnostics layout.  Creates it as a table.  Assumes each row of data is same length."""
        heading_font = QtGui.QFont()
        heading_font.setPointSize(10)
        heading_font.setBold(True)
               
        label = QtGui.QLabel(title)
        label.setFont(heading_font)                        
        
        # Convert data to 2D if it is scalar or 1D list
        if hasattr(data, "__len__"):
            if not hasattr(data[0], "__len__"):                
                data = [[row] for row in data]                
        else:
            data = [[data]]            
        
        # Create and fill table with data
        new_table = utility.LowFiTable(self.main_window, allowPaste = False, alternatingRowColors = True, allowShortcut = False)                                
        new_table.fill_table(data, readOnly = True, convertComplexNumbers = True)        

        # Resize table to contents        
        new_table.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        new_table.verticalHeader().setResizeMode(QHeaderView.ResizeToContents)
        new_table.resizeRowsToContents()
        new_table.resizeColumnsToContents()
        new_table.setFixedHeight(sum([new_table.rowHeight(r) for r in range(new_table.rowCount())]) + new_table.horizontalHeader().height() + 5)
        new_table.setFixedWidth(sum([new_table.columnWidth(c) for c in range(new_table.columnCount())]) + new_table.verticalHeader().width() + 5)
        
        self.results_layout.addWidget(label)        
        self.results_layout.addWidget(new_table)

    
    def export_fn(self):
        """Function for the Export action."""
        folder_name = QtGui.QFileDialog.getExistingDirectory(self.main_window, "Select Directory To Save Spreadsheets To")        
        if folder_name:            
            tables = []
            labels = []
            for i in range(self.results_layout.count()):
                item = self.results_layout.itemAt(i)
                if isinstance(item, QtGui.QWidgetItem):
                    item = item.widget()
                    if isinstance(item, utility.LowFiTable):
                        tables = tables + [item]
                    elif isinstance(item, QtGui.QLabel):
                        label = item.text()
                        if len(label) == 0:
                            label = str(len(tables))
                        labels = labels + [label]
            if utility.write_tables_to_csv_file(folder_name, labels, tables):
                self.main_window.show_status_message("Export to file " + folder_name + " successful.")
            else:
                self.main_window.show_status_message("Failed to export to " + folder_name + ".", error = True, beep = True)
        else:
            self.main_window.show_status_message("Export cancelled.")          
        
        