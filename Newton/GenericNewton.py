#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:34:54 2017

@author: August
"""

from scipy import *
from pylab import *

class GenericNewton():
    
    def __init__(self, tol):
        pass
    
    def findMin(self, x0):
        xk = x0
        while (err > tol):
            step = self.step(xk)
            xk1 = xk - step
            xk = xk1
            
    # Abstrakt step metod önskas här. Fixa din latmask!
        

