#
# Plot basic visualisation and contours
#
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from functions import read_single_field_binary, read_grid, maskdata, fixPlot
#
# User input data
#
maskU = True
xloc, yloc, zloc = 128, 64, 40      # Locations where to slice the contour
gridloc = '/home/alpatil/Simulations/ibmCaNS/corals/run/data/'
dataloc = '/home/alpatil/Simulations/ibmCaNS/corals/run/data/vex_fld_0002400.bin'
maskuloc = '/home/alpatil/Simulations/ibmCaNS/corals/run/data/sdfu.bin'
N = [512,512,256]
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
    U = maskdata(umask,U)
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