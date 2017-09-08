# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 09:28:57 2017
@author: Hedin
"""

from  scipy import *
from  pylab import *
import numpy as np


# 
def heaviside_a(the_x):
    # step function 
    if (the_x > 0):
        the_result = 1
    elif (the_x == 0):
        the_result = 1
    else:
        the_result = 0
    return the_result



def coef(u,u_knots,j,k):
    # u = np.linspace(u_knots[j-1],u_knots[j+4], num = 50)
    c = np.array([((u-u_knots[j-1])/(u_knots[j+k-1]-u_knots[j-1])),((u_knots[j+k]-u)/(u_knots[j+k]-u_knots[j]))])
    return c



# Find N_j^k:
def basisfunc(u,u_knots,j,k):
    if (k>0):
        N = coef(u,u_knots,j,k)[0]*basisfunc(u,u_knots,j,k-1) + coef(u,u_knots,j,k)[1]*basisfunc(u,u_knots,j+1,k-1) 
    else:
        N = heaviside_a(u-u_knots[j-1]) - heaviside_a(u - u_knots[j])
    return N;
    
    