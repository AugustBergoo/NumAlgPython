# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 20:15:19 2017
@author: Axel H, Simon J, August B, Erik S, Gustav H.
"""
from  scipy import *
from  pylab import *
from mpi4py import MPI
import matplotlib.pyplot as plt
import numpy as np
import Apartment as ap
import ApartmentHeatSolver as ahs

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

dx = 1/3 # choose a grid distance (the computing power needed depends heavily on dx).
itr = 10 # Choose the number of iterations to perform.

# Specify you rectangular rooms. Each row is a room and comprises 4 peices of 
# information. first number is: BASE length, Second is: HEIGHT,
# third and fourth are the coordinates for the top left corder of the room.
# E.g the row 1,1,3,4 will place a 1x1 room with upper left corner at X=3,Y=4.
rooms = np.array([[1,1,0,1], [1,2,1,2], [1,1,2,2]]) # Our geometry look like this.

# Make an apartment object. YAY! :). Send in the rooms matrix and the dx.
myApartment = ap.Apartment(rooms, dx)

roomTemp = 20
myApartment.set_boundary(1, 0, 1, 1, roomTemp, 2, 0) # Between rooms
myApartment.set_boundary(1, 0, 1, 1, roomTemp, 1, 1) # Between rooms
myApartment.set_boundary(2, 1, 2, 2, roomTemp, 1, 1) # Between rooms
myApartment.set_boundary(2, 1, 2, 2, roomTemp, 2, 2) # Between rooms

# Set the boundary conditions.    
cool = 5 # Given in assignment.
myApartment.set_boundary(1, 0, 2, 0, cool, 1, 1) # Window

heat = 40 # Given in assignment.
myApartment.set_boundary(0, 0, 0, 1, heat, 1, 0) # Heater
myApartment.set_boundary(1, 2, 2, 2, heat, 1, 1) # Heater
myApartment.set_boundary(3, 1, 3, 2, heat, 1, 2) # Heater

normalWallTemp = 15 # Given in assignment.
myApartment.set_boundary(0, 0, 1, 0, normalWallTemp, 1, 0) # Normal wall
myApartment.set_boundary(0, 1, 1, 1, normalWallTemp, 1, 0) # Normal wall
myApartment.set_boundary(2, 0, 2, 1, normalWallTemp, 1, 1) # Normal wall
myApartment.set_boundary(1, 1, 1, 2, normalWallTemp, 1, 1) # Normal wall
myApartment.set_boundary(2, 2, 3, 2, normalWallTemp, 1, 2) # Normal wall
myApartment.set_boundary(2, 1, 3, 1, normalWallTemp, 1, 2) # Normal wall




# Create the solver.
heatSolver = ahs.ApartmentHeatSolver()

# Solve the problem.
heatSolver.solve(myApartment, itr)

if rank == 1:
    plt.figure()
    plt.figure(figsize=(10,7))
    myApartment.plot_temperature()
