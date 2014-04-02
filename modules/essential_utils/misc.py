class calcdata(object):
    def __init__(self, raw=0, intave=[0.01,0.1]):
        import pickle as pic        
        self.datadic = {"tmp_datas":[],"tmp_tevos":[], "tmp_profs":[]}
        self.cmpdic = {"raw":raw, "intave":intave}
        self.raw = raw
        self.intave = intave
        self.addx = None
        self.addy = None
        self.dumppath = "/Users/yu/"
        self.labeldic = {"pc": "I_{\rm{pc}}"}
        self.infodic = {}
        
        try:
            f = open("/Users/yu/tmp.txt")
            self.datadic["tmp_datas"] = pic.load(f)
            f.close()
        except:
            pass
       
    def allsame(self, dic1, dic2, iglst=None):
        for k in dic1.keys():
            try:
                iglst.index(k)
            except:
                cmp1 = dic1[k] if type(dic1[k]) != ndarray else dic1[k].tolist()
                cmp2 = dic2[k] if type(dic2[k]) != ndarray else dic2[k].tolist()
                if cmp1 != cmp2:
                    return False
                    break
        return True
                
    
    def dic_pullout(self, shot, ch):
        cmpdic = self.cmpdic
        #cmpdic.update({"shot": shot, "ch":ch})
        cmpdic.update({"shot":str(shot), "ch":ch, "raw":self.raw, "intave":self.intave, "addx":self.addx, "addy":self.addy})#, "xlabel":xname, "ylabel":yname}
        if self.raw == 1:
            cmpdic.pop("intave")
        cmpdic.update(self.infodic)
        for n in range(len(self.datadic["tmp_datas"])):
            try:
                tmpdic = self.datadic["tmp_datas"][n][0]
                #if tmpdic["shot"] == str(shot) and tmpdic["ch"] == ch and tmpdic["raw"] == self.raw and tmpdic["intave"] == self.intave:
                if self.allsame(cmpdic, tmpdic):
                    return self.datadic["tmp_datas"][n]
                    break
            except:
                pass
    def dic_input_param(self, shot, ch, paradic):
        cmpdic = self.cmpdic
        #cmpdic.update({"shot": shot, "ch":ch})
        cmpdic.update({"shot":str(shot), "ch":ch, "raw":self.raw, "intave":self.intave})#, "xlabel":xname, "ylabel":yname}
        if self.raw == 1:
            cmpdic.pop("intave")
        cmpdic.update(self.infodic)
        for n in range(len(self.datadic["tmp_datas"])):
            try:
                tmpdic = self.datadic["tmp_datas"][n][0]
                #if tmpdic["shot"] == str(shot) and tmpdic["ch"] == ch and tmpdic["raw"] == self.raw and tmpdic["intave"] == self.intave:
                if self.allsame(cmpdic, tmpdic):
                    return self.datadic["tmp_datas"][n][0].update(paradic)
                    break
            except:
                pass


    def dic_input(self, shots, ch, output=0,):
        tmplst = []
        for shot in shots:
            [dats,[xname,yname]]=calc(ch, str(shot), int=self.intave[0], ave=self.intave[1], RAW=self.raw, expr_x=self.addx, expr_y=self.addy)
            infodic = {"shot":str(shot), "ch":ch, "raw":self.raw, "intave":self.intave, "xlabel":xname, "ylabel":yname, "addx":self.addx,"addy:":self.addy}
            infodic.update(self.infodic)
            self.datadic["tmp_datas"] += [[infodic, dats]]
            if output == 1:
                tmplst += [[infodic, dats]]
        if output == 1:
            return tmplst

    def get(self, shots, chs):
        ret = []
        for shot in shots:
            for ch in chs:
                tmp = self.dic_pullout(str(shot), ch)
                if tmp == None:
                    ret += [self.dic_input([str(shot)], ch, output=1)[0]]
                else:
                    ret += [tmp]
        #self.save()
        return ret


    def tevos(self, shots, chs, cmp="shot"):
        tevodic = {"shots":shots, "chs":chs, "cmp":cmp, "raw":self.raw, "intave":self.intave, "addx":self.addx, "addy":self.addy}
        for tevolst in self.datadic["tmp_tevos"]:
            if self.allsame(tevolst[0], tevodic, iglst=["ylabellst"]):
                return [tevolst[0], tevolst[1]] 
                break
        tagdic = {"shot":shots, "ch":chs, }
        dats = self.get(shots, chs)
        opp={"shot":"ch","ch":"shot"}
        xname = ""
        yiter = shots
        tevodatas = []
        ynamelst = []
        tmp = []
        
                
        for elm in tagdic[opp[cmp]]:
            for elm in tagdic[cmp]:
                for dat in dats:
                    if str(elm) == dat[0][cmp]:
                        tmp += [dat[1]]
                        ynamelst += [dat[0]["ylabel"]]
            tevodatas += [tmp]
        tevodic.update({"ylabellst": ynamelst})
        self.datadic["tmp_tevos"] += [[tevodic, tevodatas]]
        return [tevodic, tevodatas]

    def profs(self, shots, chs, gtime, gparam="tmp", paralst=None, overwrite=False):
        dats = self.get(shots, chs)
        xlst = []
        ylst = []
        ret = []
        profdic = {"shots":shots, "chs":chs, "gtime":gtime, "gparam":gparam, "paralst":paralst, "raw":self.raw, "intave":self.intave, "addx":self.addx, "addy":self.addy}
        for proflst in self.datadic["tmp_profs"]:
            if self.allsame(proflst[0], profdic):
                return proflst[1]
                break
                
        for ch in chs:
            for dat,para in zip(dats, paralst):
                try:
                    if ch == dat[0]["ch"]:
                        if overwrite:
                            raise KeyError
                        xlst += [dat[0][gparam]]
                except KeyError:
                        dat[0].update({gparam : para})
                        xlst += [dat[0][gparam]]
                        pass
                ylst += [grep_series(gtime, dat[1][0], dat[1][1])]
            if paralst == None:
                ret += [[xlst, ylst]]
            else:
                ret += [[paralst, ylst]]
            xlst = []
            ylst = []
        self.datadic["tmp_profs"] += [[profdic, ret]]
        return ret

    def grad_profs(self, shots, chs, gtime, gparam="tmp", paralst=None, overwrite=False, fitordr = 6, sen=500, graint=0.01, graave=0.1, B=1):
        #import pylab as p
        proflst = self.profs(shots, chs, gtime, gparam, paralst, overwrite)
        retlst = []
        for prof in proflst:
            a=pfit(prof[0],prof[1],fitordr,(min(prof[0]),max(prof[0]),sen)) 
            #p.plot(a[0],a[1])
            xlst, ylst, blst = ele_field(a[0], a[1], graint, graave, B=B)    
            retlst += [array(xlst), array(ylst)]
        return retlst
    
    def grad_profs_dev(self, shots, ch, gtimelst, gparam="tmp", paralst=None, overwrite=False, fitordr = 6, sen=500, graint=0.01, graave=0.1, B=1):
        from numpy import arange
        
        retlst = []
        tmin, tmax, tdelta = gtimelst
        gtimelst = arange(tmin, tmax, tdelta)
        for gtime in gtimelst:
            retlst += [self.grad_profs(shots, [ch], gtime, gparam, paralst, overwrite, fitordr, sen, graint, graave, B=B)]
        return retlst
                


#        exec "for %s in %ss:\n global %s\n for %s in %ss:\n  cnt = 0;global %s\n  for tof in map((lambda y: y['%s']==str(%s) and y['%s']==str(%s)), map(lambda x: x[0], dats[cnt]:\n    print tof\n    if tof:\n     input(dats)\n     input(tof)\n     tmp += [dats[cnt][1]]\n     if cnt2==0:\n      xname=dats[cnt][0]['xlabel']\n      yname=dats[cnt][0]['ylabel']\n     if cnt2 == 1 and cmp=='ch':yname+=[dats[cnt][0]['ylabel']]\n     cnt2=1\n    cnt+=1\n tmpdic=dict(self.profdic.items())\n tmpdic.update({'%s':%s, '%s':%ss, 'xlabel':xname, 'ylabel':yname})\n ret+=[[dict(tmpdic.items()), tmp]]\n tmp=[]\n cnt=0;cnt2=0" %(opp[cmp], opp[cmp], opp[cmp], cmp, cmp, cmp, cmp, cmp, opp[cmp], opp[cmp], opp[cmp], opp[cmp], cmp, cmp,  )

    def datname(self, dic):
        abbname={"xlabel" : "xla",
                 "ylabel" : "yla",
                 "shot"   : "sh",
                 "ch"     : "ch",
                 "raw"    : "raw",
                 "intave" : "iav",
                 }
        ret = ""
        for k,v in dic.items():
            if type(v) == list:
                v = concatanate(v)
            ret += "%s_" %abbname[k]
        return ret

    def dumpdata(self, dats, path=None, name=None, align=False):
        if path == None:
            path = self.dumppath
        if name == None:
            name = self.datname(dats[0])
            
        tag = ""
        xlabel = dats[0]["xlabel"]
        ylabel = dats[0]["ylabel"]
        for k,v in dats[0].items():
            tag += "%s = %s\n\n#" %(k , v)
        tag += "%s,  %s\n" %(xlabel, ylabel)
            
        if align:
            w_dats = alignment(dats[0])
        else:
            w_dats = dats[0]
        writedat(path+name, w_dats, tag)
        
    def save(self):
        import pickle as pic
        f = open("/Users/yu/tmp_datas.txt", "w")
        pic.dump(self.datadic["tmp_datas"], f)
        f.close()

#########################################################


def fit_diff(xlst, ylst, time, slicelst=None, M=1, sen=(20, 40, 500)):
    import pylab as p
    import numpy as n
    xlst = xlst.tolist()
    ylst = ylst.tolist()
    if slicelst != None:
        dt = xlst[1] - xlst[0]
        tmpxlst = []
        tmpylst = []
        a=[]
        for s in slicelst:
            smin = (s[0] - xlst[0]) / dt
            smax = (s[1] - xlst[0]) / dt
            tmpxlst += xlst[int(smin):int(smax)]
            tmpylst += ylst[int(smin):int(smax)]
        
    
    fxlst,fylst = pfit(n.array(tmpxlst), n.array(tmpylst), M=M, sen=sen)
    a=alignment([[xlst,ylst],[fxlst,fylst]])
    diff = grep_series(time, a[0], a[2]) - grep_series(time, a[0], a[1])
    p.plot(a[0],a[1])          
    p.plot(a[0],a[2])          
    return diff     


def writedat(path,datlst,tag="tag",delimiter=", "):
    """
    this function generates a data file from any data list(or tupple).
    The variable "tag" is written above the file after "#". 
    
    Where, a lists is inputed into 'writedat' function.
    
    >>> import os
    >>> path = os.environ["HOME"] + "/Desktop/test_writedat.txt"
    >>> done = writedat(path,[[0,1,2,3,4,5],[2,3,4,5,6,7],[3,4,65,6,7,5]],"xtag")
    """
    wlines = map((lambda x:""),range(len(datlst[0])))
    wfile = open(path,"w")
    #print datlst
    #print "datlst"
    for dat in datlst:
    
    
        n=0
        #print dat
        #print "dat"
        for line in dat:
            #print line
            if str == type(line):
                wlines[n] += "%20.20s%s"%(line, delimiter)
            else:
                wlines[n] += "%16.4e%s"%(line, delimiter)
                
#            print str(line) + delimiter
#            wlines[n] += str(line) + delimiter
            n += 1
    
    wfile.write("#%s\n"%tag)
    for wline in wlines:
        wline = wline[:-1]
        wfile.write(wline+"\n")
    
    wfile.close()
    return "Done"

def mean_std(abbchname,dlsts,xrange=None,yrange=None,xname=r"R [mm]"
            ,yname=None,leglst=0,gtime=[26,36],figsize=(9,9),loc="best",
            tick=0,bor=None,fitting=0,gfit=0,pointsize=3,
            int=0.1,ave=0.2,RAW=0,sen = 1000, nom=None,
            fit_path=None,PICPATHS=[],figtype="pdf",DATPATH="/Users/yu/"):
    
    from numpy import std,mean
    #data get area
    n = 0
    datlst = []
    datlsts = []
    elem = None
    paras = []

    for dlst in dlsts:
        limit = len(dlst) - 1
        dlst = sorted(dlst, key = lambda x:x[1])
        for cnt,(shot,para) in enumerate(dlst):
            if n == 0:
                elem = para
                paras += [para]
                n = 1

            if elem == para:
                #print "waai"
                xy = calc(abbchname,shot,int=int,ave=ave,RAW=RAW)            
                datlst += [xy[0]]
                if limit == cnt:
                    datlsts += [datlst]
                    paras += [para]
                    datlst = []
                     
            else :

                datlsts += [datlst]
                elem = para
                paras += [para]
                datlst = []
            
        n = 0
        
        cnt = 0
        stds = []
        for datlst in datlsts:
            
            para = paras[n]
            for t in datlst[0][0]:
                if gtime[0] < t:
                    if gtime[1] < t:
                        break
                    else:
                        gdats = map(lambda x: grep(t,x[0],x[1]), datlst)
                        stds += [std(gdats)]
            
            meaned = mean(stds)
            #print meaned
            n += 1

def fseek(path):
    #For Graphmake V1.1
    from glob import glob
    return True if len(glob(path)) != 0 else False

def list_search(lst, obj):
    #Obj is searched in lst without rising error.
    try:
        param = lst.index(obj)
        return param
    except:
        return None

def gdat(shotlst):
    from ftplib import FTP
    for shot in shotlst:
        shot_num="#0000" + str(shot)
        flst=[]
        path="data/"
        PATH=path+shot_num+"*"
        ftp=FTP("130.34.71.154","ppl","hs-3900")
        
        ftp.dir(PATH,flst.append)
        
        
        for lst in flst:
            fname=lst.split()[-1]
            #print fname
            file="RETR ./data/"+fname
            local="/Users/yu/data/"+fname
            ftp.retrbinary(file,open(local,"wb").write)
    
    ftp.quit()

def concatanate(lst, delim=None):
    string=""
    if delim == None:
        delim = ""
    for line in lst:
        string += str(line) + delim
    if delim == string[-1]:
        string = string[:-1]
    return string

#print concatanate([1,2,3])
#print concatanate([1,2,3], delim=",")
#input()

def home():
    import os
    return os.environ["HOME"]

def fexist(path):
    import glob as g
    return len(g.glob(path)) >= 1

def ex_mkdir(path):
    import os
    if fexist(path) == False:
        os.mkdir(path)

def filename(plane=None,dic=None,extension=None,**arg):
    """
    This function is provide easy to name to filename.
    
    >>> print filename(("test"),{"sdev":1,"a":"df"},extension=None,rtp=123, zmp=98)
    test_adf_zmp98_sdev1_rtp123
    >>> print filename(("test"),{"sdev":1,"a":"df"},"dat",rtp=123, zmp=98)
    test_adf_zmp98_sdev1_rtp123.dat
    
    """
    
    tmp=""
    if plane != None:
    	for line in plane:
    		tmp += "_%s" %line
    		
    condic = {}
    if type(dic) == dict:
        condic.update(dic)
    if len(arg) != 0:
        condic.update(arg)
    for key, value in condic.items():
        tmp += "_%s%s" %(key, value)
    
    ext = "." + extension if extension != None else "" 
    fname = tmp[1:] + ext
    
    return fname


 

#print lstsplit([1,2,3,4,5],3)
#def writedat(path,datlst,tag="tag",delimiter=", "):
#    """
#    this function generates a data file from any data list(or tupple).
#    The variable "tag" is written above the file after "#". 
#    
#    Where, a lists is inputed into 'writedat' function.
#	
#    >>> import os
#    >>> path = os.environ["HOME"] + "/Desktop/test_writedat.txt"
#    >>> done = writedat(path,[[0,1,2,3,4,5],[2,3,4,5,6,7],[3,4,65,6,7,5]],"xtag")
#    """
#    wlines = map((lambda x:""),range(len(datlst[0])))
#    wfile = open(path,"w")
#    print datlst
#    print "datlst"
#    for dat in datlst:
#    
#    
#        n=0
#        print dat
#        print "dat"
#        for line in dat:
#            print line
#            print str(line) + delimiter
#            wlines[n] += str(line) + delimiter
#            n += 1
            
#	
#	wfile.write("#%s\n"%tag)
#	for wline in wlines:
#		wline = wline[:-1]
#		wfile.write(wline+"\n")
#	
#	wfile.close()
#	return "Done"
#if __name__ == "__main__":
#    import doctest
#    doctest.testmod()


	
def grep(param,plst,glst,lst=0):
	from numpy import array
	n = 0
	retlst = []
	for dat in plst:
		if "%.3e"%float(param) == "%.3e"%float(dat):
			if lst == 0:
				return glst[n]
				break
			else:
				retlst += [glst[n]]
		n+=1
	return retlst
#	return glst[where(param==plst)[0]]
def grep_num(param,plst):
    from numpy import array
    n = 0
    for dat in plst:
        if "%.3e"%float(param) == "%.3e"%float(dat):
            return n
            break
        n+=1
def grep_series(param, plst, glst, number=None):
    delta = float(plst[1]) - float(plst[0])
    lst_num = int(float(str((float(param) - float(plst[0]))/delta)))
    ret = glst[lst_num]
    confirm = plst[lst_num]
    if str(float(confirm)) == str(float(param)):
        if number:
            return lst_num
        else:
            return ret
    else:
        raise ValueError("そんなの値リストに無いってジャイアンが言ってた!!")

def extract(ext_prm, ref_arr, tar_arr):
    delta = ref_arr[1] - ref_arr[0]
    return tar_arr[int(ext_prm / delta)]

def alignment(xylst, gcolumn=0, void=0):
    import numpy as n
    initimes = map(lambda x: x[0][0], xylst)
    index = range(len(xylst))
    try:
        dts = map(lambda x: x[0][1] - x[0][0], xylst)
    except IndexError:
        retlst = xylst[0]
        return retlst
        
    retlst = []
    for time in xylst[gcolumn][0]:
        #input("time"+time)
        tmp = map(lambda p: time-p, initimes)
        #print str(initimes) + "initimes"
        #print str(tmp) + "tmp"
        g_num = map(lambda n,p: tmp[n]/p if 0 <= tmp[n] else None, index, dts)
        #print str(g_num)+"gnum"
        #print xylst[1][1]
        retlst += [map(lambda n,p: xylst[n][1][int(p)] if p != None and p < len(xylst[n][1]) else void, index, g_num)]
        #print retlst
    
    retlst = [xylst[gcolumn][0]] + n.transpose(n.array(retlst)).tolist()
    
    return retlst
    
def alignment_usingrep(xylst, gcolumn=0, void=0):

    
    times = xylst[gcolumn][0]
    
    paralst = []
    nlst = range(len(xylst))
    for cnt in nlst:
        paralst += [[]]
    for time in times:
        gparas = map(lambda p: grep(time, p[0], p[1]), xylst)
        for n in nlst:
#            print nlst
            paralst[n] += [gparas[n]]
    tmplst = [times]+paralst
    retlst = []
    for tmp in tmplst:
        retlst += [map(lambda x: void if type(x) == list else x, tmp)]
    return retlst

#from calc import *
#a=[]
#a=[[[1,2,3],[44,55,66]],[[0,1,2,3],[44,34,999,678]],[[1,4,6],[44,55,66]],]
#"b=alignment(a)
#print b
#writedat("/Users/yu/Desktop/rensu.txt",b)
def boder(ax,width=6,length=18):
	axx=ax.xaxis.get_ticklines()
	axy=ax.yaxis.get_ticklines()
	for b in axy:
		b.set_color("k")
		b.set_markeredgewidth(width)
		b.set_markersize(length)
	for b in axx:
		b.set_color("k")
		b.set_markeredgewidth(width)
		b.set_markersize(length)

def dress(ax,xlabel,ylabel,xrange,yrange,axes=[0.1,0.1,0.8,0.8],width=6,length=18):
	import pylab as p
	ax1=ax.add_axes(axes)
	p.rc("text",usetex="True")
	boder(ax1,width,length)
	p.xticks(xrange)
	p.yticks(yrange)

#import pylab as p
#a=p.figure()
#dress(a,"aa","ii",[1,2],[1,2])
#dress(a,"aa","ii",[1,2],[1,2],[0.2,0.5,0.6,0.6])
#print "aaa"
#p.plot([0,1,2,3])
#p.show()
#p.close()


		
def channel(chname,shot):
    from subprocess import Popen,PIPE
    #Popen(["chlist","-s",str(shot)])
    p=Popen(["chlist","-s",str(shot)],stdout=PIPE)
    #Popen(["grep",chname],stdin=p.stdout)
    p2=Popen(["grep",chname],stdin=p.stdout,stdout=PIPE)
    a=p2.stdout.read().strip().split("\n")
    if len(a)==0:
#        input()
        # The space of translation of irregular chname.
        if chname == "island_shunt2":
            chname = "Island_shunt2"
        if chname == "V_electrode_LaB6":
            chname = "V_electorode_LaB6"
        if chname == "Is_mach1":
            chname = "Vs_mach1"
        if chname == "Is_mach2":
            chname = "Vs_mach2"
        #print chname+" is irregular channel name!!" 
        p=Popen(["chlist","-s",str(shot)],stdout=PIPE)
        Popen(["chlist","-s",str(shot)])
        p2=Popen(["grep",chname],stdin=p.stdout,stdout=PIPE)
        
        a = p2.stdout.readline()
    for numname in a:
        num = numname[:2].strip()
        name = numname[2:].strip()
        if name == chname: return num
#	print p2.stdout.readline().split()[0]; input()
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
#abbchan("is",79715)
#input()
def makedat(xylst,path="/Users/yu/",fname="test.dat"):
	wfile=open(path+fname,"w")

##xdatalst+=xdata
##	x=iter(xylst)
##	y=iter(xylst)
##	namegen=iter(xylst)
	num=0
	index=len(xylst)
	xgen=iter(xylst)
	ygen=iter(xylst)
##	
##	xdata[num]=[]
##	ydata[num]=[]
##	xlabel[num]=[]
##	ylabel[num]=[]
	
##	xlabel[num]+=[iter(gen.next()[1][0])]
#		ylabel[num]+=[iter(gen.next()[1][1])]
	try:
		xdata=iter(xgen.next()[0][0])
		ydatalst=[]
		while num < index:
			ydatalst+=[iter(ygen.next()[0][1])]
			num+=1
		
		while True:
			dataline=""		
			dataline+=str(xdata.next())+","
			num=0
			while num < index:
				try:
					dataline+=str(ydatalst[num].next())+","
				except:
					dataline+="0,"
				num+=1
			wfile.write(dataline.strip(",")+"\n")
	except:
		pass
	
	wfile.close()
	return path+fname

#PC,Rogowsky,He468,Nelの比較
def clpl1(shots):
	from graph import graph4
	from calc import calc3
	num=1
	
	for shot in shots:
	    PDFPATH="/Users/yu/Desktop/"+shot+"_PC_Ro_He468_NeL.eps"
	    xy1=calc3("complex",shot,"1",RAW=1)
	    xy2=calc3("complex",shot,"26",RAW=1)
	    xy3=calc3("complex",shot,"38",RAW=1)
	    xy4=calc3("complex",shot,"8",RAW=1)    
	    graph4(shot,xy1[0],xy2[0],xy3[0],xy4[0],xy1[1][0],xy1[1][1],xy2[1][1],xy3[1][1],xy4[1][1],num,PDFPATH)
	    num+=1

def clpl2(shots):
	from graph import graph4
	from calc import calc3
	num=1
	
	for shot in shots:
	    PDFPATH="/Users/yu/Desktop/"+shot+"_PV_Vfe_Vlab_NeL.eps"
	    xy1=calc3("complex",shot,"2",RAW=1)
	    xy2=calc3("complex",shot,"6",RAW=1)
	    xy3=calc3("complex",shot,"27",RAW=1)
	    xy4=calc3("complex",shot,"8",RAW=1)    
	    graph4(shot,xy1[0],xy2[0],xy3[0],xy4[0],xy1[1][0],xy1[1][1],xy2[1][1],xy3[1][1],xy4[1][1],num,PDFPATH)
	    num+=1

def clpl3(shots):
	from graph import graph7
	from calc import calc3
	from numpy import array
	import pylab
	num=1
	
	for shot in shots:
	    PICPATH="/Users/yu/Desktop/"+str(shot)+"_Mach_Probe_Current_Ratio.eps"
	    xy1=calc3("complex",str(shot),"31",0.01,0.5,RAW=0)
	    xy2=calc3("complex",str(shot),"32",0.01,0.5,RAW=0)
	    graph7(shot,xy1[0],xy2[0],xy1[1][0],xy1[1][1],xy2[1][1],PICPATH)
	pylab.show()
	pylab.close()
	    
#clpl3([80315])


def comp_shot(shots,ch,xrange=[26,36],yrange=None,int=0.01,ave=0.03,leglst=None,mark=None,RAW=0,
			fig="pdf",figsize=(9,9),gtype=0,log=0,minus=None,dname=None,loc="best",e667=881737.765546,e728=2003465.38034, reff=None, iota=None):
	from graph import graph8,graph11
	from calc import calc3,calc_triple,calc_mach,spec,calc
	from numpy import array,savetxt,transpose
	import pylab
	colgen=iter(["r","y","g","b","black","c","m","pink","b","b","white"])
#	colgen=iter(["r","r","r","r","b","b","b","b","b","b","white"])
#	pylab.rc("text",usetex=True)

	num=1
	xylst=[]
	shottag=""
	for shot in shots:
	    raw=RAW
	    xylst += [calc(ch,shot,int,ave,RAW,reff=reff,iota=iota)]
	    num+=1
	    shottag+=str(shot)+"_"
	PICPATH="/Users/yu/Desktop/"+shottag+ch+"."+fig
	
	if gtype==1:
		graph11(shots,xylst,xrange,yrange,leglst=leglst,PICPATH=PICPATH,figsize=figsize,log=log,minus=minus,loc=loc)
	else:
		graph8(shots,xylst,xrange,yrange,leglst=leglst,PICPATH=PICPATH,figsize=figsize,log=log,minus=minus,loc=loc)
	xdata=[]
	ydata=[]
	data=[xylst[0][0][0]]
	for xy in xylst:
		data+=[xy[0][1]]
	if RAW == 0:
		savetxt("/Users/yu/DATDIR/%s%sMEAN_INT%s_AVE%s.dat" %(shottag,ch,int,ave),transpose(data))
	else:
		savetxt("/Users/yu/DATDIR/%s%sRAW.dat" %(shottag,ch),transpose(data))
	
	
	
#	savetxt("/Users/yu/Desktop/"+shottag+ch+".dat",)
def comp_ch(shot,chlst,xrange=[26,36],yrangelst=None,int=0.01,ave=0.03,RAW=None,fig="pdf",
		gtype=0,figsize=(9,9),PICPATH=None,log=0,dress=0,reff=None, iota=None):
	from graph import graph9,graph10
	from calc import calc3,calc_mach,calc_triple,calc,spec
	from numpy import array,savetxt,transpose
	import pylab
	from tag import tag3
	num=0
	xylst=[]
	chtag=""
	for ch in chlst:
#	    shottag+=str(shot)+"_"
	    if type(RAW) == list:
	    	raw=RAW[num]
	    else:
	    	raw=RAW
	    xylst += [calc(ch,shot,int,ave,RAW,reff=reff, iota=iota)]
	    num+=1
	    chtag+=str(ch)+"_"
	    if raw == 0:
	    	savetxt("/Users/yu/DATDIR/%s_%s_MEAN_INT%s_AVE%s.dat" %(str(shot),ch,int,ave),transpose(xylst[-1][0]))
	    else:
	    	savetxt("/Users/yu/DATDIR/%s_%s_RAW.dat" %(str(shot),ch),transpose(xylst[-1][0]))
#	if PICPATH == None:
#		PICPATH=tag3("comp_ch","/Users/yu/Desktop/",shot,chlst,fig,gtype)
	if gtype == 1:
		graph10(shot,xylst,xrange,yrangelst,PICPATH,figsize,log=log,dress=dress)
	else:
		graph9(shot,xylst,xrange,yrangelst,PICPATH,figsize,log=log,dress=dress)
	pylab.draw()

#print_mach([79715,80335])
def profile(abbchname,dlsts,xrange=None,yrange=None,xname=r"R [mm]"
            ,yname=None,leglst=None,gtime=35.5,figsize=(9,9),loc="best",tick=0,bor=None,fitting=0,data=None,sdev=None,pointsize=3,
            int=0.01,ave=0.02,RAW=0,eleint=None,eleave=None,sen = 1000):
    from calc import calc,ele_field,pfit
    from useful import abbchan,grep
    from numpy import where,array,arange,polyfit,polyval,savetxt,transpose,mean,std,append
    from pylab import plot,xticks,yticks,xlim,ylim,xlabel,ylabel,figure,plot,savefig,rc,annotate,legend,rcParams,axes,draw,errorbar


#    print abbchname != "ele" and abbchname != "velo"
#    print abbchname == "ele"
#    input()
	###########CONFIG AREA##################
#	rc("text",usetex=True)

    rcParams["legend.fontsize"]=20
    rcParams["axes.linewidth"]=6
    rcParams["xtick.major.pad"]=12
    rcParams["ytick.major.pad"]=12
    mk = "o"
    
    	
    colgen=iter(["r","y","g","b","black","c","m","pink","b","b","white"])
    if type(data)== list:
    	datagen=iter(data)
    
    gylst=[]
    shotlst=[]
    
    ax=figure(figsize=figsize).add_axes([0.15,0.15,0.8,0.8])

    ##########CALC AREA################
    if tick == 1:
	    if type(xrange) == list:
	    	if len(xrange)==3:
	    		xdivision=xrange[2]
	    	else:
	    		xdivision=None
	    	xlimit=arange(xrange[0],xrange[1],xdivision)
	    	
	    	xticks(xlimit,xlimit,fontsize=30)
	    
	    if type(yrange) == list:
	    	if len(yrange)==3:
	    		ydivision=yrange[2]
	    	else:
	    		ydivision=None
	    	
	    	ylimit=arange(yrange[0],yrange[1],ydivision)
	    	yticks(ylimit,ylimit,fontsize=30)
	    	
    if xrange != None:
    	xlim(xrange[0],xrange[1])
    if yrange != None:
    	ylim(yrange[0],yrange[1])
		
#        ylim(yrange)
    if type(leglst) == list:
        label=iter(leglst)
    elif leglst == 0:
        pass
    else:
    	a=range(len(dlsts))
    	b=map((lambda x: "datalist%s" %(x+1)),a)
        label=iter(b)
        
        
    paralst=array([])
    std_paralst = array([])
    xlst=array([])
    num=0
    a=[]
    glst=None
    if type(gtime)==list:
    	glst=gtime
    	ggen=iter(glst)
    
    tmp_xy = []
    xylst = []
    tmp_shot = []
    shots = []
    for dlst in dlsts:
#    	print dlst
    	dlst = sorted(dlst, key = lambda x:x[1])
#    	print dlst
#    	input()
    	for dl in dlst:
        	para = dl[1]
    		if len(where(std_paralst==para)[0]) == 0:
    			std_paralst=append(std_paralst,para)
            
        	tmp_shot += [dl[0]]
        	if abbchname == "ele" or abbchname == "velo":
        		tmp_xy += [calc("vf",dl[0],int=int,ave=ave,RAW=RAW)]
        	else:
        		tmp_xy += [calc(abbchname,dl[0],int=int,ave=ave,RAW=RAW)]
        xylst += [tmp_xy]
        shotlst += [tmp_shot]
        tmp_shot = []
        tmp_xy = []


        	
    cnt1 = 0
    cnt2 = 0
    for dlst in dlsts:
    	dlst = sorted(dlst, key = lambda x:x[1])
    	if type(glst)==list:
    		gtime=ggen.next()
    	gylst=[]	
    	for dl in dlst:
        	para = dl[1]
#    		if len(where(paralst==para)[0]) == 0:
    		paralst=append(paralst,para)
            
        	xy=xylst[cnt1][cnt2]
        	cnt2 += 1
        	#gylst=append(gylst,[grep(gtime,xy[0][0],xy[0][1])])
        	gylst += [grep(float(gtime),xy[0][0],xy[0][1])]

        	xlst=append(xlst,dl[1])
        gylst=array(gylst)
        
        if abbchname == "ele" or abbchname == "velo":
        	mk = "-"
        	a=pfit(paralst,gylst,fitting,(paralst[0],paralst[-1],sen)) 
#        	plot(a[0],a[1])
        	paralst, gylst ,blst= ele_field(a[0],a[1], int=eleint, ave=eleave)
        	xy[1][1] = "E [kV/m]"
        	if abbchname == "velo" :
        		B_phi = 0.3 * 82 / paralst
        		gylst = gylst / B_phi
        		xy[1][1] = "V_phi [km/s]"
        		
#	        	

        	

        mdatlst=array([])
        stdatlst=array([])
#        print paralst
#        print gylst
#        print xlst
#        print gylst
#        print shotlst
#        print xylst
#        input()

        if sdev == 1:
        	for para in std_paralst:
        		dat=gylst[where(xlst==para)[0]]
        		mdat=mean(dat)
        		stdat=std(dat)
        		mdatlst=append(mdatlst,mdat)
        		stdatlst=append(stdatlst,stdat)
        
        		
        
		
		#################PLOT AREA######################
        if sdev == 1:
	        if leglst == 0:
	        	ax.errorbar(std_paralst,mdatlst,stdatlst,fmt=mk,markersize=pointsize,c=colgen.next())
	        else:
	        	ax.errorbar(std_paralst,mdatlst,stdatlst,fmt=mk,markersize=pointsize,c=colgen.next(),label=label.next())
	        if type(fitting) != 0:
	        	a=pfit(std_paralst,mdatlst,fitting,(std_paralst[0],std_paralst[-1],500)) 
	        	ax.plot(a[0],a[1])
	        	
	        if type(data) == list:
	        	writedat(datagen.next(),[std_paralst,mdatlst,stdatlst],xy[1][0]+", "+xy[1][1])#,stdatlst)))
	        	
        
        else:        		
	        if leglst == 0:
	        	ax.plot(paralst,gylst,mk,markersize=pointsize,c=colgen.next())
	        else:
	        	ax.plot(paralst,gylst,mk,markersize=pointsize,c=colgen.next(),label=label.next())
	       
	        if fitting!=0:
	        	if abbchname != "ele" and abbchname != "velo":
	        		a=pfit(paralst,gylst,fitting,(paralst[0],paralst[-1],500))
	        		ax.plot(a[0],a[1])
	        	
	        if type(data) == list:
	        	writedat(datagen.next(),(paralst,gylst),xy[1][0]+", "+xy[1][1])
        xlst,gylst,paralst,mdatlst,stdatlst=array([]),array([]),array([]),array([]),array([])
        
        cnt1 +=1
        cnt2 = 0
      

    xlabel(xname,fontsize=30)
    if type(yname) == str:
        ylabel(yname,fontsize=30)
    else:
        ylabel(xy[1][1],fontsize=30,fontproperties="Helvetica")
    
    if leglst != 0:
    	legend(shadow=True,loc=loc,numpoints=1)
    	
    draw()
    savefig("/Users/yu/Desktop/profile_%s.pdf" %abbchname)
  

    
def threshold(dlst,abbchname,int=0.01,ave=0.3,RAW=0,nom=None,dname=None):
	from calc import calc
	import numpy as n
	gy=n.array([])
	shotlst=[]
	
	for dl in dlst:
		time=20.
		shot=dl[0]
		gtime=dl[1]
		xy=calc(abbchname,shot,int=int,ave=ave,RAW=RAW)
		if type(nom)==str:
			x=[]
			param=[]
			nomxy=calc(nom,shot,int=int,ave=ave,RAW=RAW)
			print nomxy
			while time <= 50:
				y=xy[0][1][n.where(time==xy[0][0])[0]][0]
				nomy=nomxy[0][1][n.where(time==nomxy[0][0])[0]][0]
				print y
				print nomy
				if nomy != 0:
					param+=[[y/nomy][0]]
					print param
				x+=[time]
#				param+=xy[0][1]/nomxy[0][1]
			
#					y=xy[0][1][n.where(time==xy[0][0])[0]]
#					nomy=nomxy[0][1][n.where(time==nomxy[0][0])[0]]
#					xy[0][1]+=[y/nomy]
#					param+=xy[0][1]/nomxy[0][1]
					
				
				time+=0.1
				print time
			xy[0][0]=n.array(x)
			xy[0][1]=n.array(param)
			
#		if type(nom)==list:
#			nomxy=calc(nom[0],shot,int=int,ave=ave,RAW=RAW)
#			for no in nom[1:]:
#				nomxy[0][1]=nomxy[0][1]*calc(no,shot,int=int,ave=ave,RAW=RAW)[0][1]
#			xy[0][1]=xy[0][1]/nomxy[0][1]
		gy=n.append(gy,xy[0][1][n.where(gtime==xy[0][0])[0]])
#		if len(gy) != 1:
##			gy=gy[0]
#		print xy[0][0]
#		print xy
#		shotlst+=shot
		
#threshold([[80013,35.50]],abbchname="ilab",nom="ne",RAW=0)

def threshold(dlst,gplst,abbchan,int=0.01,ave=0.03,txt=None):
	from numpy import savetxt,append,transpose,array,sqrt
	from calc import calc
	from useful import grep
	from subprocess import call
	path="/Users/yu/Desktop/threshold_time_Zmp86_"+abbchan
	xpara=[]
	ypara=[]
	xlst=[]
	ylst=[]
	shots=[]
	tag=""
	call(["mkdir",path])
	for gparam in gplst:
		for dl in dlst:
			shot=dl[0]
			shots+=[dl[0]]
			tag+=str(shot)+"_"
			xpara+=[sqrt(dl[1])]
			xy=calc(abbchan,shot,int=int,ave=int)
			ypara=append(ypara,grep(gparam,xy[0][0],xy[0][1]))

		if type(txt) == str:
			savetxt(txt,transpose(xpara,ypara))
		else:
			savetxt(path+"/Zmp86"+abbchan+"_gtime"+str(gparam)+".dat",transpose((xpara,ypara)))
		xlst+=[xpara]
		ylst+=[ypara]
		xpara=[]
		ypara=[]
		savetxt(path+"/shots.dat",transpose(shots))
		shots=[]

	return [xlst,ylst]

def threshold2(dlst,abbchan,nom=None,Zmp=None,int=0.01,ave=0.03,txt=None,sdev=None):
	from numpy import savetxt,append,transpose,array,sqrt,where,mean,std,ones
	from calc import calc
	from useful import grep
	from subprocess import call
	path="/Users/yu/Desktop/threshold2_time_Zmp98_"+abbchan
	xpara=[]
	ypara=[]
	xlst=[]
	ylst=[]
	shots=[]
	nompara=[]
	abbpara=[]
	gtimelst=[]
	xparalst=[]
	tag=""
	paralst=array([])
	call(["mkdir",path])
	for dl in dlst:
		shot=dl[0]
		shots+=[dl[0]]
		tag+=str(shot)+"_"
		xpara+=[sqrt(dl[1])]
		xparalst+=[dl[1]]
		para = dl[1]
		if len(where(paralst==para)[0]) == 0:
			paralst=append(paralst,para)
		
		gtime=dl[2]
		xy1=calc(abbchan,shot,int=int,ave=ave)
		if type(nom) == str:
			xy2=calc(nom,shot,int=int,ave=ave)
		else:
			xy2=[[xy1[0][0],ones(len(xy1[0][1]))],["None","None"]]
		xy=[[xy1[0][0],xy1[0][1]/xy2[0][1]],["Time [msec]",xy1[1][1]+"-"+xy2[1][1]+"nom"]]
		ypara=append(ypara,grep(gtime,xy[0][0],xy[0][1]))
		abbpara=append(abbpara,grep(gtime,xy[0][0],xy1[0][1]))
		nompara=append(nompara,grep(gtime,xy[0][0],xy2[0][1]))
		gtimelst+=[gtime]
		
	mdatlst=array([])
	stdatlst=array([])	
	for para in paralst:
		dat=ypara[where(xparalst==para)[0]]
		mdat=mean(dat)
		stdat=std(dat)
		mdatlst=append(mdatlst,mdat)
		stdatlst=append(stdatlst,stdat)
	print paralst,mdatlst,stdatlst
	if sdev == 1:
		if type(nom) == str:
			savetxt(path+"/Zmp"+str(Zmp)+"_"+abbchan+"_nom_"+nom+"_sdev.txt",transpose((paralst,mdatlst,stdatlst)))
		else:
			savetxt(path+"/Zmp"+str(Zmp)+"_"+abbchan+"_sdev.txt",transpose((paralst,mdatlst,stdatlst)))
	if type(txt) == str:
		savetxt(txt,transpose(xpara,ypara))
#        else:
#			savetxt(path+"/Zmp"+str(zparam)+"_"+abbchan+"_nom_"+nom+".dat",transpose((xpara,ypara,abbpara,nompara,gtimelst,shots)))
#    xlst+=[xpara]
#    ylst+=[ypara]
#    xpara=[]
#    ypara=[]
#		savetxt(path+"/shots.dat",transpose(xy2[1][1]))
#    shots=[]
	return [xlst,ylst]

def threshold2_before_revised(dlst,zlst,abbchan,nom=None,int=0.01,ave=0.03,txt=None,sdev=None):
	from numpy import savetxt,append,transpose,array,sqrt,where,mean,std,ones
	from calc import calc
	from useful import grep
	from subprocess import call
	path="/Users/yu/Desktop/threshold2_time_Zmp98_"+abbchan
	xpara=[]
	ypara=[]
	xlst=[]
	ylst=[]
	shots=[]
	nompara=[]
	abbpara=[]
	gtimelst=[]
	xparalst=[]
	tag=""
	paralst=array([])
	call(["mkdir",path])
	for zparam in zlst:
		for dl in dlst:
			
			shot=dl[0]
			shots+=[dl[0]]
			tag+=str(shot)+"_"
			xpara+=[sqrt(dl[1])]
			xparalst+=[dl[1]]
			para = dl[1]
			if len(where(paralst==para)[0]) == 0:
				paralst=append(paralst,para)
		
			gtime=dl[2]
			xy1=calc(abbchan,shot,int=int,ave=ave)
			if type(nom) == str:
				xy2=calc(nom,shot,int=int,ave=ave)
			else:
				xy2=[[xy1[0][0],ones(len(xy1[0][1]))],["None","None"]]
			xy=[[xy1[0][0],xy1[0][1]/xy2[0][1]],["Time [msec]",xy1[1][1]+"-"+xy2[1][1]+"nom"]]
			ypara=append(ypara,grep(gtime,xy[0][0],xy[0][1]))
			abbpara=append(abbpara,grep(gtime,xy[0][0],xy1[0][1]))
			nompara=append(nompara,grep(gtime,xy[0][0],xy2[0][1]))
			gtimelst+=[gtime]
		
		mdatlst=array([])
        stdatlst=array([])	
        for para in paralst:
			dat=ypara[where(xparalst==para)[0]]
			mdat=mean(dat)
			stdat=std(dat)
			mdatlst=append(mdatlst,mdat)
			stdatlst=append(stdatlst,stdat)
        print paralst,mdatlst,stdatlst
        if sdev == 1:
        	if type(nom) == str:
				savetxt(path+"/Zmp"+str(zparam)+"_"+abbchan+"_nom_"+nom+"_sdev.dat",transpose((paralst,mdatlst,stdatlst)))
        	else:
				savetxt(path+"/Zmp"+str(zparam)+"_"+abbchan+"_sdev.dat",transpose((paralst,mdatlst,stdatlst)))
        if type(txt) == str:
			savetxt(txt,transpose(xpara,ypara))
#        else:
#			savetxt(path+"/Zmp"+str(zparam)+"_"+abbchan+"_nom_"+nom+".dat",transpose((xpara,ypara,abbpara,nompara,gtimelst,shots)))
        xlst+=[xpara]
        ylst+=[ypara]
        xpara=[]
        ypara=[]
#		savetxt(path+"/shots.dat",transpose(xy2[1][1]))
        shots=[]

	return [xlst,ylst]

	
def time_evo(dlsts,gtimelst,abbchan,int=0.01,ave=0.02,
			xrange=None,yrange=None,leglst=None,figsize=[9,9]):
	import pylab as p
	import numpy as n
	from calc import calc
	
	if type(leglst)==list:
		labels=iter(leglst)
	
	for dlst in dlsts:
		dats=[]
		for shot in dlst:
			data=calc(abbchan,shot,int,ave)
			dat=[]
			for gtime in gtimelst:
				dat+=[grep(gtime,data[0][0],data[0][1])[0]]
			dats+=[dat]
		
		lim=len(gtimelst)
		cnt=0
		
		times=[]
		means=[]
		stds=[]
		while cnt <= lim-1:
			lst=[]
			for dat in dats:
				lst+=[dat[cnt]]
			means+=[n.mean(lst)]
			stds+=[n.std(lst)]
			print n.std(lst)
			
			cnt+=1
		
		if type(xrange)==list:
			p.xlim(xrange)
		if type(yrange)==list:
			p.ylim(yrange)
		p.xlabel(data[1][0])
		p.ylabel(data[1][1])
		if type(leglst) == list:
			p.errorbar(gtimelst,means,stds,fmt="o",label=labels.next())
		else:
			p.errorbar(gtimelst,means,stds,fmt="o")
	p.legend(shadow=True,loc="best",numpoints=1)

def prof_tevo(abbchname,dlst,gtimelst,progname,xrange=None,yrange=None,PATH="/Users/yu/Desktop/",xname=r"\textit{R}_{\huge \textsf{TP}}\ \textsf{[mm]}"
            ,yname=None,leglst=None,figsize=(9,9),loc="best",tick=0,bor=None,fit=None,sdev=None,pointsize=3,
            int=0.01,ave=0.02,RAW=0,pfc = ""):
    from calc import calc
    from useful import abbchan
    from numpy import where,array,arange,polyfit,polyval,savetxt,transpose,mean,std,append
    from pylab import plot,xticks,yticks,xlim,ylim,xlabel,ylabel,figure,plot,savefig,rc,annotate,legend,rcParams,axes,draw,errorbar
    from subprocess import call
#    rc("text",usetex=True)
    rcParams["legend.fontsize"]=20
    rcParams["axes.linewidth"]=6
    rcParams["xtick.major.pad"]=12
    rcParams["ytick.major.pad"]=12
    
    call(["mkdir",PATH])

    
    if RAW == 0:
		RAWorAVE = "_int%s_ave%s" %(int,ave)
    else:
		RAWorAVE = "_RAW"
    
    	
    colgen=iter(["r","y","g","b","black","c","m","pink","b","b","white"])
    
    gylst=[]
    shotlst=[]
    dlst = sorted(dlst, key = lambda x:x[1])
    ax=figure(figsize=figsize).add_axes([0.15,0.15,0.8,0.8])
    if tick == 1:
	    if type(xrange) == list:
	    	if len(xrange)==3:
	    		xdivision=xrange[2]
	    	else:
	    		xdivision=None
	    	xlimit=arange(xrange[0],xrange[1],xdivision)
	    	
	    	xticks(xlimit,xlimit,fontsize=30)
	    
	    if type(yrange) == list:
	    	if len(yrange)==3:
	    		ydivision=yrange[2]
	    	else:
	    		ydivision=None
	    	
	    	ylimit=arange(yrange[0],yrange[1],ydivision)
	    	yticks(ylimit,ylimit,fontsize=30)
	    	

        
        
    paralst=array([])
    shotlst=array([])
    gylst=array([])
    num=0
    a=[]

    gtmin = gtimelst[0]
    gtmax = gtimelst[1]
    gtint = gtimelst[2]

    gtime = gtmin
    cnt = 0
    
    if xrange != None:
		xlim(xrange[0],xrange[1])
    if yrange != None:
		ylim(yrange[0],yrange[1])
		
    while gtime <= gtmax:
		if type(leglst) == list:
			label=iter(leglst)
		elif leglst == 0:
			pass
		else:
			a=range(len(gtimelst))
			b=map((lambda x: "datalist%s" %(x+1)),a)
			label=iter(b)
		gtime += gtint
	
    gtime = gtmin
    gtlst=arange(gtimelst[0],gtimelst[1],gtimelst[2])
    for gtime in gtlst:
    	qwe = 0
    	for dl in dlst:
        	para = dl[1]
    		if len(where(paralst==para)[0]) == 0:
    			paralst=append(paralst,para)
            
        	print dl[0]
        	xy=calc(abbchname,dl[0],int=int,ave=ave,RAW=RAW)

        	params=grep(gtime,xy[0][0],xy[0][1])
       		gylst=append(gylst,params)
        	shotlst=append(shotlst,dl[1])
        mdatlst=array([])
        stdatlst=array([])
       
        if sdev == 1:
        	for para in paralst:
        		dat=gylst[where(shotlst==para)[0]]
        		mdat=mean(dat)
        		stdat=std(dat)
        		mdatlst=append(mdatlst,mdat)
        		stdatlst=append(stdatlst,stdat)
        		
        		
        
            
#        print shotlst
#        print gylst
        if sdev == 1:
	        if leglst == 0:

	        	ax.errorbar(paralst,mdatlst,stdatlst,fmt="o",markersize=pointsize)#,c=colgen.next())
	        else:
	        	ax.errorbar(paralst,mdatlst,stdatlst,fmt="o",markersize=pointsize,label=str(gtime))
	        if type(fit)==int:
	        	a=polyfit(paralst,mdatlst,fit)
	        	fity=polyval(a,paralst)
	        	ax.plot(paralst,fity)
	        	
	        	
        
        else:
        		
	        if leglst == 0:
	        	ax.plot(shotlst,gylst,"o",markersize=pointsize,c=colgen.next())
	        else:
	        	ax.plot(shotlst,gylst,"o",markersize=pointsize,c=colgen.next(),label=str(gtime))
	        if type(fit)==int:
	        	a=polyfit(shotlst,gylst,fit)
	        	fity=polyval(a,shotlst)
	        	ax.plot(shotlst,fity)
	        
        savetxt("%sgt%s_%s_%s%s_%s.dat" %(PATH,gtime,xname,yname,RAWorAVE,pfc),transpose((paralst,mdatlst,stdatlst)))
	        	
        shotlst,gylst,paralst,mdatlst,stdatlst=array([]),array([]),array([]),array([]),array([])
        
        cnt += 1
     
      

	
    xlabel(xname,fontsize=30)
    if type(yname) == str:
        ylabel(yname,fontsize=30)
    else:
        ylabel(xy[1][1],fontsize=30,fontproperties="Helvetica")
    
    if leglst != 0:
    	legend(shadow=True,loc=loc,numpoints=1)
    	
    if bor == 1:
    	boder(ax)
    draw()

def prof_tevo2(abbchname,dlst,gtimelst,progname,xrange=None,yrange=None,PATH="/Users/yu/Desktop/",xname=r"\textit{R}_{\huge \textsf{TP}}\ \textsf{[mm]}"
            ,yname=None,leglst=None,figsize=(9,9),loc="best",tick=0,bor=None,fit=None,sdev=None,pointsize=3,
            int=0.01,ave=0.02,RAW=0,pfc = ""):
	
    from calc import calc
    from useful import abbchan
    from numpy import where,array,arange,polyfit,polyval,savetxt,transpose,mean,std,append
    from pylab import plot,xticks,yticks,xlim,ylim,xlabel,ylabel,figure,plot,savefig,rc,annotate,legend,rcParams,axes,draw,errorbar
    from subprocess import call
#    rc("text",usetex=True)
    rcParams["legend.fontsize"]=20
    rcParams["axes.linewidth"]=6
    rcParams["xtick.major.pad"]=12
    rcParams["ytick.major.pad"]=12
    
    call(["mkdir","-p",PATH])

    
    if RAW == 0:
		RAWorAVE = "_int%s_ave%s" %(int,ave)
    else:
		RAWorAVE = "_RAW"
    
    	
    colgen=iter(["r","y","g","b","black","c","m","pink","b","b","white"])
    
    gylst=[]
    shotlst=[]
    dlst = sorted(dlst, key = lambda x:x[1])
    ax=figure(figsize=figsize).add_axes([0.15,0.15,0.8,0.8])
    if tick == 1:
	    if type(xrange) == list:
	    	if len(xrange)==3:
	    		xdivision=xrange[2]
	    	else:
	    		xdivision=None
	    	xlimit=arange(xrange[0],xrange[1],xdivision)
	    	
	    	xticks(xlimit,xlimit,fontsize=30)
	    
	    if type(yrange) == list:
	    	if len(yrange)==3:
	    		ydivision=yrange[2]
	    	else:
	    		ydivision=None
	    	
	    	ylimit=arange(yrange[0],yrange[1],ydivision)
	    	yticks(ylimit,ylimit,fontsize=30)
	    	

        
        
    paralst=array([])
    shotlst=array([])
    gylst=array([])
    num=0
    a=[]

    gtmin = gtimelst[0]
    gtmax = gtimelst[1]
    gtint = gtimelst[2]

    gtime = gtmin
    cnt = 0
    
    if xrange != None:
		xlim(xrange[0],xrange[1])
    if yrange != None:
		ylim(yrange[0],yrange[1])
		
    while gtime <= gtmax:
		if type(leglst) == list:
			label=iter(leglst)
		elif leglst == 0:
			pass
		else:
			a=range(len(gtimelst))
			b=map((lambda x: "datalist%s" %(x+1)),a)
			label=iter(b)
		gtime += gtint
	
    gtime = gtmin
    gtlst=arange(gtimelst[0],gtimelst[1],gtimelst[2])
    xylst=[]
    for dl in dlst:
    	para = dl[0]
        xylst+=[calc(abbchname,dl[0],int=int,ave=ave,RAW=RAW)]
    
    
    for gtime in gtlst:
    	cnt = 0
    	qwe = 0
    	for dl in dlst:
        	para = dl[1]
        	if len(where(paralst==para)[0]) == 0:
        		paralst=append(paralst,para)
        	params=grep(gtime,xylst[cnt][0][0],xylst[cnt][0][1])
        	gylst=append(gylst,params)
        	shotlst=append(shotlst,dl[1])
        	cnt += 1
        mdatlst=array([])
        stdatlst=array([])
       
        if sdev == 1:
        	for para in paralst:
        		dat=gylst[where(shotlst==para)[0]]

        		mdat=mean(dat)
        		stdat=std(dat)
        		mdatlst=append(mdatlst,mdat)
        		stdatlst=append(stdatlst,stdat)
        		
        		
        
            
#        print shotlst
#        print gylst
        if sdev == 1:
	        if leglst == 0:

	        	ax.errorbar(paralst,mdatlst,stdatlst,fmt="o",markersize=pointsize)#,c=colgen.next())
	        else:
	        	ax.errorbar(paralst,mdatlst,stdatlst,fmt="o",markersize=pointsize,label=str(gtime))
	        if type(fit)==int:
	        	a=polyfit(paralst,mdatlst,fit)
	        	fity=polyval(a,paralst)
	        	ax.plot(paralst,fity)
	        	
	        	
        
        else:
        		
	        if leglst == 0:
	        	ax.plot(shotlst,gylst,"o",markersize=pointsize,c=colgen.next())
	        else:
	        	ax.plot(shotlst,gylst,"o",markersize=pointsize,c=colgen.next(),label=str(gtime))
	        if type(fit)==int:
	        	a=polyfit(shotlst,gylst,fit)
	        	fity=polyval(a,shotlst)
	        	ax.plot(shotlst,fity)
	        
        savetxt("%sgt%s_%s_%s%s_%s.dat" %(PATH,gtime,xname,yname,RAWorAVE,pfc),transpose((paralst,mdatlst,stdatlst)))
        shotlst,gylst,paralst,mdatlst,stdatlst=array([]),array([]),array([]),array([]),array([])
        
        cnt += 1
     
      

	
    xlabel(xname,fontsize=30)
    if type(yname) == str:
        ylabel(yname,fontsize=30)
    else:
        ylabel(xy[1][1],fontsize=30,fontproperties="Helvetica")
    
    if leglst != 0:
    	legend(shadow=True,loc=loc,numpoints=1)
    	
    if bor == 1:
    	boder(ax)
    draw()
    
   
    	
		
 
class test():
    def __init__(self,d=3,adf="df", asdf="dfgg"):
        self.g=method_history(self)
        print "helo"

    def hua(self):
        print "noh"
        self.g.input()
    def hoa(self):
        print "iiinoh"
        self.g.input()
    def uuu(self):
        print "ajad"
    def te(self):
        self.g.execute_all()

#f= test(d=34)
#f.hua()
#f.hoa()
#f.hua()
#f.hua()
#f.hua()
#f.hua()
#f.hoa()
#f.hoa()
#f.hoa()
#f.uuu()
#input("*************")
#f.te()

        
        
