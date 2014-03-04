# -*- coding: utf-8 -*-
"""
Low-fi: Low frequency induction simulation

Setup script

Authors: Julius Susanto and Tom Walker
Last edited: March 2014
"""

import sys
from cx_Freeze import setup, Executable

setup(name = "LowFi", version = "1.0", description = "Low Frequency Induction modelling tool.", executables = [Executable("main.py", base="Win32GUI")])