from subprocess import call, Popen, PIPE
from os import mkdir


class datmanage():  
    def __init__(self):
        self.paradic = {"rtp":"$R_{\rm TP}$"}
        self.datdir = "/Users/yu/datmanage"
        p = Popen(["ls",self.datdir], stdout = PIPE)
        if len(p.stdout.read()) == 0:
            mkdir(self.datdir)
    
    def showdic(self):
        print self.paradic
    
    def fpath(self, shot):
        fpath = "%s/%s.param"%(self.datdir, shot)
        return fpath 
        
    def input(self, shots, datlst):
        #data list is composed as follows
        #datlst = [["rtp", 98], ["Zmp", 86], ...]
        if type(shots) == float or type(shots) == int or type(shots) == str:
            shots = [shots]
        for  shot in shots:
            self.fname = "%s/%s.param" %(self.datdir, shot)
            o = open(self.fname, "w")
            for dat in datlst:
                o.write("%s %s\n" %(dat[0], dat[1]))
            o.close()
    
    def showpara(self, shot):
        path = self.fpath(shot)
        o = open(path)
        for line in o:
            print line
    
    def seek(self, datlst):
        p = Popen(["ls", self.datdir], stdout = PIPE)
        paraflst = p.stdout.read().split()
        retlst = []
        length = len(datlst)
        for paraf in paraflst:
            o = open("%s/%s" %(self.datdir,paraf))
#            print paraflst
#            input()
#            print paraf
            eval = 0
            for line in o:
                paravals = line.split()
#                print line
#                input()
                for pa,va in datlst:
                    print pa,paravals[0]
                    if paravals[0] == pa:
                        if float(paravals[1]) == float(va):
                            eval += 1
                            print eval
                            
            if eval == length:
                retlst += [paraf[:-6]]

#                        return paraf[:-6]
            o.close()
        print retlst
        return retlst
                 

a=datmanage()
a.input(80888,[["rtp",98],["zmp",323],["ilab_heat",22.8]])
a.input(80838,[["rtp",98],["zmp",323],["ilab_heat",22.7]])
a.input(82388,[["rtp",99],["zmp",323],["ilab_heat",22.8]])
a.input([40884,80234,94323],[["rtp",98],["zmp",322],["ilab_heat",22.8]])
a.showpara(80888)
a.seek([["rtp", 98],["zmp",323],["ilab_heat",22.8]])
