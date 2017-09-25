#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:34:54 2017

@author: Simon
"""

from scipy import *
from pylab import *

from OptimizationProblem import OptimizationProblem
import numpy as np

# func = x^2 + x + 1
# grad = 2x + 1
# x0 = np.array(0, 1)
# tol = 1e-6
# Methods = 'ClassicNewton', 'GoodBroyden', 'BadBroyden', 'DFP' and 'BFGS'
# Linesearch = 'Inexact' and 'Exact'

# problem1.solve(x0, tol, 'BadBroyden', 'Exact')

def f(x):
    return np.array(x**2)

def grad(x):
    return np.array(2*x)

def f2d(x):
    return np.array(x[0]**2 + x[1]**2)

def grad2d(x):
    return np.array([2*x[0], 2*x[1]])

def f3d(x):
    return np.array(x[0]**2 + x[1]**2 + x[2]**2)

def grad3d(x):
    return np.array([2*x[0], 2*x[1], 2*x[2]])

# Min in (0,0)
def midPol2d(x):
    return np.array(x[0]**4+x[1]**4)
    
def midPolGrad2d(x):
    return np.array([4*x[0]**3,4*x[1]**3])


tol = 1e-5
x0 = np.array([5])
x02d = np.array([20, 2])
x03d = np.array([20, 2, 30])

#problem1 = OptimizationProblem(f, grad)
#minimum = problem1.solve(x0, tol, 'ClassicNewton')
#print(minimum)
#
#problem2 = OptimizationProblem(f2d, grad2d)
#minimum = problem2.solve(x02d, tol, 'ClassicNewton')
#print(minimum)
#
#problem3 = OptimizationProblem(f3d, grad3d)
#minimum = problem3.solve(x03d, tol, 'ClassicNewton')
#print(minimum)

x04 = np.array([5,5])
problem3 = OptimizationProblem(midPol2d, midPolGrad2d)
minimum = problem3.solve(x04, tol, 'BFGS', 'Inexact')

