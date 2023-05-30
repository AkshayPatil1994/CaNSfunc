!
! Module for I/O for parameter file
!
module mod_param
    !
    use mod_types
    !
    implicit none
    public 
    integer, protected :: itot, jtot, ktot, nkstot
    real(rp), protected :: lx, ly, lz, ks
    real(rp), protected :: visci
    integer, protected :: nsteps, nsaves
    real(rp), protected :: Ub, Tw, Tsave
    integer, protected :: avgstart, avgend
contains

    subroutine read_input(myid)
        !
        use mpi 
        !
        implicit none
        integer, intent(in) :: myid
        integer :: iunit,ierr 
        ! This function reads the input file
        ! 
        ! INPUT
        !       myid:   [integer] Rank of the processor
        ! OUTPUT
        !       Print statement .OR. error code       
        !
        open(newunit=iunit,file='params.in',status='old',action='read',iostat=ierr)
        if( ierr == 0 ) then
          read(iunit,*,iostat=ierr) itot,jtot,ktot,nkstot
          read(iunit,*,iostat=ierr) lx,ly,lz,ks
          read(iunit,*,iostat=ierr) visci
          read(iunit,*,iostat=ierr) nsteps, nsaves
          read(iunit,*,iostat=ierr) Ub, Tw, Tsave
          read(iunit,*,iostat=ierr) avgstart, avgend
          if(myid == 0) print*, "Input file successfully read . . ."
        else
            if(myid == 0) print*, "Error reading input file"
            call MPI_FINALIZE(ierr)
            error stop
        end if
    end subroutine

    subroutine estParam(myid,nprocs,avgstart,avgend,nsaves,avglistlen)
        !
        use mpi 
        !
        implicit none
        integer, intent(in) :: myid, nprocs, avgstart, avgend, nsaves
        integer, intent(out) :: avglistlen
        !
        ! This subroutine computes preliminary parameters used to parallelise
        !
        ! INPUT
        !       myid:       [integer] Rank of the processor
        !       nprocs:     [integer] Total number of processors
        !       avgstart:   [integer] Starting index of the averaging fields
        !       avgend:     [integer] Ending index of the averaging fields
        !       nsaves:     [integer] Interval at which fields are saved
        ! OUTPUT
        !       avglist:    [integer array] Array of field indices to be loaded on the given
        !                   processor with rank `myid`      
        integer :: listlen

        listlen = (avgend - avgstart)/(nsaves)
        if( mod(listlen,nprocs) /= 0) Stop 'Ensure that mod(avgend - avgstart,nsaves*nprocs) == 0!'
        avglistlen = listlen/nprocs
        if( myid == 0) print*, "Each processor works with ",avglistlen," fields . . ."
        
    end subroutine estParam

 
end module mod_param
