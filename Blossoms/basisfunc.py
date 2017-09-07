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



# Find N_j^3:
def basisfunc(u_knots,j,k):
    N = np.array([0,0])
    print(N)
    u = np.linspace(u_knots[j-1],u_knots[j+4], num = 50)
    for i in range(j,j+2):
        N[i-j] = heaviside_a(u-u_knots[j-1] - heaviside_a(u - u_knots[j])
    N_old = N
    for i in range(1,k+1):
        U = array([((u-u_knots[j-1])/(u_knots[j+k-1]-u_knots[j-1])),((u_knots[j+k]-u)/(u_knots[j+k]-u_knots[j]))]);
        N = U*N_old
        N_old = N 
    return sum(N);
    
    