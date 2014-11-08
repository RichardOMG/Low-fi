# -*- coding: utf-8 -*-
"""
Low-fi: Low frequency induction simulation

Calculation method.  Called by results tab.

Authors: Julius Susanto and Tom Walker
Last edited: February 2014
"""

import globals
import numpy as np
import dateutil, pyparsing
import matplotlib.pyplot as plt

def calculate(loadLFI, mutual_impedance_formula = 0):
        # Mutual impedance formulae detailed further on.

        # Pipeline longitudinal series impedance (in Ohm/km) - from CIGRE WG 36.02 Appendix G
        # Real part (is constant as it does not depend on soil resistivity)
        omega = 2 * np.pi * globals.network_data["freq"]
        mu_0 = 4 * np.pi * 1e-7
        Zi_re = 1/(np.pi * globals.pipe_data["diameter"] * np.sqrt(2)) * ((omega * globals.pipe_data["pipe_rho"] * mu_0 * globals.pipe_data["pipe_mu"]) ** 0.5) + omega * mu_0 / 8
        
        # Pipeline longitudinal shunt admittance (in Ohm^-1/km) - from CIGRE WG 36.02 Appendix G
        # Applies only when coat_rho >> soil_rho

        ################################################
        # TO DO - expanded formulation for general case 
        #         (see Appendix G of CIGRE WG 36.02)
        ################################################
        
        Yi_re = np.pi * globals.pipe_data["diameter"] / globals.pipe_data["coat_rho"] / globals.pipe_data["coat_thickness"]
        Yi_im = omega * 8.85e-12 * globals.pipe_data["coat_mu"] * np.pi * globals.pipe_data["diameter"] / globals.pipe_data["coat_thickness"]
        Y_i = complex(Yi_re * 1000, Yi_im * 1000)
        
        # Set up empty matrices Y_p (pipeline admittance), Y_e (earth admittance), V_p (LFI voltage)
        Y_p = np.zeros([globals.no_sections,2], dtype=complex)
        Y_e = np.zeros([globals.no_sections,1], dtype=complex)
        V_p = np.zeros([globals.no_sections,1], dtype=complex)
        
        # Load currents
        I_a = complex(globals.network_data["current_a"] * np.cos(globals.network_data["angle_a"] * np.pi / 180), globals.network_data["current_a"] * np.sin(globals.network_data["angle_a"] * np.pi / 180))
        I_b = complex(globals.network_data["current_b"] * np.cos(globals.network_data["angle_b"] * np.pi / 180), globals.network_data["current_b"] * np.sin(globals.network_data["angle_b"] * np.pi / 180))
        I_c = complex(globals.network_data["current_c"] * np.cos(globals.network_data["angle_c"] * np.pi / 180), globals.network_data["current_c"] * np.sin(globals.network_data["angle_c"] * np.pi / 180))
        
        for row in range(0, globals.no_sections):
            
            # Pipeline longitudinal series impedance (in Ohm/km) - from CIGRE WG 36.02 Appendix G
            Zi_im = 1/(np.pi * globals.pipe_data["diameter"] * np.sqrt(2)) * ((omega * globals.pipe_data["pipe_rho"] * mu_0 * globals.pipe_data["pipe_mu"]) ** 0.5) + mu_0 * globals.network_data["freq"] * np.log((3.7/globals.pipe_data["diameter"]) * (globals.sections[row,4] / (mu_0 * omega)) ** 0.5)
            print(Zi_im)
            Z_i = complex(Zi_re * 1000, Zi_im * 1000)
        
            # Compute pipeline admittances
            Y_p[row,0] = 1 / (Z_i * globals.sections[row,0] / 1000)
            Y_p[row,1] = Y_i * globals.sections[row,0] / 1000
            
            # Compute earth admittances
            earth_resistance = np.complex(globals.sections[row,2], globals.sections[row,3])
            if globals.sections[row,2] > 0:
                Y_e[row] = 1 / earth_resistance
            else:
                Y_e[row] = 0
            
            # Calculate effective (geometric mean) distances
            if (row < (globals.no_sections - 1)) and (globals.sections[row + 1,1] > 0):
                L_a = (globals.sections[row,1] * globals.sections[row + 1,1]) ** 0.5
                L_b = ((globals.sections[row,1] + globals.tower_data["L_ab"]) * (globals.sections[row + 1,1] + globals.tower_data["L_ab"])) ** 0.5
                L_c = ((globals.sections[row,1] + globals.tower_data["L_ac"]) * (globals.sections[row + 1,1] + globals.tower_data["L_ac"])) ** 0.5
                L_w = ((globals.sections[row,1] + globals.tower_data["L_aw"]) * (globals.sections[row + 1,1] + globals.tower_data["L_aw"])) ** 0.5
            else:
                L_a = globals.sections[row,1]
                L_b = globals.sections[row,1] + globals.tower_data["L_ab"]
                L_c = globals.sections[row,1] + globals.tower_data["L_ac"]
                L_w = globals.sections[row,1] + globals.tower_data["L_aw"]
    
            #####################################################
            # TO DO - Earth wire shielding factor calculation
            #         for fault LFI
            #####################################################
            
            # Calculate mutual impedance of pipeline and aerial conductors
            if mutual_impedance_formula == 1 or mutual_impedance_formula == 2:
                # Ametani and Lucca both use the same inputs
                if mutual_impedance_formula == 1:
                    mutual_impedance = ametani_approximation
                else:
                    mutual_impedance = lucca_approximation
            
                rho_e = globals.sections[row,4]
                
                # Return current depth
                D_e = 658.37 * (globals.sections[row,4] / globals.network_data["freq"]) ** 0.5
                
                # For the moment depth of burial is set to 1m..            
                h2 = 1

                # Equivalent distances for conductors            
                H_aw = np.abs(globals.tower_data["H_w"] - globals.tower_data["H_a"])
                H_bw = np.abs(globals.tower_data["H_w"] - globals.tower_data["H_b"])
                H_cw = np.abs(globals.tower_data["H_w"] - globals.tower_data["H_c"])                
                H_lw = (H_aw * H_bw * H_cw) ** (0.3333333333)
                H_lp = (globals.tower_data["H_a"] * globals.tower_data["H_b"] * globals.tower_data["H_c"]) ** (0.3333333333)

                L_aw = abs(globals.tower_data["L_aw"])
                L_bw = abs(globals.tower_data["L_ab"] - globals.tower_data["L_aw"])
                L_cw = abs(globals.tower_data["L_ac"] - globals.tower_data["L_aw"])
                L_lw = (L_aw * L_bw * L_cw) ** (0.3333333333)
                L_lp = (L_a * L_b * L_c) ** (0.3333333333)     
                
                # Mutual impedances between pipeline and line conductors                
                Z_lp = mutual_impedance(omega, mu_0, rho_e, H_lp - h2, h2, L_lp)
                Z_lw = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / np.sqrt(H_lw ** 2 + L_lw ** 2)))
                Z_ap = mutual_impedance(omega, mu_0, rho_e, globals.tower_data["H_a"] - h2, h2, L_a)
                Z_bp = mutual_impedance(omega, mu_0, rho_e, globals.tower_data["H_b"] - h2, h2, L_b)
                Z_cp = mutual_impedance(omega, mu_0, rho_e, globals.tower_data["H_c"] - h2, h2, L_c)
                
                # Earthwire impedances
                Z_aw = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / np.sqrt(H_aw ** 2 + L_aw ** 2)))                
                Z_bw = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / np.sqrt(H_bw ** 2 + L_bw ** 2)))                
                Z_cw = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / np.sqrt(H_cw ** 2 + L_cw ** 2)))                
                Z_wp = mutual_impedance(omega, mu_0, rho_e, globals.tower_data["H_w"], 0, L_w)
            
                
            else:
                # AS4853 version of Carson-Clem mutual impedance approximation            
            
                # Return current depth
                D_e = 658.37 * (globals.sections[row,4] / globals.network_data["freq"]) ** 0.5
            
                D_ap = (L_a ** 2 + globals.tower_data["H_a"] ** 2) ** 0.5
                D_bp = (L_b ** 2 + globals.tower_data["H_b"] ** 2) ** 0.5
                D_cp = (L_c ** 2 + globals.tower_data["H_c"] ** 2) ** 0.5            
                
                D_aw = (globals.tower_data["L_aw"] ** 2 + (globals.tower_data["H_w"] - globals.tower_data["H_a"]) ** 2) ** 0.5
                D_bw = ((globals.tower_data["L_aw"] - globals.tower_data["L_ab"]) ** 2 + (globals.tower_data["H_w"] - globals.tower_data["H_b"]) ** 2) ** 0.5
                D_cw = ((globals.tower_data["L_aw"] - globals.tower_data["L_ac"]) ** 2 + (globals.tower_data["H_w"] - globals.tower_data["H_c"]) ** 2) ** 0.5
                D_wp = (L_w ** 2 + globals.tower_data["H_w"] ** 2) ** 0.5
                            
                # Equivalent distance for all three lines
                D_lp = (D_ap * D_bp * D_cp) ** (0.3333333333)
                D_lw = (D_aw * D_bw * D_cw) ** (0.3333333333)                
                
                # Mutual impedances between pipeline and line conductors            
                Z_lp = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_lp))
                Z_lw = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_lw))
                Z_ap = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_ap))
                Z_bp = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_bp))
                Z_cp = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_cp))
                
                # Earth wire mutual impedances
                Z_aw = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_aw))                
                Z_bw = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_bw))
                Z_cw = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_cw))                
                Z_wp = complex(9.869e-4 * globals.network_data["freq"], 2.8935e-3 * globals.network_data["freq"] * np.log10(D_e / D_wp))

            # Self impedance of earth wire
            Z_w = globals.tower_data["Z_w"]                                       
                       
            # Adjusted mutual impedance with influence of earth wire
            Z_apw = Z_ap - Z_aw * Z_wp / Z_w
            Z_bpw = Z_bp - Z_bw * Z_wp / Z_w
            Z_cpw = Z_cp - Z_cw * Z_wp / Z_w
            Z_lpw = Z_lp - Z_lw * Z_wp / Z_w
            
            # Adjust currents for line transpositions
            I_at = I_a * np.exp(complex(0, 2 * np.pi / 3 * int(globals.sections[row,5])))
            I_bt = I_b * np.exp(complex(0, 2 * np.pi / 3 * int(globals.sections[row,5])))
            I_ct = I_c * np.exp(complex(0, 2 * np.pi / 3 * int(globals.sections[row,5])))
            
            if globals.sections[row,1] < 0:
                # Non parallel section = no induced voltage
                V_p[row,0] = 0
            else:           
                if loadLFI:
                    # Load LFI (in V)
                    if (globals.tower_data["L_aw"] >= 0) or (globals.tower_data["H_w"] >= 0):
                        # With earth wire
                        V_p[row,0] = (Z_apw * I_at + Z_bpw * I_bt + Z_cpw * I_ct) * globals.network_data["shield_factor"] * globals.sections[row,0] / 1000
                    else:
                        # No earth wire
                        V_p[row,0] = (Z_ap * I_at + Z_bp * I_bt + Z_cp * I_ct) * globals.network_data["shield_factor"] * globals.sections[row,0] / 1000
                else:
                    # Fault LFI (in kV)
                    if (globals.tower_data["L_aw"] >= 0) or (globals.tower_data["H_w"] >= 0):
                        # With earth wire
                        V_p[row,0] = Z_lpw * globals.network_data["fault_current"] * globals.network_data["split_factor"] * globals.network_data["shield_factor"] * globals.sections[row,0] / 1000      
                    else: 
                        # No earth wire
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

        diagnostics = [("right of way", globals.sections), ("omega", omega), ("mu_0", mu_0), ("Zi_re", Zi_re)]        
        diagnostics = diagnostics + [("Yi_re", Yi_re), ("Yi_im", Yi_im), ("Y_i", Y_i)]        
        diagnostics = diagnostics + [("Y_p", Y_p), ("Y_e", Y_e), ("V_p", V_p)]                
        diagnostics = diagnostics + [("I_a", I_a), ("I_b", I_b), ("I_c", I_c)]        
        diagnostics = diagnostics + [("Ybus", Ybus), ("Ymat", Ymat), ("Yinv", Yinv), ("Vpipe", Vpipe), ("Vp_final", Vp_final), ("pipe_distance", pipe_distance)]        

        
        return [ pipe_distance, Vp_final, diagnostics ]


def ametani_approximation(omega, mu_0, rho, h1, h2, y):
    """Calculates mutual impedance between overhead conductor and buried conductor using the Ametani mutual impedance approximation.
    This function implements equation 27 of the paper which calculates Ohm/m.  This is converted to Ohm/km, hence the factor of 1000.
    
    A. Ametani, T. Yoneda, Y. Baba, N. Nagaoka, "An Investigation of Earth-Return Impedance Between Overhead and 
    Underground Conductors and Its Approximation", IEEE Transactions on Electromagnetic Compatibility, vol 51, 
    no. 3, pp860-867, Aug. 2009

    :param omega: System frequency (rad/s)
    :type omega: Float
    :param mu_o: Free space permeability
    :type mu_0: Float
    :param rho: Earth resistivity of soil
    :type rho: Float
    :param h1: Height of overhead conductor above ground
    :type h1: Float
    :param h2: Depth of buried of underground conductor
    :type h2: Float
    :param y: Horizontal separation between conductors
    :type y: Float
    """
    m = np.sqrt(1j * omega * mu_0 / rho)
    he = 1 / m
    H = h1 + h2 + 2 * he
    S = np.sqrt(H ** 2 + y ** 2)
    D = np.sqrt((h1 + h2) ** 2 + y ** 2)
    Zm = 1000j * omega * (mu_0 / (2 * np.pi)) * np.exp(-h2 / he) * np.log10(S / D) / np.log10(np.exp(1))    
    return Zm
    
def lucca_approximation(omega, mu_0, rho, h1, h2, y):
    """Calculates mutual impedance between overhead conductor and buried conductor using the Lucca mutual impedance approximation.
    This function implements the Lucca's approximation as expressed in Ametani's paper, equation 28.  This is converted to Ohm/km.
    
    G. Lucca, "Mutual Impedance Between an Overhead and a Buried Line with Earth Return", in Proc. Int. Electr. Eng. 
    9th Int. Conf. EMC, 1994, pp80-86
    A. Ametani, T. Yoneda, Y. Baba, N. Nagaoka, "An Investigation of Earth-Return Impedance Between Overhead and 
    Underground Conductors and Its Approximation", IEEE Transactions on Electromagnetic Compatibility, vol 51, 
    no. 3, pp860-867, Aug. 2009

    :param omega: System frequency (rad/s)
    :type omega: Float
    :param mu_o: Free space permeability
    :type mu_0: Float
    :param rho: Earth resistivity of soil
    :type rho: Float
    :param h1: Height of overhead conductor above ground
    :type h1: Float
    :param h2: Depth of buried of underground conductor
    :type h2: Float
    :param y: Horizontal separation between conductors
    :type y: Float
  
    """
    m = np.sqrt(1j * omega * mu_0 / rho)
    he = 1 / m
    H = h1 + h2 + 2 * he
    S = np.sqrt(H ** 2 + y ** 2)
    D = np.sqrt((h1 + h2) ** 2 + y ** 2)
    Zl = 1000j * omega * (mu_0 / (2 * np.pi)) * (np.log10(S / D) / np.log10(np.exp(1)) - (2 / 3) * ((he / S**2)**3) * H * (H**2 - 3 * y**2))
    return Zl