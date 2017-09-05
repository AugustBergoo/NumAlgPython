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


# we define knots and boor points:
u_knots = np.array([0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.])
boor_points = np.array([[0,0],[1,1],[2,4],[3,2],[4,7],[5,7],[6,6],[7,5],[8,7],[8,2],[7,2]])
print(type(u),type(u_knots),type(boor_points))



# Either use the spline directly and loop like this
S = np.zeros((101,2))
for i in range(0,101):
    u=(i*0.01)
    S[i,:] =  spl.spline(u,u_knots,boor_points)  

print(type(S))
plt.plot(boor_points[:,0],boor_points[:,1], 'r--')
plt.plot(boor_points[:,0],boor_points[:,1], 'ro')
plt.plot(S[:,0],S[:,1])
plt.title("Looped spline: Cubic spline with its polynomial segments and it's controll polygon")
plt.show()




# Or you can use spline_set and send in an entire grid as a numpy array like this:
u = np.arange(0,1.01,0.01)
S = spl.spline_set(u,u_knots,boor_points) 

print(type(S))
plt.plot(boor_points[:,0],boor_points[:,1], 'g--')
plt.plot(boor_points[:,0],boor_points[:,1], 'go')
plt.plot(S[:,0],S[:,1])
plt.title("spline_set: Cubic spline with its polynomial segments and it's controll polygon")
plt.show()





