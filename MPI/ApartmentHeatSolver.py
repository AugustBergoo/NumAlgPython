# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 08:58:27 2017
@author: Hedin,
"""

from pylab import *
from mpi4py import MPI
from scipy import linalg
import numpy as np
import Apartment as ap
import HeatSolver as hs

class ApartmentHeatSolver():

    # TODO: Replace with __call__ method
    def solve(self, apartment, itr):
        # Set up MPI.
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        # Save old temp for relaxation.
        oldTemp = apartment.get_coord()
        oldTemp = oldTemp[:,4]
        
        room = apartment.get_coord_for_room(rank)
        T = self._calc_toeplitz(room)
        
        # Solve for room 1 once to get things started.
        if rank == 1:
            room1 = apartment.get_coord_for_room(rank) # Extract room 1.
            updatedTemp = self._solve_PDE(room1, T) # Solve PDE.
            apartment.update_temperature(updatedTemp, rank) # Update the apartment's temp.
            #print('Apartment:',apartment.get_coord())
            # Extract room 1 and 3 with updated temperatures on the boundaries.
            room1 = apartment.get_coord_for_room(rank-1)
            room3 = apartment.get_coord_for_room(rank+1)
            
            # Send updated rooms to the other processes.
            comm.send(room1, rank-1)
            comm.send(room3, rank+1)
            
            
        # Perform the iterations.
        for i in range(itr):
            if rank == 1:    
                # Recieve apartment matrix from room 0 and 2
                status = MPI.Status()
                temp0 = comm.recv(source = rank-1, status=status)
                temp2 = comm.recv(source = rank+1, status=status)
                
                # Update temperatures in the apartment.
                apartment.update_temperature(temp0, rank-1)
                apartment.update_temperature(temp2, rank+1)
                
                # Do relaxation
                newApart = apartment.get_coord()
                newTemp = newApart[:,4]
                relaxed = self._perform_relaxation(oldTemp, newTemp)
                apartment.update_temperature(relaxed)
                
                if i == itr-1:
                    break
                
                room = apartment.get_coord_for_room(rank)            
            else:
                # Recieve apartment matrix from room 2
                status = MPI.Status()
                room = comm.recv(source = 1, status=status)
            
            # Solve the PDE.
            #print('Before solve:',room)
            updatedTemp = self._solve_PDE(room, T)
            
            if rank == 1:
                # Save old temp for relaxation.
                oldTemp = apartment.get_coord()
                oldTemp = oldTemp[:,4]
                apartment.update_temperature(updatedTemp, rank)
                
                # Extract room 1 and 3 with updated temperatures on the boundaries.
                room1 = apartment.get_coord_for_room(rank-1)
                room3 = apartment.get_coord_for_room(rank+1)
            
                # Send updated rooms to the other processes.
                comm.send(room1, rank-1)
                comm.send(room3, rank+1)
            else:
                comm.send(updatedTemp, 1)
    
    def _perform_relaxation(self, oldTemp, newTemp, w = 0.8):
        return w*newTemp + (1-w)*oldTemp
    
    def _solve_PDE(self, room, T):
        
        dx = room[1,2] - room[0,2]
        
        # Find the dimensions of the room
        n_tot = int(round((room[-1,2] - room[0,2]) * 1/dx + 1))
        m_tot = int(round((room[0,3] - room[-1,3]) * 1/dx + 1))
        
        # Only interested in internal points and can therefore remove the boundaries
        n = n_tot - 2
        m = m_tot - 2
        
        k = 0 # Index for the bc vector
        l = 0 # Index for the g vector
        bc = np.zeros((n*m,1))
        g = np.zeros((m,1))
        
        # Loops through the internal points
        for i in range(n_tot+1, m_tot*n_tot - n_tot-1, n_tot):
            for j in range(n_tot-2):
                coord = i + j
               
                # Test for boundary on top
                if(room[coord-n_tot, 5] == 1):
                    bc[k] = bc[k] + room[coord-n_tot, 4]
                
                # Test for boundary to the left
                if(room[coord-1, 5] == 1):
                    bc[k] = bc[k] + room[coord-1, 4]
                elif(room[coord-1, 5] == 2):    
                    g[l] = (room[coord-1, 4] - room[coord, 4]) / dx
                    bc[k] = bc[k] + dx * g[l] 
                    l = l + 1
                 
                # Test for boundary to the right
                if(room[coord+1, 5] == 1):
                    bc[k] = bc[k] + room[coord+1, 4]
                elif(room[coord+1, 5] == 2):
                    g[l] = (room[coord+1, 4] - room[coord, 4]) / dx
                    bc[k] = bc[k] + dx * g[l] 
                    l = l + 1
                    
                # Test for boundary on the bottom
                if(room[coord+n_tot, 5] == 1):
                    bc[k] = bc[k] + room[coord+n_tot, 4]
                     
                k = k + 1
                
        # Solves the temperatures for the internal points
        A  = T/(dx**2)   
        bc = -bc * 1/dx**2
        u = linalg.solve(A,bc)
        
        # Inserting the internal temperatures to the internal points 
        k = 0;
        for i in range(n_tot+1, m_tot*n_tot - n_tot-1, n_tot):
            for j in range(n_tot-2):
                coord = i + j
                room[coord, 4] = u[k]
                k = k + 1
                
        # Calculates the temperatures for the Neumann nodes
        l = 0
        for i in range(n_tot*m_tot):
            if (room[i, 5] == 2):
                if (i % n_tot == 0):
                    # Neumann boundary to the left
                    room[i, 4] = g[l] * dx + room[i+1, 4]
                else:
                    # Neumann boundary to the right
                    room[i, 4] = -g[l] * dx + room[i-1, 4]
                l = l + 1
                
        return room[:,4]
    
        
    def _calc_toeplitz(self, room):
        dx = room[1,2] - room[0,2]
        
        # Find the dimensions of the room
        n_tot = int(round((room[-1,2] - room[0,2]) * 1/dx + 1))
        m_tot = int(round((room[0,3] - room[-1,3]) * 1/dx + 1))
        
        # Only interested in internal points and can therefore remove the boundaries
        n = n_tot - 2
        m = m_tot - 2
        
        a = np.array([-4, 1])
        b = np.zeros(n-2)
        row = np.append(a,b)  
        
        if m > 1:
            c = np.array([1])
            d = np.zeros(n*(m-1) - 1)
            e = np.append(c,d)
            row = np.append(row,e)
            
        T = linalg.toeplitz(row)
        
        # Adds the zeros in between the "Blocks"
        for k in range(m-1):
            T[(k+1)*n-1, (k+1)*n] = 0
            T[(k+1)*n, (k+1)*n-1] = 0
            
        for i in range(n_tot*m_tot):
            if(room[i,5] == 2):
                if(i % n_tot == 0):
                    for k in range(n):
                        T[k*n,k*n] = -3
                else:
                    for k in range(n):
                        T[(k+1)*n-1,(k+1)*n-1] = -3
        return T
