#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:34:54 2017

@author: Simon
"""

from scipy import *
from pylab import *

import numpy as np

class GenericNewton():
    
    def __init__(self, tol):
        self.tol = tol;
    
    def findMin(self, x0):
        xk = x0
        
        # itr is the amount of steps the loop will run before stopping, if 
        # the tolerance is not met.
        itr = 10000
        for i in range(itr):       
            xk1 = xk - self.step(xk)
            dx = np.linalg.norm(xk1 - xk)
            print(xk)
            xk = xk1
            print(xk1)
            print(dx)
            print('-------------------')
            
            # Breaks the loop if the "step length" is shorter than the tolerance
            if dx < self.tol:
                print('The problem converged in', i, 'steps.')
                break
               
        if i == itr-1:
            print('The problem did not converge in', itr, 'steps.')
            
        return xk
