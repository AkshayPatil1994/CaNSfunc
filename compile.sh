EXEC=run/stats
mpif90 -ffree-line-length-none -o $EXEC src/types.f90  src/allocatedata.f90 src/common_mpi.f90 src/load.f90 src/utils.f90 src/param.f90 src/main.f90 -J mod/
# Clean up all module files
#rm *.mod
