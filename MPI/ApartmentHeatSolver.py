# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 08:58:27 2017
@author: Hedin,
"""
from  scipy import *
from  pylab import *

class ApartmentHeatSolver():
    
    def MakeDNIteration(room1,room2,BC1,BC2):
        w = 0.8
        # create a u-vector to store border temperature in:
        u = np.arraylist(b) # b = size of border
        for i in range(np.size(u)):
            u[i] = w*room1[] + (1-w)*room2[] #what index parameters to use here?
        return u # Eller ska temperaturen för hela rummet returneras?
        
    
    def solve(room1,room2,room3,T0,dx):
        for i in range(10):
            #Solve PDE in middel room:
            A = Solve_PDE(room2,dx,T0,BC)
            
            # Solve the two outer rooms simultanoiusly, on different CPU's:
            B = Solve_PDE(room1,dx,T0,BC)
            C = Solve_PDE(room3,dx,T0,BC)
            
            # Dessa 3 rader ska kanske ligga utanför for-loopen:
            comm=MPI.COMM_WORLD
            rank=comm.Get_rank()
            np=comm.size

            sendbufferB=['solve heat distribution in room1',B]
            sendbufferC=['solve heat distribution in room3',C]
            comm.send(sendbufferB,?)
            comm.send(sendbufferC,?)
            
            status = MPI.Status()
            recievebufferB=comm.recv(?)
            recievebufferC=comm.recv(?)  
            
            # relaxation:
            MakeDNIteration(room1,room2,BC1,BC2)
            MakeDNIteration(room2,room3,BC2,BC3)
            