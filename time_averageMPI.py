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
printinfo = True                       # Print info to screen
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
if(rank == 0):
    [N, L, ivisc, svind, waveinfo, avginfo] = readinput('params.in',verbose=printinfo)
else:
    [N, L, ivisc, svind, waveinfo, avginfo] = readinput('params.in',verbose=False)
# Create an MPI barried to sync all processors here after reading the input file
comm.Barrier()
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
farr = np.arange(avgSind,avgEind,interval)  # Array defining the files to be loaded
#
# Sanity check for analysis compatibility
#
if(rank == 0):
    sanityCheck(datasize,size,N[0:3],numfields=2,verbose=True)
#
# Results array
# 
Uplan = np.zeros([N[2],ldatasize])
#
# Print the local and total data size to screen
#
if(rank==0):
    print("                 Data size: %d | Local data size: %d"%(datasize,ldatasize))
    print("-----------------------------------------------------------------------------")
#
# Split the file-array to be run in parallel [Splitting done on all ranks]
#
farrsplit = np.array_split(farr,size,axis=0)
#
# All processors now load the masking array in memory
#
if(rank==0):
    st=time.time()  # Log start time of load
umask = read_single_field_binary(maskuloc,ng=N[0:3])
# Create a communication barrier for safety
comm.Barrier()
if(rank==0):
    et=time.time()  # Log end time of load
    print("Masking array finished loading in %f seconds on all procs . . . "%(et-st))
# Initialise the results for total time and iterations
totTime = 0
# Iterator is required by all processors
iter = 0    
#
# Now loop over the entire file arrays and perform the time averaging operations
#
for fInd in farrsplit[rank]:
    dfile = dataloc+str(fInd).zfill(7)+'.bin'
    # if(rank==0):
    #     # Load the velocity data
    st = time.time()
    U = read_single_field_binary(dfile,N[0:3])
    # Mask the data
    maskdata(umask,U)
    # Compute the planform average
    planAvg(U,Uplan[:,iter])
    # if(rank==0):
    #     # Log the start
    et = time.time()
    #     # Save total time
    totTime += (et-st)
    #     # Print information to screen
    #     print("Iteration %d/%d took %f seconds..."%(iter+1,ldatasize,et-st))
    #     # Increment iter
    #     iter += 1
    print("Done with iter %d on rank %d in %f seconds...."%(iter,rank,totTime))
    iter += 1
#
# Exit gracefully
#
if(rank == 0):     
    print("----------------------------------------------------------------")
    #print("Done in %f seconds......"%(totTime))
    print("----------------------------------------------------------------")