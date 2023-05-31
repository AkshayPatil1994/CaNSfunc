#
# Import required libraries
#
import numpy as np
import time
from rich.console import Console
from functions import read_grid, read_single_field_binary, planAvg, maskdata, readinput, printLogo, \
                      sanityCheck, gendir
#
# Setup input data
#
saveArray = True                        # Save the planform array to file
printinfo = False                       # Print info to screen
dloc = '/mnt/storage1/waveCoral/ct1'    # Base location of the data
gridloc = dloc+'/data/'                 # Set the location of the grid
uloc = dloc+'/data/vex_fld_'            # Choose the array to be loaded
vloc = dloc+'/data/vey_fld_'            # Choose the array to be loaded
wloc = dloc+'/data/vey_fld_'            # Choose the array to be loaded
maskuloc = dloc+'/data/sdfu.bin'        # Choose the u masking array
maskvloc = dloc+'/data/sdfv.bin'        # Choose the v masking array
maskwloc = dloc+'/data/sdfw.bin'        # Choose the w masking array
# - - - - Name of the outputfile to store Uplan - - - - #
#uplanoutfile = '/mnt/storage1/waveCoral/ct1/analysis/results/Uplan'
#-------------------------------------------------------------------------------#
# Do not change code below this line unless you are sure of what you are doing! #
#-------------------------------------------------------------------------------#            
console = Console()
#
# Print initial header
#
printLogo()
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
Uplan = np.zeros([N[2],datasize])       # Initialise the empty numpy arrays
urms = np.zeros([N[2],datasize])        # Root mean squared u velocity
vrms = np.zeros([N[2],datasize])        # Root mean squared u velocity
wrms = np.zeros([N[2],datasize])        # Root mean squared u velocity
#
# Run RAM sanity check [assumes double precision data]
#
sanityCheck(datasize,1,N[0:3],numfields=6,verbose=True)
# Ensure results directories exist
gendir()
#
# Read the grid once
#
st = time.time()
[xf,yf,zf,xp,yp,zp] = read_grid(loc=gridloc,ng=N[0:3],r0=[0.,0.,0.],non_uniform_grid=True)
#
# Read the masking data
#
umask = read_single_field_binary(maskuloc,ng=N[0:3])
vmask = read_single_field_binary(maskvloc,ng=N[0:3])
wmask = read_single_field_binary(maskwloc,ng=N[0:3])
et = time.time()
console.print("Grid and masking read in %f seconds . . ."%(round(et-st,3)))
#
# Set up the averaging loop
#
console.print("Starting the analysis time loop . . .")
totTime, iter = 0, 0
for find in range(avgSind,avgEind,interval):
    dufile = uloc+str(find).zfill(7)+'.bin'
    dvfile = vloc+str(find).zfill(7)+'.bin'
    dwfile = wloc+str(find).zfill(7)+'.bin'
    # Load the velocity data
    st = time.time()
    U = read_single_field_binary(dufile,N[0:3])
    V = read_single_field_binary(dvfile,N[0:3])
    W = read_single_field_binary(dwfile,N[0:3])
    # Mask the data
    U = maskdata(umask,U)
    V = maskdata(vmask,V)
    W = maskdata(wmask,W)
    # Compute the planform average
    Uplan[:,iter] = planAvg(U,Uplan[:,iter])
    urms[:,iter] = planAvg(U**2,urms[:,iter])
    vrms[:,iter] = planAvg(V**2,vrms[:,iter])
    wrms[:,iter] = planAvg(W**2,wrms[:,iter])
    # Lof the end time
    et = time.time()
    # Save total time
    totTime += (et-st)          
    console.print("Iteration %d/%d done in %f s | Estimated total time %f s"%(iter+1,datasize,et-st,(totTime/(iter+1))*datasize))
    #Increment iter
    iter += 1
#
# Save array to file
#
if(saveArray):
    np.save('stats/uplan',Uplan)        # Planform u velocity
    np.save('stats/urms',urms)          # urms velocity
    np.save('stats/vrms',vrms)          # vrms velocity
    np.save('stats/wrms',wrms)          # wrms velocity
#
# Exit gracefully
#     
console.print("Done in %f seconds . . ."%(totTime))