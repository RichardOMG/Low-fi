#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Main window

Authors: Julius Susanto and Tom Walker
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
        self.setWindowTitle('SPE Low-fi | Low Frequency Induction Simulator')
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
        
        aboutAction = QtGui.QAction('&About Low-Fi', self)
        aboutAction.setStatusTip('About Low-Fi')
        aboutAction.triggered.connect(self.about_dialog)
        
        helpAction = QtGui.QAction('&User Manual', self)
        helpAction.setShortcut('F1')
        helpAction.setStatusTip('Low-Fi user documentation')
        helpAction.triggered.connect(self.user_manual)   
        
        """
        Menubar
        """
        menu_bar = QtGui.QMenuBar() 
        fileMenu = menu_bar.addMenu('&File')
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        helpMenu = menu_bar.addMenu('&Help')
        helpMenu.addAction(helpAction)
        helpMenu.addSeparator()
        helpMenu.addAction(aboutAction)
               
        """
        Toolbar
        
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        """
        
        """
        Status line.
        """
        self.status_message = QtGui.QStatusBar()                 
        
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
        
        page1.setup(self)
        page2.setup(self)
        page3.setup(self)
        page4.setup(self)
        page5.setup(self)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(menu_bar)
        vbox.addWidget(tab_widget) 
        vbox.addWidget(self.status_message)        
        
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
            
    def show_status_message(self, message, error = False, beep = False):
        """Display a status message on the status line.
           If error is True the status text will be coloured red.
           If beep is True then the application will beep.
        """
        if(error):
            self.status_message.setStyleSheet('QStatusBar {color: red}')
        else:
            self.status_message.setStyleSheet('')
        if beep:
            QApplication.beep()
        self.status_message.showMessage(message)

    def save_as_fn(self):
        """Function for the Save As action."""
        fname = QtGui.QFileDialog.getSaveFileName(self, "Save Data File As", "", "LowFi project files (*.lfi)")
        if fname:
            if globals.write_project_to_file(fname):
                self.show_status_message("Write to file " + fname + " successful.")
                self.refresh_data()                
            else:
                self.show_status_message("Failed to save " + fname + ".", error = True, beep = True)
        else:
            self.show_status_message("Save As cancelled.")                   
            ###########################
            # TO DO - Distinguish between cancel and failure
            #       - Put open filename in title bar
            ###########################
            
    def save_fn(self):    
        """Function for the Save action."""
        if globals.filename != "":
            if globals.write_project_to_file(globals.filename):                
                self.refresh_data()        
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
        fname = QtGui.QFileDialog.getOpenFileName(self, "Open Data File", "", "LowFi project files (*.lfi)")
        if fname:
            if globals.load_project_from_file(fname):                
                self.refresh_data()
                self.show_status_message("File " + fname + " successfully loaded.")
            else:
                self.show_status_message("Failed to open " + fname + ".", error = True, beep = True)
        else:
            self.show_status_message("Open Data File cancelled.")
    
    # Launch user manual
    def user_manual(self):
        os.system("start docs/low-fi-doc.pdf")
    
    # About dialog box
    def about_dialog(self):
        QtGui.QMessageBox.about(self, "About Low-Fi",
                """<b>Low-Fi</b> is a low-frequency induction (LFI) simulator that is intended to calculate induced voltages on pipelines sharing a joint right-of-way with overhead powerlines.
                   <p>
                   This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
                   <p>
                   This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the <a href="http://www.gnu.org/licenses/gpl.html">GNU General Public License</a> for more details. 
                   <p>
                   Version: <b>v0.1 Beta<b><P>
                   <p>
                   Website: <a href="http://www.sigmapower.com.au/low-fi.html">www.sigmapower.com.au/low-fi.html</a>
                   <p> </p>
                   <p><img src="images/Sigma_Power.png"></p>
                   <p>&copy; 2014 Sigma Power Engineering Pty Ltd</p>
                   """)
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()