#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Main window

Authors: Julius Susanto and Tom Walker
Last edited: February 2014
"""

import os, sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from rightofway import *
from towergeo import *
from pipeline import *
from network import *
from results import *
from diagnostics import *
from mapping import *

import matplotlib.backends.backend_tkagg

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
        tab6 = QtGui.QWidget()
        tab7 = QtGui.QWidget()
        self.tab_widget = tab_widget
               
        tab_widget.addTab(tab1, "Right of Way")
        tab_widget.addTab(tab2, "Tower") 
        tab_widget.addTab(tab3, "Pipeline") 
        tab_widget.addTab(tab4, "Network") 
        tab_widget.addTab(tab5, "Results") 
        tab_widget.addTab(tab6, "Map") 
        
        page1 = rightofway_ui(tab1)
        page2 = towergeo_ui(tab2)
        page3 = pipeline_ui(tab3)
        page4 = network_ui(tab4)
        page5 = results_ui(tab5)
        page6 = mapping_ui(tab6)
        self.mapping = page6    
        
        self.pages = [page1, page2, page3, page4]
        
        page6.setup(self)
        page1.setup(self)
        page2.setup(self)
        page3.setup(self)
        page4.setup(self)
        page5.setup(self)
        
        
        
        # A tab for display matrices as tables for diagnostic purposes
        self.diagnostics = diagnostics_ui(tab7)
        self.diagnostics_tab = tab7
        self.diagnostics.setup(self)
               
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
            
    def refresh_mapping(self):
        """Update mapping window based on global variables."""
        self.mapping.refresh_scene()
    
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

    def diagnostics_clear(self):
        """Clear the diagnostics tab."""
        if self.tab_widget.indexOf(self.diagnostics_tab) > -1:
            self.tab_widget.removeTab(self.tab_widget.indexOf(self.diagnostics_tab))
        self.diagnostics.clear()

    def diagnostics_matrix(self, title = "", data = [[]]):
        """Make a table in the diagnostics tab filled with matrix data."""
        if self.tab_widget.indexOf(self.diagnostics_tab) == -1:
            self.tab_widget.addTab(self.diagnostics_tab, "Diagnostics")
        self.diagnostics.log(title = title, data = data)

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
                   Version: <b>v0.2<b><P>
                   <p>
                   Website: <a href="http://www.sigmapower.com.au/low-fi.html">www.sigmapower.com.au/low-fi.html</a>
                   <p> </p>
                   <p><img src="images/Sigma_Power.png"></p>
                   <p>&copy; 2014 Sigma Power Engineering Pty Ltd</p>
                   <p>All rights reserved.</p>
                   <p>
                   Redistribution and use in binary form is permitted provided that the following conditions are met:
                   <p>
                    1. Redistributions in binary form must reproduce the above copyright
                       notice, this list of conditions and the following disclaimer in the
                       documentation and/or other materials provided with the distribution.
                   <p>
                    2. All advertising materials mentioning features or use of this software
                       must display the following acknowledgement:
                       This product includes software developed by the Sigma Power Engineering Pty Ltd.
                   <p>
                    3. Neither the name of the Sigma Power Engineering Pty Ltd nor the
                       names of its contributors may be used to endorse or promote products
                       derived from this software without specific prior written permission.
                   <p>
                    THIS SOFTWARE IS PROVIDED BY SIGMA POWER ENGINEERING PTY LTD ''AS IS'' AND ANY
                    EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
                    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
                    DISCLAIMED. IN NO EVENT SHALL SIGMA POWER ENGINEERING PTY LTD BE LIABLE FOR ANY
                    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
                    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
                    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
                    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
                    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
                    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.   
                   """)
    
    # triggered on window resize    
    def resizeEvent(self, event):
        self.refresh_mapping()
    
def main():
    
    app = QtGui.QApplication(sys.argv)
    splash_pix = QPixmap('images\splash_loading.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    
    w = Window()
    w.show()
    splash.finish(w)
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()