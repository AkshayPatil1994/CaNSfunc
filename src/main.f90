! ~May 2023~
! Main program that computes the flow statistics
!   Author(s): Pedro Costa [Original code and modules]
!            : Akshay Patil 
program compstats

    use, intrinsic :: iso_fortran_env, only: compiler_options, compiler_version
    use, intrinsic :: ieee_arithmetic, only: is_nan => ieee_is_nan
    use mpi
    use mod_common_mpi,     only: myid, ierr, size
    use mod_utils,          only: echologo
    use mod_param,          only: itot, jtot, ktot, nkstot, &
                                    lx, ly, lz, ks, &
                                    visci, &
                                    nsteps, nsaves, &
                                    Ub, Tw, Tsave, &
                                    avgstart, avgend, &
                                    ! Items listed below are functions
                                    read_input, estParam
    ! All data within types is used, be careful when allocating large arrays [memory intensive]
    use mod_types           
    use mod_allocatedata,   only: initdata
    use mod_load,           only: load_one
    !
    implicit none                         

    ! Initialise MPI
    call MPI_INIT(ierr)
    call MPI_COMM_SIZE(MPI_COMM_WORLD,size,ierr)
    call MPI_COMM_RANK(MPI_COMM_WORLD,myid,ierr)
    call cpu_time(starttime)
    ! Print logo
    call echologo(myid,size)
    ! All Processors read the input file
    call read_input(myid)
    ! Estimate some preliminary parameters [used for parallelisation]
    call estParam(myid,size,avgstart,avgend,nsaves,avglistlen)
    call initdata(myid)
    ! Initialise the list of fields to load on each processor
    indexval = avgstart + myid*nsaves*avglistlen           ! Initial offset on each processor
    do gi=1,avglistlen
        avglist(gi) = indexval
        indexval = indexval + nsaves
    end do
    ! Setup communication barrier
    call MPI_BARRIER(MPI_COMM_WORLD,ierr)
    print*, "Rank ",myid, "works on files from ",avglist(1),"to",avglist(avglistlen)
    call MPI_BARRIER(MPI_COMM_WORLD,ierr)
    ! Loop over all the files to load and analyse
    do gi=1,avglistlen
        ! Define the filename
        write(infile,'(A,I7.7,A)') '../data/vex_fld_', avglist(gi),'.bin'        
        ! Load file
        call load_one(myid,infile,u) 
        !

    end do
    call cpu_time(endtime)
    print*, "Total elapsed time: ", endtime-starttime, myid

    

    ! Exit MPI
    call MPI_FINALIZE(ierr)
end program compstats