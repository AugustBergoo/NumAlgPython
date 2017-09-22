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
        delta = xnext-xk
        gamma = self.objGrad(xnext)-self.objGrad(xk)
        self.H_k = self.updateB(delta,gamma)
   
    # Check if possible to make an abstract updateB method.
        
# The following classes approximates the next hessian or hessian inverse.
# Delta is the steplenght of the current step, and gamma is the change in 
# gradient of the same step.
class GoodBroyden(QuasiNewton):
    def updateB(self,xk,xnext): 
        return

class BadBroyden(QuasiNewton):
    def updateB(self,delta,gamma): 
        u = delta-(self.H_k*gamma)
        a = 1/(np.transpose(u)*gamma)
        return self.H_k+(a*u*np.transpose(u))

class DFP(QuasiNewton):
    def updateB(self,delta,gamma):
        deltaT = np.transpose(delta)
        gammaT = np.transpose(gamma)
        term1 = self.H_k+(delta*deltaT/((deltaT)*gamma))
        term2 = (self.H_k*gamma*gammaT*self.H_k)/(gammaT*self.H_k*gamma)
        return term1 - term2
    
    
    
    

class BFGS(QuasiNewton):
    def updateB(self,delta,gamma): 
        return self.H_k + (1 + gamma.t*self.H_k*gamma/((delta.t)*gamma))*((delta*(delta.t))/((delta.t)*gamma)- (delta*(gamma.t)*self.H_k + self.H_k*gamma*(delta.t))/(delta*(delta.t))
        
    
    
    
a = GoodBroyden(objFunc,kdsjdkdds,ds sdds,,d,sd)
a.findMin()