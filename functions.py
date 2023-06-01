###########################
# FILE WITH ALL FUNCTIONS #
###########################
#
# Read single binary file [Copied from CaNS utilities]
# Author: P. Costa [original routines]
#       : A. Patil
# -
#
# SPDX-FileCopyrightText: Copyright (c) 2017-2022 Pedro Costa and the CaNS contributors. All rights reserved.
# SPDX-License-Identifier: MIT
#
# -
#
# Import all required libraries
#
import numpy as np                      # Array operations module
import os                               # OS library for dir operations
import sys                              # System library for exit 
import psutil                           # Import process utilities
import matplotlib.pyplot as plt         # Plotting library
#
# Read single binary results file
#
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
    ng = np.array(ng)           # Convert grid points list to array
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
    # Set the data to NaN inside the masking array
    dataarr[maskarr<0] = np.nan
    # Return the original array
    return dataarr 
#
# Planform average data
#
def planAvg(datarr,outvec):
    '''
        This function computes the planform average for a given array
    INPUT
        datarr:     [numpy array] Data array to be averaged
    OUTPUT
        outvec:     [Nz x 1 array]  Planform averaged array    
    '''
    # Average over homogeneous directions
    outvec = np.nanmean(datarr,axis=(0,1))
    # Return the data
    return outvec
#
# Read time averaging input file
#
def readinput(filename,verbose=False,rank=0):
    '''
        This function reads the input file for the time averaging
    INPUT
        filename:       [string] Name and location of the input file
        verbose:        [Boolean] Print the information to screen
        rank:           [integer] Default rank that prints
    OUTPUT
        parameters: [dictionary] Data with the parameters names and the data
    '''
    # Dictionary to store the results
    parameters = {}     # Store the name of the parameters
    data = {}           # Store the data
    # Open the file in read mode
    with open(filename, 'r') as file:
        current_parameter = None  # Variable to track the current parameter        
        # Read each line in the file
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace            
            # Skip comment lines starting with '!'
            if line.startswith('!'):
                current_parameter = line[1:].strip()  # Extract the parameter name
                continue            
            # Split the line by commas
            values = line.split(',')            
            # Check if it's a parameter or data line
            if current_parameter is not None:
                # Store parameter values
                parameter_values = [float(val) for val in values]
                parameters[current_parameter] = parameter_values
            else:
                # Store data values
                data[current_parameter] = [float(val) for val in values]
    # Assign the variables from param
    N = [int(value) for value in parameters['grid']]
    L = [float(value) for value in parameters['domain']]
    ivisc = [float(value) for value in parameters['ivisc']]
    svind = [int(value) for value in parameters['saveinfo']]
    waveinfo = [float(value) for value in parameters['wavecondition']]
    avginfo = [int(value) for value in parameters['avginfo']]
    # Print info to screen
    if(verbose and rank == 0):
        print("----------------------------------------------")
        print("Datatypes are enforced on return....")
        print("Parameters summary from file %s ..."%(filename))
        for parameter, values in parameters.items():
            print(f"{parameter}: {values}")
        print("----------------------------------------------")

    return N, L, ivisc, svind, waveinfo, avginfo
#
# Sanity check for the MPI code
#
def sanityCheck(ds,size,N,numfields=1,verbose=False):
    '''
        This function tests the MPI run
    INPUT
        ds:         [integer] Number of total files to be read
        size:       [integer] Number of CPUs used to run the case
        N:          [3 x 1 list] Number of grid points in x, y, and z
        numfield:   [integer] Number of arrays loaded in parallel
        verbose:    [Boolean] Print info to screen
    OUTPUT
        None
    '''
    # Force load psutil [seems to crash without a force load]
    # import psutil
    # Check if datasize is compatible
    if(ds % size != 0):
        print("You are trying to load %d files with %d processors"%(ds,size))
        print("Please ensure mod(%d,%d) == 0...."%(ds,size))
        sys.exit("Please ensure that you load atleast %d files in total"%(size))

    # Check total system memory available
    tmem = psutil.virtual_memory().total
    tmem = tmem/(1024**3)   # Convert bytes to GB
    # Estimate the size of data
    floatsize = 8   # Size of DP float
    fsGB = (N[0]*N[1]*N[2]*floatsize)/(1024**3) # Estimated size of the array in GB
    # Compare the file size against the installed virtual memory
    memchk = fsGB*numfields*size < tmem
    # Print warning
    if(memchk == False):
        print("Warning: RAM may be insufficient, please consider using nprocs < %d"%(size))
        print("")
        print("     -       -       -       -       -       -       -       -")
    else:
        print("             Memory check successful, running the analysis")
        print("     -       -       -       -       -       -       -       -")
    # Print to screen
    if(verbose):
        print("         Required memory ",round(fsGB*numfields*size,2)," | GB available memory ",round(tmem,2),"GB")
        print("     -       -       -       -       -       -       -       -")
#
# Interpolate U from faces to cell center
#
def interpU(Uin,dir):
    '''
        This function interpolates the velocity from faces to cell-centers
    INPUT
        Uin:    [3D numpy array] Velocity vector to be interpolated
        dir:    [integer] Direction in which interpolation is needed
                1 - interpolate in x
                2 - interpolate in y
                3 - interpolate in z
    OUTPUT
        Uin:    [3D numpy array] Returns the output array
    '''
    usize = np.size(Uin)
    match dir:
        case 1:
            Uin[0:usize[0]-1,:,:] = 0.5*(Uin[0:usize[0]-1,:,:] + Uin[1:usize[0],:,:]) 
        case 2:
            Uin[:,0:usize[1]-1,:] = 0.5*(Uin[:,0:usize[1]-1,:] + Uin[:,1:usize[1],:])     
        case 3:
            Uin[:,:,0:usize[2]-1] = 0.5*(Uin[:,:,0:usize[2]-1] + Uin[:,:,1:usize[2]])
        case _:
            raise ValueError("Invalid interpolation direction specified dir = %d"%(dir))
    return Uin        
#
# Generate results storing arrays
#
def gendir():
    '''
        This function generates the required directories to store the data
    INPUT
        None
    OUTPUT
        Generates the directories if not already present
    '''
    direxists = os.path.isdir("stats")
    if(direxists):
        print("`stats/` directory already exists . . .")
    else:
        os.mkdir("stats/")
        print("`stats/` directory successfully created . . .")
#
# Set default plotting size
#
def fixPlot(thickness=1.5, fontsize=20, markersize=8, labelsize=15, texuse=False, tickSize = 15):
    '''
        This plot sets the default plot parameters
    INPUT
        thickness:      [float] Default thickness of the axes lines
        fontsize:       [integer] Default fontsize of the axes labels
        markersize:     [integer] Default markersize
        labelsize:      [integer] Default label size
    OUTPUT
        None
    '''
    # Set the thickness of plot axes
    plt.rcParams['axes.linewidth'] = thickness    
    # Set the default fontsize
    plt.rcParams['font.size'] = fontsize    
    # Set the default markersize
    plt.rcParams['lines.markersize'] = markersize    
    # Set the axes label size
    plt.rcParams['axes.labelsize'] = labelsize
    # Enable LaTeX rendering
    plt.rcParams['text.usetex'] = texuse
    # Tick size
    plt.rcParams['xtick.major.size'] = tickSize
    plt.rcParams['ytick.major.size'] = tickSize
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
#
# Print utils logo
#     
def printLogo():
    print("-----------------------------------------------------------------------------")
    print(" ██████╗ █████╗ ███╗   ██╗███████╗      ██╗   ██╗████████╗██╗██╗     ███████╗")
    print("██╔════╝██╔══██╗████╗  ██║██╔════╝      ██║   ██║╚══██╔══╝██║██║     ██╔════╝")
    print("██║     ███████║██╔██╗ ██║███████╗█████╗██║   ██║   ██║   ██║██║     ███████╗")
    print("██║     ██╔══██║██║╚██╗██║╚════██║╚════╝██║   ██║   ██║   ██║██║     ╚════██║")
    print("╚██████╗██║  ██║██║ ╚████║███████║      ╚██████╔╝   ██║   ██║███████╗███████║")
    print(" ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝       ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝")
    print("-----------------------------------------------------------------------------")