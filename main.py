#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Main window

Author: Julius Susanto
Last edited: November 2013
"""

import os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from rightofway import *
from towergeo import *
from pipeline import *
from network import *
from results import *
import globals

class Window(QtGui.QWidget):
    
    def __init__(self):
        super(Window, self).__init__()
        
        globals.init()
        self.initUI()
        
    def initUI(self):
        
        self.resize(700, 500)
        self.centre()
        self.setWindowTitle('Low-fi: Low Frequency Induction Simulation')
        self.setWindowIcon(QtGui.QIcon('icons\web.png'))    
              
        """
        Actions
        """
        exitAction = QtGui.QAction(QtGui.QIcon('icons\exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        ###########################
        # TO DO - Add Save button which will be greyed out if no changes from saved data
        #         Save button should bring up Save As if no open file
        ###########################

        saveAsAction = QtGui.QAction(QtGui.QIcon('icons\saveas.ico'), 'Save &As', self)
        saveAsAction.setShortcut('Ctrl+A')
        saveAsAction.setStatusTip('Save project as')
        saveAsAction.triggered.connect(self.save_as_fn)


        openAction = QtGui.QAction(QtGui.QIcon('icons\open.ico'), '&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open project')
        openAction.triggered.connect(self.open_fn)

        """
        Menubar
        """
        menu_bar = QtGui.QMenuBar() 
        fileMenu = menu_bar.addMenu('&File')
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        
               
        """
        Toolbar
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        """
        
        """
        Tabs
        """
        tab_widget = QtGui.QTabWidget()
        tab1 = QtGui.QWidget()
        tab2 = QtGui.QWidget() 
        tab3 = QtGui.QWidget()
        tab4 = QtGui.QWidget()
        tab5 = QtGui.QWidget()
               
        tab_widget.addTab(tab1, "Right of Way")
        tab_widget.addTab(tab2, "Tower") 
        tab_widget.addTab(tab3, "Pipeline") 
        tab_widget.addTab(tab4, "Network") 
        tab_widget.addTab(tab5, "Results") 
        
        page1 = rightofway_ui(tab1)
        page2 = towergeo_ui(tab2)
        page3 = pipeline_ui(tab3)
        page4 = network_ui(tab4)
        page5 = results_ui(tab5)
        self.pages = [page1, page2, page3, page4, page5]
        
        page1.setup()
        page2.setup()
        page3.setup()
        page4.setup()
        page5.setup()
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(menu_bar)
        vbox.addWidget(tab_widget) 
        
        self.setLayout(vbox)
        
        #self.statusBar().showMessage('Ready')
        
    def centre(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def refresh_data(self):
        """Refresh each page with data from globals variables."""
        for p in self.pages:
            p.refresh_data()
            

    def save_as_fn(self):
        """Function for the Save As action."""
        if globals.write_project_to_file(QtGui.QFileDialog.getSaveFileName(self, "Save Data File As", "", "LowFi project files (*.lfi)")):
            return
        print("Error writing to file or Save As cancelled.")
            ###########################
            # TO DO - Distinguish between cancel and failure
            #       - Some sort of error notification
            #       - Put open filename in title bar
            ###########################
            
    def save_fn(self):    
        """Function for the Save action."""
        if globals.filename != "":
            if globals.write_project_to_file(globals.filename):
                return                    
        ###########################
        # TO DO - Some sort of error notification
        ###########################
            
    def open_fn(self):
        """Function for the Open action."""
        ###########################
        # TO DO - Confirmation for opening file if data is unsaved
        #       - Put open filename in title bar
        ###########################
        if globals.load_project_from_file(QtGui.QFileDialog.getOpenFileName(self, "Open Data File", "", "LowFi project files (*.lfi)")):
            self.refresh_data()
        else:
            print("Error opening file or file open cancelled.")
            ###########################
            # TO DO - Distinguish between cancel and failure
            #       - Some sort of error notification
            ###########################         
    
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()