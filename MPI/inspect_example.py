#  Before you use this file, install mpi4py on your computer
#  anaconda users do this like that:    conda install mpi4py
#
#  in a command window execute then the following command
#
#  mpiexec -n 2 python ~/Desktop/inspect.py
#  (replace "Desktop" by the path o this file and replace the number of
#  processors from 2 to the number you want.)


from mpi4py import MPI
from scipy import *

comm=MPI.COMM_WORLD
rank=comm.Get_rank()
np=comm.size
print('I am CPU {} and I see in total {} CPUs\n'.format(rank,comm.size))
sendbuffer=['Here my message, enjoy it!',rank*ones((3,))]
comm.send(sendbuffer,(rank+1)%np,0)
print('I sent to {} this information:\n'.format((rank+1)%np), sendbuffer)
status = MPI.Status()
recievebuffer=comm.recv(source=(rank-1)%np,status=status)
print('I obtained from {} this information:\n'.format((rank-1)%np), recievebuffer)
