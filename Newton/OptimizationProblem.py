#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 15:17:48 2017

@author: Simon
"""

from scipy import *
from pylab import *

import numpy as np

from QuasiNewton import GoodBroyden
from QuasiNewton import BadBroyden
from QuasiNewton import DFP
from QuasiNewton import BFGS

from Linesearch import Linesearch
from GenericNewton import GenericNewton
from ClassicNewton import ClassicNewton


class OptimizationProblem():
    def __init__(self, objFunc, objGrad):
        self.objFunc = objFunc
        self.objGrad = objGrad
        
    
    def solve(self, x0, tol, method, linesearchMethod = None):
         
        # LinesearchMethods = 'Inexact' and 'Exact'
        if linesearchMethod is not None:
            if linesearchMethod == 'Exact':
                linesearch = Linesearch.exactLinesearch
            elif linesearchMethod == 'Inexact':
                linesearch = Linesearch.inexactLinesearch
            else:
                raise ValueError('The specified linesearch is invalid')
        
        # Finds the dimension of the problem
        dim = np.size(x0)
        
        # Methods = 'ClassicNewton', 'GoodBroyden', 'BadBroyden', 'DFP' and 'BFGS'
        if method == 'ClassicNewton':
            problem = ClassicNewton(self.objFunc, self.objGrad, tol)            
        
        elif method == 'GoodBroyden':
            problem = GoodBroyden(self.objFunc, self.objGrad, linesearch, tol, dim) 
        
        elif method == 'BadBroyden':
            problem = BadBroyden(self.objFunc, self.objGrad, linesearch, tol, dim) 
        
        elif method == 'DFP':
            problem = DFP(self.objFunc, self.objGrad, linesearch, tol, dim)
        
        elif method == 'BFGS':
            problem = BFGS(self.objFunc, self.objGrad, linesearch, tol, dim)
#        
        else:
            raise ValueError('The specified method is invalid')
        
        
        # Solves the problem
        minimum = problem.findMin(x0)
        print('Value:', float(self.objFunc(minimum)))
        
    