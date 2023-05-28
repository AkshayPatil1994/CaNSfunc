import numpy as np
import matplotlib.pyplot as plt
from functions import read_grid, readinput, fixPlot
# Read input file
[N, L, ivisc, svind, waveinfo, avginfo] = readinput('params.in',verbose=False)
Tw = waveinfo[1]        # Wave period [s]
nsaveT = waveinfo[2]    # Data is stored every `nsaveT` seconds in real time [s]
nsteps = svind[0]       # Total number of iterations in the simulation
interval = svind[1]     # Data is stored every `interval`
avgSind = avginfo[0]    # Start index to begin averaging
avgEind = avginfo[1]    # End index to begin averaging
datasize = int((avgEind-avgSind)/interval)  # Define the size of the result array
# Setup preliminary data
dloc = '/home/alpatil/Simulations/ibmCaNS/corals/ct2'    # Base location of the data
gridloc = dloc+'/data/'                 # Set the location of the grid
dataloc = dloc+'/data/vex_fld_'         # Choose the array to be loaded
maskuloc = dloc+'/data/sdfu.bin'        # Choose the masking array
outfile = '/home/alpatil/Simulations/ibmCaNS/corals/ct2/'
# Load average arrays
[xf,yf,zf,xp,yp,zp] = read_grid(loc=gridloc,ng=N[0:3],r0=[0.,0.,0.],non_uniform_grid=True)
fname = outfile+'Uplan.npy'
Uplan = np.load(fname)
fname = outfile+'urms.npy'
urms = np.load(fname)
# Plotting
plt.figure(1,figsize=(10,10))
fixPlot(thickness=3.0,fontsize=30)
plt.subplots_adjust(wspace=0.6)
plt.subplot(1,2,1)
plt.plot(urms/waveinfo[0],zp/L[2],'r-.')
plt.axis('square')
plt.subplot(1,2,2)
plt.plot(Uplan/waveinfo[0],zp/L[2],'k')
plt.axis('square')
plt.show()