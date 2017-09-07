# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 10:40:41 2017
@author: Hedin
"""
from  scipy import *
from  pylab import *
import numpy as np

import basisfunc as bf

u_knots = np.array([0.,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.])



j = 5
k = 3

# for i in range()
N = basisfunc(u_knots,j,k)

print(N)



# Hej hopp