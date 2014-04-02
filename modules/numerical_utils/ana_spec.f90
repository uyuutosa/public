subroutine autocorr(st_n, x, y, n, retx, rety, ret_n)
    implicit none
    integer :: st_n
    double precision :: x(n), y(n)
    integer i, n, ret_n, ret_len
    double precision :: retx(ret_n), rety(ret_n)
    double precision dx
    
    ret_len = size(x) - 2 * ret_n
    dx = x(2) - x(1)
    do i = 1 + st_n, ret_n + st_n
        retx(i-st_n) = dx * (i - 1)
        rety(i-st_n) = sum(y(ret_n+1+(i-1):n-(ret_n-(i-1))) * y(ret_n+1:n-ret_n)) / ret_len
        rety(i-st_n) = rety(i - st_n) / (sum(y(ret_n+1:n-ret_n)**2)/ ret_len)
    end do
end subroutine

subroutine crosscorr(st_n, x1, y1, y2, n, retx, rety, ret_n)
    implicit none
    integer :: st_n
    double precision:: x1(n), y1(n), y2(n)
    integer i, n, ret_n, ret_len
    double precision :: retx(ret_n), rety(ret_n)
    double precision :: dx

    ret_len = size(x1) - 2 * ret_n
    dx = x1(2) - x1(1)
    do i = 1 + st_n, ret_n + st_n
        retx(i-st_n) = dx * (i - 1)
        rety(i-st_n) = sum(y1(ret_n + 1 + (i - 1) : n - (ret_n - (i-1))) * y2(ret_n + 1 : n - ret_n)) / ret_len
        rety(i-st_n) = rety(i-st_n) / ((sum(y1(ret_n + 1 : n - ret_n) ** 2) / ret_len) ** 0.5)
        rety(i-st_n) = rety(i-st_n) / ((sum(y2(ret_n + 1 : n - ret_n) ** 2)/ ret_len) ** 0.5)
    end do
end subroutine

subroutine run_crosscorr(st_n, x1, y1, y2, n, wid_n, retx, rety, retlag, ret_row_n, ret_col_n)
    implicit none
    integer  st_n, wid_n
    double precision:: x1(n), y1(n), y2(n)
    integer i, j, n, ret_row_n, ret_col_n, ret_len
    double precision :: retx(ret_col_n, ret_row_n), rety(ret_col_n, ret_row_n), retlag(ret_col_n, ret_row_n)
    !double precision :: retx(col_n-2*ret_n, ret_n), rety(col_n-2*ret_n, ret_n), retlag(col_n-2*ret_n, ret_n)
    double precision dx

    ret_len = size(x1) - 2 * ret_row_n
    dx = x1(2) - x1(1)
    do j = 1, ret_row_n
        call samenum(dx * (i - 1), ret_col_n, retlag(:,i-st_n))
        do i = 1 + st_n, wid_n + st_n
            call crosscorr(st_n, x1(j, j + wid_n), y1(j, j + wid_n), y2(j, j + wid_n), wid_n, ret_x(:, j), ret_y(:, j), ret_col_n)
            !retx(i-st_n, j) = dx * (i - 1)
            !rety(i-st_n, j) = sum(j + y1(ret_row_n + 1 + (i - 1) : j + wid_n - (ret_row_n - (i-1))) * y2(j + ret_row_n + 1 : j + wid_n - ret_row_n)) / ret_len
            !!rety(i-st_n, j) = sum(y1(ret_row_n + 1 + (i - 1) : n - (ret_row_n - (i-1))) * y2(ret_row_n + 1 : n - ret_row_n)) / ret_len
            !rety(i-st_n, j) = rety(i-st_n, j) / ((sum(y1(j + ret_row_n + 1 : j + wid_n - ret_row_n) ** 2) / ret_len) ** 0.5)
            !rety(i-st_n, j) = rety(i-st_n, j) / ((sum(y2(j + ret_row_n + 1 : j + wid_n - ret_row_n) ** 2)/ ret_len) ** 0.5)
        end do
    end do
end subroutine

subroutine crosscorr_func(st_n, x1, y1, y2, n, retx, rety, retlag, ret_row_n, ret_col_n)
    implicit none
    integer  st_n
    double precision:: x1(n), y1(n), y2(n)
    integer i, n, ret_row_n, ret_col_n
    double precision :: retx(ret_col_n, ret_row_n), rety(ret_col_n, ret_row_n), retlag(ret_col_n, ret_row_n)
    !double precision :: retx(col_n-2*ret_n, ret_n), rety(col_n-2*ret_n, ret_n), retlag(col_n-2*ret_n, ret_n)
    double precision dx

    dx = x1(2) - x1(1)
    do i = 1 + st_n, ret_row_n + st_n
        retx(:,i-st_n) = x1(ret_row_n + 1 : n - ret_row_n)
        rety(:,i-st_n) = y1(ret_row_n + 1 + (i - 1) : n - (ret_row_n - (i-1))) * y2(ret_row_n + 1 : n - ret_row_n)
        !rety(:,i-st_n) = rety(:,i-st_n) / (y1(ret_row_n + 1 : n - ret_row_n) ** 2) ** 0.5
        !rety(:,i-st_n) = rety(:,i-st_n) / (y2(ret_row_n + 1 : n - ret_row_n) ** 2) ** 0.5
        !call samenum(dx * (i - 1), retlag(:,i-st_n))
        call samenum(dx * (i - 1), ret_col_n, retlag(:,i-st_n))
    end do
end subroutine

subroutine samenum(val, num, retarr)
    implicit none
    double precision val
    integer num, cnt
    double precision :: retarr(num)

    !num = size(retarr)
    do cnt = 1, num
        retarr(cnt) = val
    end do
end subroutine 
