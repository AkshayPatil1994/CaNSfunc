# Canonical Navier-Stokes Analysis Routines

## Requirements

The installation below assumes you have already created a virtual python environment
```
pip install -r requirements.txt
```
## Input file `params.in`

Every line that starts with a `!` represents the key to the dictionary when reading the file for computing time averages. For example, `grid` can be used to access the grid information. Parameters below are in order corresponding to the list elements.

- `grid`: Computational grid points  
    - `Nx` - Number of grid points in x  
    - `Nx` - Number of grid points in y  
    - `Nx` - Number of grid points in z  
    - `Nks` - Number of grid points over the roughness height `ks`  
- `domain`: Domain length   
    - `lx` - Domain length in x
    - `ly` - Domain length in y
    - `lz` - Domain length in z
    - `ks` - Height of the roughness
-  `ivisc`: Inverse of the the viscosity i.e., [`Re`] Reynolds number  
- `saveinfo`: Information about simulation data saves   
    - `niter` - Total number of iterations in the simulations
    - `nsaves` - Frequency at which results are saved
- `wavecondition`: Wave forcing conditions 
    - `Ub` - Wave orbital velocity in `[m/s]`
    - `Tw` - Wave period is `[s]`
    - `dts` - Results saved every `dts` `[s]`
- `avginfo`: User input for averaging
    - `avgs` - At which index does the time averaging start?
    - `avge` - At which index does the time averaging end?

