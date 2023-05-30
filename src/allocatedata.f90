!
! This module allocates all the arrays
!
module mod_allocatedata
    !
    use mpi
    use mod_types
    use mod_param,  only: itot, jtot, ktot
    !
    implicit none
contains 

    subroutine initdata(myid)
        ! 
        use mpi
        use mod_types,  only: avglist, avglistlen, u
        use mod_param,  only: itot, jtot, ktot
        !
        implicit none
        integer, intent(in) :: myid
        ! This function initialises all the working data arrays
        ! 
        ! INPUT
        !       myid:       [integer] Rank fo the processors
        ! OUTPUT
        !       Allocates all the arrays
        allocate ( avglist(avglistlen) )
        ! velocity data array
        allocate ( u(itot,jtot,ktot) )


    end subroutine initdata

end module mod_allocatedata