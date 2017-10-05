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
        self.H_k = self.updateH(delta,gamma)
        
        return -delta
   
    # Check if possible to make an abstract updateB method.
        
# The following classes approximates the next hessian or hessian inverse.
# Delta is the steplenght of the current step, and gamma is the change in 
# gradient of the same step.

class BadBroyden(QuasiNewton):
    def updateH(self,delta,gamma): 
        u = delta-(self.H_k@gamma)
        a = 1/(np.dot(u,gamma))
        return self.H_k+(a*np.outer(u,u))


class DFP(QuasiNewton):
    def updateH(self,delta,gamma):
        term1 = self.H_k+(np.outer(delta,delta)/(delta@gamma))
        term2 = (self.H_k@np.outer(gamma,gamma)@self.H_k)/(gamma@self.H_k@gamma)
        return term1 - term2    
    

class BFGS(QuasiNewton):
    def updateH(self,delta,gamma): 
        dTg = delta@gamma
        term1 = self.H_k + (1 + gamma@self.H_k@gamma/dTg)*(np.outer(delta,delta)/dTg)
        term2 = (np.outer(delta,gamma)@self.H_k + self.H_k@np.outer(gamma,delta))/dTg
        return term1 - term2
    
# Broyden Rank1 update of Q

class GoodBroyden(QuasiNewton):
    def __init__(self, objFunc, objGrad, linesearch, tol, dim):
        super(GoodBroyden, self).__init__(objFunc, objGrad, linesearch, tol, dim)
        self.Q_k = np.eye(dim)

  
    def updateH(self,delta,gamma):
        self.Q_k = self.Q_k + np.outer((gamma-self.Q_k@delta),delta)/(delta@delta)
        return solve(np.eye(len(self.Q_k)),(self.Q_k))
        
