def outline():
    xi = 0.05
    yi = 0 
    dx = obj.x.ptp() * 1e-1
    dy = obj.y.ptp() * 1e-1
    s_dx = ini_s_dx = obj.x.ptp() * 1e-1
    s_dy =ini_s_dy =obj.y.ptp() * 1e-1
    sxlim = [obj.x.min()/1.1,obj.x.max()*1.1,dx]
    sylim = [obj.y.min()/1.1,obj.y.max()*1.1,dy]
    xlst = []
    ylst = []
    n =0
    s_old = 0
    ratio = 1
    #search initial coordinate
    b = False
    for xi in arange(*sxlim):
        for yi in arange(*sylim):
            tof1 = obj.slice_arr([xi - (s_dx*ratio)/2, xi + (s_dx*ratio)/2])
            if tof1: 
                tof2 = obj.slice.slice_arr([yi - (s_dy*ratio)/2, yi + (s_dy*ratio)/2],1)
    
            if tof1 and tof2:
                b = True
                break
        if b: break
        
#
    cond = 3
    retsign = False
    add_x = 0
    add_y = 0
    tof = False
    xi_ini = xi
    input(xi_ini)
    yi_ini = yi
    cnt = 0
    while True:
        #print back_arr
        #input((xi,yi))
        tof1=tof2=False
        #input([xi - (s_dx*ratio)/2, xi + (s_dx*ratio)/2])
        if cnt >= 10 and (xi - (ini_s_dx)/2 <= xi_ini and xi_ini <= xi + (ini_s_dx)/2) and(yi - (ini_s_dy)/2 <= yi_ini and yi_ini <= yi + (ini_s_dy)/2):
            print "break"   
            break
        tof1 = obj.slice_arr([xi - (s_dx)/2, xi + (s_dx)/2])
        if tof1: tof2 = obj.slice.slice_arr([yi - (s_dy)/2, yi + (s_dy)/2],1)
        #input((tof1,tof2))
        if tof1 and tof2 and not retsign:
            cnt += 1
            r = obj.slice.slice
            #input(r.x)
            r.gradient(1)
            a = r.grad
            #s = int(arctan(a) / (pi / 2)  * M )
            #if abs(s - s_old) > s_c:
             #   dx *= -1

            r.average()
            #print obj.xmean,obj.ymean
            #print xi,yi,0
            xlst += [r.xmean]
            ylst += [r.ymean]
            #print yi,obj.ymean
            #print "helo"
            #input((xi, yi))
            back = (cond+4)%8
            back2 = (cond + 1+4)%8
            back3 = (cond  - 1  +4)%8
            back4 = (cond  + 2  +4)%8
            back5 = (cond  - 2  +4)%8
            back_arr = array([back,back2,back3,back4, back5])
            #back_arr = array([back,back2,back3])
            add_x = 0
            add_y = 0
            #print back_arr
            #print cond
            
            s_dx = ini_s_dx
            s_dy = ini_s_dy

        else:
            ratio = 1.001 + dx
            s_dx *= ratio
            s_dy *= ratio
        #print s_dx
        #input((xi, yi))
        #print retsign, cond
        xi -= add_x
        yi -= add_y
        #print xi,add_x,add_y,cond,dx
        cond = (cond+1)%8
        retsign = False
       # input(back_arr)
        if cond == 0 and (cond != back_arr).all():
            add_x = -dx
            add_y = 0
        elif cond == 1 and (cond != back_arr).all():
            add_x = -dx
            add_y = -dy

        elif cond == 2 and (cond != back_arr).all():
            add_x = 0
            add_y = -dy
        elif cond == 3 and (cond != back_arr).all():
            add_x = dx
            add_y = -dy
        elif cond == 4 and (cond != back_arr).all():
            add_x = dx
            add_y = 0
        elif cond == 5 and (cond != back_arr).all():
            add_x = dx
            add_y = dy
        elif cond == 6 and (cond != back_arr).all():
            add_x = 0
            add_y = dy
        elif cond == 7 and (cond != back_arr).all():
            add_x = -dx
            add_y = dy      
        elif back:
            #print "adsf"
            #print cond,back
            add_x = 0
            add_y = 0
            retsign = True
            #raise ValueError, "Can not data finded."
        
        xi += add_x
        yi += add_y
        n += 1
        #print xi, yi

        print n 
        if n == 1000:
            break
d = handle_3d(xlst, ylst)
d.view()
