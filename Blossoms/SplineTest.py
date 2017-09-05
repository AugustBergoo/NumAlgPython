# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 13:04:20 2017
@author: Axel
"""
from  scipy import *
from  pylab import *
import numpy as np
import matplotlib.pyplot as plt
import Spline as spl



# Example code that gets s(u) given knots and boor points and plots the result.
# Note that each knot has a corresponding boor point. It is important that these 
# are np.arrays, ordered in rising order, i.e [u1, u2, u3...] and [d1,d2,d3...].

u_knots = np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.])
boor_points = np.array([[1,1],[2,4],[3,2],[4,7],[5,7],[6,6],[7,5],[8,7],[8,2],[7,2]])
S = np.zeros((91,2))
for i in range(0,91):
    u=(i*0.01)+0.1
    S[i,:] =  spl.spline(u,u_knots,boor_points)  


plt.plot(boor_points[:,0],boor_points[:,1], 'r--')
plt.plot(boor_points[:,0],boor_points[:,1], 'ro')
plt.plot(S[:,0],S[:,1])
plt.title("Cubic spline with its polynomial segments and it's controll polygon")
plt.show()




