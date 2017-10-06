# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 08:58:27 2017
@author: Hedin,
"""
from  scipy import *
from  pylab import *
from mpi4py import MPI
import Apartment as ap

class ApartmentHeatSolver():

    # TODO: Replace with __call__ method
    def solve(self, apartment, itr):
        # Set up MPI.
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()

        # Save old temp for relaxation.
        oldTemp = apartment.get_coord()
        oldTemp = oldTemp[:,4]
        
        # Solve for room 1 once to get things started.
        if rank == 1:
            room1 = apartment.get_coord_for_room(rank) # Extract room 1.
            updatedTemp = self._solve_PDE(room1) # Solve PDE.
            apartment.update_temperature(updatedTemp, rank) # Update the apartment's temp.
                     
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
            updatedTemp = self._solve_PDE(room)
            
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
    
    def _solve_PDE(self, room):
        return room[:,4]
    
    
