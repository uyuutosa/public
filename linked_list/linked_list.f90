module linked_list
    !use dataset, only : data_order, xydata

    implicit none
!    private
    public
    type xydata
        double precision, pointer :: x(:),&
                        &y(:)
                            
        double precision :: x_range(2),&
               &y_range(2)
        
        character :: x_name,&
                    &y_name
    end type
    type data_order
        integer shot
        double precision :: int_ave(2) = (/0,0/)
        double precision fmin, fmax, omin, omax
        character(20) chname
    end type

    type node
        type(data_order)  :: order 
        type(xydata), pointer :: xys => null()
        type(node), pointer :: next => null(),&
                              &pre  => null(),&
                              &init => null(),& 
                              &last => null(),&
                              &curr => null(),& 
                              &key => null(),& 
                              &val => null(),&
                              &lst => null(),&
                              &string => null(),&
                              &dtype => null()
        integer :: int
        integer, pointer :: intarr(:)
        double precision :: real
        double precision, pointer :: realarr(:)
        character(20) :: char
        character(20), pointer :: chararr(:)
        character(1) :: str
        logical :: point = .false.
        
        integer :: n = 1
    end type

    !public :: node, append, show_list, list_deallocate,list_init, refer
! interfaces----------------------------------------------------------
    interface append
        module procedure append_int, append_char, append_real
    end interface 

    interface append_arr
        module procedure append_intarr, append_chararr, append_realarr
    end interface 
! interfaces----------------------------------------------------------
contains
    subroutine dt_deallocate(dt)
        type(node), pointer :: dt
        integer i, n
        
        n = get_n(dt)
        do i = 1, n
            call refer(dt,i)
            if (i /= n) then
                dt => dt%next
                deallocate(dt%pre%dtype)
                deallocate(dt%pre)
            end if 
        end do
        deallocate(dt%dtype)
        deallocate(dt)
    end subroutine

    recursive subroutine renew_dtype(list, char)
        type(node), pointer :: list,&
                               &dt => null(),&
                               &tmpnode => null(),&
                               &init => null() 

        character(*) :: char
        integer i, n

        dt => list%dtype
        if (associated(dt)) call dt_deallocate(dt)
        allocate(dt)

        dt%init => dt
        dt%last => dt
        n = len(char)
        do i = 1, n
            dt%n = i
            dt%str = char(i:i)
            allocate(dt%dtype)
            dt%dtype%str = "!"
            dt%dtype%n = 1
            dt%dtype%init => dt%dtype
            dt%dtype%last => dt%dtype
            if (i /= n) then
                allocate(tmpnode)
                call node_joint(dt, tmpnode)
                tmpnode%init => dt%init
                tmpnode%init%last => tmpnode
                dt => tmpnode 
            end if
        end do
        list%dtype => dt%init
    end subroutine 
        
    recursive subroutine list_init(list)
        type(node), pointer :: list
        allocate(list)

        list%pre => list
        list%init => list
        list%last => list
        call renew_dtype(list, "none")

    end subroutine 

    subroutine refer(list, num)
        type(node), pointer :: list
        integer i, num
        
        list => list%init

        do i =  1, num - 1
            list => list%next
        end do
    end subroutine

    function get_n(list)
        type(node), pointer :: list
        integer get_n

        get_n =  list%init%last%n
    end function

    recursive subroutine puts_node(list, form, adv)
        type(node), pointer :: list
        character(len=*), optional :: form, adv
        integer i

        if (.not. present(form)) form = "(a)"
        if (.not. present(adv)) adv = "yes"

        if (strchar(list%dtype, "int")) write(*, fmt='(I5)', advance='no') list%int
        if (strchar(list%dtype, "intarr")) then 
            write(*, fmt='(a)', advance='no') "array( "
            do i = 1, size(list%intarr)
                write(*, fmt='(I5)', advance='no') list%intarr(i:i) 
                write(*, fmt='(a)', advance='no') ", "
            end do
            write(*, fmt='(a)', advance='no') " )"
        end if 
        if (strchar(list%dtype, "char")) write(*, fmt='(a)', advance='no') trim(list%char)
        if (strchar(list%dtype, "real")) write(*, fmt='(f10.5)', advance='no') list%real
        if (strchar(list%dtype, "realarr"))  then
            write(*, fmt='(a)', advance='no') "array( "
            do i = 1, size(list%realarr)
                write(*, fmt='(f10.5)', advance='no') list%realarr(i:i)
                write(*, fmt='(a)', advance='no') ", "
            end do
            write(*, fmt='(a)', advance='no') " )"
            !write(*, '(A,\)') " )"
        end if 
        if (strchar(list%dtype, "hash")) then
            call puts_node(list%key)
            write (*,fmt='(a)', advance='no') ":"
            call  puts_node(list%val)
        end if
        if (strchar(list%dtype, "str") .or. strchar(list%dtype, "!")) then
            do i = 1, get_n(list)
                call refer(list, i)
                write(*, fmt='(a)', advance='no') list%str
            end do
        end if
        if (strchar(list%dtype, "list")) call show_list(list%lst, adv="no")
        if (strchar(list%dtype, "string")) call show_list(list%string, adv="no")
    end subroutine

    recursive subroutine list_deallocate(list)
        type(node), pointer :: list
        integer n, i,t
        do
            n = list%init%last%n
            do i = 1, n
                call refer(list, i)
                if (associated(list%curr)) then
                    list => list%curr
                    exit
                end if
            end do
            if (i == n + 1) exit
        end do
        
        n = list%init%last%n
        call refer(list, 1)
        do i = 1, n
            if (strchar(list%dtype, "hash")) then
                if (associated(list%key)) then
                    !call show_list(list%key)
                    call refer(list%key,get_n(list%key))
                    list%key%curr => null()
                    call list_deallocate(list%key)
                    list%val%curr => null()
                    call list_deallocate(list%val)
                end if
            else if (strchar(list%dtype, "string")) then
                if (associated(list%string)) then
                    list%string%curr => null()
                    !print *, get_str(list%lst%dtype)
                    call list_deallocate(list%string)
                end if
            else if (strchar(list%dtype, "list")) then
                if (associated(list%lst)) then
                    call refer(list%lst,get_n(list%lst))
                    list%lst%curr => null()
                    !print *, get_str(list%lst%dtype)
                    call list_deallocate(list%lst)
                end if
            else if (strchar(list%dtype, "xydata")) then
                deallocate(list%xys%x)
                deallocate(list%xys%y)
                deallocate(list%xys)
            !else if (strchar(list%dtype, "order")) then
            !    deallocate(list%order)
            end if
            call dt_deallocate(list%dtype)
            if (i /= n) then
                list => list%next
                deallocate(list%pre)
            else
                deallocate(list)
            end if 
        end do
    end subroutine

    subroutine show_list(show_node, num, adv)
        type(node), pointer :: show_node
        integer, optional :: num
        character(*), optional :: adv
        character(3) inadv
        integer n, i
        
        if (.not. present(adv)) then
            inadv = "yes"
        else
            inadv = "no"
        end if

        n = show_node%init%last%n
        show_node => show_node%init
        write(*, fmt='(a)', advance='no') "[ "
        if (present(num)) then
            call refer(show_node, num)
            call puts_node(show_node, "a","no")
        else
            call refer(show_node, 1)
            call puts_node(show_node, "a","no")
            if (strchar(show_node%dtype, "str") .or. strchar(show_node%dtype, "!") ) then
                write(*, fmt='(a)', advance='no') " (string)]"
                return
            end if
            write(*, fmt='(a)', advance='no') ", "
            if (n /= 1) then
                do i= 1, n - 1 
                    show_node => show_node%next
                    call puts_node(show_node, "a","no")
                    if (i /= n-1) write(*, fmt='(a)', advance='no') ", "
                end do
            end if
        end if
        write(*, '(a)', advance=inadv) " ]"
    end subroutine

    function get_str(show_node)
        type(node), pointer :: show_node
        integer n, i
        character(100) :: get_str

        get_str = "" 
        n = show_node%init%last%n
        do i= 1, n 
            call refer(show_node, i)
            get_str(i:i) = show_node%str
        end do
        get_str = trim(get_str)
    end function
    subroutine show_str(show_node)
        type(node), pointer :: show_node
        integer n, i

 
        n = show_node%init%last%n
        call refer(show_node, 1)
        call puts_node(show_node, "a","no")
        if (n /= 1) then
            do i= 1, n - 1 
                show_node => show_node%next
                call puts_node(show_node, "a","no")
            end do
        end if
    end subroutine
    
    subroutine key_val(hash, delimiter)
        type(node), pointer :: hash
        character(len=*), optional :: delimiter
        integer n, i
        
        if (.not. present(delimiter)) delimiter =","
        n = get_n(hash)
        
        do i = 1, n
            call refer(hash, i)
            if (strchar(hash%dtype, "hash"))then
                print *, trim(hash%key%char), ":",trim(hash%val%char)

            end if 
        end do
    end subroutine

    subroutine get_keys(hash, ret_list)
        type(node), pointer :: hash, ret_list
        integer i, n
        
        n = get_n(hash)
        
        do i = 1, n
            call refer(hash, i)
            if (strchar(hash%dtype, "hash"))then
                call append_hash(ret_list, trim(hash%key%char), trim(hash%val%char))
            end if 
        end do
    end subroutine

    function get_val(hash, key)
        type(node), pointer :: hash
        character(*) key 
        character(100) :: get_val
        integer i, n


        n = get_n(hash)
        do i = 1, n 
            call refer(hash, i) 
            if (strchar(hash%dtype, "hash") .and. strchar(hash%key, trim(key))) then
                get_val = get_str(hash%val)
                get_val = trim(get_val)
!                call renew_dtype(ret_list, get_str(hash%val%dtype))
                exit
            end if
        end do
    end function
    subroutine get_val_tmp(hash, key, ret_list)
        type(node), pointer :: hash, ret_list
        character(*) key 
        integer i, n

        if (associated(ret_list)) ret_list => null()
        !if (.not. associated(ret_list)) call list_init(ret_list)

        n = get_n(hash)
        do i = 1, n 
            call refer(hash, i) 
            if (strchar(hash%dtype, "hash") .and. strchar(hash%key, trim(key))) then
                ret_list => hash%val
!                call renew_dtype(ret_list, get_str(hash%val%dtype))
                exit
            end if
        end do
    end subroutine

! string data handling****************************** 
!    function get_str(str)
!        type(node), pointer :: str
!        character, pointer :: get_str
!
!        allocate(get_str(get_n(str)))
!30      if (loop(str)) then
!            get_str = get_str//str%str
!            goto 30
!    end function

    subroutine string(list, line)
        type(node), pointer :: list
        character(*) :: line
        integer i
        if (associated(list)) list => null()
        !if (associated(list)) call list_deallocate(list) 

        do i = 1, len(line)
            call append_str(list, line(i:i))
        end do
    end subroutine

    subroutine copy_string(list, ret_list)
        type(node), pointer :: list, ret_list
        integer i

        ret_list => null()

        call refer(list, 1)
        do while(loop(list))
            call append_str(ret_list, list%str)
        end do
    end subroutine

    subroutine strip(list)
        type(node), pointer :: list,&
                              &fow => null(),&
                              &bak => null()

        integer i, n

        n = get_n(list)
        if (n == 1) return

        do i = 1, n
            call refer(list, i)
            if (list%str /= " " .and. .not. strchar(list%dtype, "blank") ) then
                if (i /= 1)call list_sep_del(list,i-1,"next")
                exit
            end if 
        end do

        call n_update(list)
        n = get_n(list)
        if (n == 1) return
        do i = n, 1, -1
            call refer(list, i)
            if (list%str /= " " .and. .not. strchar(list%dtype, "blank")) then
                if (i /= n) call list_sep_del(list,i,"pre")
                exit
            end if 
        end do
        call n_update(list)
    end subroutine

    subroutine list_sep_del(list, n, forb)
        type(node), pointer :: list,& 
                              &fow => null(),&
                              &bak => null()

        integer  n  
        character(*) forb

        call list_separate(list, fow, bak, n)

        if (forb == "pre") then
            list => fow
            call list_deallocate(bak)
        else
            list => bak
            call list_deallocate(fow)
        end if
    end subroutine

!    subroutine change_init(init, list)
!        type(node), pointer :: init, list 
!
!        list%init => list
!        list%init%last => init%last
!    end subroutine
!        
!    subroutine change_last(list, init)
!        type(node), pointer :: init, list 
!
!        init%last => list
!    end subroutine
    subroutine concatenate(fow, bak)
        type(node), pointer :: fow, bak
        integer :: n 
        
        bak%init%pre => fow%init%last
        fow%init%last%next => bak%init
        fow%init%last => bak%init%last

        call n_update(fow)
    end subroutine

    subroutine lrange(list, idx)
        type(node), pointer :: list, str
        character(*) idx 
        character(5) st_c, en_c, num
        integer i, st, en

        list => null()
        str => null()
        call string(str, idx)
        call split(str, " ")
        if (get_n(str) == 2) then
            call refer(str,1)
            st_c = get_str(str%lst)
            read(st_c, *) st
            call refer(str,2)
            en_c = get_str(str%lst)
            read(en_c, *) en
            do i = st, en
                call append_int(list, i)
            end do
        else
            do while(loop(str))
                num = get_str(str%lst)
                read(num, *) i
                call append_int(list, i)
            end do
        end if
        call list_deallocate(str)
    end subroutine

    subroutine list_nullify(list)
        type(node), pointer :: list
        call refer(list, 1)
        do while(loop(list))
            list%lst => null()
            call renew_dtype(list, "blank")
        end do
    end subroutine

    subroutine slice(list, idx, ret_list)
        type(node), pointer :: list,  idxlst, ret_list
        character(len=*), optional :: idx
        integer i

        idxlst => null()


        call lrange(idxlst, idx)

        call refer(idxlst, 1)
        do while(loop(idxlst))
            i = idxlst%int
            call refer(list, i)
            call append_bylist(ret_list, list)
        end do
        call list_deallocate(idxlst)
    end subroutine
    
    subroutine split(list, delimiter)
        type(node), pointer :: list, ret_list=>null(),&
                              &fow => null(),&
                              &bak => null(),&
                              &fow2 => null(),&
                              &bak2 => null(),&
                              &dellst => null()

        character(len=*), optional :: delimiter 
        integer :: del_len,  i, n = 1

        
        ret_list => null()
        if (.not. present(delimiter)) then
            call string(dellst, ",")
        else
            call string(dellst, delimiter)
        end if
        
        del_len = get_n(dellst)


        do i= 1, get_n(list)
            call refer(list, i)
            call refer(dellst, n)
            if (list%str == dellst%str) then
                if (n == del_len) then
                    call list_separate(list, fow, bak, i)
                    call list_separate(fow, fow2, bak2, i - del_len)
                    call strip(fow2)
                    call append_string(ret_list, trim(get_str(fow2)))
                    call insert_blank(bak, i, 1, "pre")
                    list => bak
                    call list_deallocate(bak2)
                    fow => null()
                    bak => null()
                    !fow2 => null()
                    bak2 => null()
                    !call list_deallocate(fow)
                    call list_deallocate(fow2)
                    n = 1
                else
                    n = n + 1
                end if 
            else
                n = 1
            end if    

        end do 
        call strip(list)
        call append_string(ret_list, trim(get_str(list)))
        call list_deallocate(dellst)
        call list_deallocate(list)
        list => ret_list
    end subroutine

    subroutine split_tmp(list, ret_list, delimiter)
        type(node), pointer :: list, ret_list,&
                              &fow => null(),&
                              &bak => null(),&
                              &fow2 => null(),&
                              &bak2 => null(),&
                              &dellst => null()

        character(len=*), optional :: delimiter 
        integer :: del_len,  i, n = 1

        
        ret_list => null()
        if (.not. present(delimiter)) then
            call string(dellst, ",")
        else
            call string(dellst, delimiter)
        end if
        
        del_len = get_n(dellst)


        do i= 1, get_n(list)
            call refer(list, i)
            call refer(dellst, n)
            if (list%str == dellst%str) then
                if (n == del_len) then
                    call list_separate(list, fow, bak, i)
                    call list_separate(fow, fow2, bak2, i - del_len)
                    call strip(fow2)
                    call append_string(ret_list, get_str(fow2))
                    call insert_blank(bak, i, 1, "pre")
                    list => bak
                    call list_deallocate(bak2)
                    fow => null()
                    bak => null()
                    fow2 => null()
                    bak2 => null()
                    !call list_deallocate(fow)
                    !call list_deallocate(fow2)
                    n = 1
                else
                    n = n + 1
                end if 
            else
                n = 1
            end if    

        end do 
        call strip(list)
        call append_string(ret_list, get_str(list))
        call list_deallocate(dellst)
    end subroutine

    subroutine list_separate(list, fow, bak, n)
        type(node), pointer :: list, fow, bak 
        integer :: n 

        
        call refer(list, n)
        
        fow => list
        bak => list%next
        fow%next => null()
        bak%pre => null()
        
        bak%init => bak
        bak%init%last => list%init%last
        fow%init%last => fow

        call n_update(fow)
        call n_update(bak)
    end subroutine

    subroutine insert_blank(list, b_num, n, forb)
        type(node), pointer :: list, inslst => null()
        integer b_num, i, n, n_last
        character(*) forb
        
        n_last = get_n(list)
        inslst => null()
        do i = 1, b_num
            call append_blank(inslst)
        end do

        call refer(list, n)
        
        if (forb == "pre") then
            if (n /= 1) then
                call node_joint(inslst%init%last, list)
                call node_joint(list, inslst%init)
            else
                call node_joint(inslst%init%last,list)
                inslst%init%last => list%init%last
                list => inslst%init
            end if
        else if (forb == "next") then
            if (n /= n_last) then
                call node_joint(inslst%init%last,list)
                call node_joint(list, inslst%init)
            else
                call node_joint(list, inslst%init)
                list%init%last => inslst%init%last
            end if
        else
            print *, "bad 'fob'. 'fob' is only possible to assign 'pre' or 'next'."
            stop
        end if
        call n_update(list)
    end subroutine

    subroutine node_joint(fow, bak)
        type(node), pointer :: fow, bak

        fow%next => bak
        bak%pre => fow
    end subroutine

    subroutine node_divide(fow, bak)
        type(node), pointer :: fow, bak

        fow%next => null()
        bak%pre => null()
    end subroutine

    subroutine n_update(list)
        type(node), pointer :: list, init => null()
        integer :: i = 1
        
        list%init%last%point = .true.
        list => list%init
        init => list
        i = 1 ! initial val is disabled... Why??
        do 
            list%n = i
            list%init => init
            i = i + 1
            if (list%point) then
                list%point = .false.
                 exit
            end if
            list => list%next
        end do

    end subroutine

    subroutine append_blank(curr_node)
        type(node), pointer :: curr_node, next_node => null()

        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "blank")
        else
            call list_init(next_node)
            call renew_dtype(next_node, "blank")
            call append_update(curr_node, next_node)
        end if
    end subroutine

    subroutine append_str(curr_node, param)
        character(*), intent(in) :: param
        type(node), pointer :: curr_node, next_node => null()

        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "str")
            curr_node%str = param
        else
            call list_init(next_node)
            call renew_dtype(next_node, "str")
            next_node%str = param
            call append_update(curr_node, next_node)
        end if
    end subroutine

    function match_str(str1, str2, nostrip)
        type(node), pointer :: str1, str2
        logical :: match_str
        logical, optional :: nostrip
        integer i, n

        if (.not. present(nostrip)) then
            call strip(str1)
            call strip(str2)
        end if
        !print *, "----------------"
        !call show_list(str1)
        !call show_list(str2)
        !print *, "----------------"
        
        n = get_n(str1)
        if (n /= get_n(str2)) then
            match_str = .false.
            return
        end if
        
        do i = 1, n
            call refer(str1, i)
            call refer(str2, i)
            if (str1%str /= str2%str) then
                match_str = .false.
                return
            end if
        end do
        match_str = .true.
    end function

    function strchar(str, char)
        type(node), pointer :: str
        character(*) char
        logical :: strchar 
        integer i, n

        n = get_n(str)
        if (n /= len(char)) then
            strchar = .false.
            return
        end if 
        
        do i = 1, n
            call refer(str, i)
            if (str%str /= char(i:i)) then
                strchar = .false.
                return
            end if
        end do
        strchar = .true.
    end function

    subroutine append_chararr(curr_node, param)
        character(*), target, intent(in) :: param(:)
        type(node), pointer :: curr_node, next_node => null()

        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "chararr")
            curr_node%chararr => param
        else
            call list_init(next_node)
            call renew_dtype(next_node, "chararr")
            next_node%chararr => param
            call append_update(curr_node, next_node)
        end if
    end subroutine

    subroutine append_intarr(curr_node, param)
        integer, target, intent(in) :: param(:)
        type(node), pointer :: curr_node, next_node => null()

        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "intarr")
            curr_node%intarr => param
        else
            call list_init(next_node)
            call renew_dtype(next_node, "intarr")
            next_node%intarr => param
            call append_update(curr_node, next_node)
        end if
    end subroutine
        
    subroutine append_realarr(curr_node, param)
        double precision, target, intent(in) :: param(:)
        type(node), pointer :: curr_node, next_node => null()

        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "realarr")
            curr_node%realarr => param
        else
            call list_init(next_node)
            call renew_dtype(next_node, "realarr")
            next_node%realarr => param
            call append_update(curr_node, next_node)
        end if
    end subroutine

    subroutine append_bylist(list, param)
        type(node), pointer :: list, param

        if (get_str(param%dtype) == "int") then
            call append_int(list, param%int)
        else if (get_str(param%dtype) == "real") then 
            call append_real(list, param%real)
        else if (get_str(param%dtype) == "list") then 
            call append_list(list, param%lst)
        else if (get_str(param%dtype) == "string") then 
            call append_string(list, trim(get_str(param%string)))
        else if (get_str(param%dtype) == "str") then 
            call append_string(list, trim(get_str(param)))
        end if
    end subroutine

    subroutine append_string(curr_node, param)
        type(node), pointer :: curr_node, str,&
                              &next_node => null()
        character(*) :: param
        integer i
        !if (associated(list)) list => null()
        !if (associated(tmplist)) tmplist => null()
        !if (associated(list)) call list_deallocate(list) 

        str => null()
        call string(str, param)

        !call show_list(str, 1)

        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "string")
            curr_node%string => str
            str%curr => curr_node
        else
            call list_init(next_node)
            call renew_dtype(next_node, "string")
            next_node%string => str
            str%curr => next_node
            call append_update(curr_node, next_node)
        end if
    end subroutine

    integer function append_list_txt(curr_node, path, delim)
        character(len=*) path, delim
        character(100) line
        type(node), pointer :: curr_node ,str
        integer ierr

        if (.not. associated(curr_node)) call list_init(curr_node)

        open(55, file=path, status='old', iostat=ierr, err=501)
        do
            str => null()
            read(55, fmt='(a)', err=501, end=501) line
            call string(str, trim(line))
            if (line(1:1) == "#") cycle
            call split(str, delim)
            call append_list(curr_node, str)
        end do

501     close(55) 
        append_list_txt = ierr
    end function
    
    subroutine append_list(curr_node, param)
        type(node), pointer :: curr_node, param,&
                              &next_node => null()


        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "list")
            curr_node%lst => param
            param%curr => curr_node
        else
            call list_init(next_node)
            call renew_dtype(next_node, "list")
            next_node%lst => param
            param%curr => next_node
            call append_update(curr_node, next_node)
        end if
    end subroutine
        
! string data handling****************************** 
! hash data handling******************************** 
    subroutine append_hash(curr_node, key, val)
        character(len=*) key, val
        type(node), pointer :: curr_node,&
                              &key_node => null(),&
                              &val_node => null(),&
                              &next_node => null() 

        if (.not. associated(curr_node)) call list_init(curr_node)
        call string(key_node, key) 
        call string(val_node, val)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "hash")
            curr_node%key => key_node
            key_node%curr => curr_node
            curr_node%val => val_node 
            val_node%curr => curr_node
        else
            call list_init(next_node)
            call renew_dtype(next_node, "hash")
            next_node%key => key_node
            key_node%curr => next_node
            next_node%val => val_node
            val_node%curr => next_node
            call append_update(curr_node, next_node)
        end if
    end subroutine

    integer function append_hash_txt(curr_node, path, delim)
        character(len=*) path, delim
        character(100) line
        type(node), pointer :: curr_node ,str,&
                              &key,&
                              &val
        integer ierr

        key => null()
        val => null()

        if (.not. associated(curr_node)) call list_init(curr_node)

        open(55, file=path, status='old', iostat=ierr, err=500)
        do
            str => null()
            read(55, fmt='(a)', err=500, end=500) line
            call string(str, trim(line))
            call split(str, delim)
            call refer(str, 1)
            key => str
            call refer(str, 2)
            val => str
            call append_hash(curr_node, trim(get_str(key%string)), trim(get_str(val%string)))
            call list_deallocate(str)
        end do

500     close(55) 
        append_hash_txt = ierr
    end function    

    subroutine append_hash_list(curr_node, list)
        type(node), pointer :: curr_node,&
                              &key_node => null(),&
                              &val_node => null(),&
                              &next_node => null(),&
                              &list 

        if (.not. associated(curr_node)) call list_init(curr_node)
        !call show_list(curr_node%dtype)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "hash")
            call refer(list, 1)
            key_node => list
            curr_node%key => list%lst
            list%lst%curr => curr_node
            list%lst => null()
            call refer(list, 2)
            val_node => list
            curr_node%val => list%lst
            list%lst%curr => curr_node
            list%lst => null()
        else
            call list_init(next_node)
            call renew_dtype(next_node, "hash")
            call refer(list, 1)
            key_node => list
            next_node%key => list%lst
            list%lst%curr => next_node
            list%lst => null()
            call refer(list, 2)
            val_node => list
            next_node%val => list%lst
            list%lst%curr => next_node
            list%lst => null()
            call append_update(curr_node, next_node)
        end if
        !call list_separate(list, key_node, val_node, 1)
        call list_deallocate(list)
    end subroutine
! hash data handling******************************** 

! append subroutines******************************** 
    subroutine append_int(curr_node, param)
        integer, intent(in) :: param
        type(node), pointer :: curr_node, next_node => null()
        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "int")
            curr_node%int = param
        else
            call list_init(next_node)
            call renew_dtype(next_node, "int")
            next_node%int = param
            call append_update(curr_node, next_node)
        end if
    end subroutine

    subroutine append_char(curr_node, param)
        character(len=*), intent(in) :: param
        type(node), pointer :: curr_node, next_node => null()

        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "char")
            curr_node%char = param
        else
            call list_init(next_node)
            call renew_dtype(next_node, "char")
            next_node%char = param
            call append_update(curr_node, next_node)
        end if
    end subroutine

    subroutine append_real(curr_node, param)
        double precision, intent(in) :: param
        type(node), pointer :: curr_node, next_node => null()

        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "real")
            curr_node%real = param
        else
            call list_init(next_node)
            call renew_dtype(next_node, "real")
            next_node%real = param
            call append_update(curr_node, next_node)
        end if
    end subroutine
! append subroutines******************************** 
    subroutine append_update(curr_node, next_node)
        type(node), pointer :: curr_node, next_node

            next_node%init => curr_node%init
            curr_node%init%last => next_node
            next_node%n = curr_node%n + 1
            call node_joint(curr_node, next_node)
            curr_node => next_node
    end subroutine

! unit test area********************************** 
    subroutine test_linked_list()
        type(node), pointer :: list => null(),&
                              &list2 => null(),&
                              &list3 => null(),&
                              &str => null()
        integer :: intarr(2) = 10
        character(3) :: chaarr(3) = "dddd" 
        print *, "Unit test for linked list module. "
        print *, "This module provids useful list structure."
        print *, "List have variable number of the 'node',"
        print *, "which is minimum unit of list, is"
        print *, "which is extracted, added"
        print *, "removed and so on from a list."
        print *, ""
        print *, "1. New node add to list."
        print *, ""
        print *, "call append(list, 33)"
        print *, ""
        call append(list, 33)
        print *, "2. List supports some types, int, double, string, array..."
        print *, ""
        print *, "call append(list, 1)"
        print *, "call append(list, 3.14)"
        print *, "call append_arr(list, intarr) !integer :: intarr(5) = 10"
        print *, "call string(str, 'hello')"
        print *, "call append_list(list, str)"
        print *, ""
        call append(list, 1)
        call append_arr(list, intarr)
        call string(str, "hello")
        call append_list(list, str)
        print *, "3. Nested list is  supported."
        print *, ""
        print *, "call append_list(list, list2)"
        print *, ""
        call append(list2, 10)
        call append_list(list, list2)
        print *, "4. Associative array is also suported"
        print *, ""
        print *, "call append_hash(list, 'hei', 'ho')"
        print *, ""
        call append_hash(list, "hei", "ho")
        print *, "5. The contents of list is able to view as follows."
        print *, ""
        print *, "call show_list(list)"
        print *, ""
        print *, "list = "
        call show_list(list)
        print *, ""
        print *, "6. Iteration is easy. function loop is supported."
        print *, ""
        print *, "do while(loop(list))"
        print *, "    call append(list3, list3%n)"
        print *, "end do "
        print *, ""
        do while(loop(list))
            call append(list3, list%n)
        end do 
        print *, "list3 = "
        call show_list(list3)
        print *, ""
        print *, "7.List is not deallocated automatically." 
        print *, "Deallocation is needed. 'list_deallocate' "
        print *, "deallocats all nodes recursively."
        print *, ""
        print *, "call list_deallocate(list)"
        print *, "call list_deallocate(list3)"
        print *, ""
        call list_deallocate(list)
        call list_deallocate(list3)
        print *, "Deallocation is done. If any error is not occur,"
        print *, "this unit test is successful."
    end subroutine

!utility functions ---------------------------------------- 
    subroutine append_order(curr_node, param)
        type(data_order) :: param
        type(node), pointer :: curr_node, next_node => null()
        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "order")
            curr_node%order = param
        else
            call list_init(next_node)
            call renew_dtype(next_node, "order")
            next_node%order = param
            call append_update(curr_node, next_node)
        end if
    end subroutine
    subroutine append_dset(curr_node, param)
        type(xydata), pointer :: param
        type(node), pointer :: curr_node, next_node => null()
        if (.not. associated(curr_node)) call list_init(curr_node)
        if (strchar(curr_node%dtype, "none")) then
            call renew_dtype(curr_node, "xydata")
            curr_node%xys => param
        else
            call list_init(next_node)
            call renew_dtype(next_node, "xydata")
            next_node%xys => param
            call append_update(curr_node, next_node)
        end if
    end subroutine

    function loop(list)
        type(node), pointer :: list
        logical loop

        if (.not.list%init%point) then
            call refer(list, 1)
            call move_point(list)
            if (list%n == 1) list%point = .True.
        else
            list%init%point = .False.
        end if

        if (list%point) then
            loop = .True.
            list%point = .False.
            if (associated(list%next)) then
                list%next%point = .True.
            else 
                list%init%point = .True.
            end if
            
        else
            loop = .False.
        end if
    end function

    subroutine move_point(list)
        type(node), pointer :: list
        integer i, n

        n = list%n
        do i = 1, get_n(list)
            call refer(list, i)
            if (list%point) return
        end do
        call refer(list, n)
    end subroutine

    subroutine arr_conv(list, retarr)
        type(node), pointer :: list
        double precision :: retarr(:)
        integer i, n

        n = get_n(list)

        do i = 1, n
            call refer(list, i)
            retarr(i) = list%real
        end do
    end subroutine

    function sum_list_real(list)
        type(node), pointer :: list
        double precision :: sum_list_real 
        integer i, n

        n = get_n(list)
        sum_list_real = 0
        do i = 1, n
            call refer(list, i)
            sum_list_real = sum_list_real + list%real
        end do
    end function

    function mean_list_real(list)
        type(node), pointer :: list
        double precision :: mean_list_real
        integer i, n

        n = get_n(list)
        mean_list_real = 0
        do i = 1, n
            call refer(list, i)
            mean_list_real = mean_list_real + list%real
        end do

        mean_list_real = mean_list_real / n
    end function

    function std_list_real(list)
        type(node), pointer :: list
        double precision :: std_list_real, mval
        integer i, n

        n = get_n(list)
        std_list_real = 0
        mval = mean_list_real(list)
        do i = 1, n
            call refer(list, i)
            std_list_real = std_list_real + (list%real - mval) ** 2
        end do
        std_list_real = (std_list_real / n) ** 0.5 
    end function

    subroutine mul_list_real(alst, blst, retlst)
        type(node), pointer :: alst, blst
        type(node), pointer :: retlst
        integer i

        retlst => null()
        do i = 1, get_n(alst)
            call refer(alst, i)            
            call refer(blst, i)            
            call append_real(retlst, alst%real * blst%real)
        end do
    end subroutine

    function grad_list_real(xlist, ylist)
        type(node), pointer :: xlist, ylist
        type(node), pointer :: xxlist, xylist
        double precision :: grad_list_real
        double precision :: sumx, sumy, sumxx, sumxy
        integer n

        xxlist => null()
        xylist => null()

        n = get_n(xlist)
        sumx = sum_list_real(xlist)
        sumy = sum_list_real(ylist)
        call mul_list_real(xlist, xlist, xxlist)
        sumxx = sum_list_real(xxlist)
        call mul_list_real(xlist, ylist, xylist)
        sumxy = sum_list_real(xylist)
        grad_list_real = ((n * sumxy) - sumx * sumy) / (n * sumxx - sumx ** 2)
    end function

    subroutine pullout(arr, logarr, retlst)
        type(node), pointer :: retlst
        double precision :: arr(:)
        logical :: logarr(:)
        integer i, n
        
        n = size(arr)
        do i = 1, n
            if (logarr(i)) then
                call append_real(retlst, arr(i))
            end if
        end do
    end subroutine
end module
