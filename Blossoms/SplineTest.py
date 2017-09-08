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
bp = np.array([[0,0], [1,1], [2,4], [3,2], [4,7], [5,7], [6,6], [7,5], [8,7], [8,2], [7,2]])
bp2 = np.array([[0,7], [3,3], [1,1], [0,3], [3,4], [6,4], [7,6], [6,7], [5,5], [5,3], [6,1]])
bp3 = np.array([[0,0], [1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7], [6,6], [5,5], [4,4], [3,3], [2,2], [1,1]])
bp4 = np.array([[0.5,.5], [1,0], [1,1], [0,1], [0,0], [1,0], [1,1], [0,1], [0,0], [1,1], [0,0]])

bp5 = np.array([[0,1], [1,2], [3,3], [6,2], [5,3]])
bp6 = np.array([[0,-1],[1,1],[2,-2]])
grid = np.linspace(0, 1, 100)

s1 = spl.Spline(bp5, grid)
s1(True)
s2 = spl.Spline(bp6, grid)
s2(True)

s_comb= s1 + s2
s_comb(True)





#Plotting different splines
#spline = spl.Spline(boor_points, grid)
#spline() #True if boor points shall be plotted, False otherwise. 

#spline2 = spl.Spline(boor_points2, grid)
#spline2()

#spline3 = spl.Spline(boor_points3, grid)
#spline3()

#spline4 = spl.Spline(boor_points4, grid)
#spline4()