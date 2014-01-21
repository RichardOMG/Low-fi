#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Low-fi: Low frequency induction simulation

Results Tab

Author: Julius Susanto
Last edited: January 2014
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os, sys
import globals
import numpy as np
import dateutil, pyparsing
import matplotlib.pyplot as plt

                      
class results_ui(QtGui.QVBoxLayout): 
    
    def setup(self):
        
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
    
    # Calculate load and fault LFI voltages on the pipeline
    def calculate(self, tableWidget):
        
        # Pipeline longitudinal series impedance (in Ohm/km) - from CIGRE WG 36.02 Appendix G
        omega = 2 * np.pi * globals.network_data["freq"]
        mu_0 = 4 * np.pi * 1e-7
        Zi_re = 1/(np.pi * globals.pipe_data["diameter"] * np.sqrt(2)) * ((omega * globals.pipe_data["pipe_rho"] * mu_0 * globals.pipe_data["pipe_mu"]) ** 0.5) + omega * mu_0 / 8
        Zi_im = mu_0 * globals.network_data["freq"] * np.log((3.7/globals.pipe_data["diameter"]) * (globals.pipe_data["soil_rho"]/ (mu_0 * omega)) ** 0.5)
        Z_i = complex(Zi_re * 1000, Zi_im * 1000)
        
        # Pipeline longitudinal shunt admittance (in Ohm^-1/km) - from CIGRE WG 36.02 Appendix G
        Yi_re = np.pi * globals.pipe_data["diameter"] / globals.pipe_data["coat_rho"] / globals.pipe_data["coat_thickness"]
        Yi_im = omega * 8.85e-12 * globals.pipe_data["coat_mu"] * np.pi * globals.pipe_data["diameter"] / globals.pipe_data["coat_thickness"]
        Y_i = complex(Yi_re * 1000, Yi_im * 1000)
        
        # Return current depth
        D_e = 658.37 * (globals.pipe_data["soil_rho"] / globals.network_data["freq"]) ** 0.5
        
        # Set up empty matrices Y_p (pipeline admittance), Y_e (earth admittance), V_p (LFI voltage)
        Y_p = np.zeros([globals.no_sections,2], dtype=complex)
        Y_e = np.zeros([globals.no_sections,1], dtype=complex)
        V_p = np.zeros([globals.no_sections,1], dtype=complex)
        
        # Load currents
        I_a = complex(globals.network_data["current_a"] * np.cos(globals.network_data["angle_a"] * np.pi / 180), globals.network_data["current_a"] * np.sin(globals.network_data["angle_a"] * np.pi / 180))
        I_b = complex(globals.network_data["current_b"] * np.cos(globals.network_data["angle_b"] * np.pi / 180), globals.network_data["current_b"] * np.sin(globals.network_data["angle_b"] * np.pi / 180))
        I_c = complex(globals.network_data["current_c"] * np.cos(globals.network_data["angle_c"] * np.pi / 180), globals.network_data["current_c"] * np.sin(globals.network_data["angle_c"] * np.pi / 180))
        
        for row in range(0, globals.no_sections):
            # Compute pipeline admittances
            Y_p[row,0] = 1 / (Z_i * globals.sections[row,0] / 1000)
            Y_p[row,1] = Y_i * globals.sections[row,0] / 1000
            
            # Compute earth admittances
            if globals.sections[row,2] > 0:
                Y_e[row] = 1 / globals.sections[row,2]
            else:
                Y_e[row] = 0
            
            # Calculate effective (geometric mean) distances
            if row < (globals.no_sections - 1):
                L_a = (globals.sections[row,1] * globals.sections[row + 1,1]) ** 0.5
                L_b = ((globals.sections[row,1] + globals.tower_data["L_ab"]) * (globals.sections[row + 1,1] + globals.tower_data["L_ab"])) ** 0.5
                L_c = ((globals.sections[row,1] + globals.tower_data["L_ac"]) * (globals.sections[row + 1,1] + globals.tower_data["L_ac"])) ** 0.5
                L_w = ((globals.sections[row,1] + globals.tower_data["L_aw"]) * (globals.sections[row + 1,1] + globals.tower_data["L_aw"])) ** 0.5
            else:
                L_a = globals.sections[row,1]
                L_b = globals.sections[row,1] + globals.tower_data["L_ab"]
                L_c = globals.sections[row,1] + globals.tower_data["L_ac"]
                L_w = globals.sections[row,1] + globals.tower_data["L_aw"]
                
            D_ap = (L_a ** 2 + globals.tower_data["H_a"] ** 2) ** 0.5
            D_bp = (L_b ** 2 + globals.tower_data["H_b"] ** 2) ** 0.5
            D_cp = (L_c ** 2 + globals.tower_data["H_c"] ** 2) ** 0.5
            
            #########################################################
            # TO DO - Earth wire shielding factor calculation
            #         At the moment, a user-defined shielding 
            #         factor is used (a bit dodgy as can be "tuned")
            #########################################################
            # D_wp = (L_w ** 2 + globals.tower_data["H_w"] ** 2) ** 0.5
            
            # Equivalent distance for all three lines
            D_lp = (D_ap * D_bp * D_cp) ** (0.3333333333)
            
            # Mutual impedances between pipeline and line conductors
            Z_lp = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_lp))
            Z_ap = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_ap))
            Z_bp = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_bp))
            Z_cp = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_cp))
            
            if self.combo.currentText() == "Load LFI":
                # Load LFI (in V)
                V_p[row,0] = (Z_ap * I_a + Z_bp * I_b + Z_cp * I_c) * globals.network_data["shield_factor"] * globals.sections[row,0] / 1000
            else:
                # Fault LFI (in kV)
                V_p[row,0] = Z_lp * globals.network_data["fault_current"] * globals.network_data["split_factor"] * globals.network_data["shield_factor"] * globals.sections[row,0] / 1000        
        
        # LFI voltage vector
        Vbus = np.zeros([1 + 2 * globals.no_sections,1], dtype=complex)
        Vbus = np.concatenate((Vbus, V_p))
        
        # Construct Ybus matrix
        n = globals.no_sections
        order = 1 + 3 * n
        Ybus = np.zeros([order,order], dtype=complex)
        
        for row in range(0, n):
            # Include earth admittance
            if row == 0:
                Ybus[0, 0] = Y_e[0,0]
                Ybus[2, 2] = Y_p[row,0] + Y_p[row,1]
            else:
                Ybus[2*(row+1), 2*(row+1)] = Y_p[row,0] + Y_p[row,1]+ Y_e[row,0]
            
            Ybus[2*n + row + 1, 2*row] = 1
            Ybus[2*n + row + 1, 2*row + 1] = -1
            
            Ybus[2*row, 2*n + row + 1] = 1
            Ybus[2*row + 1, 2*n + row + 1] = -1
            
            Ybus[2*(row+1) - 1, 2*(row+1) - 1] = Y_p[row,0]
            Ybus[2*(row+1), 2*(row+1) - 1] = -Y_p[row,0]
            Ybus[2*(row+1) - 1, 2*(row+1)] = -Y_p[row,0]
        
        # Solve linear system
        Ymat = np.matrix(Ybus)
        Yinv = Ymat.getI()
        Vpipe = Yinv * Vbus
        
        # Get the final pipeline-to-earth touch voltage (absolute value, every second node)
        Vp_final = np.absolute(Vpipe[0:2*n+1:2])
        
        # Plot results
        pipe_distance = np.concatenate(([0], np.cumsum(globals.sections[:,0])))
        plt.plot(pipe_distance, Vp_final)
        plt.xlim([0, pipe_distance[n]])
        plt.xlabel("Distance along pipeline (m)")
        
        if self.combo.currentText() == "Load LFI":
            plt.ylabel("Pipeline-to-earth touch voltage (V)")
            plt.title("Load LFI Voltages")
        else:
            plt.ylabel("Pipeline-to-earth touch voltage (kV)")
            plt.title("Fault LFI Voltages")
        
        plt.grid(color = '0.75', linestyle='--', linewidth=1)
        plt.show()
        
        ##############
        # Diagnostics
        ##############
        
        #print pipe_distance
        #print Vp_final
        

    def refresh_data(self):
        """Update text fields to match global variables."""
        ##############
        # TO DO - Remove this if we don't need it
        ##############
        