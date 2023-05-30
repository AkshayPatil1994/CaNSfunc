!
! This module defines all the necessary operations and functions
!
module mod_operators
    use mpi
    use mod_types,  only: rp, ii, jj, kk, deno
    use mod_param,  only: itot, jtot, ktot 
    implicit none    
contains

    subroutine maskdata(mask,data)
        real(rp), intent(in) :: mask(:,:,:)
        real(rp), intent(inout) :: data(:,:,:)
        ! This functions masks the inputdata in place
        !
        ! INPUT
        !       mask:       [itot x jtot x ktot array] masking array
        !       itot, jtot, ktot:   [integers] grid size in x, y, and z
        ! OUTPUT/INPUT
        !       data:       [itot x jtot x ktot array] data to be masked
        !
        do kk=1,ktot
            do jj=1,jtot
                do ii=1,itot
                    if(mask(ii,jj,kk) <= 0.0) then
                        data(ii,jj,kk) = 0.0
                    end if
                end do
            end do
        end do

    end subroutine maskdata

    subroutine planAvg(Uin,Uout)
        real(rp), intent(in) :: Uin(:,:,:)
        real(rp), intent(out) :: Uout(:)
        ! This function computes the planform average for the given array
        ! 
        ! INPUT
        !       Uin:    [itot x jtot x ktot array] Input array
        ! OUTPUT
        !       Uout:   [ktot array] Output array 
        do kk=1,ktot
            Uout(kk) = sum(Uin(:,:,kk))/deno(kk)
        end do
        
    end subroutine planAvg

end module mod_operators