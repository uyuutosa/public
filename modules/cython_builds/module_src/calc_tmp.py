#self.calc.py V1.0
#from heliacdatmanage import triple_manage

import heliacdatmanage as hel
from numpy import *
def calc_old(calc_cmd,shot,ch,dataFname,INTERVAL_TIME,AVERAGE_TIME,RAWorAVE):
    from subprocess import call,Popen,PIPE
    from os import environ
    
    DATAFNAME=environ["HOME"]+"/calc_data/"+dataFname
    rmcmd=["rm",DATAFNAME]
    call(rmcmd)
    cmd=[calc_cmd]
    p=Popen([calc_cmd,"-s",shot,"-c",ch],stdin=PIPE,stdout=PIPE)
    
    if RAWorAVE==0:
        ans=["n\n","n\n","y\n","","",""]
        ans[3]=dataFname+"\n"
        ans[4]=INTERVAL_TIME+"\n"
        ans[5]=AVERAGE_TIME+"\n"            
                
    else:
        ans=["n\n","y\n","","n\n"]
        ans[2]=dataFname+"\n"            

    for a in ans:    
        p.stdin.write(a)
        
    p.stdin.close()
    p.stdout.close()
    p.wait()
    
    return DATAFNAME

def calc2(calc_cmd,shot,ch,dataFname,INTERVAL_TIME,AVERAGE_TIME,RAWorAVE):
    from subprocess import call,Popen,PIPE
    from os import environ
    from numpy import zeros
    DATAFNAME=environ["HOME"]+"/calc_data/"+dataFname
    rmcmd=["rm",DATAFNAME]
    call(rmcmd)
    cmd=[calc_cmd]
    p=Popen([calc_cmd,"-s",shot,"-c",ch],stdin=PIPE,stdout=PIPE)
    
    if RAWorAVE==0:
        ans=["n\n","n\n","y\n","","",""]
        ans[3]=dataFname+"\n"
        ans[4]=INTERVAL_TIME+"\n"
        ans[5]=AVERAGE_TIME+"\n"            
                
    else:
        ans=["n\n","y\n","","n\n"]
        ans[2]=dataFname+"\n"            

    for a in ans:    
        p.stdin.write(a)
        
    p.stdin.close()
    p.stdout.close()
    p.wait()
    
    n_data=len(open(DATAFNAME,"rU").readlines())
    xx=zeros(n_data-1)
    yy=zeros(n_data-1)
    rfile=open(DATAFNAME)
    rfile.readline()
    for line in range(n_data-1):
        a=rfile.readline()
        b=a.split(",")
        xx[line]=float(b[0])
        yy[line]=float(b[1])
        
    rfile.close()
    return [xx,yy]

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

def specify_zeropoint(timelst, data_container):
    from useful import grep_series
    from numpy import mean

    [[x, y], [x_name, y_name]]  = data_container
    tmplst = []

    y_list = y.tolist()

    for t_min, t_max in timelst:
         tmplst += y_list[grep_series(t_min, x, x, True) : grep_series(t_max, x, x, True)]

    y -= mean(tmplst)
    
    return [[x, y], [x_name, y_name]]

def calc3(calc_cmd,shot,ch,INTERVAL_TIME=0.05,AVERAGE_TIME=0.5,RAW=0):
    from subprocess import call,Popen,PIPE
    from os import environ
    from numpy import zeros
    avename=shot+"_"+ch+"_INT_"+str(INTERVAL_TIME)+"_AVE_"+str(AVERAGE_TIME)+".dat"
    rawname=shot+"_"+ch+"_RAW.dat"
#####################################    
    if RAW == 0:
        NAME= environ["HOME"]+"/calc_data/"+avename
        if len(Popen(["ls",environ["HOME"]+"/calc_data/"+avename],stdout=PIPE).stdout.read()) == 0:
            #p=Popen([calc_cmd,"-s",shot,"-c",ch, "-a"],stdin=PIPE,stdout=PIPE,stderr=PIPE)
            p=Popen([calc_cmd,"-s",shot,"-c",ch, "-a", "-o","3.5,14.5"],stdin=PIPE,stdout=PIPE,stderr=PIPE)
            #p=Popen([calc_cmd,"-s",shot,"-c",ch, "-a", "-o","4,14"],stdin=PIPE,stdout=PIPE,stderr=PIPE)
            #p=Popen([calc_cmd,"-s",shot,"-c",ch, "-a", "-o","-49,-29"],stdin=PIPE,stdout=PIPE,stderr=PIPE)
        
            if RAW==0:
                rmcmd=["rm",NAME]
                ans=["n\n","n\n","y\n","","",""]
                ans[3]=avename+"\n"
                ans[4]=str(INTERVAL_TIME)+"\n"
                ans[5]=str(AVERAGE_TIME)+"\n" 
                
            for a in ans:    
                p.stdin.write(a)  
            p.stdin.close()
            p.stdout.close()
            p.stderr.close()
            p.wait()        
#####################################    

    else: 
        NAME= environ["HOME"]+"/calc_data/"+rawname
        if len(Popen(["ls",environ["HOME"]+"/calc_data/"+rawname],stdout=PIPE).stdout.read()) == 0:
            p=Popen([calc_cmd,"-s",shot,"-c",ch, "-a","-o","3.5,13.5"],stdin=PIPE,stdout=PIPE,stderr=PIPE)
            #p=Popen([calc_cmd,"-s",shot,"-c",ch, "-a","-o","-49,-29"],stdin=PIPE,stdout=PIPE,stderr=PIPE)
        
            NAME=environ["HOME"]+"/calc_data/"+rawname
            rmcmd=["rm",NAME]
            ans=["n\n","y\n","","n\n"]
            ans[2]=rawname+"\n"            
        
            for a in ans:    
                p.stdin.write(a)
                
            p.stdin.close()
            p.stdout.close()
            p.stderr.close()
            p.wait()
            
    n_data=len(open(NAME,"rU").readlines())
    dlst=[]
    rfile=open(NAME)
    labels=rfile.readline().split(",")[:-1]
    collst=len(labels)
    for column in range(collst):
        dlst+=[zeros(n_data-1)]
    
    for line in range(n_data-1):
        a=rfile.readline()
        b=a.split(",")[:-1]
        try:
            for column in range(collst): 
                dlst[column][line]=float(b[column])
        except ValueError:
            pass         
        
    rfile.close()
    ret = [dlst, labels]
    #if RAW == 0:
    #    ret = ave([dlst, labels], INTERVAL_TIME, widRAGE_TIME)
        
    return ret

def calc_mach(shot,itvl=0.01,wid=0.3,RAW=0, chs = ["Is_mach1", "Is_mach2"], name=r"$R_{\rm Mach}$", calib=1.24, vmach=None, Z=2, ti=5, num=None, mvelo=1):
    from calc import calc3
    from useful import channel,alignment
    from numpy import array, log, sqrt
    #if num == None:
    #    xy1=calc3("complex",str(shot),channel(chs[0],str(shot)),itvl,wid,RAW=RAW)
    #    xy2=calc3("complex",str(shot),channel(chs[1],str(shot)),itvl,wid,RAW=RAW)
    #else:
    #    xy1=calc3("complex",str(shot),str(num[0]),itvl,wid,RAW=RAW)
    #    xy2=calc3("complex",str(shot),str(num[1]),itvl,wid,RAW=RAW)
    #    input(xy1)

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

def calc_mvelo(shot,itvl=0.01,wid=0.3,RAW=0, chs=["Is_mach1","Is_mach2"], calib=1.24 ,coff=43.711):
    from calc import calc3
    from useful import channel
    from numpy import array
    
    calib_coff = coff
    
    xy1=calc3("complex",str(shot),channel(chs[0],str(shot)),itvl,wid,RAW=RAW)
    xy2=calc3("complex",str(shot),channel(chs[1],str(shot)),itvl,wid,RAW=RAW)
    MPCR_data=[xy1[0][0],((calib*xy1[0][1]-xy2[0][1])/(calib*xy1[0][1]+xy2[0][1]))*calib_coff]
    MPCR_tag=[xy1[1][0],r"$V_{\rm MP}\ \rm [km/s]$"]
    MPCR=[MPCR_data,MPCR_tag]
    return MPCR

def calc_Mp(shot,itvl=0.01,ave=0.1,RAW=0, reff=None, iota=None):
    from calc import calc_mvelo, calc_triple
    from useful import channel,grep_num
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



def calc_triple(shot,chname=None,INTERVAL_TIME=0.01,AVERAGE_TIME=0.03,RAW=0):
    from subprocess import call,Popen,PIPE
    from useful import channel
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
            p=Popen(["triple","-s",str(shot),"-c",ch, "-a", "-o", "-49,-29"],stdin=PIPE,stdout=PIPE)
            #p=Popen(["triple","-s",str(shot),"-c",ch, "-an", "-o", "4,14", "-t", "20"],stdin=PIPE,stdout=PIPE)
            
            rmcmd=["rm",NAME]
            ans=["n\n","n\n","y\n","","",""]
            ans[3]=avename+"\n"
            ans[4]=str(INTERVAL_TIME)+"\n"
            ans[5]=str(AVERAGE_TIME)+"\n"                  
        
            for a in ans:    
                p.stdin.write(a)
                
            p.stdin.close()
            p.stdout.close()
            p.wait()
    else :
        NAME=environ["HOME"]+"/calc_data/"+rawname
        if len(Popen(["ls",NAME],stdout=PIPE).stdout.read()) == 0:
            p=Popen(["triple","-s",str(shot),"-c",ch, "-a", "-o", "-49,-29"],stdin=PIPE,stdout=PIPE)
            #p=Popen(["triple","-s",str(shot),"-c",ch, "-a", "-o", "4,14", "-t", "20"],stdin=PIPE,stdout=PIPE)

            rmcmd=["rm",NAME]
            ans=["n\n","y\n","","n\n"]
            ans[2]=rawname+"\n"            
        
            for a in ans:    
                p.stdin.write(a)
                
            p.stdin.close()
            p.stdout.close()
            p.wait()
    
    n_data=len(open(NAME,"rU").readlines())
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

def calc_triple2(shot,chname=None,INTERVAL_TIME=0.01,AVERAGE_TIME=0.03,RAW=0):
    from subprocess import call,Popen,PIPE
    from useful import channel
    from os import environ
    from numpy import zeros
    avename=str(shot)+"_INT"+str(INTERVAL_TIME)+"_AVE"+str(AVERAGE_TIME)+".dat"
    rawname=str(shot)+"_triple_RAW.dat"
    
    chdic={"te2":1,"ne2":2,"vf2":3,"vs2":4}

    ch=channel("Probe Current 2",str(shot))+","
    ch+=channel("Probe Bias 2",str(shot))+","
    ch+=channel("Vf-i-diamag 2",str(shot))+","
    ch+=channel("Vf-e-diamag 2",str(shot))
    #print ch
    if RAW == 0:
        NAME= environ["HOME"]+"/calc_data/"+avename
        if len(Popen(["ls",NAME],stdout=PIPE).stdout.read()) == 0:
            p=Popen(["triple","-s",str(shot),"-c",ch, "-a", "-o", "1,10"],stdin=PIPE,stdout=PIPE)
            
            rmcmd=["rm",NAME]
            ans=["n\n","n\n","y\n","","",""]
            ans[3]=avename+"\n"
            ans[4]=str(INTERVAL_TIME)+"\n"
            ans[5]=str(AVERAGE_TIME)+"\n"                  
        
            for a in ans:    
                p.stdin.write(a)
                
            p.stdin.close()
            p.stdout.close()
            p.wait()
    else :
        NAME=environ["HOME"]+"/calc_data/"+rawname
        if len(Popen(["ls",NAME],stdout=PIPE).stdout.read()) == 0:
            p=Popen(["triple","-s",str(shot),"-c",ch, "-a", "-o", "1,10"],stdin=PIPE,stdout=PIPE)

            rmcmd=["rm",NAME]
            ans=["n\n","y\n","","n\n"]
            ans[2]=rawname+"\n"            
        
            for a in ans:    
                p.stdin.write(a)
                
            p.stdin.close()
            p.stdout.close()
            p.wait()
    
    n_data=len(open(NAME,"rU").readlines())
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

def spec(shot,itvl=0.01,ave=0.03,RAW=0,e667=881737.765546,e728=2003465.38034):
    from numpy import savetxt,transpose
    xy1=calc("he728",shot,itvl,ave,RAW)
    xy2=calc("he667",shot,itvl,ave,RAW)
    x=(667.8/728.1)*(1.8299/6.3705)*(e728/e667)*(xy2[0][1]/xy1[0][1])
    ne= 5.8118e+12 - 6.3082e+13 * x +2.6453e+14 * pow(x,2) - 5.7518e+14 * pow(x,3) +7.6283e+14 * pow(x,4) - 6.4752e+14 * pow(x,5) +3.5986e+14 * pow(x,6) - 1.3036e+14 * pow(x,7) +2.9691e+13 * pow(x,8) - 3.8683e+12 * pow(x,9) +2.2081e+11 * pow(x,10)
    
    xy=[[xy1[0][0],ne*1e-12],["Time [ms]","ne_spec [10^12 cm^-3]"]]
    
    return xy
def ele_pressure(shot,itvl=0.01,ave=0.03,RAW=0):
    from useful import abbchan
    from calc import calc_triple
    
    xy_te = [calc_triple(str(shot),"te",itvl,ave,RAW=RAW)]
    xy_ne = [calc_triple(str(shot),"ne",itvl,ave,RAW=RAW)]
    
    xy = [["",""],["Time [ms]","neTe [a.u.]"]]
    xy[0][0] = xy_te[0][0][0]
    xy[0][1] = xy_te[0][0][1]*xy_ne[0][0][1]
    
    return xy

def i_pressure(shot,itvl=0.01,ave=0.03,RAW=0, Ti=2.5):
    from useful import abbchan
    from calc import calc_triple
    
    xy_ne = [calc_triple(str(shot),"ne",itvl,ave,RAW=RAW)]
    
    xy = [["",""],["Time [ms]","neTi [a.u.]"]]
    xy[0][0] = xy_ne[0][0][0]
    xy[0][1] = Ti*xy_ne[0][0][1] 
    
    return xy

def e_pressure(shot,itvl=0.01,ave=0.03,RAW=0):
    from useful import abbchan
    from calc import calc_triple
    
    xy_te = [calc_triple(str(shot),"te",itvl,ave,RAW=RAW)]
    xy_ne = [calc_triple(str(shot),"ne",itvl,ave,RAW=RAW)]
    
    xy = [["",""],["Time [ms]","neTe_2 [a.u.]"]]
    xy[0][0] = xy_te[0][0][0]
    xy[0][1] = xy_te[0][0][1]*xy_ne[0][0][1]
    
    return xy

def mvelo(shot,itvl=0.01,ave=0.02,RAW=0):
#    from useful import abbcan
    from calc import calc_triple, calc_mach
    from numpy import log, sqrt
    
    m_i = 1.67262e-27
    k = 1.380658e-23
    M_c = 1.0
    
    t, R = calc_mach(shot, itvl, ave, RAW)[0]
    T_e = calc_triple(shot,"te", itvl, ave, RAW)[0][1]
    V_p = [[t[:-1],sqrt(( m_i * T_e ) / m_i ) * M_c * log(R[:-1])],["Time [ms]", "V_p [m/s]"]]
    return V_p

def R_lab(shot,itvl=0.01,ave=0.03,RAW=0):
    from useful import abbchan
    from calc import calc
    
    xy_vlab = calc("vlab", str(shot), itvl, ave, RAW=RAW)
    xy_ilab = calc("ilab", str(shot), itvl, ave, RAW=RAW)
    
    xy = [["",""],["Time [ms]",r"$R_{\rm{LaB_6}}\ \rm{[\Omega]}$"]]
    xy[0][0] = xy_vlab[0][0]
    xy[0][1] = xy_vlab[0][1] / xy_ilab[0][1]
    
    return xy

def ne_ave(shot, itvl=0.01, ave=0.02, RAW=0, vpp = 1.4, line=139e-3, width=0.01, d_time=1):
    from calc import calc
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
    from useful import grep_series
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
    from useful import alignment
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


def calc(abbchname,shot,itvl=0.01,ave=0.03,RAW=0,e667=881737.765546,e728=2003465.38034, reff=None, iota=None, nom=None, expr_x=None, expr_y=None, timelst=None, f_name=None, vpp = 0.05, line=139e-3, width=0.01):
    from numpy import array,int_
    from useful import abbchan, alignment
    from calc import spec

    #if f_name != None:
    #    o = open(f_name)
    #     = o.read()

    shot = int_(float(shot))
    if abbchname == "mpcr":
        xy = calc_mach(str(shot),itvl,ave,RAW=RAW)
    elif abbchname == "te":
        xy = calc_triple(str(shot),str(abbchname),itvl,ave,RAW=RAW)
    elif abbchname == "ne":
        xy = calc_triple(str(shot),str(abbchname),itvl,ave,RAW=RAW)
    elif abbchname == "vf":
        xy = calc_triple(str(shot),str(abbchname),itvl,ave,RAW=RAW)
    elif abbchname == "vs":
        xy = calc_triple(str(shot),str(abbchname),itvl,ave,RAW=RAW)
    elif abbchname == "te2":
        xy = calc_triple2(str(shot),str(abbchname),itvl,ave,RAW=RAW)
    elif abbchname == "ne2":
        xy = calc_triple2(str(shot),str(abbchname),itvl,ave,RAW=RAW)
    elif abbchname == "vf2":
        xy = calc_triple2(str(shot),str(abbchname),itvl,ave,RAW=RAW)
    elif abbchname == "vs2":
        xy = calc_triple2(str(shot),str(abbchname),itvl,ave,RAW=RAW)
    elif abbchname == "ele_pressure":
        xy = pressure(str(shot),itvl,ave,RAW=RAW)
    elif abbchname == "ipress":
        xy = i_pressure(str(shot),itvl,ave,RAW=RAW)
    elif abbchname == "epress":
        xy = e_pressure(str(shot),itvl,ave,RAW=RAW)
    elif abbchname == "spec":
        xy = spec(shot,itvl=itvl,ave=ave,RAW=RAW,e667=e667,e728=e728)
    elif abbchname == "mvelo":
        xy = calc_mvelo(shot,itvl,ave,RAW)
    elif abbchname == "mp":
        xy = calc_Mp(shot,itvl,ave,RAW, reff, iota)
    elif abbchname == "rlab":
        xy = R_lab(str(shot),itvl,ave,RAW=RAW)
    elif abbchname == "mag":
        xy = mag(str(shot),itvl,ave,RAW=RAW)
    elif abbchname == "vmach1":
        xy = calc_mach(str(shot),itvl,ave,RAW=RAW, chs= ["Ism_u1", "Ism_d1"], name=r"$V_{\rm p1}\ \rm [km/s]$", calib=0.86048, vmach=True)
        #xy = calc_mach(str(shot),int,ave,RAW=RAW, chs= ["Ism_u1", "Ism_d1"], name=r"$V_{\rm p1}\ \rm [km/s]$", calib=0.85189832078193817, vmach=True)
    elif abbchname == "vmach2":
        xy = calc_mach(str(shot),itvl,ave,RAW=RAW, chs= ["Ism_u2", "Ism_d2"], name=r"$V_{\rm p2}\ \rm [km/s]$", calib=1.1048, vmach=True)
        #xy = calc_mach(str(shot),int,ave,RAW=RAW, chs= ["Ism_u1", "Ism_d1"], name=r"$V_{\rm p1}\ \rm [km/s]$", calib=0.85189832078193817, vmach=True)
    elif abbchname == "vmach3":
        xy = calc_mach(str(shot),itvl,ave,RAW=RAW, chs= ["Ism_u3", "Ism_d3"], name=r"$V_{\rm p3}\ \rm [km/s]$", calib=1.0076, vmach=True)
        #xy = calc_mach(str(shot),int,ave,RAW=RAW, chs= ["Ism_u1", "Ism_d1"], name=r"$V_{\rm p1}\ \rm [km/s]$", calib=0.85189832078193817, vmach=True)
    elif abbchname == "mpcr1":
        #xy = calc_mach(str(shot),int,ave,RAW=RAW, chs= ["Ism_u1", "Ism_d1"], name=r"$R_{\rm Mach1}$", calib=1, num=[27,28])
        xy = calc_mach(str(shot),itvl,ave,RAW=RAW, chs= ["Ism_u1", "Ism_d1"], name=r"$R_{\rm Mach1}$", calib=0.856329850669, num=[27,28])
        #change 20131119xy = calc_mach(str(shot),int,ave,RAW=RAW, chs= ["Ism_u1", "Ism_d1"], name=r"$R_{\rm Mach1}$", calib=0.86084, num=[27,28])
        #xy = calc_mach(str(shot),int,ave,RAW=RAW, chs= ["Ism_u1", "Ism_d1"], name=r"$R_{\rm Mach1}$", calib=0.85189832078193817)
    elif abbchname == "mpcr2":
        #xy = calc_mach(str(shot),int,ave,RAW=RAW, chs= ["Ism_u2", "Ism_d2"], name=r"$R_{\rm Mach2}$", calib=1, num=[29,30])
        xy = calc_mach(str(shot),itvl,ave,RAW=RAW, chs= ["Ism_u2", "Ism_d2"], name=r"$R_{\rm Mach2}$", calib=1.14898490437, num=[29,30])
        #change 20131119xy = calc_mach(str(shot),int,ave,RAW=RAW, chs= ["Ism_u2", "Ism_d2"], name=r"$R_{\rm Mach2}$", calib=1.1048, num=[29,30])
        #xy = calc_mach(str(shot),int,ave,RAW=RAW, chs= ["Ism_u2", "Ism_d2"], name=r"$R_{\rm Mach2}$", calib=1.1096947078915167)
    elif abbchname == "mpcr3":
        #xy = calc_mach(str(shot),itvl,ave,RAW=RAW, chs= ["Ism_u3", "Ism_d3"], name=r"$R_{\rm Mach3}$", calib=1, num=[31,32])
        xy = calc_mach(str(shot),itvl,ave,RAW=RAW, chs= ["Ism_u3", "Ism_d3"], name=r"$R_{\rm Mach3}$", calib=1.04608681374, num=[31,32])
        #change 20131119xy = calc_mach(str(shot),int,ave,RAW=RAW, chs= ["Ism_u3", "Ism_d3"], name=r"$R_{\rm Mach3}$", calib=1.0076, num=[31,32])
    elif abbchname == "mvelo1":
        xy = calc_mach(str(shot),itvl,ave,RAW=RAW, chs= ["Ism_u1", "Ism_d1"], name=r"$R_{\rm Mach1}$", calib=0.86084, num=[27,28], mvelo=31.92)
    elif abbchname == "mvelo2":
        xy = calc_mach(str(shot),itvl,ave,RAW=RAW, chs= ["Ism_u2", "Ism_d2"], name=r"$R_{\rm Mach2}$", calib=1.1048, num=[29,30], mvelo=31.92)
    elif abbchname == "mvelo3":
        xy = calc_mach(str(shot),itvl,ave,RAW=RAW, chs= ["Ism_u3", "Ism_d3"], name=r"$R_{\rm Mach3}$", calib=1.0076, num=[31,32], mvelo=31.92)
    elif abbchname == "<ne>":
        xy = ne_ave(str(shot),itvl,ave, RAW, vpp, line, width) 
#class triple_manage():
#    def __init__(self, shot, itvl=0.01, wid=0.1, raw=False, stime=(26, 36)):
    elif abbchname == "triple_wp":
        t = hel.triple_manage(shot,itvl, ave, RAW) 
        t.calc_all()
        xy = t
    elif abbchname == "te_wp":
        t = hel.triple_manage(shot,itvl, ave, RAW) 
        t.calc_te()
        xy = [[t.te.x, t.te.y],["Time [ms]", "tmp"]]
    elif abbchname == "pc_wp":
        t = hel.triple_manage(shot,itvl, ave, RAW) 
        t.calc_pc()
        xy = [[t.pc.x, t.pc.y],["Time [ms]", "tmp"]]
    elif abbchname == "pb_wp":
        t = hel.triple_manage(shot,itvl, ave, RAW) 
        t.calc_pb()
        xy = [[t.pb.x, t.pb.y],["Time [ms]", "tmp"]]
    elif abbchname == "ne_wp":
        t = hel.triple_manage(shot,itvl, ave, RAW) 
        t.calc_ne()
        xy = [[t.ne.x, t.ne.y],["Time [ms]", "tmp"]]
    elif abbchname == "vf_wp":
        t = hel.triple_manage(shot,itvl, ave, RAW) 
        t.calc_vf()
        xy = [[t.vf.x, t.vf.y],["Time [ms]", "tmp"]]
    elif abbchname == "vs_wp":
        t = hel.triple_manage(shot,itvl, ave, RAW) 
        t.calc_vs()
        xy = [[t.vs.x, t.vs.y],["Time [ms]", "tmp"]]
    else :
        xy=calc3("complex",str(shot),abbchan(str(abbchname),str(shot)),itvl,ave,RAW=RAW)
    if nom != None:
        xy2 = calc(nom, str(shot), itvl, ave, RAW=RAW)
        x, y1, y2 = alignment([xy[0],xy2[0]], void=float("inf"))
        xy = [[array(x), array(y1) / array(y2)],[xy[1][0],xy[1][1]+" / "+ xy2[1][1]]]
    if expr_x or expr_y:
        calc_expr(xy, expr_y, expr_x, shot, itvl=itvl, wid=ave, RAW=RAW, vpp=vpp, line=line, width=width)
 #       ops = expr.split()
 #       line = "xy[0][1] = xy[0][1]"
 #       paras = []
 #       n = 0
 #       for op in ops:
 #           try:
 #               float(op)
 #               line += op
 #           except:
 #               if len(op) != 1:
 #                   paras += [calc(op, str(shot), itvl, ave, RAW=RAW)[0]]
 #                   line += "array(paras[%s])" %n
 #                   n += 1
 #               else:
 #                   line += op
#
#        aligns = [xy[0]]
#        for para in paras:
#            aligns += [para]
#        paras = alignment(aligns)
#        xy[0][0] = array(paras[0])
#        xy[0][1] = array(paras[1])
#        paras = paras[2:]
#        print line
#        exec line
#        xy[1][1] += expry
#    xy = [[xy[0][0],xy[0][1]],[xy[1][0],xy[1][1]]]
    if timelst:
        xy = specify_zeropoint(timelst, xy)
    return xy
##def calc(abbchname,shot,int=0.01,ave=0.03,RAW=0,e667=881737.765546,e728=2003465.38034, reff=None, iota=None, nom=None):
##    from numpy import array
##    from useful import abbchan, alignment
##    from calc import spec
##    lst = [abbchname,nom]
##    xys = []
##    for abbchname in lst:
##        if abbchname == "mpcr":
##            xy = calc_mach(str(shot),int,ave,RAW=RAW)
##        elif abbchname == "te":
##            xy = calc_triple(str(shot),str(abbchname),int,ave,RAW=RAW)
##        elif abbchname == "ne":
##            xy = calc_triple(str(shot),str(abbchname),int,ave,RAW=RAW)
##        elif abbchname == "vf":
##            xy = calc_triple(str(shot),str(abbchname),int,ave,RAW=RAW)
##        elif abbchname == "vs":
##            xy = calc_triple(str(shot),str(abbchname),int,ave,RAW=RAW)
##        elif abbchname == "pressure":
##            xy = pressure(str(shot),int,ave,RAW=RAW)
##        elif abbchname == "spec":
##            xy = spec(shot,int=int,ave=ave,RAW=RAW,e667=e667,e728=e728)
##        elif abbchname == "mvelo":
##            xy = calc_mvelo(shot,int,ave,RAW)
##        elif abbchname == "mp":
##            xy = calc_Mp(shot,int,ave,RAW, reff, iota)
#        elif abbchname == "rlab":
#            xy = R_lab(str(shot),int,ave,RAW=RAW)
#        else :
#            xy=calc3("complex",str(shot),abbchan(str(abbchname),str(shot)),int,ave,RAW=RAW)
#        xys += [xy]
#    print xys
#    x, y1, y2 = alignment([xys[0][0],xys[1][0]], void=float("inf"))
#    xy = [[array(x), array(y1) / array(y2)],[xy[1][0],xys[0][1][1]+" / "+ xys[0][1][1]]]
#    return xy



def fit( xlst, ylst, itvl=None, ave=None):
    from numpy import array,sum,where

    xlst = array(xlst)
    ylst = array(ylst)

    if len(xlst) != len(ylst):
        print "The number of X low is different with the number of y low !!"
    elif itvl == None: 
        n = len(xlst)
        x = sum(xlst)
        y = sum(ylst)
        xy = sum(xlst * ylst)
        xsqua = sum(xlst ** 2)
        
        a = ( n * xy- x * y ) / ( n * xsqua - x ** 2 )
        b = ( xsqua * y- xy * x ) / ( n * xsqua - x ** 2 )
    
        return a,b
    
    elif type(itvl) != None:
        itvl = float(itvl)
        wid = float(ave)
        cnt = float(xlst[0])
        xmax = float(xlst[-1]) 
        cntlst = []
        alst = []
        blst = []
        avelst=[]
        while cnt < xmax: 
            widmin = cnt - wid/2
            widmax = cnt + wid/2
            xlst_min = xlst[where(xlst >= widmin)[0]]
            ylst_min = ylst[where(xlst >= widmin)[0]]
            xlst_len = where(xlst_min <= widmax )[0]
            

            if len(xlst_len) != 0:
                xlst_tmp=xlst_min[xlst_len]
                ylst_tmp=ylst_min[xlst_len]

                n = len(xlst_tmp)
                x = sum(xlst_tmp)
                y = sum(ylst_tmp)
                xy = sum(xlst_tmp * ylst_tmp)
                xsqua = sum(xlst_tmp ** 2)
            
                a = ( n * xy- x * y ) / ( n * xsqua - x ** 2 )
                b = ( xsqua * y- xy * x ) / ( n * xsqua - x ** 2 )
                
                cntlst += [cnt]
                alst += [a]
                blst += [b]
                
            cnt += itvl
        
        #import useful as u
        #u.writedat("/Users/yu/a.txt",[alst],"a")

        return cntlst,alst,blst
        
            
def ele_field(rlst, vslst, itvl, ave,B=1):
    from numpy import array
    xlst,ylst,blst = fit(rlst, vslst, itvl, ave)
    elelst = (array(ylst)) / B
    
    return array(xlst),elelst,blst
    
def pfit(xlist,ylist,M=8,sen=(82,123,1)):
    import numpy as np
    xlist = np.array(xlist)
    ylist = np.array(ylist)
    def y(x, wlist):
        ret = wlist[0]
        for i in range(1, M+1):
            ret += wlist[i] * (x ** i)
        return ret
    
    def estimate(xlist, tlist):
        A = []
        for i in range(M+1):
            for j in range(M+1):
                temp = (xlist**(i+j)).sum()
                A.append(temp)
        A = np.array(A).reshape(M+1, M+1)
     
        T = []
        for i in range(M+1):
            T.append(((xlist**i) * tlist).sum())
        T = np.array(T)
        wlist = np.linalg.solve(A, T)
        return wlist
    
    wlist = estimate(xlist, ylist)

    xs = np.arange(sen[0], sen[1] + sen[2], sen[2])
    model = [y(x, wlist) for x in xs]
    
    return xs, model

def dft(arr):
    k = arange(arr.size)
    n = arange(arr.size)
    return array(map(lambda x: (arr * exp(- x * n * 1j * 2 * pi / arr.size)).sum(), k))
    
def idft(arr):
    k = arange(arr.size)
    n = arange(arr.size)
    return array(map(lambda x: (arr.conj() * exp(- x * n * 1j * 2 * pi / arr.size)).sum().conjugate() / arr.size, k))
    
def bit_rev(n, conca=False):
    if n == 2:
        tmp =  array([0,1])
    elif n == 1:
        tmp =  array([0])
    elif n <= 0:
        raise ValueError
    else:
        pw = int(log(n)/log(2))
        minpw = pw - 2
        tmp = array([0, 2, 1, 3]) * 2 ** minpw
        retlst = []
        cnt = minpw - 1
        #cnt = minpw 
        #add_arr = repeat(arange(2**cnt) , 2 ** (cnt + 1))
        #tmp = tile(tmp, cnt+1)
        #tmp = tmp + add_arr
        while cnt >= 0:
            tmp = append(tmp, tmp + 2 ** cnt)
            cnt -= 1
        
    if conca:
        add_arr = repeat(arange(conca/tmp.size) * tmp.size, tmp.size)
        tmp = tile(tmp, conca/tmp.size) + add_arr
    return tmp

def butterfly(a, b, w):
    wb = (w * b)
    ret_a = a + wb
    ret_b = a - wb
    return ret_a, ret_b


def myfft_slow(arr):
    arr = array(arr, dtype=complex)
    anum = arr.size
    pnum = int(log(anum) / log(2))
    revarr = bit_rev(anum)
    arr = arr[revarr]
    for n in xrange(1, pnum + 1):
        tmp_warr = exp(-1.j * 2.  * pi / (2.**(n))) ** arange(2**(n-1))
        tmp_warr = tmp_warr[bit_rev(2.**(n - 1))]
        warr = array([])
        while True:
            if warr.size == anum / 2: 
                break
            for tmp_w in tmp_warr:
                warr = append(warr, tmp_w)
        revarr = bit_rev(2**n, anum)
        arr = arr[revarr]
        arr = append([butterfly(x, y, z) for x,y,z in zip(arr[range(0,anum,2)], arr[range(1,anum,2)], warr)],[])[revarr]
    return arr   

def myfft2(arr):
    arr = array(arr, dtype=complex)
    anum = arr.size
    pnum = int(log(anum) / log(2))
    revarr = bit_rev(anum)
    arr = arr[revarr]
    w = exp(-1j * 2 * pi / anum) ** arange(anum/2)
    for s in xrange(1, pnum + 1):
        k1 = 2 ** s
        k2 = k1 / 2
        Nk1 = anum/k1
        for m in xrange(k2):
            kn = (m) * Nk1 
            for q in xrange(m,anum, k1):
                r = q + k2
                Xtmp =  w[kn] * arr[r]
                arr[r] = arr[q] - Xtmp
                arr[q ] = arr[q] + Xtmp
    return arr

def zero_pad(arr, pnum):
    add_num = 2 ** pnum - arr.size
    return append(arr, zeros(add_num))
    
def myfft(arr, pnum=False):
    if pnum == False:
        pnum = log(arr.size)/log(2)
        if pnum - int(pnum) == 0:
            pnum = int(pnum)
        else:
            pnum = int(pnum + 1)
            arr = zero_pad(arr, pnum)
    else:
        arr = zero_pad(arr, pnum)
    arr = array(arr, dtype=complex)
    anum = arr.size
    revarr = bit_rev(anum)
    arr = arr[revarr]
    for n in xrange(1, pnum + 1):
        tmp_warr = exp(-1.j * 2.  * pi / (2.**(n))) ** arange(2**(n-1))
        tmp_warr = tmp_warr[bit_rev(2.**(n - 1))]
        warr = tile(tmp_warr, anum / (2**(n)))
        revarr = bit_rev(2**n, anum)
        arr = arr[revarr]
        a = arr[range(0,anum,2)]
        wb = arr[range(1,anum,2)] * warr
        ret_a = a + wb
        ret_b = a - wb
        arr = append(array([ret_a, ret_b]).transpose(),[])[revarr]
    return arr   
 
def myifft(arr):
    pnum = log(arr.size)/log(2)
    if pnum - int(pnum) == 0:
        pnum = int(pnum)
    else:
        pnum = int(pnum + 1)
        arr = zero_pad(arr, pnum)
    arr = array(arr, dtype=complex).conj()
    anum = arr.size
    revarr = bit_rev(anum)
    arr = arr[revarr]
    for n in xrange(1, pnum + 1):
        tmp_warr = exp(-1.j * 2.  * pi / (2.**(n))) ** arange(2**(n-1))
        tmp_warr = tmp_warr[bit_rev(2.**(n - 1))]
        warr = tile(tmp_warr, anum / (2**(n)))
        revarr = bit_rev(2**n, anum)
        arr = arr[revarr]
        a = arr[range(0,anum,2)]
        wb = arr[range(1,anum,2)] * warr
        ret_a = a + wb
        ret_b = a - wb
        arr = append(array([ret_a, ret_b]).transpose(),[])[revarr]
    return arr.conj() / arr.size

def wig_spec(arr, n=None, pnum=False):
    if n == None:
        n = arr.size
    a = arr[0:n/2][-1::-1]
    b = arr[n/2-1:][0:a.size]

    arr = 2 * a * b.conj()
    return fft.fft(arr)
    #return myfft(arr, pnum)

def myfftfreq(n, tstep=1):
    return arange(n) / (n * float(tstep))
#from numpy import *
#a=pfit(array([1,2,3,4,5]),array([1,3,5,6,8]),6)
#from pylab import *
#plot(a[0],a[1])
#plot(array([1,2,3,4,5]),array([1,5,2,6,3]))
#xlim(0,6)
#ylim(0,10)
#show()
#close()
#
