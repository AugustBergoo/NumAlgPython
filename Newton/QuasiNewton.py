#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:52:34 2017

@author: August
"""

from scipy import *
from pylab import *
import numpy as np
from GenericNewton import GenericNewton

class QuasiNewton(GenericNewton):
    # Assume we input objFunc and objGrad as pyton functions. E.g objFunc(xk) 
    # will return the function value in xk. Remember lineaserch is a pyton
    # function  always.
    
    # We start by setting the Hessian to the unit matrix. This was legit
    # according to the literature...
    def __init__(self, objFunc, objGrad, linesearch, tol, dim):
        super(QuasiNewton, self).__init__(tol)
        self.objFunc = objFunc
        self.objGrad = objGrad
        self.linesearch = linesearch
        self.H_k = np.eye(dim)
        
    
    # Structure of the step method:
        # A) set sk=-Hkkgk
        # B) line Search along sk giving xk+1=xk+ alpha*sk
        # C) update Hk giving, offcourse Hk+1
    def step(self, xk):
        #A)
        g_k = self.objGrad(xk)
        s_k = -self.H_k@g_k
        #B)
        alpha = self.linesearch(xk, s_k, self.objFunc, self.objGrad)
        xnext = xk + alpha*s_k
        #C)
        delta = xnext-xk
        gamma = self.objGrad(xnext)-self.objGrad(xk)
        self.H_k = self.updateB(delta,gamma)
        
        return xnext
   
    # Check if possible to make an abstract updateB method.
        
# The following classes approximates the next hessian or hessian inverse.
# Delta is the steplenght of the current step, and gamma is the change in 
# gradient of the same step.
class GoodBroyden(QuasiNewton):
    def updateB(self,delta,gamma):
        return self.H_k + (delta -self.H_k@gamma)@delta.T@self.H_k/(delta.T@self.H_k@gamma)

class BadBroyden(QuasiNewton):
    def updateB(self,delta,gamma): 
        return self.H_k+(delta -self.H_k@gamma)@gamma.T/(gamma.T@gamma)

class DFP(QuasiNewton):
    def updateB(self,delta,gamma):
        term1 = self.H_k+(delta@delta.T/((delta.T)@gamma))
        term2 = (self.H_k@gamma@gamma.T*self.H_k)/(gamma.T@self.H_k@gamma)
        return term1 - term2    
    

class BFGS(QuasiNewton):
    def updateB(self,delta,gamma): 
        dTg = np.transpose(delta)@gamma
        term1 = self.H_k + (1 + gamma.T@self.H_k@gamma/dTg)*(delta@delta.T)/dTg
        term2 = (delta@gamma.T@self.H_k + self.H_k@gamma@delta.T)/dTg
        return term1 - term2
        
    # Oklar Broydenmetod
#==============================================================================
#     class BadBroyden(QuasiNewton):
#     def updateB(self,delta,gamma): 
#         u = delta-(self.H_k@gamma)
#         a = 1/(np.transpose(u)@gamma)
#         return self.H_k+(a*u@np.transpose(u))
#==============================================================================
