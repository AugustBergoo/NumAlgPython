# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 10:40:41 2017
@author: Hedin
"""
#from  scipy import *
#from  pylab import *
import numpy as np
import matplotlib.pyplot as plt
import basisfunc as bf

# Give desired values to u_knots and constants:
u_knots = np.array([0.1,0.1,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.,1.,1.])
j = 3
k = 3

# Evaluate the basis function:
[u,N] = bf.evalbasisfunc(u_knots,j,k)

# Plot The basis function:
plt.plot(u,N[0,:])
plt.ylabel('Basis Function: N(u)')
plt.xlabel('u')
plt.show()