# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 12:55:24 2017
Last updated on 2017-09-07 16.01
@author: Axel, Simon, August
"""
from  scipy import *
from  pylab import *

import numpy as np
import matplotlib.pyplot as plt

class Spline():
    
    # Acts as the Constructor and assigns the attributes.
    def __init__(self, boor_points):
        # Attributes
        self.u_knots = np.linspace(0, 1, np.size(boor_points)/2)
        self.boor_points = boor_points
        
        # Extends the lengths of the attributes.
        self.extend_u_knots() 
        self.extend_boor_points()
       
    # Calculates and plots the spline given a grid.
    # plot_boor is a boolean indicating whether the boor points should be 
    # plotter or not.
    def __call__(self, grid, plot_boor):
        S = self.calc_spline(grid)  
        self.plot_spline(S, plot_boor)
        
    # Calculates the whole spline point by point.
    def calc_spline(self, grid):
        S = np.zeros((np.size(grid), 2))
        for i in range(0, np.size(grid)):
            S[i,:] = self.calc_spline_point(grid[i])
        return S    
        
    # Calculates a single spline point.
    def calc_spline_point(self, grid_point):
        hot_interval = self.find_hot_interval(grid_point)
        relevant_boor_points = self.find_boor_points(hot_interval)
        
        return self.blossom_recursion(grid_point, relevant_boor_points, hot_interval)

    
    # Extends the knots and boor points in order to define the spline at the edges 
    # of the interval.
    def extend_u_knots(self):
        self.u_knots = np.append([self.u_knots[0], self.u_knots[0]], self.u_knots[:])
        self.u_knots = np.append(self.u_knots[:], [self.u_knots[-1], self.u_knots[-1]])
        
    def extend_boor_points(self):
        self.boor_points = np.r_['0,2', self.boor_points, [self.boor_points[-1], self.boor_points[-1]]]
        self.boor_points = np.r_['0,2', [self.boor_points[0], self.boor_points[0]], self.boor_points]
    
    
    # Finds the index of the hot interval i.e the index of the two knots between 
    # which the investigated value of grid_point is located.
    def find_hot_interval(self, grid_point) :
        index = np.argmax(self.u_knots >= grid_point)
        
        if(index != 0) :
            return [index-1, index]
        elif grid_point == self.u_knots[-1]: 
            return [np.size(self.u_knots)-4, np.size(self.u_knots)-3]
        elif grid_point == self.u_knots[0]:
            return[2, 3]
        else:
            raise ValueError('It appears that grid_point is not in the specified interval')

    
    # Returns the relevant boor points given the relevant interval.
    def find_boor_points(self, hot_interval) :
        return np.matrix([[self.boor_points[hot_interval[0]-2,0], self.boor_points[hot_interval[0]-2, 1]],
                          [self.boor_points[hot_interval[0]-1,0], self.boor_points[hot_interval[0]-1, 1]],
                          [self.boor_points[hot_interval[0],0],   self.boor_points[hot_interval[0],   1]],
                          [self.boor_points[hot_interval[0]+1,0], self.boor_points[hot_interval[0]+1, 1]]])
    
        
    # Finds the value of s(grid_point) recursively. Each function run determines the
    # values of the next colon of boor points (see lecture notes Advanced numerical
    # algorithms 1.7 LTH).
    def blossom_recursion(self, grid_point, relevant_boor_points, hot_interval, level=2) :
        if level >= 0 :
            d = np.zeros((level+1, 2))
            for i in range(0, level+1) :
                u_leftmost = self.u_knots[hot_interval[0] - (level-i)]
                u_rightmost = self.u_knots[hot_interval[1] + i]
                alpha = (u_rightmost-grid_point) / (u_rightmost-u_leftmost)
                d[i,:] = (alpha*relevant_boor_points[i,:]) + ((1-alpha)*relevant_boor_points[i+1,:])
            return self.blossom_recursion(grid_point, d, hot_interval, level-1)
        else :
            return relevant_boor_points
    
    # Plots the spline and occasionally the boor points.
    def plot_spline(self, S, plot_boor):
        if plot_boor:
            plt.plot(self.boor_points[:,0], self.boor_points[:,1], 'ro--')
        plt.plot(S[:,0], S[:,1])
        plt.title("Looped spline: Cubic spline with its polynomial segments and it's control polygon")
        plt.show()
