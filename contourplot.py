#
# Plot basic visualisation and contours
#
import numpy as np
import cmocean
import matplotlib.pyplot as plt
from functions import read_single_field_binary, read_grid, maskdata
#
# User input data
#
maskU = True
gridloc = '../data/'
dataloc = '../data/vex_fld_0001000.bin'
maskuloc = '../data/umask.bin'
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
