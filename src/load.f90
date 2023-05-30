!
! File I/O module
!
module mod_load
    !
    use mpi
    use mod_types,      only: rp, kk
    use mod_param,      only: ktot
    ! 
    implicit none
    
contains
    
    subroutine load_one(myid,filename,data)
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

    subroutine write1dprof(myid, filename, data)
        integer, intent(in) :: myid
        character(200), intent(in) :: filename
        real(rp), intent(in) :: data(:)
        ! This function writes the 1D profiles to file
        !
        ! INPUT
        !       myid:           [integer] Processor rank
        !       filename:       [character] Name of the file
        !       data:           [ktot sized array] 1D data vector to be written to file
        ! OUTPUT
        !       Data is written to the specified file
        open(unit=myid,file=filename,action='write',form='formatted',status='replace',access='stream')
        do kk=1,ktot
            write(myid,*) data(kk)
        end do 
        close(unit=myid)

    end subroutine write1dprof
end module mod_load
