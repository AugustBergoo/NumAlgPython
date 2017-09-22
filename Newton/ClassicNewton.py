#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 16:12:11 2017

@author: Gustav
"""

from scipy import *
from pylab import *

import numpy as np
import scipy.linalg as sl

from GenericNewton import GenericNewton

class ClassicNewton(GenericNewton):
    
    def __init__(self, objFunc, objGrad, tol):
        super(ClassicNewton, self).__init__(tol)
        self.objFunc = objFunc  #Oanvänd, så jag kanske inte ska ha denna raden kod.
        self.objGrad = objGrad

        
    
    def step(self, xk):
        delta_x = 0.01 #Ska vi ha detta som inparameter?
        
        # Create empty Hessian
        H = np.zeros((np.size(xk),np.size(xk)))
        
        # Create a matrix containing rows where only the "current varible x_n is 
        # increased by delta_x (used in finite difference)"
        delta_xk = np.zeros((np.size(xk),np.size(xk)))
        for i in range(np.size(xk)):
            vec = np.zeros(np.size(xk))
            vec[i] = delta_x
            delta_xk[i,:] = xk + delta_x*vec
            
        # Calc values of Hessian by finite differences:
        for i in range(np.size(xk)):
            for j in range(np.size(xk)):
                grad1 = self.objGrad(xk + delta_xk[j,:])
                grad2 = self.objGrad(xk)
                H[i,j] = (grad1[j] - grad2[j]) / delta_x
        
        # symmetrizing step:
        G = (1/2)*(H + H.transpose())
        
        # Test om G är pos. def. Raise exception if not:
        #is_pd(G)
        
        # Apply choleskys method to turn G into an (upper) trangle matrix.
        A = sl.cholesky(G)
        
        # steplength is calculated through solving a linear eqn sys. with cho_solve():
        # (the zero after A indicates that lower is false i.e. A is an upper)
        steplength = sl.cho_solve((A,0),self.objGrad(xk))
        return steplength
    
    
# Test for potitive definiteness:
def is_pd(K):
    try:
        np.linalg.cholesky(K)
        return 1 
    except np.linalg.linalg.LinAlgError as err:
        if 'Matrix is not positive definite' in err.message:
            return 0
    raise ValueError('Something')