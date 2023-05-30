!
! File I/O module
!
module mod_load
    !
    use mpi
    use mod_types,     only: rp
    ! 
    implicit none
    
contains
    
    subroutine load_one(myid,filename,data)
        !
        use mpi
        use mod_types,     only: rp
        !
        implicit none
        integer, intent(in) :: myid
        character(200), intent(in) :: filename
        real(rp), intent(out) :: data(:,:,:)
        ! This function reads the input file with data
        !
        ! INPUT
        !       myid:               [integer] Rank of the processor
        !       filename:           [character] Name of the input file
        ! OUTPUT
        !       data:               [itot x jtot x ktot] array with field info
        open(unit=myid,file=filename,action='read',form='unformatted',status='old',access='stream')
        read(unit=myid) data(:,:,:)
        close(unit=myid)

    end subroutine load_one

end module mod_load
