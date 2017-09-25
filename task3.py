# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 14:24:19 2017

@author: steen_000
"""

def BsplineBase(uknot, j):
    # BsplineBase computes the j:th B spline Basefunction. 
    
    u = uknot(j-1) + (uknot(j+3)-uknot(j-1))*range(0:101)/100; %ska va elementvis addition
    # Computation of N^0
    N0 = 
    urel = uknot(j-1:j+3)
    