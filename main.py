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

class Window(QtGui.QWidget):
    
    def __init__(self):
        super(Window, self).__init__()
        
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

        """
        Menubar
        """
        menu_bar = QtGui.QMenuBar() 
        fileMenu = menu_bar.addMenu('&File')
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
        tab_widget.addTab(tab2, "Tower Geometry") 
        tab_widget.addTab(tab3, "Pipeline") 
        tab_widget.addTab(tab4, "Load / Fault") 
        tab_widget.addTab(tab5, "Results") 
        
        page1 = rightofway_ui(tab1)
        page2 = towergeo_ui(tab2)
        
        page1.setup()
        page2.setup()
        
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

def main():
    
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()