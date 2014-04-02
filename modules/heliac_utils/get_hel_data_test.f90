program main
    use tmp
    double precision, pointer :: x(:) => null(), y(:) => null()
    call get_hel_data(80000,1, x, y)
    print *,"aaa"
    print *,x,y
end program
