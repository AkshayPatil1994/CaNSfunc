#
# Import required libraries
#
from mpi4py import MPI                  # MPI module
import math                             # Math module
import numpy as np                      # Array operations module
import time                             # Time measurement modules
import os                               # OS library for dir operations
import sys                              # System library for exit 
import psutil                           # Import process utilities
from functions import read_grid, read_single_field_binary, planAvg, maskdata, readinput, printLogo, sanityCheck
#
# Initialise MPI and communications
#
comm = MPI.COMM_WORLD   # Initialise MPI comm-world        
rank = comm.Get_rank()  # Get rank of each proc
size = comm.Get_size()  # Get size of mpirun for each instance
#
# Print header
#
if(rank == 0):
    printLogo()
#
# Setup input data [All processors initialise the data that is common]
#
saveArray = True                        # Save the planform array to file
printinfo = False                       # Print info to screen
dloc = '/mnt/storage1/waveCoral/ct1'    # Base location of the data
gridloc = dloc+'/data/'                 # Set the location of the grid
dataloc = dloc+'/data/vex_fld_'         # Choose the array to be loaded
maskuloc = dloc+'/data/sdfu.bin'        # Choose the masking array
# - - - - Name of the outputfile to store Uplan - - - - #
outfile = '/mnt/storage1/waveCoral/ct1/analysis/results/Uplan'
#-------------------------------------------------------------------------------#
# Do not change code below this line unless you are sure of what you are doing! #
# #-------------------------------------------------------------------------------#            
#
# Read input file [All processors read the input file]
#
[N, L, ivisc, svind, waveinfo, avginfo] = readinput('params.in',verbose=printinfo)
# Create an MPI barried to sync all processors here after reading the input file
comm.Barrier()
#
# Sanity check for analysis compatibility
#
if(rank == 0):
    sanityCheck(size,N[0:3],numfields=2,verbose=True)
#
# Setup the preliminary data [All processors are aware of the parameters]
#
Tw = waveinfo[1]                            # Wave period [s]
nsaveT = waveinfo[2]                        # Data is stored every `nsaveT` seconds in real time [s]
nsteps = svind[0]                           # Total number of iterations in the simulation
interval = svind[1]                         # Data is stored every `interval`
avgSind = avginfo[0]                        # Start index to begin averaging
avgEind = avginfo[1]                        # End index to begin averaging
datasize = int((avgEind-avgSind)/interval)  # Define the size of the result array
ldatasize = math.floor(datasize/size)       # Define the local datasize
if(rank==0):
    print("                 Data size: %d | Local data size: %d"%(datasize,ldatasize))
    print("-----------------------------------------------------------------------------")
#
# 
#

#
# Exit gracefully
#
if(rank == 0):     
    print("----------------------------------------------------------------")
    #print("Done in %f seconds......"%(totTime))
    print("----------------------------------------------------------------")