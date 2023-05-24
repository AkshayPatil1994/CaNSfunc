#
# Import required libraries
#
import numpy as np
import time
from functions import read_grid, read_single_field_binary, planAvg, maskdata, readinput
#
# Setup input data
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
# Print initial header
#
if(printinfo):
    print("----------------------------------------------------------------")
#
# Read input file    
#
[N, L, ivisc, svind, waveinfo, avginfo] = readinput('params.in',verbose=printinfo)
#
# Setup the preliminary data
#
Tw = waveinfo[1]        # Wave period [s]
nsaveT = waveinfo[2]    # Data is stored every `nsaveT` seconds in real time [s]
nsteps = svind[0]       # Total number of iterations in the simulation
interval = svind[1]     # Data is stored every `interval`
avgSind = avginfo[0]    # Start index to begin averaging
avgEind = avginfo[1]    # End index to begin averaging
datasize = int((avgEind-avgSind)/interval)  # Define the size of the result array
Uplan = np.zeros([N[2],datasize])      # Initialise the empty numpy arrays
#
# Read the grid once
#
[xf,yf,zf,xp,yp,zp] = read_grid(loc=gridloc,ng=N[0:3],r0=[0.,0.,0.],non_uniform_grid=True)
#
# Read the masking data
#
umask = read_single_field_binary(maskuloc,ng=N[0:3])
#
# Set up the averaging loop
#
print("----------------------------------------------------------------")
print("Starting the analysis time loop.....")
totTime, iter = 0, 0
for find in range(avgSind,avgEind,interval):
    dfile = dataloc+str(find).zfill(7)+'.bin'
    # Load the velocity data
    st = time.time()
    U = read_single_field_binary(dfile,N[0:3])
    # Mask the data
    maskdata(umask,U)
    # Compute the planform average
    planAvg(U,Uplan[:,iter])
    # Lof the end time
    et = time.time()
    # Save total time
    totTime += (et-st)          
    print("Iteration %d/%d completed in %f seconds. . . ."%(iter+1,datasize,et-st))
    #Increment iter
    iter += 1
#
# Save array to file
#
if(saveArray):
    np.save(outfile,Uplan)
#
# Exit gracefully
#     
print("----------------------------------------------------------------")
print("Done in %f seconds......"%(totTime))
print("----------------------------------------------------------------")