! ~May 2023~
! Main program that computes the flow statistics
!   Author(s): Pedro Costa [Original code and modules]
!            : Akshay Patil 
program compstats

    use, intrinsic :: iso_fortran_env, only: compiler_options, compiler_version
    use, intrinsic :: ieee_arithmetic, only: is_nan => ieee_is_nan
    use mpi
    use mod_common_mpi,     only: myid, ierr, size
    use mod_utils,          only: echologo, queryRAM
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
    use mod_operators,      only: maskdata, planAvg
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
    if(myid == 0) then
        call queryRAM(myid=myid,size=size,narrays=4,itot=itot,jtot=jtot,ktot=ktot)
    end if 
    ! Initialise the list of fields to load on each processor
    indexval = avgstart + myid*nsaves*avglistlen           ! Initial offset on each processor
    do gi=1,avglistlen
        avglist(gi) = indexval
        indexval = indexval + nsaves
    end do

    ! Setup communication barrier
    if(myid == 0) print*, "-----------------------------------------------------------------------------"
    call MPI_BARRIER(MPI_COMM_WORLD,ierr)
    print*, "Rank ",myid, "works on files from ",avglist(1),"to",avglist(avglistlen)
    call MPI_BARRIER(MPI_COMM_WORLD,ierr)

    ! Load masking data [on all processors]
    infile = '../data/sdfu.bin'
    call load_one(myid,infile,umask)
    
    ! Compute the averaging denominator
    deno = itot*jtot*ktot
    do kk=1,ktot
        do jj=1,jtot
            do ii=1,itot 
                if(umask(ii,jj,kk) <= 0.0) then                  
                    deno(kk) = deno(kk) - 1
                end if 
            end do
        end do
    end do
    ! Write denominator used for averaging to file
    if(myid == 0) then
        infile = '../data/denominator.dat'
        open(unit=myid,file=infile,action='write',form='formatted',status='replace',access='stream')
        do kk=1,ktot
            write(myid,*) deno(kk)
        end do
        close(unit=myid)
    end if
    ! Communication and I/O barrier
    call MPI_BARRIER(MPI_COMM_WORLD,ierr)
    ! Loop over all the files to load and analyse
    do gi=1,avglistlen
        ! Define the filename
        write(infile,'(A,I7.7,A)') '../data/vex_fld_', avglist(gi),'.bin'        
        ! Load file
        call load_one(myid,infile,u) 
        ! Mask data
        call maskdata(umask,u)
        ! Planform average the velocity
        call planAvg(u,uplan)
    end do
    call cpu_time(endtime)
    print*, "Total elapsed time: ", endtime-starttime

    

    ! Exit MPI
    call MPI_FINALIZE(ierr)
end program compstats