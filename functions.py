###########################
# FILE WITH ALL FUNCTIONS #
###########################
#
# Read single binary file [Copied from CaNS utilities]
# Author: P. Costa
#
# -
#
# SPDX-FileCopyrightText: Copyright (c) 2017-2022 Pedro Costa and the CaNS contributors. All rights reserved.
# SPDX-License-Identifier: MIT
#
# -
def read_single_field_binary(filenamei,ng,iskip=[1,1,1],r0=[0.,0.,0.]):
    '''
        This file reads a single binary field generated within CaNS
    INPUT
        filenamei:  [string] Filename and location of the binary data to be read
        ng:         [3 x 1 -- list] Size of the grid in x, y, and z
        iskip:      [3 x 1 -- list] Data is written every nth point in x, y, and z
        r0:         [3 x 1 -- list] Location of the origin
    OUTPUT
        data:       [ng sized -- numpy array] Numpy array as output          
    '''
    #
    # Force import libraries
    #
    import numpy as np
    import os
    import sys
    #
    # Check if the file directory exists
    #
    filestat = os.path.exists(filenamei)
    if(filestat == False):
        sys.exit("The input file at %s does not exist!"%(filenamei))
    #
    # Setting up some parameters
    #
    iprecision = 8              # precision of the real-valued data
    r0 = np.array(r0)           # domain origin
    iskip = np.array(iskip)     # Convert iskip to array
    precision  = 'float64'      # Set the float precision
    if(iprecision == 4): precision = 'float32'
    #
    # read binary file
    #
    n           = (ng[:]/iskip[:]).astype(int)
    data        = np.zeros([n[0],n[1],n[2]])
    fld         = np.fromfile(filenamei,dtype=precision)
    data[:,:,:] = np.reshape(fld,(n[0],n[1],n[2]),order='F')
    # Return the required array
    return data
#
# Read the grid information 
#
def read_grid(loc='data/',iprecision=8,ng=[10,10,10],r0=[0.,0.,0.],non_uniform_grid = False):
    '''
        This function reads the grid information generated within CaNS
    INPUT
        loc:                [string] Location where the grid information is saved
        iprecision          [integer] Precision used for the arrays
        ng:                 [3 x 1 -- list] Size of the grid in x, y, and z
        r0:                 [3 x 1 -- list] Location of the origin
        non_uniform_grid:   [Boolean] Is the grid non uniform
    OUTPUT
        xp, yp, zp:         [Numpy arrays] Cell-Center grid
        xu, yv, zw:         [Numpy arrays] Cell-Face grid
    '''
    import numpy as np
    import os
    import sys
    #
    # Check if the file directory exists
    #
    filestat = os.path.exists(loc)
    if(filestat == False):
        sys.exit("The input file at %s does not exist!"%(loc))
    #
    # setting up some parameters
    #
    r0 = np.array(r0) # domain origin
    precision  = 'float64'
    if(iprecision == 4): precision = 'float32'
    #
    # read geometry file
    #
    geofile  = loc+"geometry.out"
    geo = np.loadtxt(geofile, comments = "!", max_rows = 2)
    ng = geo[0,:].astype('int')
    l  = geo[1,:]
    dl = l/(1.*ng)
    #
    # read and generate grid
    #
    xp = np.arange(r0[0]+dl[0]/2.,r0[0]+l[0],dl[0]) # centered  x grid
    yp = np.arange(r0[1]+dl[1]/2.,r0[1]+l[1],dl[1]) # centered  y grid
    zp = np.arange(r0[2]+dl[2]/2.,r0[2]+l[2],dl[2]) # centered  z grid
    xu = xp + dl[0]/2.                              # staggered x grid
    yv = yp + dl[1]/2.                              # staggered y grid
    zw = zp + dl[2]/2.                              # staggered z grid
    if(non_uniform_grid):
        grdfile = loc+'grid.bin'                    # Specify the location of the grid file
        f   = open(grdfile,'rb')
        grid_z = np.fromfile(f,dtype=precision)
        f.close()
        grid_z = np.reshape(grid_z,(ng[2],4),order='F')
        zp = r0[2] + np.transpose(grid_z[:,2]) # centered  z grid
        zw = r0[2] + np.transpose(grid_z[:,3]) # staggered z grid

    return xp, yp, zp, xu, yv, zw        
#
# Mask user data
#
def maskdata(maskarr,dataarr):
    '''
        This function masks the dataarr and sets the internal location to `NaN`
    INPUT
        maskarr:    [Numpy array] Masking array
        dataarr:    [Numpy array] Data array that requries masking
    OUTPUT
        datarr:     [Numpy array] The data is masked in place        
    '''
    import numpy
    # Set the data to NaN inside the masking array
    dataarr[maskarr<0] = numpy.nan
    # Return the original array
    return dataarr 