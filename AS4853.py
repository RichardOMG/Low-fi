# -*- coding: utf-8 -*-
"""
AS4853 calculation module

Performs calculations to analyse induced voltages on metallic pipelines due to nearby AC powerlines.
Variables are capitalised in the same style as AS4853:2012 to enhance readability when compared to the standard.

@author: Tom Walker
@lastupdate: 2013-12-31
"""
import numpy as np 

def mutual_impedances_load_LFI(Hap, Lap, Hwp, Lwp, rw, GMRw, p, f):
    """Return the mutual impedances Zap, Zbp, Zcp calculated from overhead high voltage powerline and metallic pipeline geometry.
       Refer AS4853:2012 Appendix B for calculation methodologies.
        B2 - LFI calculation - no overhead earthwires.
        B3 - LFI calculation - with overhead earthwires.
       
       This calculation is intended for the following cases:
         Single wire earth return systems
         1 to N circuit 3-phase systems with 0 to 2 earth wires    
    
       To simplify error handling the following assumptions are made:
         Size of Hap and Lap will be equal
         Size of Hwp and Lwp will be equal
         Input data is meaningful         
    
       Calculations are only valid for conditions where d <= 90 * sqrt(p/f).              
              
       Calculation for 2 earth wires has not yet been implemented.
              
       :param Hap: phase conductor height above pipeline (m)
       :type Hap: list of conductor height values structured as [[circuit 1 phase conductor heights]...[circuit N phase conductor heights]]
       :param Lap: phase conductor horizontal distance to pipeline (m)
       :type Lap: list of conductor horizontal distances structured as [[circuit 1 phase conductors]...[circuit N phase conductors]]
       :param Hwp: earth conductor height from pipeline (m)
       :type Hwp: list of earth conductor heights structured as [conductor 1, conductor 2]
       :param Lwp: earth conductor horizontal distance to pipeline (m)
       :type Lwp: list of earth conductor distances structured as [conductor 1, conductor 2]
       :param rw: a.c. resistance of earthwires (Ohm/km)
       :type rw: list of resistances structured as [conductor 1, conductor 2]
       :param GMRw: geometric mean radius of earthwires 
       :type rw: list of mean radii as [conductor 1, conductor 2]
       :param p: soil resistivity (Ohm.m) 
       :type p: float
       :param f: system frequency (Hz)
       :type f: float
       
       :returns: mutual impedances between conductor and pipeline for each active conductor
       :rtype: 2-D numpy array of complex numbers
    """
    Hap = np.array(Hap)
    Lap = np.array(Lap)
    Dap = np.sqrt(Hap**2 + Lap**2)
    
    De = earth_return_current_depth(p, f)
    Zap = np.array([[mutual_impedance(De, Dnp, f) for Dnp in Dcctp] for Dcctp in Dap])
    
    Hwp = np.array(Hwp)
    Lwp = np.array(Lwp)
    Dwp = np.sqrt(Hwp**2 + Lwp**2)
    earths = Dwp.shape
    
    if earths[0] == 0:
        Zapp = Zap
    elif earths[0] == 1:
        Daw = np.array((Hap - Hwp[0])**2 + (Lap - Lwp[0])**2)
        Zaw = np.array([[mutual_impedance(De, Dnw, f) for Dnw in Dcctw] for Dcctw in Daw])        
        Zwp = mutual_impedance(De, Dwp[0], f)
        Zw = earth_wire_self_impedance(De, GMRw, rw, f)
        Zapp = Zap - (Zaw * Zwp) / Zw
    elif earths[0] == 2:
        # Two earthwires..
        # Need a more complicated expression for Zapp
        Zapp = Zap   
    
    return Zapp
    
    
def mutual_impedance_fault_LFI(Hap, Lap, Hwp, Lwp, KSF, p, f):
    """Return the mutual impedance Z1p calculated from overhead high voltage powerline and metallic pipeline geometry.
    Refer AS4853:2012 Appendix C
    C2 - Calculations using p = 100Ohm.m
    C3 - Mutual impedance when p varies from 100Ohm.m
    
    Conductors are lumped to determine a geometric mean separation.  Impedance is calculated for single mean conductor.
    
    Keyword arguments:
    :param Hap: phase conductor height above pipeline (m)
    :type Hap: list of conductor height values structured as [[circuit 1 phase conductor heights]...[circuit N phase conductor heights]]
    :param Lap: phase conductor horizontal distance to pipeline (m)
    :type Lap: list of conductor horizontal distances structured as [[circuit 1 phase conductors]...[circuit N phase conductors]]
    :param Hwp: earth conductor height from pipeline (m)
    :type Hwp: list of earth conductor heights structured as [conductor 1, conductor 2]
    :param Lwp: earth conductor horizontal distance to pipeline (m)
    :type Lwp: list of earth conductor distances structured as [conductor 1, conductor 2]
    :param KSF: shielding factor (ratio of current in ground to current in high voltage powerline)
    :type KSF: complex
    :param p: soil resistivity (Ohm.m) 
    :type p: float
    :param f: system frequency (Hz)
    :type f: float
    
    :returns: mutual impedance between faulted conductor and pipeline, adjusted shielding factor
    :rtype: list structured as [Z1p, KSFp]

    """
    Hap = np.array(Hap)
    Lap = np.array(Lap)
    Dap = np.sqrt(Hap**2 + Lap**2)
    actives = np.prod(Hap.shape)
    
    D1p = Dap.prod()**(1.0 / actives)
       
    De = earth_return_current_depth(p, f)
    Z1p = mutual_impedance(De, D1p, f)
    
    Hwp = np.array(Hwp)
    Lwp = np.array(Lwp)
    Dwp = np.sqrt(Hwp**2 + Lwp**2)    
    earths = np.prod(Dwp.shape)
        
    KSFp = KSF    

    if earths > 0:
        Dwp = Dwp.prod()**(1.0 / earths)
        Zwp = mutual_impedance(De, Dwp, f)
        KSFp = 1 - (1 - KSF) * Zwp / Z1p
            
    return [Z1p, KSFp]

def induced_voltage_load_LFI_per_length(Zap, Ia, k = 1.0):
    """Return the voltage induced on the metallic pipeline due to load conditions.
    Refer AS4853:2012 equation B1    
    
    :param Zap: mutual impedance between pipeline and powerline (Ohm/km)
    :type Zap: 2-D list of mutual impedances structured as [[Z1ap Z1bp Z1cp]...[Znap Znbp Zncp]]
    :param Ia: load condition phase currents (A)
    :type Ia: 2-D list of phase currents structured as [[I1a I1b I1c]...[Ina Inb Inc]]
    :param k: shielding factor
    :type k: complex
    
    :returns: voltage induced on metallic pipeline (V/km)
    :rtype: complex
    """
    Ia = np.array(Ia)
    Zap = np.array(Zap)
    Vp = (Ia * Zap).sum() * k
    return Vp
    
def induced_voltage_load_LFI(Zap, Ia, L, k = 1.0):
    """Return the voltage induced on the metallic pipeline due to load conditions.
    Refer AS4853:2012 equation B1    
    
    :param Zap: mutual impedance between pipeline and powerline (Ohm/km)
    :type Zap: 2-D list of mutual impedances structured as [[Z1ap Z1bp Z1cp]...[Znap Znbp Zncp]]
    :param Ia: load condition phase currents (A)
    :type Ia: 2-D list of phase currents structured as [[I1a I1b I1c]...[Ina Inb Inc]]
    :param L: length of exposure (km)
    :type L: float
    :param k: shielding factor
    :type k: complex
    
    :returns: voltage induced on metallic pipeline (V)
    :rtype: complex
    """
    return induced_voltage_load_LFI_per_length(Zap, Ia, k) * L
    
def induced_voltage_fault_LFI_per_length(Z1p, If, KSF):
    """Return the voltage induced on the metallic pipeline due to fault conditions.
    Refer AS4853:2012 equation C5
    
    Note that load LFI functions provide a more general version of this function.    
    
    :param Z1p: mutual impedance between pipeline and powerline (Ohm/km)
    :type Zap: complex
    :param If: fault current (A)
    :type I0: complex
    :param KSF: shielding factor
    :type KSF: complex
    
    :returns: voltage induced on metallic pipeline (V/km)
    :rtype: complex
    """
    return Z1p * If * KSF
    
def induced_voltage_fault_LFI(Z1p, If, L, KSF):
    """Return the voltage induced on the metallic pipeline due to fault conditions.
    Refer AS4853:2012 equation C5
    
    Note that load LFI functions provide a more general version of this function.    
    
    :param Z1p: mutual impedance between pipeline and powerline (Ohm/km)
    :type Zap: complex
    :param If: fault current (A)
    :type I0: complex
    :param L: length of exposure (km)
    :type L: float    
    :param KSF: shielding factor
    :type KSF: complex
    
    :returns: voltage induced on metallic pipeline (V)
    :rtype: complex
    """
    return Z1p * If * KSF * L
    
def earth_return_current_depth(p = 100.0, f = 50.0):
    """Calculate the earth return current depth De.
    Refer AS4853:2012 Equation C2.
    
    :param p: soil resistivity (Ohm.m) 
    :type p: float
    :param f: system frequency (Hz)
    :type f: float
    
    :returns: earth current return depth, De (m)
    :rtype: float
    """
    return 658.37 * np.sqrt(p / f)

def check_distance_validity(d, p = 100.0, f = 50.0):
    """Check if parallel exposure separation distance is such that calculation will be accurate.
    Refer AS4853:2012 Appendix C2.

    :param d: separation distance between conductor and pipeline (m)
    :type d: float
    :param p: soil resistivity (Ohm.m) 
    :type p: float
    :param f: system frequency (Hz)
    :type f: float
    
    :returns: true if parallel exposure separation distance is within limits of the standard
    :rtype: boolean
    """    
    return d <= (90 * np.sqrt(p / f))    

def mutual_impedance(Dep, Dlp, f = 50.0):
    """Calculate mutual impedance between conductor and pipeline.
    Refer AS4853:2012 Equation C1.        
    
    :param De: earth return current depth (m)
    :type De: float
    :param Dlp: separation distance between conductor and pipeline (m)
    :type D1p: float
    :param f: system frequency (Hz)
    :type f: float
    
    :returns: Mutual impedance between conductor and pipeline (Ohm/km)
    :rtype: complex
    """    
    return complex(9.869e-4 * f, 2.8935e-3 * f * np.log10(Dep / Dlp))

def earth_wire_self_impedance(De, GMRw, rw, f = 50.0):
    """Calculate the self impedance of an earth wire.
    Refer AS3854:2012 Appendix B3.
        
    :param De: earth return current depth (m)
    :type De: float
    :param GMRw: Geometric mean radius of earthwire (m)
    :type GMRw: float
    :param rw: AC resistance of earthwire (Ohm/km)
    :type rw: float
    :param f: system frequency (Hz)
    :type f: float
    
    :returns: Self impedance of earth wire (Ohm/km)
    :rtype: complex
    """
    return complex(rw + 9.869e-4 * f, 2.8935e-3 * f * np.log10(De / GMRw))

def to_do():
    """To do list:
                
         calculation for shielding factors
         calculation for pipeline electrical characteristics
         circuit model of pipeline (Appendix E - LFI calculation)
         
         tables of conductor A.C. resistance, square area, radius
                 
         functions to log progress of calc for verification purposes (to file, etc.)
         
         graph Z1p for varying distance, check validity of parallel exposure distances
         
         handling of underground cables (refer shielding factor given in appendix B4)
         
         error handling, sanitising inputs         
         
         """
         

         