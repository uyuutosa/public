from useful import *
from pylab import *

def comp_shot(shots,ch,xrange=[26,36],yrange=None,int=0.01,ave=0.03,leglst=None,mark=None,RAW=0,
            fig="pdf",figsize=(9,12),gtype=0,log=0,minus=None,dname=None,loc="best",e667=881737.765546,e728=2003465.38034,
            datapath=None):
    from graph import graph8,graph11
    from calc import calc3,calc_triple,calc_mach,spec,calc
    from numpy import array,savetxt,transpose
    import pylab
    colgen=iter(["r","y","g","b","black","c","m","pink","b","b","white"])
#    colgen=iter(["r","r","r","r","b","b","b","b","b","b","white"])
#    pylab.rc("text",usetex=True)

    num=1
    xylst=[]
    shottag=""
    for shot in shots:
        raw=RAW
        xylst += [calc(ch,shot,int,ave,RAW)]
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
        savetxt(datapath+"%s%sMEAN_INT%s_AVE%s.txt" %(shottag,ch,int,ave),transpose(data))
    else:
        savetxt(datapath+"%s%sRAW.txt" %(shottag,ch),transpose(data))

def comp_ch(shot,chlst,xrange=[26,36],yrangelst=None,int=0.01,ave=0.03,RAW=None,fig="pdf",
        gtype=0,figsize=(9,12),PICPATH=None,log=0,dress=0,datapath=None):
    from graph import graph9,graph10
    from calc import calc3,calc_mach,calc_triple,calc,spec
    from numpy import array,savetxt,transpose
    import pylab
    from tag import tag3
    num=0
    xylst=[]
    chtag=""
    for ch in chlst:
#        shottag+=str(shot)+"_"
        if type(RAW) == list:
            raw=RAW[num]
        else:
            raw=RAW
        xylst += [calc(ch,shot,int,ave,RAW)]
        num+=1
        chtag+=str(ch)+"_"
        if raw == 0:
            savetxt(datapath+"%s_%s_MEAN_INT%s_AVE%s.txt" %(str(shot),ch,int,ave),transpose(xylst[-1][0]))
        else:
            savetxt(datapath+"%s_%s_RAW.txt" %(str(shot),ch),transpose(xylst[-1][0]))
    if PICPATH == None:
        PICPATH=tag3("comp_ch","/Users/yu/Desktop/",shot,chlst,fig,gtype)
    if gtype == 1:
        graph10(shot,xylst,xrange,yrangelst,PICPATH,figsize,log=log,dress=dress)
    else:
        graph9(shot,xylst,xrange,yrangelst,PICPATH,figsize,log=log,dress=dress)
    pylab.draw()
def namemake(shot,ch):
    name = ""
    
    if type(ch) == list:
        for elm in ch:
            name += str(elm) + "_"
    else:
        name += str(ch) + "_"
        
    if type(shot) == list:
        for elm in shot:
            name += str(elm) + "_"
    else:
        name += str(shot) + "_"
    name = name[:-1]+".txt"
    return name

def grep(param,plst,glst):
    from numpy import array
    n = 0
    for dat in plst:


        if str(float(param)) == str(float(dat)):
#            print n
            return glst[n]
            break
        n+=1

def grep_num(param,plst):
    from numpy import array
    n = 0
    for dat in plst:


        if str(float(param)) == str(float(dat)):
#            print n
            return n
            break
        n+=1
    
class tevo():
    from subprocess import Popen
    from os import mkdir
    from datetime import date
    
    def __init__(self):
        from os import mkdir
        from datetime import date
        
        self.path = "/Users/yu/Desktop/"
        self.dirname = self.path+"exp"+date.today().isoformat()
        self.picdir = self.dirname+"/PICTUREDIR/"
        self.datdir = self.dirname+"/DATDIR/"
        self.confdir = self.dirname+"/CONFDIR/"
        self.stodir = self.dirname+"/STODIR/"
        self.figsize = (9,9)
        self.gtype = 1
        self.mpcrx=[26,36]
        self.mpcry=[-0.1,0.2]
        self.pcx=[26,36]
        self.pcy=[0,3]
        self.pbx=[26,36]
        self.pby=[0,3]
        self.tex=[26,36]
        self.tey=[0,3]
        self.nex=[26,36]
        self.ney=[0,3]
        self.ilabx=[26,36]
        self.ilaby=[0,3]
        self.vlabx=[26,36]
        self.vlaby=[0,3]
        self.chx=[26,36]
        self.chy=[0,3]
        self.int = 0.02
        self.ave = 0.03
        self.RAW = 1
        self.conflst=[]
        self.shotlst=[]
                
        

        try:
            o=open(self.confdir+"conf.txt")
            o.readline()
            for a in o:
                dlst = map(lambda x:x.strip(), a.split(",")[:-1])
                self.conflst += [dlst]
                self.shotlst += [dlst[0]]
            o.close()
        
        except:
            mkdir(self.dirname)
            mkdir(self.picdir)
            mkdir(self.datdir)
            mkdir(self.confdir)
            mkdir(self.stodir)
            o = open(self.confdir+"conf.txt","w")
            o.close()
            
    
    def conf(self,shot,conftag):
        CONFPATH = self.confdir+"conf_"+conftag+".txt"
        elm = grep_num(shot,self.shotlst)
        if  type(elm) == int: 
            self.shotlst.pop(elm)
            self.conflst.pop(elm)
            
        print "config %s" %shot
        confs = [str(shot)]
        question = ["Zmp?","thetamp?","Rtp?","PFC?","Bias?"]
        qnum = range(len(question))
        cnt = 0
        for q in question:
            tmp = [raw_input(q)]
            if qnum[cnt] == "":
                confs += qnum[cnt]
            else:
                confs += tmp
                qnum[cnt] = tmp
            cnt += 1
        self.conflst += [confs]
        self.shotlst += [shot]
        self.conflst = sorted(self.conflst)
        wconf = map(lambda x: ", ".join(x)+"\n",self.conflst)
        o = open(CONFPATH,"w")
        o.write("#Zmp [mm], theta[deg], Rtp[mm], Ipfc [A], Bias [V]\n")
        for wrine in wconf:
            o.write(wrine)
        o.close()
    
    def showconf(self):
        from os import listdir
        n = 0
        flst = listdir(self.confdir)
        for tmp in flst:
            print str(n) + ". " + tmp
            n +=1
        
        refile = flst[input("Which config file is showed ?")]
        o = open(self.confdir + refile)
        for a in o:
            print a 
        
    def mach(self,token=None):
        if token != None:
            shots = token
        else:
            shots = self.shotlst
            
        if type(self.shotlst) == list:
            comp_shot(shots, "mpcr",self.mpcrx,self.mpcry,
                       datapath=self.datdir,figsize=self.figsize,
                       gtype=self.gtype,int=self.int,ave=self.ave,
                       RAW=self.RAW)
            
    def pc(self,token=None):
        if token != None:
            shots = token
        else:
            shots = self.shotlst
            
        if type(self.shotlst) == list:
            comp_shot(shots, "mpcr",self.pcx,self.pcy,
                       datapath=self.datdir,figsize=self.figsize,
                       gtype=self.gtype,int=self.int,ave=self.ave,
                       RAW=self.RAW)

    def pb(self,token=None):
        if token != None:
            shots = token
        else:
            shots = self.shotlst
            
        if type(self.shotlst) == list:
            comp_shot(shots, "pb",self.pbx,self.pby,
                       datapath=self.datdir,figsize=self.figsize,
                       gtype=self.gtype,int=self.int,ave=self.ave,
                       RAW=self.RAW)
            
    def ilab(self,token=None):
        if token != None:
            shots = token
        else:
            shots = self.shotlst
            
        if type(self.shotlst) == list:
            comp_shot(shots, "ilab",self.ilabx,self.ilaby,
                       datapath=self.datdir,figsize=self.figsize,
                       gtype=self.gtype,int=self.int,ave=self.ave,
                       RAW=self.RAW)
            
    def vlab(self,token=None):
        if token != None:
            shots = token
        else:
            shots = self.shotlst
            
        if type(self.shotlst) == list:
            comp_shot(shots, "vlab",self.vlabx,self.vlaby,
                       datapath=self.datdir,figsize=self.figsize,
                       gtype=self.gtype,int=self.int,ave=self.ave,
                       RAW=self.RAW)

    def ne(self,token=None):
        if token != None:
            shots = token
        else:
            shots = self.shotlst
            
        if type(self.shotlst) == list:
            comp_shot(shots, "ne",self.nex,self.ney,
                       datapath=self.datdir,figsize=self.figsize,
                       gtype=self.gtype,int=self.int,ave=self.ave,
                       RAW=self.RAW)
            
    def te(self,token=None):
        if token != None:
            shots = token
        else:
            shots = self.shotlst
            
        if type(self.shotlst) == list:
            comp_shot(shots, "te",self.tex,self.tey,
                       datapath=self.datdir,figsize=self.figsize,
                       gtype=self.gtype,int=self.int,ave=self.ave,
                       RAW=self.RAW)

    def ha(self,token=None):
        if token != None:
            shots = token
        else:
            shots = self.shotlst
            
        if type(self.shotlst) == list:
            comp_shot(shots, "ha",self.hax,self.hay,
                       datapath=self.datdir,figsize=self.figsize,
                       gtype=self.gtype,int=self.int,ave=self.ave,
                       RAW=self.RAW)
    
    
    def pl(self,ch,token=None):
        if token != None:
            shots = token
        else:
            shots = self.shotlst
            
        if type(self.shotlst) == list:
            comp_shot(shots, ch,self.chx,self.chy,
                       datapath=self.datdir,figsize=self.figsize,
                       gtype=self.gtype,int=self.int,ave=self.ave,
                       RAW=self.RAW)
            
#    def profmach(self):
#        
    
    def wasto(self,shots):
        self.ast = shots
        line = ", ".join(map(lambda x:str(x),shots))
        o = open(self.stodir+"asto.txt","w")
        o.write(line)
        o.close() 
        
    def wbsto(self,shots):
        self.bst = shots
        line = ", ".join(map(lambda x:str(x),shots))
        o = open(self.stodir+"bsto.txt","w")
        o.write(line)
        o.close() 
    
    def wcsto(self,shots):
        self.cst = shots
        line = ", ".join(map(lambda x:str(x),shots))
        o = open(self.stodir+"csto.txt","w")
        o.write(line)
        o.close()
        
    def wdsto(self,shots):
        self.dst = shots
        line = ", ".join(map(lambda x:str(x),shots))
        o = open(self.stodir+"dsto.txt","w")
        o.write(line)
        o.close()
        
    def westo(self,shots):
        self.est = shots
        line = ", ".join(map(lambda x:str(x),shots))
        o = open(self.stodir+"esto.txt","w")
        o.write(line)
        o.close()
        
    def wfsto(self,shots):
        self.ft = shots
        line = ", ".join(map(lambda x:str(x),shots))
        o = open(self.stodir+"fsto.txt","w")
        o.write(line)
        o.close()   
        
    def reasto(self):
        o = open(self.stodir + "asto.txt")
        self.ast = o.read().split(", ") 
        
    def rebsto(self):
        o = open(self.stodir + "bsto.txt")
        self.bst = o.read().split(", ") 
        
    def recsto(self):
        o = open(self.stodir + "csto.txt")
        self.cst = o.read().split(", ") 
    
    def redsto(self):
        o = open(self.stodir + "dsto.txt")
        self.dst = o.read().split(", ")
    
    def reesto(self):
        o = open(self.stodir + "esto.txt")
        self.est = o.read().split(", ")
        
    def refsto(self):
        o = open(self.stodir + "fsto.txt")
        self.fst = o.read().split(", ")

#a=tevo()
#print a.conflst
#print a.shotlst
#a.conf(80888)
#a.conf(80888)
#print a.shotlst
#print a.conflst
#a.mach()
#
#show()
#close()