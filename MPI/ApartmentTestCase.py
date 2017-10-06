# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 11:48:38 2017
@author: Axel H, Simon J, August B, Erik S, Gustav H.
"""
from  scipy import *
from  pylab import *
import numpy as np
import Apartment as Ap
import unittest


class ApartmentTestCase(unittest.TestCase):
    
    def setUp(self):
        self.dx=1/3
        # I use our geometry here, but anything should work, as long as
        # the rooms don't overlap and they are all are connected.
        self.rooms = np.array([[1,1,0,1],[1,2,1,2],[1,1,2,2]])
        self.myApartment = Ap.Apartment(self.rooms,self.dx)
        

    def tearDown(self):
        self.myApartment=None
        self.dx=np.nan
        self.rooms=np.nan
        
    #Test that the nodes of the rooms does not extend beyond their boundaries
    def test_node_placement(self):

        for i in range(0,len(self.rooms[:,0])):
            room = self.myApartment.get_coord_for_room(i)
            x1=self.rooms[i,2]
            x2=self.rooms[i,0]+self.rooms[i,2]
            y1=self.rooms[i,3]-self.rooms[i,1]
            y2=self.rooms[i,3]
           
            self.assertTrue((room[:,2]<=x2).all())
            self.assertTrue((room[:,3]<=y2).all())
            self.assertTrue((room[:,2]>=x1).all())
            self.assertTrue((room[:,3]>=y1).all())
            
    #Linspace some temperatures and check that the temperatures are prescribed correctly  
    #with update_temperature.      
    def test_change_temperature(self):
        T1=1
        T2=50
        for i in range(0,len(self.rooms[:,0])):
             room = self.myApartment.get_coord_for_room(i)
             newTemperature = np.linspace(T1,T2,len(room[:,0]))
             self.myApartment.update_temperature(i,newTemperature)
        for i in range(0,len(self.rooms[:,0])):
            room = self.myApartment.get_coord_for_room(i) 
            self.assertTrue((room[:,4]<=T2).all())
            self.assertTrue((room[:,4]>=T1).all())
            
     
    #Set the top two left nodes of each room to T and check that only
    #These nodes where changed. And that they are exactly T.    
    def test_boundary_temperature(self):
        T=5
        for i in range(0,len(self.rooms[:,0])):
             room = self.myApartment.get_coord_for_room(i)
             X1= self.rooms[i,2]
             Y1= self.rooms[i,3]
             X2= X1+self.dx
             Y2= Y1
             self.myApartment.set_boundary(X1,Y1,X2,Y2,T,1,i)
             self.assertTrue((room[:,4]<=T).all())
             self.assertTrue((room[:,4]==T).any())
             self.assertTrue(room[0,4]==T)
             self.assertTrue(room[1,4]==T)
             self.assertFalse(room[2,4]==T)
             self.assertFalse(room[-1,4]==T)
            
        

if __name__ == '__main__':
    unittest.main()