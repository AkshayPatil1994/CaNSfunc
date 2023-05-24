#
# Plot basic visualisation and contours
#
import psutil as ps
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from functions import read_single_field_binary, read_grid, maskdata, fixPlot
#
# Log initial memory load
#
pinit = ps.Process()
imem = pinit.memory_info().rss  # Log the initial memory
#
# User input data
#
findex = '0002400'                      # Index of the file to be loaded included padded 0s
N = [512,512,256]                       # Grid size
maskU = True                            # Do you wish to mask the velocity?
xloc, yloc, zloc = 128, 64, 40          # Locations where to slice the contour
dloc = '/home/alpatil/Simulations/ibmCaNS/corals/run'    # Base location of the data
#
# Setting up the right data directories
#
gridloc = dloc+'/data/'
dataloc = dloc+'/data/vex_fld_'+findex+'.bin'
maskuloc = dloc+'/data/sdfu.bin'
#
# Load the grid
#
[xf,yf,zf,xp,yp,zp] = read_grid(loc=gridloc,ng=N,r0=[0.,0.,0.],non_uniform_grid=True)
#
# Load the velocity and Umask
#
U = read_single_field_binary(dataloc,N)
# Load masking if user prompts
if(maskU):
    # Load the masking array
    umask = read_single_field_binary(maskuloc,N)
    # Mask the data
    maskdata(umask,U)
# Log the end process memory
emem = pinit.memory_info().rss  # Log the end memory
memuse = emem - imem            # Total memory used
memuse = ps._common.bytes2human(memuse) # Convert to human readable format
print("Estimated memory used: ",memuse)
#
# Plot the contour map
#
fixPlot(thickness=2.5, fontsize=25, markersize=8, labelsize=20)
plt.figure(1,figsize=(10,10))
cmap = cmocean.cm.curl                       # Choose a colormap
plt.contourf(xf,yp,np.squeeze(U[:,:,zloc]).T,cmap=cmap)
# Axis labels
plt.xlabel(r'$x_1$',fontsize=25)
# Quality fixes 
plt.gca().set_facecolor('yellow')
plt.axis('equal')
plt.show()