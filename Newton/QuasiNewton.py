#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:52:34 2017

@author: August
"""

from scipy import *
from pylab import *

class QuasiNewton(GenericNewton):
    
    def __init__(self, objFunc, objGrad, linesearch, tol):
        super(tol)
        pass
    
    def step(self, xk):
        pass
        
    # Check if possible to make an abstract updateB method.
        

class GoodBroyden(QuasiNewton):
    def updateB(self): 
        pass

class BadBroyden(QuasiNewton):
    def updateB(self): 
        pass

class DFP(QuasiNewton):
    def updateB(self): 
        pass

class BFGS(QuasiNewton):
    def updateB(self): 
        pass
        