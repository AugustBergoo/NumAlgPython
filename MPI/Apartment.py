# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 17:32:03 2017
@author: Axel H, Simon J, August B, Erik S, Gustav H.
"""
from  scipy import *
from  pylab import *
import matplotlib.pyplot as plt
import numpy as np
from pylab import cm,imshow,colorbar,title,show


class Apartment:
    
    #The Apartment class creates an apartment with arbitrary many rectangular rooms.
    #it is asumed the rooms are conected and does not overlap.
    #rooms: nx4 np.array: one row is one room: firts two numbers are base and height,
    #second two define the upper left corner coordinate of the room (base,height,x,y)
    def __init__(self,rooms,dx):
        self.dx=dx
        self.rooms = rooms
        self.NmbrNodes=0
        #remeber that some nodes exist twice since they are part of two rooms
        for i in range(0,len(rooms[:,0])):
            rows= int(rooms[i,1]/self.dx)+1
            colons = int(rooms[i,0]/self.dx)+1
            self.NmbrNodes = self.NmbrNodes + (rows*colons)
        self.coord = self.coord_extract()
        self.coord_by_room=[]
        count=0
        for i in range(0,len(rooms[:,0])):
            NbrRoomNodes=int((rooms[i,0]/dx+1)*(rooms[i,1]/dx+1))
            self.coord_by_room.append(self.coord[count:(count+NbrRoomNodes),:])
            count = count + NbrRoomNodes
            
    #Here we plot the the nodes of the geometry along with the node labels and
    #the room labels. This is good to run to understand and check that all is
    #as expected.     
    def plot_mesh(self):
        for i in range(0,self.NmbrNodes):
            plt.plot(self.coord[i,2],self.coord[i,3],'ro')
            plt.annotate(int(self.coord[i,0]), xy=(self.coord[i,2],self.coord[i,3]))
 
        for i in range(0,len(self.coord_by_room)):
            room = (self.coord_by_room[i])
            roomNbr=int(room[0,1])
            x=room[:,2].mean()
            y=room[:,3].mean()
            plt.text(x, y,roomNbr, fontsize=40)
            plt.title("$Apartment$ $Nodes$",fontsize=15)
          
    # I use imshow here. That means each node is a pixel and some interpolation is preformed between pixels.
    # This also means that each node is extended to a squared area with the node in the center of the area. So
    # for very low dx (1/2 or 1/4) it will appear that the geometry is in fault. However all the meshes are correct.           
    def plot_temperature(self):
        x = arange(self.coord[:,2].min(),self.coord[:,2].max()+(self.dx/2),self.dx)
        y = arange(self.coord[:,3].min(),self.coord[:,3].max()+(self.dx/2),self.dx)
        z = np.zeros((len(y),len(x)))*np.nan
        for i in range(0,self.NmbrNodes): 
            z[(int(round(-(self.coord[i,3]/self.dx)+(len(y)-1)))),(int(round((self.coord[i,2]/self.dx))))]=self.coord[i,4]
        im = imshow(z,cm.gnuplot2,interpolation='bilinear')
        colorbar(im) 
        title('$Apartment$ $Temperature$ $Distribution$',fontsize=15)
        show()     
        
    # Private Internal method for constructing the coord matrix.(don't run this outside) 
    # 1ts colon: node number, 2d colon: xCoord, 3rd colon: ycoord, 4th colon: Temperature
    def coord_extract(self):
        coord = np.zeros((self.NmbrNodes,5))
        node=0
        for i in range(0,len(self.rooms[:,0])):
            upperLeft = np.array([self.rooms[i,2],self.rooms[i,3]])
            for n in range(0,int((self.rooms[i,1]/self.dx)+1)):
                for m in range(0,int((self.rooms[i,0]/self.dx)+1)):
                    coord[node,0]=node
                    coord[node,1]=i+1
                    coord[node,2]=self.dx*m+upperLeft[0]
                    coord[node,3]=-self.dx*n+upperLeft[1]
                    node=node+1
        return coord       
    
    #The entire apartment information is accesible here (I would use the room
    #information though if I where you).
    def get_coord(self):
        return self.coord
    
    #To set the temperature to single a value along a vertical or horizontal line
    #use this function. The temperature is set to "Temperature" between (x1,y1)
    #and (x2,y2).
    def set_boundary(self,x1,y1,x2,y2,Temperature):
        for i in range(0,self.NmbrNodes):
            if x1<=self.coord[i,2]<=x2 and y1<=self.coord[i,3]<=y2:
                self.coord[i,4]=Temperature
                
    #We can update all the temperatures of a room of the apartment via this 
    #function. The new temperatures goes in as a vector with lenght equal
    #to the number of nodes in the specified room.
    def update_temperature(self,roomNbr,newTemperatures):
        room= self.get_coord_for_room(roomNbr)  
        room[:,4]=newTemperatures
           
        
     # Each individual room of the apartment is accessible here    
    def get_coord_for_room(self,roomNbr):
        return self.coord_by_room[roomNbr-1]


