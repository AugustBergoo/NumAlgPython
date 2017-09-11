# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 12:55:24 2017
Last updated on 2017-09-07 16.01
@author: Axel, Simon, August
"""
from  scipy import *
from  pylab import *

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import basisfunc as bf

class Spline():
    
    # Acts as the Constructor and assigns the attributes.
    def __init__(self, grid, points, interpolation=False):
        if(grid == None or points == None or np.size(grid) == 0 or np.size(points) == 0):
            raise ValueError("Size of grid or points is zero or None")
        
        #Attributes
        self.u_knots = np.linspace(0, 1, np.size(points, 0))
        self.extend_u_knots()
        
        if(not interpolation):
            # Attributes
            self.boor_points = points
            self.S = np.zeros((np.size(grid), 2))
            
            # Extends the lengths of the attributes.
            extended_boor_points = self.extend_boor_points()
            
            self.calc_spline(grid, extended_boor_points)  
        
        else:    
            interpolation_points = points
            nbr_points = len(points)
            
            xi = np.zeros(nbr_points)
            
            for i in range(len(xi)):
                xi[i] = (self.u_knots[i+1] + self.u_knots[i+2] + self.u_knots[i+3])/3
                
            print(xi)
            vander_matrix = np.zeros((nbr_points, nbr_points))
            
            for i in range(0, nbr_points):
                for j in range(0, nbr_points):
                    vander_matrix[i, j] = self.basisfunc(xi[i], j+2, 3)
            print(vander_matrix)
            
            
            bp = sp.linalg.solve(vander_matrix, points)
            splinetest = Spline(grid, bp)
            splinetest(True)
            plt.plot(points[:,0], points[:,1], 'go')
            #return Spline(grid, boor_points)
            
     
        
        
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
            zero = np.zeros((length_1-length_2, 2))
            spline.boor_points = np.concatenate([spline.boor_points, zero])
            
        elif(length_1 < length_2):
            boor = np.zeros((length_2, 2)) 
            zero = np.zeros((length_2-length_1, 2))
            self.boor_points = np.concatenate([self.boor_points, zero])
           
        # Creates a grid with the same size as the spline with most spline-points.
        grid = np.linspace(0, 1, np.size(self.S, 0)) if (np.size(self.S, 0) > np.size(spline.S, 0)) else np.linspace(0, 1, np.size(spline.S, 0))
        
        # Sums the (x,y)-coordinates elementwise in the de Boor points of spline1 and spline2  
        for i in range(np.size(boor, 0)):
            boor[i,0] = self.boor_points[i,0] + spline.boor_points[i,0]
            boor[i,1] = self.boor_points[i,1] + spline.boor_points[i,1]
        
        return Spline(grid, boor)

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


    # Define Heaviside Function:
    def heaviside_a(self,x):
        if (x > 0):
            result = 1
        elif (x == 0):
            result = 1
        else:
            result = 0
        return result
    
    
    # Define a function to calculate coefficient polynomials for the N's:
    def coef(self,u,j,k):
       
        if (self.u_knots[j+k-2]-self.u_knots[j-2]) == 0:
            c1 = 0
        else: 
            c1 = ((u-self.u_knots[j-2])/(self.u_knots[j+k-2]-self.u_knots[j-2]))
        
        if (self.u_knots[j+k-1]-self.u_knots[j-1]) == 0:
            c2 = 0
        else:
            c2 = ((self.u_knots[j+k-1]-u)/(self.u_knots[j+k-1]-self.u_knots[j-1]))

        return np.array([c1,c2])
    
    
    # Define a function that computes basisfunction Nj(u), of degree k.
    def basisfunc(self,u,j,k):
        
        if (k>0):
            # If k>0, N is a function of N of lower degrees.  
            N = self.coef(u,j,k)[0]*self.basisfunc(u,j,k-1) + self.coef(u,j,k)[1]*self.basisfunc(u,j+1,k-1) 
        else:
            # If k=0, N consists of Heavisides:
            N = self.heaviside_a(u-self.u_knots[j-2]) - self.heaviside_a(u - self.u_knots[j-1])
        return N;