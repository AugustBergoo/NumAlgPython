# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 12:14:13 2017
@author: Axel
"""
from  scipy import *
from  pylab import *
import numpy as np
import matplotlib.pyplot as plt

from OptimizationProblem import OptimizationProblem
from QuasiNewton import QuasiNewton
from Linesearch import Linesearch

def esyPol(x):
    return np.array(x**2+1)

def esyPolGrad(x):
    return np.array(2*x)

def midPol2d(x):
    return np.array(x[0]**4+x[1]**4)

def midPolGrad2d(x):
    return np.array([4*x[0]**3,4*x[1]**3])

def hardPol2d(x):
    return np.array(100*((x[1]-x[0]**2)**2)+((1-x[0])**2)).T

def hardPolGrad2d(x):
    return np.array([2*((200*x[0]**3)-(200*x[0]*x[1])+(x[0]-1)),200*(x[1]-(x[0]**2))]).T


dk=np.array([-1,-1])
x0=np.array([5,5])
tol=0.000001

#m = x0 + Linesearch.inexactLinesearch(x0,dk,esyPol2d,esyPolGrad2d)*dk


#t = np.arange(x0-1., m+1, .001)
#plt.plot(t, esyPol(t), 'b-',)
#plt.plot(m,esyPol(m),'ro')
#plt.plot(x0,esyPol(x0),'bo')
#plt.show()

#x01=np.array([200])
problemPol = OptimizationProblem(midPol2d,midPolGrad2d)
problemPol.solve(x0, tol, "BadBroyden", "Inexact")