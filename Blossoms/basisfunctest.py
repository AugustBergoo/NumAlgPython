# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 10:40:41 2017
@author: Hedin
"""
from  scipy import *
from  pylab import *
import numpy as np
import matplotlib.pyplot as plt
import basisfunc as bf

u_knots = np.array([0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.])



j = 5
k = 3



# for i in range()
u = np.linspace(u_knots[j-1],u_knots[j+3], num = 50)
N = np.zeros((1,len(u)))
for i in range(len(u)):
    #print(u[i])
    N[0,i] = bf.basisfunc(u[i],u_knots,j,k)

#print(N)


plt.plot(u,N[0,:])
plt.ylabel('Basis Function')
plt.show()



# Hej hopp