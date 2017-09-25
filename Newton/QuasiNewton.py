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
        print(self.H_k)
        g_k = self.objGrad(xk)
        s_k = -self.H_k@g_k
        #B)
        alpha = self.linesearch(xk, s_k, self.objFunc, self.objGrad)
        xnext = xk + alpha*s_k
        #C)
        delta = xnext-xk
        gamma = self.objGrad(xnext)-self.objGrad(xk)
        self.H_k = self.updateB(delta,gamma)
        #print(self.H_k)
        
        return -delta
   
    # Check if possible to make an abstract updateB method.
        
# The following classes approximates the next hessian or hessian inverse.
# Delta is the steplenght of the current step, and gamma is the change in 
# gradient of the same step.
class GoodBroyden(QuasiNewton):
    def updateB(self,delta,gamma):
        return self.H_k + np.outer((delta -self.H_k@gamma),delta)@self.H_k/(delta@self.H_k@gamma)

class BadBroyden(QuasiNewton):
    def updateB(self,delta,gamma): 
        return self.H_k+np.outer((delta -self.H_k@gamma),gamma)/(gamma@gamma)

class DFP(QuasiNewton):
    def updateB(self,delta,gamma):
        term1 = self.H_k+(np.outer(delta,delta)/(delta@gamma))
        term2 = (self.H_k@np.outer(gamma,gamma)@self.H_k)/(gamma@self.H_k@gamma)
        return term1 - term2    
    

class BFGS(QuasiNewton):
    def updateB(self,delta,gamma): 
        print("delta: ",np.shape(np.transpose(delta)), "gamma: ",np.shape(gamma))
        print("delta@gamma.T: ",delta@gamma.T)
        dTg = delta@gamma
        
        term1 = self.H_k + (1 + gamma@self.H_k@gamma/dTg)*(np.outer(delta,delta)/dTg)
        term2 = (np.outer(delta,gamma)@self.H_k + self.H_k@np.outer(gamma,delta)/dTg)
        return term1 - term2
    
#==============================================================================
# class BroydenQ(QuasiNewton):
#     def __init__(self, objFunc, objGrad, linesearch, tol, dim):
#         super(BroydenQ, self).__init__(objFunc, objGrad, linesearch, tol, dim)
#         self.Q_k = initialQ
#     
#     def updateB(self,delta,gamma):
#         self.Q_k = self.Q_k + np.outer((gamma-Q_k@delta),delta)/np.dot(delta,delta)
#         return inv(self.Q_k)
#==============================================================================
        
    # Oklar Broydenmetod
#==============================================================================
#     class BadBroyden(QuasiNewton):
#     def updateB(self,delta,gamma): 
#         u = delta-(self.H_k@gamma)
#         a = 1/(np.transpose(u)@gamma)
#         return self.H_k+(a*u@np.transpose(u))
#==============================================================================
