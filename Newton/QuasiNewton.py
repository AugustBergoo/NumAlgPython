#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:52:34 2017

@author: August
"""

from scipy import *
from pylab import *
import numpy as np

class QuasiNewton(GenericNewton):
    # Assume we input objFunc and objGrad as pyton functions. E.g objFunc(xk) 
    # will return the function value in xk. Remember lineaserch is a pyton
    # function  always.
    
    # We start by setting the Hessian to the unit matrix. This was legit
    # according to the literature...
    def __init__(self, objFunc, objGrad, linesearch, tol, initialGuess):
        super(tol)
        self.objFunc = objFunc
        self.objGrad = objGrad
        self.linesearch = linesearch
        self.H_k = np.eye(len(initialGuess))
        
    
    # Structure of the step method:
        # A) set sk=-Hkkgk
        # B) line Search along sk giving xk+1=xk+ alpha*sk
        # C) update Hk giving, offcourse Hk+1
    def step(self, xk):
        #A)
        g_k = self.objGrad(xk)
        s_k = -self.H_k*g_k
        #B)
        alpha = linesearch(xk, s_k, self.objFunc, self.objGrad)
        xnext = xk + aplha*s_k
        #C)
        self.H_k = self.updateB(xk,xnext)
   
    # Check if possible to make an abstract updateB method.
        

class GoodBroyden(QuasiNewton):
    def updateB(self,xk,xnext): 
        return

class BadBroyden(QuasiNewton):
    def updateB(self,xk,xnext): 
        pass

class DFP(QuasiNewton):
    def updateB(self,xk,xnext): 
        pass

class BFGS(QuasiNewton):
    def updateB(self,xk,xnext): 
        pass
    
    
    
a = GoodBroyden(objFunc,kdsjdkdds,ds sdds,,d,sd)
a.findMin()