# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 13:35:27 2017

@author: steen_000
"""
from scipy import *
from pylab import *
import numpy as np


delta = np.array([[1],[0]])
gamma = np.array([[2],[0]])  #0.71 approx 1/sqrt(2)


H_k = 0.5*np.eye(2)
#Good Broyden

def updateB(H_k,delta,gamma):
        return H_k + (delta -H_k@gamma)@delta.T@H_k/(delta.T@H_k@gamma)
    
    
print('GoodBroyden ger ')
print(updateB(H_k,delta,gamma))

#BadBroyden
def updateBB(H_k,delta,gamma): 
        return H_k+(delta -H_k@gamma)@gamma.T/(np.transpose(gamma)@gamma)
    
    
print('BadBroyden ger ')
print(updateBB(H_k,delta,gamma))


#DFP
def updateDFP(H_k,delta,gamma):

        term1 = H_k+(delta@delta.T/((delta.T)@gamma))
        term2 = (H_k@gamma@gamma.T*H_k)/(gamma.T@H_k@gamma)
        return term1 - term2 
    
print('DFP ger ')
print(updateDFP(H_k,delta,gamma))


#BFGS
def updateBFGS(H_k,delta,gamma): 
        deltaT = np.transpose(delta)
        gammaT = np.transpose(gamma)
        dTg = np.transpose(delta)@gamma
        term1 = H_k + (1 + gammaT@H_k@gamma/dTg)*(delta@deltaT)/dTg
        term2 = (delta@gammaT@H_k + H_k@gamma@deltaT)/dTg
        return term1 - term2

print('BFGS ger ')
print(updateBFGS(H_k,delta,gamma))


