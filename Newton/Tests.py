#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 17:33:02 2017

@author: August
"""

from scipy import *
from pylab import *
import numpy as np
import unittest as ut
from OptimizationProblem import OptimizationProblem
import chebyquad_problem_NG4oWEq as cheb
import scipy.optimize as so
from Linesearch import Linesearch

class Functions():
    # Min in (0,0)
    def esyPol(self, x):
        return np.array(x**2+1)

    def esyPolGrad(self, x):
        return np.array(2*x)
    
    # Min in (0,0)
    def midPol2d(self, x):
        return np.array(x[0]**4+x[1]**4)
    
    def midPolGrad2d(self, x):
        return np.array([4*x[0]**3,4*x[1]**3])
    
    # Min in (1,1)
    def rosenbrock(self, x):
        return np.array(100*((x[1]-x[0]**2)**2)+((1-x[0])**2))
    
    def rosenbrockGrad(self, x):
        return np.array([2*((200*x[0]**3)-(200*x[0]*x[1])+(x[0]-1)),200*(x[1]-(x[0]**2))])
    
    def chebyquad(self, x):
        return cheb.chebyquad(x)
    
    def chebyquadGrad(self, x):
        return cheb.gradchebyquad(x)
    
    

class Tests(ut.TestCase):
    
    def setUp(self):
        self.functions = Functions();
        self.tol = 1e-10
        
    def tearDown(self):
        del self.functions
        del self.tol
        
    def test_exactLinesearch_searchRight(self):
        linesearch = Linesearch.exactLinesearch
        x0 = np.array([-2])
        dk = np.array([1])
        step = linesearch(x0, dk, self.functions.esyPol, self.functions.esyPolGrad)
        minimum = x0 + step*dk
        self.assertAlmostEqual(minimum[0], 0, 3)
        
    def test_exactLinesearch_searchLeft(self):
        linesearch = Linesearch.exactLinesearch
        x0 = np.array([2])
        dk = np.array([-1])
        step = linesearch(x0, dk, self.functions.esyPol, self.functions.esyPolGrad)
        minimum = x0 + step*dk
        self.assertAlmostEqual(minimum[0], 0, 3)
        
    def test_inexactLinesearch_searchRight(self):
        linesearch = Linesearch.inexactLinesearch
        x0 = np.array([-2])
        dk = np.array([1])
        step = linesearch(x0, dk, self.functions.esyPol, self.functions.esyPolGrad)
        minimum = x0 + step*dk
        self.assertAlmostEqual(minimum[0], 0, 3)
        
    def test_inexactLinesearch_searchLeft(self):
        linesearch = Linesearch.inexactLinesearch
        x0 = np.array([2])
        dk = np.array([-1])
        step = linesearch(x0, dk, self.functions.esyPol, self.functions.esyPolGrad)
        minimum = x0 + step*dk
        self.assertAlmostEqual(minimum[0], 0, 3)
        
    def test_inexactLinesearch_rosenbrock(self):
        linesearch = Linesearch.inexactLinesearch
        x0 = np.array([-1.5, 3])
        dk = np.array([2.5, -2])
        step = linesearch(x0, dk, self.functions.rosenbrock, self.functions.rosenbrockGrad)
        minimum = x0 + step*dk
        for i in range(np.size(minimum)):
            self.assertAlmostEqual(minimum[i], 1, 3)
    
    def test_ClassicNewton_midPol2d(self):
        x0 = np.array([20, 2])
        problem = OptimizationProblem(self.functions.midPol2d, self.functions.midPolGrad2d)
        minimum = problem.solve(x0, self.tol, "ClassicNewton")
        for i in range(np.size(minimum)):
            self.assertAlmostEqual(minimum[i], 0, 3)

#    def test_ClassicNewton_rosenbrock(self):
#        x0 = np.array([5,5])
#        problem = OptimizationProblem(self.functions.rosenbrock, self.functions.rosenbrockGrad)
#        minimum = problem.solve(x0, self.tol, "ClassicNewton")
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], 1, 3)
#
#    def test_ClassicNewton_chebyquad_n4(self):
#        #x0 = np.array([5,5,5,5])
#        x0 = np.linspace(0,1,4)
#        problem = OptimizationProblem(self.functions.chebyquad, self.functions.chebyquadGrad)
#        minimum = problem.solve(x0, self.tol, "ClassicNewton")
#
#        xmin= so.fmin_bfgs(self.functions.chebyquad, x0, self.functions.chebyquadGrad)  # should converge after 18 iterations
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], xmin[i], 3)
#
#    def test_ClassicNewton_chebyquad_n8(self):
#        x0 = np.array([1.5, 1.5, -3, 10, 0, -3.5, 1, 4])
#        problem = OptimizationProblem(self.functions.chebyquad, self.functions.chebyquadGrad)
#        minimum = problem.solve(x0, self.tol, "ClassicNewton")
#
#        xmin= so.fmin_bfgs(self.functions.chebyquad, x0, self.functions.chebyquadGrad)  # should converge after 18 iterations
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], xmin[i], 3)
#
#    def test_ClassicNewton_chebyquad_n11(self):
#        x0 = np.array([1.5, 1.5, -3, 10, 0, -3.5, 1, 4, 5, 5, 5])
#        problem = OptimizationProblem(self.functions.chebyquad, self.functions.chebyquadGrad)
#        minimum = problem.solve(x0, self.tol, "ClassicNewton")
#
#        xmin= so.fmin_bfgs(self.functions.chebyquad, x0, self.functions.chebyquadGrad)  # should converge after 18 iterations
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], xmin[i], 3)
            
    def test_BadBroyden_midPol2d_exact(self):
        x0 = np.array([5,5])
        problem = OptimizationProblem(self.functions.midPol2d,self.functions.midPolGrad2d)
        minimum = problem.solve(x0, self.tol, "BadBroyden","Exact")
        for i in range(np.size(x0)):
            self.assertAlmostEqual(minimum[i],0,3)
        
    def test_BadBroyden_midPol2d_inexact(self):
        x0 = np.array([5,5])
        problem = OptimizationProblem(self.functions.midPol2d,self.functions.midPolGrad2d)
        minimum = problem.solve(x0, self.tol, "BadBroyden","Inexact")
        for i in range(np.size(x0)):
            self.assertAlmostEqual(minimum[i],0,3)
    
    def test_DFP_midPol2d_exact(self):
        x0 = np.array([5,5])
        problem = OptimizationProblem(self.functions.midPol2d,self.functions.midPolGrad2d)
        minimum = problem.solve(x0, self.tol, "DFP","Exact")
        for i in range(np.size(x0)):
            self.assertAlmostEqual(minimum[i],0,3)
        
    def test_DFP_midPol2d_inexact(self):
        x0 = np.array([5,5])
        problem = OptimizationProblem(self.functions.midPol2d,self.functions.midPolGrad2d)
        minimum = problem.solve(x0, self.tol, "DFP","Inexact")
        for i in range(np.size(x0)):
            self.assertAlmostEqual(minimum[i],0,3)
    
    def test_BFGS_midPol2d_exact(self):
        x0 = np.array([5,5])
        problem = OptimizationProblem(self.functions.midPol2d,self.functions.midPolGrad2d)
        minimum = problem.solve(x0, self.tol, "BFGS","Exact")
        for i in range(np.size(x0)):
            self.assertAlmostEqual(minimum[i],0,3)
        
    def test_BFGS_midPol2d_inexact(self):
        x0 = np.array([5,5])
        problem = OptimizationProblem(self.functions.midPol2d,self.functions.midPolGrad2d)
        minimum = problem.solve(x0, self.tol, "BFGS","Inexact")
        for i in range(np.size(x0)):
            self.assertAlmostEqual(minimum[i],0,3) 
        
#    def test_GoodBroyden_exact_midPol2d(self):
#        x0 = np.array([5,5])
#        problem = OptimizationProblem(self.functions.midPol2d, self.functions.midPolGrad2d)
#        minimum = problem.solve(x0, self.tol, "GoodBroyden", "Exact")
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], 0, 3)
#        
#    def test_GoodBroyden_inexact_midPol2d(self):
#        x0 = np.array([5,5])
#        problem = OptimizationProblem(self.functions.midPol2d, self.functions.midPolGrad2d)
#        minimum = problem.solve(x0, self.tol, "GoodBroyden", "Inexact")
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], 0, 3)
#            
#    def test_GoodBroyden_exact_rosenbrock(self):
#        x0 = np.array([1.5, 1.5])
#        problem = OptimizationProblem(self.functions.rosenbrock, self.functions.rosenbrockGrad)
#        minimum = problem.solve(x0, self.tol, "GoodBroyden", "Exact")
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], 1, 3)
#        
#    def test_GoodBroyden_inexact_rosenbrock(self):
#        x0 = np.array([1.5, 1.5])
#        problem = OptimizationProblem(self.functions.rosenbrock, self.functions.rosenbrockGrad)
#        minimum = problem.solve(x0, self.tol, "GoodBroyden", "Inexact")
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], 1, 3)
#            
#    def test_GoodBroyden_exact_chebyquad_n4(self):
#        x0 = np.array([1.5, 1.5, -3, 10])
#        problem = OptimizationProblem(self.functions.chebyquad, self.functions.chebyquadGrad)
#        minimum = problem.solve(x0, self.tol, "GoodBroyden", "Exact")
#        
#        xmin= so.fmin_bfgs(self.functions.chebyquad, x0, self.functions.chebyquadGrad)  # should converge after 18 iterations
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], xmin[i], 3)
#            
#    def test_GoodBroyden_exact_chebyquad_n8(self):
#        x0 = np.array([1.5, 1.5, -3, 10, 0, -3.5, 1, 4])
#        problem = OptimizationProblem(self.functions.chebyquad, self.functions.chebyquadGrad)
#        minimum = problem.solve(x0, self.tol, "GoodBroyden", "Exact")
#        
#        xmin= so.fmin_bfgs(self.functions.chebyquad, x0, self.functions.chebyquadGrad)  # should converge after 18 iterations
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], xmin[i], 3)
#            
#    def test_GoodBroyden_exact_chebyquad_n11(self):
#        x0 = np.array([1.5, 1.5, -3, 10, 0, -3.5, 1, 4, 5, 5, 5])
#        problem = OptimizationProblem(self.functions.chebyquad, self.functions.chebyquadGrad)
#        minimum = problem.solve(x0, self.tol, "GoodBroyden", "Exact")
#        
#        xmin= so.fmin_bfgs(self.functions.chebyquad, x0, self.functions.chebyquadGrad)  # should converge after 18 iterations
#        for i in range(np.size(minimum)):
#            self.assertAlmostEqual(minimum[i], xmin[i], 3)
    
    if __name__ == '__main__' :
        ut.main()
        
        
    
    
    
    
    