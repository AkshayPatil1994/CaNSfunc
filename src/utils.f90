!
! Module for miscellaneous utilites
!
module mod_utils

contains

    subroutine echologo(myid,size)
        !
        use mpi
        !
        implicit none 
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

end module mod_utils