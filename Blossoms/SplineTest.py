# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 13:04:20 2017
Last updated on 2017-09-07 16.01
@author: Axel, Simon, August
"""
from  scipy import *
from  pylab import *
import numpy as np

import Spline as spl

#Den här filen testar bara vår spline klass. 

# We define boor points and a grid:
boor_points = np.array([[0,0], [1,1], [2,4], [3,2], [4,7], [5,7], [6,6], [7,5], [8,7], [8,2], [7,2]])
boor_points2 = np.array([[0,7], [3,3], [1,1], [0,3], [3,4], [6,4], [7,6], [6,7], [5,5], [5,3], [6,1]])
boor_points3 = np.array([[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7]])
grid = np.linspace(0, 1, 100)

#Plotting different splines
my_spline = spl.Spline(boor_points)
my_spline(grid, True) #True if boor points shall be plotted, False otherwise. 

my_spline2 = spl.Spline(boor_points2)
my_spline2(grid, False)

my_spline3 = spl.Spline(boor_points3)
my_spline3(grid, True)


