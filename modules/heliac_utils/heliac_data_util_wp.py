#self.calc.py V1.0
#from heliacdatmanage import triple_manage

import heliac_util as hel
from numpy import *

def channel(chname,shot):
    from subprocess import Popen,PIPE
    p=Popen(["chlist","-s",str(shot)],stdout=PIPE)
    p2=Popen(["grep",chname],stdin=p.stdout,stdout=PIPE)
    a=p2.stdout.read().strip().split("\n")
    if len(a)==0:
        if chname == "island_shunt2":
            chname = "Island_shunt2"
        if chname == "V_electrode_LaB6":
            chname = "V_electorode_LaB6"
        if chname == "Is_mach1":
            chname = "Vs_mach1"
        if chname == "Is_mach2":
            chname = "Vs_mach2"
        p=Popen(["chlist","-s",str(shot)],stdout=PIPE)
        Popen(["chlist","-s",str(shot)])
        p2=Popen(["grep",chname],stdin=p.stdout,stdout=PIPE)
        
        a = p2.stdout.readline()
    for numname in a:
        num = numname[:2].strip()
        name = numname[2:].strip()
        if name == chname: return num
    p.stdout.close()
    p2.stdout.close()

def abbchan(chname, shot):
	abbr={"pc":"Probe Current",
		  "pb":"Probe Bias",
		  "vfi":"Vf-i-diamag",
		  "vfe":"Vf-e-diamag",
	      "pchs":"Probe Current HS",
		  "pbhs":"Probe Bias HS",
		  "vfihs":"Vf-i-diamag HS",
		  "vfehs":"Vf-e-diamag HS",
		  "rf":"RF Current",
		  "nel":"NeL",
		  "ccc":"CENTER COIL CURRENT",
		  "vcc":"VERTICAL COIL CURRENT",
		  "tcc":"TOROIDAL COIL CURRENT",
		  "ha":"H_a",
		  "ot":"One Turn",
		  "is":"island_shunt2",
		  "rog":"Rogowsky",
		  "vlab":"V_electrode_LaB6",
		  "ilab":"I_electrode_LaB6",
		  "ism1":"Is_mach1",
		  "ism2":"Is_mach2",
		  "he728":"I_He_728",
		  "he667":"I_He_667",
	      "he468":"I_He_468",
	      "vbm":"Vb_mach" ,
          "ilim":"I_limiter", 
          "mag+":"V_magnetic_forward+",
          "mag-":"V_magnetic_backward+", 
          "mag+":"V_magnetic_forward-",
          "mag-":"V_magnetic_backward-", 
          "mag+":"V_magnetic+",
          "mag-":"V_magnetic-", 
          "ismu1":"Ism_u1",
          "ismd1":"Ism_d1",
          "ismu2":"Ism_u2",
          "ismd2":"Ism_d2",
          "ismu3":"Ism_u3",
          "ismd3":"Ism_d3",
          "pc2":"Probe Current 2",
          "pb2":"Probe Bias 2",
          "vfi2":"Vf-i-diamag 2",
          "vfe2":"Vf-e-diamag 2",
          "vpd":"V_electrode_PdAu",
          "ipd":"I_electrode_PdAu",
    }
	return channel(abbr[chname],shot)



def gdat_wh(calc_cmd,shot,ch,INTERVAL_TIME=0.05,AVERAGE_TIME=0.5,RAW=0):
    from subprocess import call,Popen,PIPE
    from os import environ
    from numpy import zeros
    avename=shot+"_"+ch+"_INT_"+str(INTERVAL_TIME)+"_AVE_"+str(AVERAGE_TIME)+".dat"
    rawname=shot+"_"+ch+"_RAW.dat"
    if RAW == 0:
        NAME= environ["HOME"]+"/calc_data/"+avename
        if len(Popen(["ls",environ["HOME"]+"/calc_data/"+avename],stdout=PIPE).stdout.read()) == 0:
            p=Popen([calc_cmd,"-s",shot,"-c",ch],stdin=PIPE)
            if RAW==0:
                rmcmd=["rm",NAME]
                ans=["n\n","n\n","y\n","","",""]
                ans[3]=avename+"\n"
                ans[4]=str(INTERVAL_TIME)+"\n"
                ans[5]=str(AVERAGE_TIME)+"\n" 
            for a in ans:    
                p.stdin.write(a)  
            p.stdin.close()
            #p.stdout.close()
            #p.stderr.close()
            p.wait()        
    else: 
        NAME= environ["HOME"]+"/calc_data/"+rawname
        if len(Popen(["ls",environ["HOME"]+"/calc_data/"+rawname],stdout=PIPE).stdout.read()) == 0:
            p=Popen([calc_cmd,"-s",shot,"-c",ch],stdin=PIPE)#,stdout=PIPE,stderr=PIPE)
            NAME=environ["HOME"]+"/calc_data/"+rawname
            rmcmd=["rm",NAME]
            ans=["n\n","y\n","","n\n"]
            ans[2]=rawname+"\n"            
            for a in ans:    
                p.stdin.write(a)
            p.stdin.close()
            #p.stdout.close()
            #p.stderr.close()
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
    return ret

def calc(abbchname,shot,itvl=0.01,ave=0.03,RAW=0,e667=881737.765546,e728=2003465.38034, reff=None, iota=None, nom=None, expr_x=None, expr_y=None, timelst=None, f_name=None, vpp = 0.05, line=139e-3, width=0.01):
    from numpy import array,int_
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
    if timelst:
        xy = specify_zeropoint(timelst, xy)
    return xy


