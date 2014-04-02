module heliac_data_retrieve
    use linked_list
    use heliac_data_loader
    use calc_tools, only : average, xy, ne_calc, te_calc,&
                          &vf_calc, vs_calc, periodic_subtract

    implicit none
    !use dataset
    
!    type data_order
!        integer shot
!        real :: int_ave(2) = (/0,0/)
!        real fmin, fmax, omin, omax
!        character chname
!    end type
!    type(heliac_data) :: rawdata

    interface 
    end interface
    character(50) :: chtxtpath = "/Users/yu/chconv.txt"
contains
	SUBROUTINE UNIT_CALC(chdata)
		USE HELIAC_DATA_LOADER
!
		TYPE(CHANNEL_DATA),	INTENT(INOUT)		::	chdata
!
		INTEGER	::	i, unit
!
		unit  =INT(LOG10(ABS(MAXVAL(chdata%data) - MINVAL(chdata%data))))

!
		DO i=1, chdata%n_size
			chdata%data(i)=chdata%data(i)/10.0**unit
		END DO
!
		IF(SCAN(chdata%unit, "V")/=0)THEN
			WRITE(chdata%unit,*)unit
			chdata%unit="(10^"//TRIM(ADJUSTL(chdata%unit))//" V)"
		ELSE IF(SCAN(chdata%unit, "A")/=0)THEN
			WRITE(chdata%unit,*)unit
			chdata%unit="(10^"//TRIM(ADJUSTL(chdata%unit))//" A)"
		ELSE
			chdata%unit="(10^"//TRIM(ADJUSTL(chdata%unit))//")"
		END IF
!
	END SUBROUTINE UNIT_CALC
    
    subroutine get_data(olst, retlst)
        type(node), pointer :: olst, retlst
        type(heliac_data), pointer :: rawdata 
        type(xydata), pointer :: xys
        integer, pointer :: shot => null()
        character(len(olst%order%chname)), pointer :: chname => null()
        real, pointer :: int_ave(:) => null()
        double precision, allocatable :: retx(:), rety(:)
        integer i, chnum, ierr, ch

        retlst => null()
        
        do i = 1, get_n(olst) 
            allocate(rawdata)
            call refer(olst, i)
            shot => olst%order%shot
            allocate(xys)
            xys%x_name = "Time [ms]"
            if (olst%order%chname == "ne") then 
                call ne_calc(shot, retx, rety)
                call pointtar(xys%x, retx)
                call pointtar(xys%y, rety)
            else if (olst%order%chname == "te") then 
                call te_calc(shot, retx, rety)
                call pointtar(xys%x, retx)
                call pointtar(xys%y, rety)
            else if (olst%order%chname == "vf") then 
                call vf_calc(shot, retx, rety)
                call pointtar(xys%x, retx)
                call pointtar(xys%y, rety)
            else if (olst%order%chname == "vs") then 
                call vs_calc(shot, retx, rety)
                call pointtar(xys%x, retx)
                call pointtar(xys%y, rety)
            else
                ierr =  heliac_data_init(rawdata)
                ierr = open_file(rawdata, shot, .true.)
                ierr = heliac_param_load(rawdata)
                ch = chconv(rawdata, olst%order%chname)
                ierr = heliac_chdata_load(rawdata, ch)
                call channel_data_convert(rawdata%raw(ch))
                !if (olst%order%chname == "pb") call periodic_subtract(rawdata%raw(ch)%time, rawdata%raw(ch)%data, 2d1)
                call pointtar(xys%x, rawdata%raw(ch)%time)
                call pointtar(xys%y, rawdata%raw(ch)%data)
                call close_file(rawdata)
            end if
            !if (allocated(retx)) deallocate(retx)
            !if (allocated(rety)) deallocate(rety)
            !call rev_ground(omin, omax, rawdata%raw(ch))
            !call filter(fmin, fmax, 0., 0., rawdata%raw(ch))
            !call unit_calc(rawdata%raw(ch))
           !xys%y_name = get_chname(rawdata, chname)
            !if (olst%order%int_ave(1) /= 0) call ave(xys, olst%order%int_ave(1), olst%order%int_ave(2))
            !xys%y => rawdata%raw(ch)%data
            call append_dset(retlst, xys)
            deallocate(rawdata)
        end do
    end subroutine

    subroutine pointtar(pt, tar)
        double precision, pointer :: pt(:)
        real(8), target :: tar(:)

        pt => tar
    end subroutine 

    subroutine get_chname(rawdata, chname, ret_list)
        type(heliac_data) :: rawdata
       ! logical, optional :: noabb = .false.
        character(80) line
        character(*) chname
        integer :: mode = 0
        integer shmin, shmax
        type(node), pointer :: str => null(),&
                              &hlist => null(),& 
                              &hash => null(),&
                              &ret_list
        hash => null()
        open(10, file=chtxtpath, status="old", err = 100)

        do 
            read(10, "(a)", end=999) line

            if (line == "##common ch num & name correspondence##") then
                mode = 1
                read(10, "(a)", end=999) line
            end if
            if (line == "##typing error##") mode = 2
            if (line == "") mode = 0
            !if (line == "##typing error of ch num & name correspondence") mode = 2

            call string(str, line)
            call strip(str)

            call split(str,hlist, ": ")
            !call show_list(hlist)
            if (mode == 1) then
                call append_hash_list(hash, hlist)
            else if (mode == 2) then
                mode = 3
                call append_hash_list(hash, hlist)
            else if (mode == 3) then
                if (shmin <= rawdata%shot .and. rawdata%shot <= shmax) call append_hash_list(hash, ret_list)
            end if
        hlist => null()
        end do
999     continue        
        call get_val(hash, chname, ret_list)
        close(10)
        return

        
        100 print *, chtxtpath, " is not found."
            stop
    end subroutine

    function chconv(rawdata, chname)
        type(heliac_data) :: rawdata
        type(node), pointer :: ret_str => null()
        character(20) long_chname
        character(*) , target :: chname
        integer i, chconv

        ret_str => null()
        call get_chname(rawdata, chname, ret_str)

        do i = 1, MAX_CH_NUM
            if (strchar(ret_str, trim(rawdata%raw(i)%title))) then
                chconv = i
                exit
            end if
        end do   
        call list_deallocate(ret_str)
    end function



    subroutine test_heliac_data_retrieve
        type(node), pointer :: olst => null(), retlst => null(), writelst => null()
        type(data_order) :: order
        character(10) shot, ch, itvl, awid
        integer shot_int,i
        real itvl_real, awid_real

        call list_init(olst)
        call list_init(retlst)
        call getarg(1, shot)
        call getarg(2, ch)
        read (shot, *) shot_int
        order%shot = shot_int
        order%chname = trim(ch)
        if (iargc() == 4) then
            call getarg(3, itvl)
            call getarg(4, awid)
            read (itvl, *) itvl_real
            read (awid, *) awid_real
        end if
        order%int_ave(1) = itvl_real
        order%int_ave(2) = awid_real
        call append_order(olst, order)

        call get_data(olst, retlst)
        call refer(retlst, 1)
        
        !print *,retlst%xys%x
        !print *,retlst%xys%y
        call append_arr(writelst, retlst%xys%x)
        call append_arr(writelst, retlst%xys%y)
        !call writedat("testdata.txt", writelst)
        call list_deallocate(olst)
        call list_deallocate(retlst)
       
    end subroutine

end module
