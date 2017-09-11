# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 09:28:57 2017
@author: Hedin
"""

import numpy as np

# Define Heaviside Function:
def heaviside_a(x):
    if (x > 0):
        result = 1
    elif (x == 0):
        result = 1
    else:
        result = 0
    return result


# Define a function to calculate coefficient polynomials for the N's:
def coef(u,u_knots,j,k):
    # u = np.linspace(u_knots[j-1],u_knots[j+4], num = 50)
    try :
        c1 = ((u-u_knots[j-1])/(u_knots[j+k-1]-u_knots[j-1]))
    except ZeroDivisionError:
        c1 = 0
        print("c1 var 0")
        
    try :
        c2 = ((u_knots[j+k]-u)/(u_knots[j+k]-u_knots[j]))
    except ZeroDivisionError:
        c2=0
        print("c2 var 0")
        
    return np.array([c1,c2])


# Define a function that computes basisfunction Nj(u), of degree k.
def basisfunc(u,u_knots,j,k):
    if (k>0):
        # If k>0, N is a function of N of lower degrees.  
        N = coef(u,u_knots,j,k)[0]*basisfunc(u,u_knots,j,k-1) + coef(u,u_knots,j,k)[1]*basisfunc(u,u_knots,j+1,k-1) 
    else:
        # If k=0, N consists of Heavisides:
        N = heaviside_a(u-u_knots[j-1]) - heaviside_a(u - u_knots[j])
    return N;


# Define a function that evaluates basisfunction over an interval u    
def evalbasisfunc(u_knots,j,k):
    u = np.linspace(u_knots[0],u_knots[-1], num = 100)
    N = np.zeros((1,len(u)))
    for i in range(len(u)):
        N[0,i] = basisfunc(u[i],u_knots,j,k)
    return [u,N]
