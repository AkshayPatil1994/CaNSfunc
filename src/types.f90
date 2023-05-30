! Copied from CaNS
!
! This module declared the type of the data
!
module mod_types
    use mpi, only: MPI_REAL,MPI_DOUBLE_PRECISION
    !
    ! Please note that the code below forces double precision.
    !
    integer, parameter, public :: sp = selected_real_kind(6 , 37), &
                                  dp = selected_real_kind(15,307), &
                                  i8 = selected_int_kind(18)
    integer, parameter, public :: rp = dp
    integer, parameter, public :: MPI_REAL_RP = MPI_DOUBLE_PRECISION
    !
    ! Define data on all processors
    !
    ! Globally available parameters
    integer :: ii, jj, kk   ! Global grid iterators
    integer :: gi           ! Global arbitrary iterator
    integer :: indexval    
    ! CPU time parameters
    real(rp) :: starttime, endtime 
    ! File names
    character(200) :: infile  
    ! File list params
    integer :: avglistlen 
    integer, allocatable, dimension(:) :: avglist 
    ! Data arrays
    integer, allocatable, dimension(:) :: deno 
    real(rp), allocatable, dimension(:,:,:) :: umask
    real(rp), allocatable, dimension(:,:,:) :: u
    real(rp), allocatable, dimension(:) :: uplan

end module mod_types
  