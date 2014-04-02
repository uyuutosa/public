def calc_mvelo(shot,itvl=0.01,wid=0.3,RAW=0, chs=["Is_mach1","Is_mach2"], calib=1.24 ,coff=43.711):
    from numpy import array
    
    calib_coff = coff
    
    xy1=calc3("complex",str(shot),channel(chs[0],str(shot)),itvl,wid,RAW=RAW)
    xy2=calc3("complex",str(shot),channel(chs[1],str(shot)),itvl,wid,RAW=RAW)
    MPCR_data=[xy1[0][0],((calib*xy1[0][1]-xy2[0][1])/(calib*xy1[0][1]+xy2[0][1]))*calib_coff]
    MPCR_tag=[xy1[1][0],r"$V_{\rm MP}\ \rm [km/s]$"]
    MPCR=[MPCR_data,MPCR_tag]
    return MPCR

def calc_Mp(shot,itvl=0.01,ave=0.1,RAW=0, reff=None, iota=None):
    from numpy import array, sqrt, pi
    start_time = 22
    end_time = 38
    
    mi = 1.67262e-27
    k = 1.380658e-23
    R = 0.58
    
    Theta = iota * reff / R#(2*pi*R)
    t, vp = calc_mvelo(shot, itvl, ave, RAW)[0]
    Te = calc_triple(shot,"te", itvl, ave, RAW)[0][1]
    
    
    #Since the number of list is different between "triple" and "complex", their is balanced.
    stnum = grep_num(start_time,t)
    ennum = grep_num(end_time,t)
    t = array(t[stnum:ennum])
    vp = array(vp[stnum:ennum])
    Te = array(Te[stnum:ennum])
    q=1.60217733e-19
    
    Mp = (vp*1e3) / (sqrt(0.2 * q * Te / (4*mi)) * Theta)
    input(Theta)
    input(sqrt(0.2 * q * 20 / (4*mi)))
     
    T_e = calc_triple(shot,"te", itvl, ave, RAW)[0][1]
    Mp_data=[t,Mp]
    Mp_tag=[r"$Time\ \rm{[ms]}$",r"$M_{\rm p}$"]
    ret=[Mp_data,Mp_tag]
    return ret
def calc_mach(shot,itvl=0.01,wid=0.3,RAW=0, chs = ["Is_mach1", "Is_mach2"], name=r"$R_{\rm Mach}$", calib=1.24, vmach=None, Z=2, ti=5, num=None, mvelo=1):
    from numpy import array, log, sqrt
    xy1=calc3("complex",str(shot),channel(chs[0],str(shot)),itvl,wid,RAW=RAW)
    xy2=calc3("complex",str(shot),channel(chs[1],str(shot)),itvl,wid,RAW=RAW)
    if vmach:
        mp = 1.672e-27
        c = 1.60217733e-19
        k = 1.38065e-23
        #coff = c / k
        te = calc_triple(str(shot),"te",itvl,wid,RAW=RAW)
        tmp = alignment([xy1[0], xy2[0], te[0]])
        te = [tmp[0], tmp[2]]
        #te[0][1]= .5
        ti = te[0][1] / 10
       # ti = 5
        MPCR_data=[xy1[0][0],1e-3*(c*(Z*te[0][1]+ti)/(4*sqrt(2*Z*mp*ti*c)))*log((calib*xy1[0][1])/(xy2[0][1])) * mvelo]
    else:
        MPCR_data=[xy1[0][0],((calib*xy1[0][1]-xy2[0][1])/(calib*xy1[0][1]+xy2[0][1])) * mvelo]
    #MPCR_tag=[xy1[1][0],r"$I_{\rm s1}-I_{\rm s2}/I_{\rm s1}+I_{\rm s2}$"]
    MPCR_tag=[xy1[1][0],name]
    MPCR=[MPCR_data,MPCR_tag]
    return MPCR

def specify_zeropoint(timelst, data_container):
    from modules.essential_utils.obj_util import pullout
    from numpy import mean

    [[x, y], [x_name, y_name]]  = data_container
    tmplst = []

    y_list = y.tolist()

    for t_min, t_max in timelst:
         tmplst += y_list[grep_series(t_min, x, x, True) : grep_series(t_max, x, x, True)]

    y -= mean(tmplst)
    
    return [[x, y], [x_name, y_name]]

def ave(datalst, itvl, wid):
    from numpy import array, mean
    from decimal import Decimal
    [[x,y],[xname, yname]] = datalst

    dt = (x[1] - x[0])
    intelm = int(Decimal(str(itvl / dt)))
    averange = int(Decimal(str(wid / (2 * dt))))

    x_ave = []
    y_ave = []

    l = len(x)
    n = 0
    while n < l:
        x_ave += [x[n]]
        elmin = n - averange
        elmax = n + averange
        if elmin < 0:
            elmin = 0
        if elmax > l:
            elmax = l-1
        y_ave  += [mean(y[elmin : elmax])]
        n += intelm
    return [[array(x_ave).round(3), array(y_ave)], [xname, yname]]

def spec(shot,itvl=0.01,ave=0.03,RAW=0,e667=881737.765546,e728=2003465.38034):
    from numpy import savetxt,transpose
    xy1=calc("he728",shot,itvl,ave,RAW)
    xy2=calc("he667",shot,itvl,ave,RAW)
    x=(667.8/728.1)*(1.8299/6.3705)*(e728/e667)*(xy2[0][1]/xy1[0][1])
    ne= 5.8118e+12 - 6.3082e+13 * x +2.6453e+14 * pow(x,2) - 5.7518e+14 * pow(x,3) +7.6283e+14 * pow(x,4) - 6.4752e+14 * pow(x,5) +3.5986e+14 * pow(x,6) - 1.3036e+14 * pow(x,7) +2.9691e+13 * pow(x,8) - 3.8683e+12 * pow(x,9) +2.2081e+11 * pow(x,10)
    
    xy=[[xy1[0][0],ne*1e-12],["Time [ms]","ne_spec [10^12 cm^-3]"]]
    
    return xy
def ele_pressure(shot,itvl=0.01,ave=0.03,RAW=0):
    
    xy_te = [calc_triple(str(shot),"te",itvl,ave,RAW=RAW)]
    xy_ne = [calc_triple(str(shot),"ne",itvl,ave,RAW=RAW)]
    
    xy = [["",""],["Time [ms]","neTe [a.u.]"]]
    xy[0][0] = xy_te[0][0][0]
    xy[0][1] = xy_te[0][0][1]*xy_ne[0][0][1]
    
    return xy

def i_pressure(shot,itvl=0.01,ave=0.03,RAW=0, Ti=2.5):
    
    xy_ne = [calc_triple(str(shot),"ne",itvl,ave,RAW=RAW)]
    
    xy = [["",""],["Time [ms]","neTi [a.u.]"]]
    xy[0][0] = xy_ne[0][0][0]
    xy[0][1] = Ti*xy_ne[0][0][1] 
    
    return xy

def e_pressure(shot,itvl=0.01,ave=0.03,RAW=0):
    
    xy_te = [calc_triple(str(shot),"te",itvl,ave,RAW=RAW)]
    xy_ne = [calc_triple(str(shot),"ne",itvl,ave,RAW=RAW)]
    
    xy = [["",""],["Time [ms]","neTe_2 [a.u.]"]]
    xy[0][0] = xy_te[0][0][0]
    xy[0][1] = xy_te[0][0][1]*xy_ne[0][0][1]
    
    return xy

def mvelo(shot,itvl=0.01,ave=0.02,RAW=0):
    from numpy import log, sqrt
    
    m_i = 1.67262e-27
    k = 1.380658e-23
    M_c = 1.0
    
    t, R = calc_mach(shot, itvl, ave, RAW)[0]
    T_e = calc_triple(shot,"te", itvl, ave, RAW)[0][1]
    V_p = [[t[:-1],sqrt(( m_i * T_e ) / m_i ) * M_c * log(R[:-1])],["Time [ms]", "V_p [m/s]"]]
    return V_p

def R_lab(shot,itvl=0.01,ave=0.03,RAW=0):
    
    xy_vlab = calc("vlab", str(shot), itvl, ave, RAW=RAW)
    xy_ilab = calc("ilab", str(shot), itvl, ave, RAW=RAW)
    
    xy = [["",""],["Time [ms]",r"$R_{\rm{LaB_6}}\ \rm{[\Omega]}$"]]
    xy[0][0] = xy_vlab[0][0]
    xy[0][1] = xy_vlab[0][1] / xy_ilab[0][1]
    
    return xy

def ne_ave(shot, itvl=0.01, ave=0.02, RAW=0, vpp = 1.4, line=139e-3, width=0.01, d_time=1):
    from numpy import array, where, append, arccos, pi, mean
    
    [[x, y], [x_name, y_name]] = calc("nel", shot, itvl, ave, RAW)
    
    #w_min, w_max, dy = window
    
    y_max = max(y)
    y_maxs = where((y >= (y_max - width)) == (y <= (y_max + width)))[0]
    revmax_t = x[y_maxs]

    y_min = min(y)
#    input(y_min)
#    input(y <= (y_min + width)) 
#    input(len(y <= (y_min + width))) 
#    input(len(y <= y_min)) 
    y_mins = where(y <= (y_min + width))[0]
    revmin_t = x[y_mins]

    vpp = (y_max - y_min) if vpp == 0 else vpp

#    input(mean(y[0:10]))
    rev = {"norev": 1, "rev": -1, "frev": -1, "2rev": 1}
    switch = "frev" if revmin_t[0] < revmax_t[0] else "norev"


    if switch == "norev":
        add = {"norev": arccos(1-2*mean(y[0:50])/vpp), "rev": - arccos(1-2*mean(y[0:50])/vpp)+2*pi,"frev": -arccos(1-2*mean(y[0:50])/vpp), "2rev": 2*pi-  arccos(1-2*mean(y[0:50])/vpp)}
    else:
        add = {"norev": -arccos(1-2*mean(y[0:50])/vpp), "rev": +arccos(1-2*mean(y[0:50])/vpp)+2*pi, "frev":  arccos(1-2*mean(y[0:50])/vpp), "2rev": 2*pi- ( - arccos(1-2*mean(y[0:50])/vpp))}

    if (len(revmin_t[where(revmin_t < revmax_t[0])[0]]) % 2) == 1:
        switch = "frev"
        

    dt = x[1] - x[0]

    dora = {"live":True, "dead":0}
    status = "live"

    ret_y = array([])
    for time, param in zip(x, y):
        if revmax_t[-1] == time:
            switch = "rev" 
        if dora[status] == True:
            if len(where(revmin_t == time)[0]):
                if switch == "rev":
                    switch = "2rev"
                elif switch == "norev":
                    switch = "frev"
                elif switch == "2rev":
                    switch = "rev"
                else:
                    switch = "norev"
                status = "dead"
            elif len(where(revmax_t == time)[0]):
                if switch == "rev":
                    switch = "norev"
                else:
                    switch = "rev"
                status = "dead"
        else:

            dora[status] += dt
            if str(dora[status]) == str(float(d_time)):
                print dora[status]
                print time
                dora[status] = 0 
                status = "live"
        stickout = 0
        if (param / vpp) >= 1:
            stickout = arccos(1 - 2 * (param / vpp - 1))
            param = 1 * vpp
        elif (param / vpp) <= 0:
            stickout = arccos(1 - 2 * (param / vpp + 1))
            param = -1 * vpp

        ret_y = append(ret_y, rev[switch] * arccos(1 - 2 * param / vpp) + add[switch] + stickout)
     

    ret_y = 5.91857991409e-2 * ret_y / line
    #print vpp, line, width, vpp
    #print  [[x, ret_y], ["Time [ms]", r"$\left< n_e \right>\ \rm [10^{12} cm^{-3}]$ "]]
    return [[x, ret_y], ["Time [ms]", r"$\left< n_e \right>\ \rm [10^{12} cm^{-3}]$ "]]














#print mvelo(80888)
def mag(shot, itvl=0.01, ave=0.03, RAW=0, offset=26):
    from numpy import array, mean

    [mag1xy, trash] = calc("mag+", str(shot), itvl, ave, RAW=RAW)
    [mag2xy, trash] = calc("mag-", str(shot), itvl, ave, RAW=RAW)
#a=loadtxt("test5.dat",comments="#", delimiter=",").transpose()
#b=loadtxt("test6.dat",comments="#", delimiter=",").transpose()
    #print mean(mag1xy[1][grep_series(1, mag1xy[0], mag1xy[1], number=True):grep_series(2, mag1xy[0], mag1xy[1], number=True)])
    #print mean(mag2xy[1][grep_series(1, mag1xy[0], mag2xy[1], number=True):grep_series(2, mag1xy[0], mag2xy[1], number=True)])
    
    mag1xy[1] -= mean(mag1xy[1][grep_series(1, mag1xy[0], mag1xy[1], number=True):grep_series(2, mag1xy[0], mag1xy[1], number=True)])
    mag2xy[1] -= mean(mag2xy[1][grep_series(1, mag2xy[0], mag2xy[1], number=True):grep_series(2, mag2xy[0], mag2xy[1], number=True)])

    c = mag1xy[1]-mag2xy[1]
#plot(a[0],c)
#input()
#close()

    dt = (mag1xy[0][1] - mag1xy[0][0]) * 1e-3
    g = 51
    S = 11.155e-6
    N = 30

    n=0
    V=[]
    tmp = c[0] * dt
    l = len(c)
    while n < l:
        V += [tmp + c[n]*dt]
        #print tmp
        tmp += c[n]*dt
        n += 1
    B = array(V) / (N * S * g)
    return specify_zeropoint([[28, 30]],[[mag1xy[0], array(B)], ["Time [ms]", "B [T]"]])

def calc_expr(xy, expr_y="", expr_x="", shot=80000, itvl=0.01, wid=0.01, RAW=1, vpp=None, line=None, width=None):
    from numpy import array
    try:
        ops_x = expr_x.split()
    except:
        ops_x = [" "]
        expr_x = ""

    try:
        ops_y = expr_y.split()
    except:
        ops_y = [" "]
        expr_y = ""
    paras = []
    n = 0
    linedic = {
                "line_x" : "xy[0][0] = xy[0][0]",
                "line_y" : "xy[0][1] = xy[0][1]"
                }
    tmp_shot = shot
    for ops,name in zip([ops_x, ops_y],["line_x","line_y"]):
        for op in ops:
            shot = tmp_shot
            try: 
                float(op)
                linedic[name] += op
            except ValueError:
                if len(op) != 1:
                    try:
                        tmp_shot = shot
                        op.index("_")
                        shot, op = op.split("_")
                    except ValueError:
                        pass
                    paras += [calc(op, str(shot), itvl, wid, RAW=RAW, vpp=vpp, line=line, width=width)[0]]
                    linedic[name] += "array(paras[%s])" %n
                    n += 1
                else:
                    linedic[name] += op
 
    aligns = [xy[0]]
    for para in paras:
        aligns += [para]
    paras = alignment(aligns)
    xy[0][0] = array(paras[0])
    xy[0][1] = array(paras[1])
    paras = paras[2:]
    for line in linedic.values():
        print line
        exec line
    xy[1][0] += expr_x
    xy[1][1] += expr_y
    xy = [[xy[0][0],xy[0][1]],[xy[1][0],xy[1][1]]]
    return xy


#print calc_expr(calc("pc",83002,int=0.1,ave=0.1,RAW=0),"+ 80000_pc","* 83032_pc", 83031, itvl=0.1,wid=0.1,RAW=0)
def calc_triple_wh(shot,chname=None,INTERVAL_TIME=0.01,AVERAGE_TIME=0.03,RAW=0):
    from subprocess import call,Popen,PIPE
    from os import environ
    from numpy import zeros
    avename=str(shot)+"_triple_INT"+str(INTERVAL_TIME)+"_AVE"+str(AVERAGE_TIME)+".dat"
    rawname=str(shot)+"_triple_RAW.dat"
    
    chdic={"te":1,"ne":2,"vf":3,"vs":4}

    ch=channel("Probe Current",str(shot))+","
    ch+=channel("Probe Bias",str(shot))+","
    ch+=channel("Vf-i-diamag",str(shot))+","
    ch+=channel("Vf-e-diamag",str(shot))
    #print ch
    if RAW == 0:
        NAME= environ["HOME"]+"/calc_data/"+avename
        if len(Popen(["ls",NAME],stdout=PIPE).stdout.read()) == 0:
            #p=Popen(["triple","-s",str(shot),"-c",ch, "-a"],stdin=PIPE,stdout=PIPE)
            p=Popen(["triple","-s",str(shot),"-c",ch],stdin=PIPE)
            #p=Popen(["triple","-s",str(shot),"-c",ch, "-an", "-o", "4,14", "-t", "20"],stdin=PIPE,stdout=PIPE)
            
            rmcmd=["rm",NAME]
            ans=["n\n","n\n","y\n","","",""]
            ans[3]=avename+"\n"
            ans[4]=str(INTERVAL_TIME)+"\n"
            ans[5]=str(AVERAGE_TIME)+"\n"                  
        
            for a in ans:    
                p.stdin.write(a)
                
            p.stdin.close()
            p.wait()
    else :
        NAME=environ["HOME"]+"/calc_data/"+rawname
        if len(Popen(["ls",NAME],stdout=PIPE).stdout.read()) == 0:
            p=Popen(["triple","-s",str(shot),"-c",ch], stdin=PIPE)#, "-a", "-o", "-49,-29"],stdin=PIPE,stdout=PIPE)
            #p=Popen(["triple","-s",str(shot),"-c",ch, "-a", "-o", "4,14", "-t", "20"],stdin=PIPE,stdout=PIPE)

            rmcmd=["rm",NAME]
            ans=["n\n","y\n","","n\n"]
            ans[2]=rawname+"\n"            
        
            for a in ans:    
                p.stdin.write(a)
                
            p.stdin.close()
            #p.stdout.close()
            p.wait()
    
    try:
        n_data=len(open(NAME,"rU").readlines())
    except:
        raise ValueError, "Data is not found."

    dlst=[]
    rfile=open(NAME)
    labels=rfile.readline()[:-2].split(",")
    collst=len(labels)
    for column in range(collst):
        dlst+=[zeros(n_data-1)]
    
    for line in range(n_data-1):
        a=rfile.readline()
        b=a[:-2].split(",")
        try:
            for column in range(collst): 
                dlst[column][line]=float(b[column])
        except ValueError:
            pass
    if type(chname) == str:
        dlst=[dlst[0],dlst[chdic[chname]]]
        labels=[labels[0],labels[chdic[chname]]]
        
    rfile.close()
    return dlst,labels
