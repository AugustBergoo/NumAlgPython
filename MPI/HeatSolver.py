import scipy
import numpy as np
import Apartment as ap


def PDE_solve(room):
    
    dx = room[1,2] - room[0,2]
    
    # Find the dimensions of the room
    n_matrix = int((room[-1,2] - room[0,2]) * 1/dx + 1)
    m_matrix = int((room[0,3] - room[-1,3]) * 1/dx + 1)
    
    # Only interested in internal points and can therefore remove the boundaries
    n = n_matrix - 2
    m = m_matrix - 2
    
    # Creating the Toeplitz matrix
    a = np.array([-4, 1])
    b = np.zeros(n-2)
    row = np.append(a,b)  
    
    if m > 1:
        c = np.array([1])
        d = np.zeros(n*(m-1) - 1)
        e = np.append(c,d)
        row = np.append(row,e)
        
    T = scipy.linalg.toeplitz(row)
    
    # Adds the zeros in between the "Blocks"
    for k in range(m-1):
        T[(k+1)*n-1, (k+1)*n] = 0
        T[(k+1)*n, (k+1)*n-1] = 0
    
    index = 0
    bc = np.zeros((n*m,1))
    g = np.zeros((m,1))
    # 2 is the amount of neumann nodes
    for i in range(n_matrix+1, m_matrix*n_matrix - n_matrix-1, n_matrix):
        for j in range(n_matrix-2):
            coord = i + j
           
            if(room[coord-n_matrix, 5] == 1):
                bc[index] = bc[index] + room[coord-n_matrix, 4]
            elif(room[coord-n_matrix, 5] == 1):
                 print("NEUMANN TOP")
            
            if(room[coord-1, 5] == 1):
                bc[index] = bc[index] + room[coord-1, 4]
            elif(room[coord-1, 5] == 2):    
                for k in range(n):
                    T[k*n,k*n] = -3
                g[0] = (room[coord-1, 4] - room[coord, 4]) / dx
                bc[index] = bc[index] + dx * g[0] #TODO: Get g somehow
                print('NEUMAAN DETECTED LEFT!')
                
            if(room[coord+1, 5] == 1):
                bc[index] = bc[index] + room[coord+1, 4]
            elif(room[coord+1, 5] == 2):
                for k in range(n):
                    T[(k+1)*n-1,(k+1)*n-1] = -3
                g[1] = (room[coord+1, 4] - room[coord, 4]) / dx
                bc[index] = bc[index] + dx * g[1] #TODO: Get g somehow
                print('NEUMAAN DETECTED RIGHT!')
                 
            if(room[coord+n_matrix, 5] == 1):
                bc[index] = bc[index] + room[coord+n_matrix, 4]
            elif(room[coord+n_matrix, 5] == 2):
                print("NEUMANN BOTTOM")
                 
            index = index + 1
    
    #Toeplitz FINAL
    A  = T/(dx**2)  
    print(A)
    
    bc = -bc * 1/dx**2
    print('boundary :', bc)
    
    u = scipy.linalg.solve(A,bc)
    print('u:',u)
    
    # Inserting the internal temperatures to the internal points 
    index = 0;
    for i in range(n_matrix+1, m_matrix*n_matrix - n_matrix-1, n_matrix):
        for j in range(n_matrix-2):
            coord = i + j
            room[coord, 4] = u[index]
            index = index + 1
            
    # TODO: Make sure that the Neumann boundary gets an updated temperature 
    index = 0
    for i in range(n_matrix*m_matrix):
        if (room[i, 5] == 2):
            if (i % n_matrix == 0):
                room[i, 4] = g[index] * dx + room[i+1, 4] 
            else:
                room[i, 4] = -g[index] * dx + room[i-1, 4] 
            index = index + 1
    print(room)
#np.set_printoptions(threshold = np.nan)
#
#dx = 1/3
#rooms = np.array([[1,1,0,1]])
#myApartment = Apartment(rooms, dx)
#
#myApartment.set_boundary(0,0,0,1,0,2,0)
#myApartment.set_boundary(0,1,1,1,15,1,0)
#myApartment.set_boundary(1,0,1,1,15,1,0)
#myApartment.set_boundary(0,0,1,0,15,1,0)
#
#room = myApartment.get_coord()
#print(room)
#myApartment.plot_mesh()
#
#PDE_solve(room)
#dx = 1/3
#room = np.array([0,0,0,0])
#bc = np.array([-2,-2,-2,-2]) * 1/dx**2
#PDE_solve(1, room, dx, bc, 4, 4)

# This initializes the different toeplitz matricies that are useful for 
    # the specified rooms. One toeplitz for room 1 and 3 and one toeplitz
    # for room 2. 
    
    # m is the amount of rows and n is the amount of columns.

