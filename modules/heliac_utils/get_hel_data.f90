module mod_get_hel_data
    use heliac_data_loader
    implicit none 
    type xydata
        double precision :: xarr(20000)
        double precision :: yarr(20000)
    end type
contains

integer function get_hel_data(shot, ch, xys)
    type(xydata) :: xys
    integer shot, ch, ierr
    type(heliac_data), pointer :: rawdata 

    rawdata => null()
    print *,"aaa"
    allocate(rawdata)
    print *,"bbb"
    ierr = heliac_data_init(rawdata)
    ierr = open_file(rawdata, shot, .true.)
    ierr = heliac_param_load(rawdata)
    ierr = heliac_chdata_load(rawdata, ch)
    call channel_data_convert(rawdata%raw(ch))
    get_hel_data = size(rawdata%raw(ch)%time)
    xys%xarr = rawdata%raw(ch)%time
    xys%yarr = rawdata%raw(ch)%data
    print *, xys%yarr
    call close_file(rawdata)
end function
end module
