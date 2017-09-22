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
    return np.array(x**3)

def grad(x):
    return np.array(3*x**2)

def f2d(x):
    return np.array(x[0]**2 + x[1]**2)

def grad2d(x):
    return np.array([2*x[0], 2*x[1]])


tol = 1e-5
x0 = np.array([0.01])
x02d = np.array([[0.01, 0.02]]).T
gradd = grad2d(x02d)

#problem1 = OptimizationProblem(f, grad)
problem2 = OptimizationProblem(f2d, grad2d)

#problem1.solve(x0, tol, 'ClassicNewton')
problem2.solve(x02d, tol, 'ClassicNewton')

