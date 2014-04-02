from modules.numerical_utils.multidimensional_util.handle_3d import handle_3d
from modules.numerical_utils.multidimensional_util.handle_4d import handle_4d
from modules.numerical_utils.multidimensional_util.handle_5d import handle_5d
from modules.essential_utils.file_util import *
from modules.essential_utils.dir_util import *
#from modules.heliac_utils.heliac_datamanage import *
#from modules.heliac_utils.heliac_data_util_wfcxx import *
#from calctools import *
from modules.heliac_utils.heliac_data_util import *
import glob as g

class heliac_param_util():
    namedic={
        "pc": r"\qI\Q\ss\z{}\v{} [A]",
        "pchs": r"\qI\Q\ss\z{}\v{} [A]",
        "pb": r"\qV\Q\s+\z{}\v{} [V]",
        "pbhs": r"\qV\Q\s+\z{}\v{} [V]",
        "vfe": r"\qV\Q\sfe-diamag\z{}\v{} [V]",
        "vfi": r"\qV\Q\sfi-diamag\z{}\v{} [V]",
        "vfehs": r"\qV\Q\sfe-diamag\z{}\v{} [V]",
        "vfihs": r"\qV\Q\sfi-diamag\z{}\v{} [V]",
        "vf": r"\qV\Q\sf\z{}\v{} [V]",
        "vs": r"\qV\Q\ss\z{}\v{} [V]",
        "te": r"\qT\Q\se\z{}\v{} [eV]",
        "ne": r"\qn\Q\se\z{}\v{} [10\S12\z{}\v{}cm\S-3\z{}\v{}]",
        "nel": r"\qV\Q\snel\v{}\z{} [V]",
        "ccc": r"\qI\Q\sccc\v{}\z{} [A]",
        "vcc": r"\qI\Q\svcc\v{}\z{} [A]",
        "tcc": r"\qI\Q\stcc\v{}\z{} [A]",
        "ha": r"\qI\Q\s\xa\v{}\z{} [V]",
        "ot": r"\qV\Q\sloop\v{}\z{} [V]",
        "is": r"\qI\Q\sex\v{}\z{} [A]",
        "vlab": r"\qV\Q\sE\v{}\z{} [V]",
        "ilab": r"\qI\Q\sE\v{}\z{} [A]",
        "ism1": r"\qI\Q\ss_mach_upper\v{}\z{} [A]",
        "ism2": r"\qI\Q\ss_mach_lower\v{}\z{} [A]",
        "he728": r"\qI\Q\sHe_728\v{}\z{} [V]",
        "he667": r"\qI\Q\sHe_667\v{}\z{} [V]",
        "he468": r"\qI\Q\sHe_468\v{}\z{} [V]",
        "bvm": r"\qV\Q\sbias_mach\v{}\z{} [V]",
        "vlim": r"\qI\Q\sLimiter\v{}\z{} [A]",
        "ism1": r"\qI\Q\ss_Mach_upper\v{}\z{} [A]",
        "ism2": r"\qI\Q\ss_Mach_lower\v{}\z{} [A]",
        "ismu1": r"\qI\Q\ss_Mach1_upper\v{}\z{} [A]",
        "ismd1": r"\qI\Q\ss_Mach1_lower\v{}\z{} [A]",
        "ismu2": r"\qI\Q\ss_Mach2_upper\v{}\z{} [A]",
        "ismd2": r"\qI\Q\ss_Mach2_lower\v{}\z{} [A]",
        "ismu3": r"\qI\Q\ss_Mach2_upper\v{}\z{} [A]",
        "ismd3": r"\qI\Q\ss_Mach3_lower\v{}\z{} [A]",
        "mpcr1": r"\qR\Q\sMach1\v{}\z{} [A]",
        "mpcr2": r"\qR\Q\sMach2\v{}\z{} [A]",
        "mpcr3": r"\qR\Q\sMach3\v{}\z{} [A]",
        "pc2": r"\qI\Q\ss2\z{}\v{} [A]",
        "pb2": r"\qV\Q\s+2\z{}\v{} [A]",
        "vfe": r"\qV\Q\sfe-diamag\z{}\v{} [V]",
        "vfi": r"\qV\Q\sfi-diamag\z{}\v{} [V]",
        "vpd": r"\qV\Q\selectrode_PdAu\z{}\v{} [V]",
        "ipd": r"\qI\Q\selectrode_PdAu\z{}\v{} [A]",
        }

    def get_chname(self, ch):
        if ch in self.namedic:
            return self.namedic[ch]
        else:
            return "No name"
        
    def set_paraname(self, ch, gnum=0, xlabel="Time [ms]"):
        self.set_xlabel(xlabel, gnum)
        self.set_ylabel(self.get_chname(ch), gnum)

def ave_tmp(x,y, itvl, AVE):
    from numpy import array, mean
    from decimal import Decimal

    dt = (x[1] - x[0])
    intelm = int(Decimal(str(itvl / dt)))
    averange = int(Decimal(str(AVE / (2 * dt))))

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
    #self.ave = handle_3d(array(x_ave), array(y_ave))
    return array(x_ave),array(y_ave)

class fish(handle_3d, heliac_param_util):
    def __init__(self, shot=None, ch=None, itvl=0.01, wid=0.1, raw=0, para=None):
        self.pklpath=home()+"/pkldir"
        handle_3d.__init__(self, x=None,y=None, z=None)
        ifnonemkdir(self.pklpath)
        if not (shot is None): 
            self.dset_wp(shot, ch, itvl, wid, raw, para)

    def dset(self, shot, ch, itvl=0.01, wid=0.1, raw=0, para=None):
        self.hist.input()
        self.set_paraname(ch, gnum=0)
#        x,y = get_xy(shot, ch)
        pkl = "%s/%s_%s.pkl" %(self.pklpath, shot, ch)
        dmp = handle_3d()
        if len(g.glob(pkl)) == 0:
            [[x,y]] = get_multixy([shot], ch, itvl, wid, 1)
            z = None
            dmp.dinput([x,y,z])
            dmp.dump_pickle(pkl)
        else:
            dmp.load_pickle(pkl)
            x,y,z = dmp.getdata()

        if raw != 1:
            x,y = ave_tmp(x,y,itvl,wid)

        self.xname = "tmp"
        self.yname = "tmp"
            
        z = ones(len(x)) * para if not para is None else None
        if z is None:
            self.set_data(x,y) 
        else:
            self.set_data(x,y,z)  

    def dset_wfcxx(self, shot, ch, itvl=0.01, wid=0.1, raw=0, para=None):
        self.hist.input()
        #self.set_paraname(ch, gnum=0)
#        x,y = get_xy(shot, ch)
        pkl = "%s/%s_%s.pkl" %(self.pklpath, shot, ch)
        dmp = handle_3d()
        if len(g.glob(pkl)) == 0:
            x,y = gdat(shot, ch)
            z = None
            dmp.dinput([array(x),array(y),z])
            #dmp.dump_pickle(pkl)
        else:
            dmp.load_pickle(pkl)
            x,y,z = dmp.getdata()

        if raw != 1:
            x,y = ave_tmp(x,y,itvl,wid)

        self.xname = "tmp"
        self.yname = "tmp"
            
        z = ones(len(x)) * para if not para is None else None
        if z is None:
            self.set_data(x,y) 
        else:
            self.set_data(x,y,z)  
            
    def dset_wp(self, shot, ch, itvl=0.01, wid=0.1, raw=0, para=None):
        self.hist.input()
        self.set_paraname(ch, gnum=0)
        [[x,y],[xn,yn]] = calc(ch, shot, itvl=itvl, ave=wid, RAW=raw)
        self.xname = xn
        self.yname = yn
        if para: 
            z = ones(x.size, dtype=double) * para
            self.set_data(x, y, z)
        else:
            self.set_data(x, y)

    def crosspara(self, shot, ch1, ch2, slst=[26,36], xy=True, abcs=0, lgtd=1, itvl=0.01, wid=0.1, raw=0, para=None):
        obj1 = fish(shot, ch1, itvl, wid, raw, para)
        obj2 = fish(shot, ch2, itvl, wid, raw, para)

        obj1.combine(obj2, slst, xy, abcs, lgtd)

        self.x = obj1.cmb.x
        self.y = obj1.cmb.y
        self.z = obj1.cmb.z

class multifish(handle_4d):
    def __init__(self, shots=None, chs=None, itvl=0.01, wid=0.1, raw=0, para=None):
        self.pklpath=home()+"/pkldir"
        handle_4d.__init__(self)
        if not (shots is None): 
            self.dset(shots, chs, itvl, wid, raw, para)

    def dset_fast(self, shots, chs, itvl=0.01, wid=0.1, raw=0):
        self.hist.input()
        tmparrs = get_multixy(shots, chs, itvl, wid, raw)
        tmplst = []
        for arr in tmparrs:
            tmplst += [handle_3d(arr[0],arr[1])]
            #deallo_xy()
        self.set_multi(tmplst) 

    def crosspara(self, shots, chs, slst=[26,36], xy=True, abcs=0, lgtd=1, itvl=0.01, wid=0.1, raw=0, para=None, shch="sh"):

        shchlst = [shot, chs]
        objlst = []
        for param1 in chs if shch=="sh" else shots:
            for param2 in shots if shch=="sh" else chs:
                if shch == "sh":
                    shot = param1
                    ch1, ch2 = param2
                else:
                    shot = param2
                    ch1, ch2 = param1
                obj=fish()
                obj.crosspara(shot, ch1, ch2, slst, xy, abcs, lgtd, itvl, wid, raw, para)
                objlst += [obj]

        self.set_multi(objlst)

    def dset_wp(self, shots, chs, itvl=0.01, wid=0.1, raw=0, para = None, zadj=None, shch="sh"):
        self.hist.input()
        tmparrs =[]
        chs = chs.split(",")
        pdic = {"sh":shots, "ch":chs}
        opp = {"sh":"ch", "ch":"sh"}
        i = 0
        while i < len(pdic[opp[shch]]):
            j = 0
            while j < len(pdic[shch]):
               # pkl = "%s/%s_%s.pkl" %(self.pklpath, shot, ch)
               #tmparr = gt_multixy([shot], ch, itvl, wid, 1)
                if shch == "sh":
                    csh = j
                    cch = i
                else:
                    csh = i
                    cch = j
                
                [tmparr,[xn,yn]] = calc(chs[cch], shots[csh], itvl=itvl, ave=wid, RAW=raw)
                tmparrs += [tmparr]
                j += 1
            i += 1
                #tmparrs += [get_multixy([shot], ch, itvl, wid, raw)]
                
        tmplst = []
        if type(para) != type(None): pgen = iter(para)
        for arr in tmparrs:
       #      if raw != 1:
       #         arr = [ave_tmp(arr[0][0],arr[0][1], itvl, wid)]
            tmplst += [handle_3d(arr[0],arr[1])] if para is None else [handle_3d(arr[0],arr[1], pgen.next()*ones(len(arr[0])))]
            #deallo_xy()
        self.set_multi(tmplst) 
        self.T = True

    def dset(self, shots, chs, itvl=0.01, wid=0.1, raw=0, para = None, zadj=None):
        self.hist.input()
        tmparrs =[]
        chs = chs.split(",")
        for ch in chs:
            for shot in shots:
                pkl = "%s/%s_%s.pkl" %(self.pklpath, shot, ch)
                dmp = handle_3d()
                if len(g.glob(pkl)) == 0:
                    tmparr = get_multixy([shot], ch, itvl, wid, 1)
                    dmp.dinput([tmparr[0][0], tmparr[0][1],None])
                    dmp.dump_pickle(pkl)
                    tmparrs += [tmparr]
                else:
                    dmp.load_pickle(pkl)
                    x,y,z = dmp.getdata()
                    tmparrs += [[[x,y]]]
                #tmparrs += [get_multixy([shot], ch, itvl, wid, raw)]
                
        tmplst = []
        if type(para) != type(None): pgen = iter(para)
        for arr in tmparrs:
            if raw != 1:
                arr = [ave_tmp(arr[0][0],arr[0][1], itvl, wid)]
            tmplst += [handle_3d(arr[0][0],arr[0][1])] if para is None else [handle_3d(arr[0][0],arr[0][1], pgen.next()*ones(len(arr[0][0])))]
            #deallo_xy()
        self.set_multi(tmplst) 
        self.T = True

    def dset_txt(self, rfile, ch, itvl=0.01, wid=0.1, raw=0, comment="#"):
        self.hist.input()
        o = open(rfile)

        lst = o.read().strip().split("\n")
        map(lambda x: lst.pop(lst.index(x)) if x[0] == comment else None, lst)
        lst = [[float(y) for y in x.split()] for x in lst]
        lst = sorted(lst, key=lambda x: x[1])
        shots, para = array(lst).transpose()
        shots = array(shots, dtype = int)
        para = array(para, dtype = double)
        self.dset(shots, ch, itvl, wid, raw, para)
        o.close()
    
    def dset_txt_wp(self, rfile, ch, itvl=0.01, wid=0.1, raw=0, comment="#"):
        self.hist.input()
        o = open(rfile)

        lst = o.read().strip().split("\n")
        map(lambda x: lst.pop(lst.index(x)) if x[0] == comment else None, lst)
        lst = [[float(y) for y in x.split()] for x in lst]
        lst = sorted(lst, key=lambda x: x[1])
        shots, para = array(lst).transpose()
        shots = array(shots, dtype = int)
        para = array(para, dtype = double)
        self.dset_wp(shots, ch, itvl, wid, raw, para)
        o.close()
    
    def dset_mvelo_txt_wp(self, rfile, itvl=0.01, wid=0.1, raw=0, comment="#"):
        self.hist.input()
        o = open(rfile)

        lst = o.read().strip().split("\n")
        map(lambda x: lst.pop(lst.index(x)) if x[0] == comment else None, lst)
        lst = [[float(y) for y in x.split()] for x in lst]
        lst = sorted(lst, key=lambda x: x[1])
        shots, para = array(lst).transpose()
        shots = array(shots, dtype = int)
        para = array(para, dtype = double)

        tmpshots = []
        tmppara = []
        for p in para:
            tmppara += [p+3, p+8, p+13]
            
        para = tmppara
        #shots = append(array([],dtype=int), [[x,x,x] for x in shots])
        self.dset_wp(shots, "mvelo1,mvelo2,mvelo3", itvl, wid, raw, para, shch="ch")
        o.close()
    def dset_mach_txt_wp(self, rfile, itvl=0.01, wid=0.1, raw=0, comment="#", imach=False):
        self.hist.input()
        o = open(rfile)

        lst = o.read().strip().split("\n")
        map(lambda x: lst.pop(lst.index(x)) if x[0] == comment else None, lst)
        lst = [[float(y) for y in x.split()] for x in lst]
        lst = sorted(lst, key=lambda x: x[1])
        shots, para = array(lst).transpose()
        shots = array(shots, dtype = int)
        para = array(para, dtype = double)

        tmpshots = []
        tmppara = []
        for p in para:
            tmppara += [p+3, p+8, p+13]
            
        para = tmppara
        #shots = append(array([],dtype=int), [[x,x,x] for x in shots])
        chs = "mpcr1,mpcr2,mpcr3" if not imach else "imach1,imach2,imach3"
        self.dset_wp(shots, chs, itvl, wid, raw, para, shch="ch")
        self.transpose()
        sort_idx = argsort(self.z[0])
        self.x = self.x[:, sort_idx]
        self.y = self.y[:, sort_idx]
        self.z = self.z[:, sort_idx]
        o.close()

    def crosspara(self, shotlst, chlst, slst=[26,36], xy=True, abcs=0, lgtd=1, itvl=0.01, wid=0.1, raw=0, para=None):
        objlst = []
        for ch1, ch2 in chlst:
            for shot in shotlst:
                obj = fish()
                obj.crosspara(shot, ch1, ch2, slst, xy, abcs, lgtd, itvl, wid, raw, para)
                objlst += [obj]
       
        self.set_multi(objlst)
        

    def CCD_loadtxt(self, path):
        if type(path) == str:
            path = [path]
        
        xlst = []
        ylst = []
        dylst = []
        for pa in path:
            arrs = loaddat(pa)
            xlst += [[arrs[0], arrs[0], arrs[0]]]
            ylst += [arrs[1:4]]
            dylst += [arrs[4:]]

        xlst = crush_lst(xlst)
        ylst = crush_lst(ylst)
        dylst = array(crush_lst(dylst))
        self.dinput([xlst, ylst, None])
        self.err = dylst
        self.T = True

        

    def CCD_view(self, sepnum=1, dump=False):
        self.set_mkall(0.5, [2,4], [1,4])
        self.view(layout="triple", abcs=0,lgtd=1, T=True, sepnum=sepnum, dirname="tmpdir", filename="tmp", device="pdf", dump=True)
        

#class fish_school(comparison):
#    def __init__(self, datlst=None):
#        comparison.__init__(self, datlst=datlst)
#        
#    def CCD_loadtxt(self):
        


class triple_manage():
    def __init__(self, shot, itvl=0.01, wid=0.1, raw=False, stime=(26, 36), offset=(11.5,18)):
        self.shot = shot
        self.stime = stime
        self.itvl = itvl
        self.wid = wid
        self.raw = raw
        self.offset = offset
#        self.calc_all()
        self.pc = None
        self.pb = None
        self.vfi = None
        self.vfe = None
        self.vf = None
        self.te = None
        self.ne = None
        self.vs = None
        self.S = 9.412211590e-7
        self.c = 1.60217733e-19
        self.mi = 1.67262158e-27
        self.alpha = 4

    def calc_all(self):
        self.calc_te()
        self.calc_ne()
        self.calc_vf()
        self.calc_vs()

    def calc_vf(self):
        if self.vfi is None:
            self.vfi = fish(self.shot, "vfi", self.itvl, self.wid, self.raw)
            self.vfi.zero_adj(self.offset)
            self.vfi = self.vfi.zadj
            self.vfi.slice_arr(self.stime)
            self.vfi = self.vfi.slice
        if self.vfe is None: 
            self.vfe = fish(self.shot, "vfe", self.itvl, self.wid, self.raw)
            self.vfe.zero_adj(self.offset)
            self.vfe = self.vfe.zadj
            self.vfe.slice_arr(self.stime)
            self.vfe = self.vfe.slice
        
        x = self.vfi.x
        y = (self.vfi.y + self.vfe.y) / 2

        self.vf = handle_3d(x, y)


    def calc_pc(self):
        if self.pc is None: 
            self.pc = fish(self.shot, "pc", self.itvl, self.wid, self.raw)
            self.pc.zero_adj(self.offset)
            self.pc = self.pc.zadj
            self.pc.slice_arr(self.stime)
            self.pc = self.pc.slice

    def calc_pb(self):
        import time as t
        if self.pb is None: 
            self.pb = fish(self.shot, "pb", self.itvl, self.wid, self.raw)
            self.pb.zero_adj(self.offset)
            self.pb = self.pb.zadj
            self.pb.punch_out([self.offset],inv=True)
            self.pb.pout.gnufit("a+b*sin(2*pi/20*x+c)", [0.01, 0.01, 0.01], itvl=self.itvl,show=False )
            print self.shot
            print "**************"
            self.pb.y -= self.pb.pout.gnu.fitpara[0]
            self.pb.slice_arr(self.stime)
            self.pb = self.pb.slice

    def calc_te_simple(self):
        self.calc_pb()

        if self.vf is None: self.calc_vf()

        x = self.pb.x
        y = (self.pb.y - self.vf.y) / log(2)
        self.te_simple = handle_3d(x, y)

    def calc_te(self, N=100, bias=91.8):
        self.calc_pb()

        if self.vf is None: self.calc_vf()

        x = self.pb.x
        self.vd2 = handle_3d(x, self.pb.y - self.vf.y)
        y = self.vd2.y / log(2)
        for i in range(N):
            y = self.vd2.y / log(2 / (exp(- bias/ y) + 1))
        self.te = handle_3d(x, y)

    def calc_ne(self):
        self.calc_pc()
        self.calc_te()

        phi = exp(- self.pb.y / self.te.y)

        x = self.pb.x
        #y = exp(0.5) * (self.pc.y / self.c / self.S) * (self.mi / self.te.y / self.c) ** 0.5  * (1 / (phi - 1))
        y = exp(0.5) * (- self.pc.y / self.c / self.S) * (self.mi / self.te.y / self.c) ** 0.5  
        y /= 1e18
        self.ne = handle_3d(x, y)

        self.unit = "[10^18 m^-3]"
        
    def calc_vs(self):
        self.calc_vf()
        self.calc_te()

        x = self.vf.x
        y = self.vf.y + self.alpha * self.te.y

        self.vs = handle_3d(x, y)

    def view(self):
        self.all = handle_4d([self.te, self.ne, self.vf, self.vs])
        self.all.set_string(r"#%s" %self.shot,(0.55,0.95), charsize=2)
        self.all.set_ylabel(r"\qT\Q\se\v{}\z{} [eV]", 0)
        self.all.set_ylabel(r"\qn\Q\se\v{}\z{} [10\S12\v{}\z{} cm\S-3\v{}\z{}]", 1)
        self.all.set_ylabel(r"\qV\Q\sf\v{}\z{} [V]", 2)
        self.all.set_ylabel(r"\qV\Q\ss\v{}\z{} [V]", 3)
        self.all.set_xlabel("Time [ms]", 0)
        self.all.set_xlabel("Time [ms]", 1)
        self.all.set_xlabel("Time [ms]", 2)
        self.all.set_xlabel("Time [ms]", 3)
        self.all.view("quad", sepnum=1)


#class dish(handle_5d):
#    def __init__(self, datlst=None):
#        handle_5d.__init__(datlst):
#
#    def triple_datlst(self, ):
        



    #def calc_ne(self):
    #def calc_vf(self):
    #def calc_vs(self):
#    def checkdata(self, dname="raw"):
#        x,y,z = self.get_data(dname)
#        self.set_xydata(x,y)
#        self.open_grace()
#
#    def cnv_rho(dfile, mcirc=2000):
#        o = open()


#a = fish(80000,"pc")
#a = multifish()
#a.dset([80259,80000,80000,80000],"pc,rf,rf,pc,vfe,vfi",itvl=0.01,wid=2)

#b=fish()
#b.dset(80000,"pc")
#b.view()
#a.colmnview()
#a.checkdata()
