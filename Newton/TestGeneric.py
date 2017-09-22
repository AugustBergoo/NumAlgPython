# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 12:14:13 2017
@author: Axel
"""
from  scipy import *
from  pylab import *
import numpy as np

from OptimizationProblem import OptimizationProblem
from QuasiNewton import QuasiNewton
from Linesearch import Linesearch

def esyPol(x):
    return np.array([x*x*x-2*x*x+1])

def esyPolGrad(x):
    return np.array([3*x*x-4*x])


x0=np.array([1.5])
tol=0.001

problemPol = OptimizationProblem(esyPol,esyPolGrad)
linesearchMethod = Linesearch()
problemPol.solve(x0, tol, "DFP", linesearchMethod.exactLinesearch)