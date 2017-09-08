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
    def __init__(self, boor_points, grid):
        # Attributes
        self.u_knots = np.linspace(0, 1, np.size(boor_points, 0))
        self.boor_points = boor_points
        self.S = np.zeros((np.size(grid), 2))
        
        # Extends the lengths of the attributes.
        self.extend_u_knots() 
        extended_boor_points = self.extend_boor_points()
        
        self.calc_spline(grid, extended_boor_points)  
       
    # Plots the spline, plot_boor is a boolean indicating whether the boor points should be 
    # plotted or not.
    def __call__(self, plot_boor=False):
        self.plot_spline(plot_boor)
        
        
    def __add__(self, spline):
        length_1 = np.size(self.boor_points, 0)
        length_2 = np.size(spline.boor_points, 0)
        
        # Determines which spline is the longest and adds zeros to the end
        # of the shorter spline's boor_points-vector, until both of the 
        # splines' lengths are equal.
        if(length_1 >= length_2):
            boor = np.zeros((length_1, 2)) 
            zero = zeros((length_1-length_2, 2))
            spline.boor_points = np.concatenate([spline.boor_points, zero])
            
        elif(length_1 < length_2):
            boor = np.zeros((length_2, 2)) 
            zero = zeros((length_2-length_1, 2))
            self.boor_points = np.concatenate([self.boor_points, zero])
           
        # Creates a grid with the same size as the spline with most spline-points.
        grid = np.linspace(0, 1, np.size(self.S, 0)) if (np.size(self.S, 0) > np.size(spline.S, 0)) else np.linspace(0, 1, np.size(spline.S, 0))
        
        # Sums the (x,y)-coordinates elementwise in the de Boor points of spline1 and spline2  
        for i in range(np.size(boor, 0)):
            boor[i,0] = self.boor_points[i,0] + spline.boor_points[i,0]
            boor[i,1] = self.boor_points[i,1] + spline.boor_points[i,1]
        
        return Spline(boor, grid)

    # Calculates the whole spline point by point.
    def calc_spline(self, grid, extended_boor_points):       
        for i in range(0, np.size(grid)):
            self.S[i,:] = self.calc_spline_point(grid[i], extended_boor_points)   
        
    # Calculates a single spline point.
    def calc_spline_point(self, grid_point, extended_boor_points):
        hot_interval = self.find_hot_interval(grid_point)
        relevant_boor_points = self.find_boor_points(hot_interval, extended_boor_points)
        
        return self.blossom_recursion(grid_point, relevant_boor_points, hot_interval)

    
    # Extends the knots and boor points in order to define the spline at the edges 
    # of the interval.
    def extend_u_knots(self):
        self.u_knots = np.append([self.u_knots[0], self.u_knots[0]], self.u_knots[:])
        self.u_knots = np.append(self.u_knots[:], [self.u_knots[-1], self.u_knots[-1]])
        
    def extend_boor_points(self):
        extended_boor_points = np.r_['0,2', self.boor_points, [self.boor_points[-1], self.boor_points[-1]]]
        return np.r_['0,2', [self.boor_points[0], self.boor_points[0]], extended_boor_points]

    
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
    def find_boor_points(self, hot_interval, extended_boor_points) :
        return np.matrix([[extended_boor_points[hot_interval[0]-2,0], extended_boor_points[hot_interval[0]-2, 1]],
                          [extended_boor_points[hot_interval[0]-1,0], extended_boor_points[hot_interval[0]-1, 1]],
                          [extended_boor_points[hot_interval[0],0],   extended_boor_points[hot_interval[0],   1]],
                          [extended_boor_points[hot_interval[0]+1,0], extended_boor_points[hot_interval[0]+1, 1]]])
    
        
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
    def plot_spline(self, plot_boor):
        if plot_boor:
            plt.plot(self.boor_points[:,0], self.boor_points[:,1], 'ro--')
        plt.plot(self.S[:,0], self.S[:,1])
        plt.title("Looped spline: Cubic spline with its polynomial segments and it's control polygon")
        #plt.show()
