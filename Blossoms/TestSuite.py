# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 10:22:00 2017
Last updated on 2017-09-07 16.01
@author: August
"""
from  scipy import *
from  pylab import *
import numpy as np
import unittest as utest

import Spline as spl
import basisfunc as bf

class TestSuite(utest.TestCase) :

    def test_straight_line(self) :
        boor_points = np.array([[0,0], [1,0], [2,0], [3,0], [4,0], [5,0]])
        grid = np.linspace(0, 1, 100)
        spline = spl.Spline(grid, boor_points)
        for point in spline.S :
            self.assertEqual(point[1], 0)

    def test_negative_boor_points(self) :
        boor_points = np.array([[-1,-1], [-2,-2], [-3,-3], [-4,-4], 
                                [-5,-5]])
        grid = np.linspace(0, 1, 100)
        spline = spl.Spline(grid, boor_points)
        for point in spline.S :
            self.assertTrue(point[0] < 0)
            self.assertTrue(point[1] < 0)

    def test_empty_boor_points(self) :
        boor_points = np.array([])
        grid = np.linspace(0, 1, 100)
        
        with self.assertRaises(ValueError) :
            spl.Spline(grid, boor_points)
    
    def test_empty_grid(self) :
        boor_points = np.array([[0,0], [1,0], [2,0], [3,0], [4,0], [5,0]])
        grid = np.array([])
        
        with self.assertRaises(ValueError) :
            spl.Spline(grid, boor_points)
            
    def test_add(self) :
        b1 = np.array([[0,0], [1,1], [2,2], [3,3], [4,4], [5,5]])
        b2 = np.array([[0,0], [1,-1], [2,-2], [3,-3], [4,-4], [5,-5]])
        grid = np.linspace(0, 1, 100)
        spline1 = spl.Spline(grid, b1)
        spline2 = spl.Spline(grid, b2)
        spline3 = spline1 + spline2
        
        for point in spline3.S :
            self.assertEqual(point[1], 0)
            
    def test_add_diff_boor_length(self) :
        b1 = np.array([[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,0], [7,0]])
        b2 = np.array([[0,0], [1,-1], [2,-2], [3,-3], [4,-4], [5,-5]])
        grid = np.linspace(0, 1, 100)
        spline1 = spl.Spline(grid, b1)
        spline2 = spl.Spline(grid, b2)
        spline3 = spline1 + spline2
        
        for point in spline3.S :
            self.assertEqual(point[1], 0)

    def test_add_diff_grid_length(self) :
        boor_points = np.array([[0,0], [1,1], [2,2], [3,3], [4,4], [5,5]])
        grid1 = np.linspace(0, 1, 100)
        grid2 = np.linspace(0, 1, 50)
        spline1 = spl.Spline(grid1, boor_points)
        spline2 = spl.Spline(grid2, boor_points)
        spline3 = spline1 + spline2
        
        self.assertEqual(np.size(spline3.S, 0), np.size(grid1) if 
                          np.size(grid1) >= np.size(grid2) else np.size(grid2))
        
    def test_add_commutative(self) :
        b1 = np.array([[0,0], [1,1], [2,2], [3,3], [4,4], [5,5]])
        b2 = np.array([[0,0], [1,-1], [2,-2], [3,-3], [4,-4], [5,-5]])
        grid = np.linspace(0, 1, 100)
        spline1 = spl.Spline(grid, b1)
        spline2 = spl.Spline(grid, b2)
        spline3 = spline1 + spline2
        spline4 = spline2 + spline1
        
        for i in range(np.size(grid)) :
            self.assertEqual(spline3.S[i,0], spline4.S[i,0])
            self.assertEqual(spline3.S[i,1], spline4.S[i,1])
            
    def test_basis_sum(self) :
        k = 3
        grid = np.linspace(0, 1, 100)
        boor_points = np.array([[0,0], [1,1], [2,2], [3,3], [4,4], [5,5]])
        s = spl.Spline(grid, boor_points)
        
        u_array = np.linspace(s.u_knots[3], s.u_knots[-4]) # Tests 50 values of u.
        for u in u_array :
            base_sum = 0
            for j in range(2,len(s.u_knots)-2) : # Iterate over each base function.
                base_sum += s.basisfunc(u, j, k)
            self.assertAlmostEqual(base_sum, 1) # Test if the sum is equal to 1.
            
            
        

if __name__ == '__main__' :
    utest.main()