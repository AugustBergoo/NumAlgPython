# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 20:15:19 2017
@author: Axel H, Simon J, August B, Erik S, Gustav H.
"""
from  scipy import *
from  pylab import *
import matplotlib.pyplot as plt
import numpy as np
import Apartment as Ap
from timeit import default_timer as timer


#Example commands for clearification and learning follows. This code may also
#be copied for other parts of the project.(our setup is coded below ;) )
  
#NOW HIT THAT RUN BUTTON before you start reading all the boring details :D!
#-----------------------------------------------------------------------------

np.set_printoptions(threshold=np.nan)   #so that we can see all of the matrices     

dx=1/2 #choose a grit distance (the computing power needed depends heavily on dx)

#specify you rectangular rooms. Each row is a room and comprises 4 peices of 
#information. first number is: BASE length, Second is:HEIGHT,
# Third and fourth are the coordinates for the top left corder of the room.
# E.g the row 1,1,3,4 will place a 1x1 room with upper left corner at X=3,Y=4.


rooms = np.array([[1,1,0,1],[1,2,1,2],[1,1,2,2]]) #Our geometry look like this

#Make a apartment object. YAY! :). Send in the rooms matrix and the dx.
startApartment = timer()
myApartment = Ap.Apartment(rooms,dx)
endApartment= timer()

plt.figure()    #lets plot the mesh
plt.figure(figsize=(10,7)) #just to make the plot nice and big

myApartment.plot_mesh() #call plot_mesh on the apartment object to vizualise.

#(some nodes ave two labels since they are part of two rooms in the apartment.
#However I belive you will not have to think about this. I'v written the code
#so that they always update together.)

#THOUGH! If you update a node by yourself without the use of my update methods
# make sure it is not a doublet node, if so update both if that is what you want.
#-----------------------------------------------------------------------------

#Now we will learn how to prescribe temperatures at horizontal and vertical
#lines. Nice for seting boundary values :)
#Our problem with wondow,heaters and normal walls look like this:
    
cool=5 #given in assignment degreees celsius I imagine
myApartment.set_boundary(1,0,2,0,cool,1,1) #window

heat=40 #given in assignment degreees celsius I imagine
myApartment.set_boundary(1,2,2,2,heat,1,1) #Heater
myApartment.set_boundary(3,1,3,2,heat,1,2) #Heater
myApartment.set_boundary(0,0,0,1,heat,1,0) #Heater

normalWallTemp = 15 #given in assignment degreees celsius I imagine
myApartment.set_boundary(2,2,3,2,normalWallTemp,1,2) #Normal wall
myApartment.set_boundary(2,1,3,1,normalWallTemp,1,2) #Normal wall
myApartment.set_boundary(2,0,2,1,normalWallTemp,1,1) #Normal wall
myApartment.set_boundary(0,0,1,0,normalWallTemp,1,0) #Normal wall
myApartment.set_boundary(0,1,1,1,normalWallTemp,1,0) #Normal wall
myApartment.set_boundary(1,1,1,2,normalWallTemp,1,1) #Normal wall
#-----------------------------------------------------------------------------

#Lets get some color ploting going. We plot the apartment with our specified
#edge temperatures.
plt.figure()
plt.figure(figsize=(10,7))
myApartment.plot_temperature() #call plt_Temperature to visualise the distribution
#-----------------------------------------------------------------------------

#The coord matrix is the real deal here. It containsfor each and every node: 
#nodal numbers, room number, (x,y) coordiinates and the Temperature in the node.

#We can either fetch the joint coord matrix for the entire apartment. Not so useful as
# the room specific ones though.
coord = myApartment.get_coord()

#Now this is what I belive you will want to use. Fetch the coord matrix for
#any room with get_coord_foor_room(). 
room1 = myApartment.get_coord_for_room(0)
room2 = myApartment.get_coord_for_room(1)
room3 = myApartment.get_coord_for_room(2)

#to get the temperature vector of the room just cut out the 5th colon
TemperatureRoom1 = room1[:,4]
#To get the node label
NodeLabelsRoom1 = room1[:,0]
#To get what room these nodes belongs to
BelongsToRooms = room1[:,1]
#To get x and y coord
xCoordsRoom1 = room1[:,2]
yCoordsRoom1 = room1[:,3]

#Test to write room1 in the console window after you'v run the code here.
#seeing the matrix really makes it clear how the information is structured
#-----------------------------------------------------------------------------
links = myApartment.get_links()
#finaly lets learn how to update all the  temperatures of a room.
newTemperature=np.linspace(1,50,len(room3[:,0]))
startupdate = timer()
myApartment.update_temperature(2,newTemperature)
endupdate = timer()
print("Creating an apartment with dx= ",dx," takes: ",(endApartment-startApartment)*1000," ms")
print("-----------------------")
print("updating the Temperaure of room 3 takes: ",(endupdate-startupdate)*1000," ms")
coord = myApartment.get_coord()

