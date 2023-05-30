!
! Module for miscellaneous utilites
!
module mod_utils
    !
    use mpi
    !
    implicit none
contains

    subroutine echologo(myid,size)
        integer, intent(in) :: myid, size 
        !
        ! This function prints the logo
        !
        ! INPUT
        !       myid:       [integer] Rank of the MPI process
        !       size:       [integer] Total number of processors used
        ! OUTPUT
        !       Prints the logo
        if(myid == 0) print*, "-----------------------------------------------------------------------------"
        if(myid == 0) print*, " ██████╗ █████╗ ███╗   ██╗███████╗      ██╗   ██╗████████╗██╗██╗     ███████╗"
        if(myid == 0) print*, "██╔════╝██╔══██╗████╗  ██║██╔════╝      ██║   ██║╚══██╔══╝██║██║     ██╔════╝"
        if(myid == 0) print*, "██║     ███████║██╔██╗ ██║███████╗█████╗██║   ██║   ██║   ██║██║     ███████╗"
        if(myid == 0) print*, "██║     ██╔══██║██║╚██╗██║╚════██║╚════╝██║   ██║   ██║   ██║██║     ╚════██║"
        if(myid == 0) print*, "╚██████╗██║  ██║██║ ╚████║███████║      ╚██████╔╝   ██║   ██║███████╗███████║"
        if(myid == 0) print*, " ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝       ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝"
        if(myid == 0) print*, "-----------------------------------------------------------------------------"
        if(myid == 0) print*, "             Starting analysis with ",size," processors"
    end subroutine echologo

    subroutine queryRAM(myid,size,narrays,itot,jtot,ktot)
        integer, intent(in) :: myid, size, narrays, itot, jtot, ktot 
        real :: requiredRAM 
        ! This functions queries the system installed RAM
        !
        ! INPUT
        !       myid:       [integer] Processor id
        !       size:       [integer] Total number of processors used
        !       narrays:    [integer] Total number of 3D arrays declared
        !       itot, jtot, ktot:   [integers] Size of the grid in x, y, and z
        ! OUTPUT
        !       Prints the required memory [estimated!]
        requiredRAM = (real(itot*jtot*ktot*narrays*real(size+1)*8.0)/1e9) 
        print*, "Estimated memory required: ", 1.1*requiredRAM, "GB . . ."
    end subroutine queryRAM
end module mod_utils