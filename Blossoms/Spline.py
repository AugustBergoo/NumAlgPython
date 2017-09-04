# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 12:55:24 2017
@author: Axel
"""
from  scipy import *
from  pylab import *
import numpy as np


#calculates the value s(u) based on the knot points u_knots and the controll
#points boor_points.
def spline(u, u_knots, boor_points) :
    hot_interval = find_hot_interval(u,u_knots)
    if range_check(u_knots,hot_interval):
        relevant_boor_points = find_boor_points(hot_interval, boor_points)
        return blossom_recursion(u,u_knots,relevant_boor_points,hot_interval,2)
    else:
        return ValueError('u value is dependent on values outside the interval')
    
    
    
    
    
# Finds the index of the hot interval i.e the index of the two knots between 
# which the investigated value u is located.
def find_hot_interval(u, u_knots) :
    index = -1
    for i in range(0,np.size(u_knots)):
        if u>=u_knots[i] and u<=u_knots[i+1] :
            index = i
            
    if(index == -1) :
        raise ValueError('It appears that u is not in the specified interval')
    else:
        return [index, index+1]
    
    
    
    
# Checks that the the u value is not in need of knots outside the interval.
def range_check(u_knots,hot_interval):
    if hot_interval[0]-2<0 or hot_interval[0]+1>np.size(u_knots)-1:
        return False
    else: 
        return True
    
    
    
    
# returns the relevant boor points given the relevant interval.
def find_boor_points(hot_interval, boor_points) :
    return np.matrix([[boor_points[hot_interval[0]-2,0],boor_points[hot_interval[0]-2,1]],
                      [boor_points[hot_interval[0]-1,0],boor_points[hot_interval[0]-1,1]],
                      [boor_points[hot_interval[0],0],boor_points[hot_interval[0],1]],
                      [boor_points[hot_interval[0]+1,0],boor_points[hot_interval[0]+1,1]]])
    

    
    
# finds the value of s(u) recursively. Each function run determines the
# values of the next colon of boor points (see lecture notes Advanced numerical
# algorithms 1.7 LTH)
def blossom_recursion(u, u_knots, relevant_boor_points, hot_interval, level=2) :
    if level>=0 :
        d = np.zeros((level+1,2))
        for i in range(0,level+1) :
            u_leftmost = u_knots[hot_interval[0]-(level-i)]
            u_rightmost = u_knots[hot_interval[1]+i]
            alpha = (u_rightmost-u)/(u_rightmost-u_leftmost)
            d[i,:] = (alpha*relevant_boor_points[i,:])+((1-alpha)*relevant_boor_points[i+1,:])
        return blossom_recursion(u, u_knots, d, hot_interval, level-1)
    else:
        return relevant_boor_points



