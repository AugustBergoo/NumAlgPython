# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 12:55:24 2017
@author: Axel
"""
from  scipy import *
from  pylab import *
import numpy as np


#calculates the value s(u) based on the knot points u_knots and the controll
#points boor_points. Here u is a float.
def spline(u, u_knots, boor_points) :
    u_knots = extend_u_knots(u_knots)
    boor_points = extend_boor_points(boor_points)
    
    hot_interval = find_hot_interval(u,u_knots)
    relevant_boor_points = find_boor_points(hot_interval, boor_points)
    
    return blossom_recursion(u,u_knots,relevant_boor_points,hot_interval,2)




#calculates a range of s(u) based on the knot points u_knots and the controll
#points boor_points. Here u is a numpy array.
def spline_set(u, u_knots, boor_points):
    S = np.zeros((np.size(u),2))
    for i in range(0,np.size(u)):
        S[i,:] = spline(u[i],u_knots,boor_points)
    return S
    


# extends the knots and boor points in order to define the spline at the edges 
# of the interval
def extend_u_knots(u_knots):
    u_knots = np.append([u_knots[0],u_knots[0]],u_knots[:])
    return np.append(u_knots[:],[u_knots[-1],u_knots[-1]])
    
def extend_boor_points(boor_points):
    boor_points = np.r_['0,2',boor_points,[boor_points[-1],boor_points[-1]]]
    return np.r_['0,2',[boor_points[0],boor_points[0]],boor_points]




# Finds the index of the hot interval i.e the index of the two knots between 
# which the investigated value u is located.
def find_hot_interval(u, u_knots) :

    index = np.argmax(u_knots>=u)
    
    if(index != 0) :
        return [index-1, index]
    elif u==u_knots[-1]: 
        return [np.size(u_knots)-4, np.size(u_knots)-3]
    elif u==u_knots[0]:
        return[2,3]
    else:
        raise ValueError('It appears that u is not in the specified interval')
    
    
    

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



