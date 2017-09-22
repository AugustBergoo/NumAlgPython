#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:25:00 2017

@author: August
"""

from scipy import *
from pylab import *
import numpy as np

class Linesearch():
    
    def makeT(self,func, grad, epsilon,xk):
        def T(step):
            return func(xk) + epsilon*step*grad(xk)
        return T
    
    def inexactLinesearch(self, xk, dk, func, grad): # Notation: see Antoniou Lu pp.112
        """Armijo's rule"""
        epsilon = 0.25
        alpha = 2 
        lamb = 2 # Initial guess for lambda.
        
        T = self.makeT(func, grad, epsilon,xk)
        
        while func(xk + lamb*dk) > T(lamb) and func(xk + alpha*lamb*dk) < T(alpha*lamb):
            if func(xk + lamb*dk) > T(lamb): # The step was too large
                lamb /= alpha
            else: # The step was too small.
                lamb *= alpha
        
        return lamb
        
    
    def exactLinesearch(self, xk, dk, func, grad):
        """The bisection method"""
        a = 0 # Lower interval.
        b = 2 # Upper interval.
        tol = 0.001

        # Find the upper interval by using parts of Armijo's rule.
        epsilon = 0.25
        alpha = 2
        T = self.makeT(func, grad, epsilon,xk)
        
        while func(xk + alpha*b*dk) < T(alpha*b):
            print(func(xk + alpha*b*dk),T(alpha*b))
            b *= alpha
        
        d_lamb = tol + 1
        old_lamb = 0
        while d_step > tol:
            lamb = (a + b) / 2
            if (grad(xk + lamb*dk) <= 0):
                a = lamb
            else:
                b = lamb
            
            d_lamb = abs(old_lamb - lamb)
            old_lamb = lamb
        
        return lamb
        
    
    

    
    