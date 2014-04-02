#!/usr/bin/env python
#-*- coding:utf-8 -*-
import Gnuplot
from subprocess import *
from datfilemanage import *
from tempfile import *
import os
from copy import *
from itertools import *

from gracemanage import * 
class gnuplotmanage(loaddatmanage):
    def __init__(self):
        loaddatmanage.__init__(self)
        self.xname = None
        self.yname = None
        self.xr = None
        self.yr = None
        self.term = "aqua"
        self.size = None
        self.debag = "debug=1"
        self.gp_init()

    def gp_init(self,):
        self.g = Gnuplot.Gnuplot()
        #self.g = Gnuplot.Gnuplot(self.debag)
    def picopen():
        call("open " + self.outpath)
        
    def multiplot(self, col, row):
        self.g("set multiplot layout %s,%s" %(col, row))

    def terminal(self, name, size=None):
        self.term = name
        cmd = "set term %s " %name 
        if size != None:
            self.size = size
        cmd += "size %scm, %scm " %self.size if self.size != None else ""
        self.g(cmd)

    def setx11(self):
        self.term = "x11"
        self.g("set term x11" )
    def wait(self):
        if self.term == "x11"  : raw_input("Please enter to close graph...")

    def setpdf(self, width=29.7, hight=21, outpath="tmp.pdf"):
        self.term = "pdf"
        self.outpath = outpath
        self.g("set term pdf enhanced " )
        #self.g("set term pdf enhanced size %scm, %scm" %(width, hight))
        self.g("set output '%s'" %outpath)
    

    def xrange(self, min, max):
        self.xr = "[%s:%s]" %(min, max)

    def yrange(self, min, max):
        self.yr = "[%s:%s]" %(min, max)
        
    def prof_evo(self, dlst):
        if type(dlst[0]) == str: #check file name or data array
            arrs = array(self.loadprofdat(dlst))
            arrs = arrs.transpose()
            #arrs = []
            #for datpath in dlst:
            #    arrs = array([arrs, loaddat(datpath, conbine = True)])
        else:
            arrs = dlst
        len(arrs)
        for arr in arrs.transpose():
            d = Gnuplot.Data(arr[0],arr[1])
            self.g.plot(d, xlabel= None, xrange= self.xr, yrange=self.yr)
        self.wait()

    def complot(self, dlst):
        if type(dlst[0]) == str: #check file name or data array
            arrs = []
            for datpath in dlst:
                arrs = array([arrs, loaddat(datpath, conbine = True, delim=",")])
        else:
            arrs = dlst
        d = []
        for x,y in arrs:
            d += [Gnuplot.Data(x, y)]
        self.g.plot(d[0], xlabel= None, xrange= self.xr, yrange=self.yr)
        self.wait()
    
            
#### ROOT ####

class rootmanage():
    def __init__(self):
        self.w = rootmacro()
        



    def draw(self):
        self.w.set_xyzdata(gnum=0, snum=0)

    def bin_modify(self):
        pass

#    def


        

class rootprop():
    def __init__(self):
        self.tmpdic = {"snum" : [],
                          "gtype" : "normal",
                          "xtics" : None,
                          "ytics" : None,
                          "xtickitvl" : None,
                          "ytickitvl" : None,
                          "xlabel" : "",
                          "ylabel" : "",
                          "xlim" : [None, None],
                          "ylim" : [None, None],
                          "zlim" : [None, None],
                          "lim" : None,
                          "legloc" : "rightup",
                          "legloctype" : "wratio",
                          "xbin" : None,
                          "ybin" : None,
                          }
        self.mkall = None
        self.lineall = None
        self.dnum = 0
        self.axnumlst = []
        self.initialize()

    def set_xbin(self, val, gnum=0):
        self.gdiclst[gnum]["xbin"] = val

    def set_ybin(self, val, gnum=0):
        self.gdiclst[gnum]["ybin"] = val

    def get_xbin(self, gnum=0):
        return self.gdiclst[gnum]["xbin"]

    def get_ybin(self, gnum=0):
        return self.gdiclst[gnum]["ybin"]

    def initialize(self):
        self.gdiclst = []
        self.decolst = []
        self.g_add() 
        self.s_add(0)

    def plot_init(self):
        self.iterstr_init()

    def iterstr_init(self):
        n = 0
        while n < len(self.decolst):
            i = 0
            if self.decolst[n][0] == "iterst":
                while i < len(self.decolst[n][1]):
                    if type(self.decolst[n][1][i]) != str:
                        self.decolst[n][1][i][1] = 0
                    i += 1
            n += 1

    def get_gnum(self):
        return len(self.gdiclst)

    def get_snum(self,gnum):
        return len(self.gdiclst[0]["snum"])

    def dcnt(self):
        self.dnum += 1

    def get_dnum(self):
        return self.dnum

    def g_add(self):
        self.gdiclst += [deepcopy(self.tmpdic)]

    def s_add(self,gnum):
        sdic = {"legend" : None,
                "marker" : None,
                "err" : None,
                "line" : None,}
        while True:
            try:
                self.gdiclst[gnum]["snum"] += [deepcopy(sdic)]
                break
            except:
                self.g_add()
#     def scnt(self, gnum):
#         gnum = str(gnum)
#         if gnum in self.gdic:
#             self.gdiclst[gnum]["snum"] += 1
#         else:
#             self.gupdate()
#             self.gdiclst.update({gnum:{"snum" : 0}})
#
#         return self.gdiclst[gnum]["snum"]

    def gnum_check(self, gnum):
        while True:
            try:
                self.gdiclst[gnum]
                break
            except IndexError:
                self.g_add()
                #raise IndexError, "Graph number %s is not defineded." %gnum
    
    def snum_check(self, gnum, snum):
        while True:
            try:
                self.gdiclst[gnum]["snum"][snum]
                break
            except:
            #except IndexError, TypeError:
                self.s_add(gnum)

    def errorbar_input(self, gnum=0, snum=0, color=1, patn=1, size=1, lwidth=2, lstyle=1, rlwidth=1, rlstyle=1):
        self.gnum_check(gnum)
        self.snum_check(gnum, snum)
        self.gdiclst[gnum]["snum"][snum]["err"] = (color, patn, size, lwidth, lstyle, rlwidth, rlstyle)

    def lineall_input(self, select=0, size=1, color=1, lstyle=1):
        self.lineall = (select, size, color, lstyle)

    def mkall_input(self, size=1, color=1, mstyle=1, fptn=[1], lwidth=[1], lstyle=[1]):
        self.mkall = (size, color, mstyle, fptn, lwidth, lstyle)

    def style_line_input(self, width=1, color=0, lstyle=1, gnum=0, snum=0):
        self.gnum_check(gnum)
        self.snum_check(gnum, snum)
        self.gdiclst[gnum]["snum"][snum]["line"] = (width, color, lstyle)

    def mk_input(self, size=1, color=0, mstyle=1, fcolor=None, fptn=1, lwidth=1, lstyle=1, gnum=0, snum=0):
        self.gnum_check(gnum)
        self.snum_check(gnum, snum)
        self.gdiclst[gnum]["snum"][snum]["marker"] = (size, color, mstyle, fcolor, fptn, lwidth, lstyle)

    def lim_input(self, xmin, xmax, ymin, ymax, gnum, tnum=6):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["lim"] = (xmin, xmax, ymin, ymax, tnum)

    def set_xlim(self, xmin, xmax, gnum=0):
        self.gdiclst[gnum]["xlim"] = [xmin, xmax]
    def set_ylim(self, ymin, ymax, gnum=0):
        self.gdiclst[gnum]["ylim"] = [ymin, ymax]
    def set_zlim(self, zmin, zmax, gnum=0):
        self.gdiclst[gnum]["zlim"] = [zmin, zmax]
        
    def get_xlim(self, gnum=0):
        return self.gdiclst[gnum]["xlim"] 
    def get_ylim(self, gnum=0):
        return self.gdiclst[gnum]["ylim"]
    def get_zlim(self, gnum=0):
        return self.gdiclst[gnum]["zlim"] 
    def get_lim(self, gnum=0):
        return self.gdiclst[gnum]["xlim"] + self.gdiclst[gnum]["ylim"] +  self.gdiclst[gnum]["zlim"] 
        
    def autolim_input(self,xarr,yarr, margin=0.1, gnum=0):
        xmin,xmax = self.autoscale(xarr, margin)
        ymin,ymax = self.autoscale(yarr, margin)
        self.prop.lim_input(xmin,xmax,ymin,ymax,gnum)

    def xlabel_input(self, xname, gnum):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["xlabel"] = xname

    def ylabel_input(self, yname, gnum):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["ylabel"] = yname
            
    def leg_input(self, leg, gnum, snum, loc="rightup", loctype="view"):
        self.gnum_check(gnum)
        self.snum_check(gnum, snum)
        #input((gnum,snum))
        #input(self.gdiclst)
        self.gdiclst[gnum]["snum"][snum]["legend"] = leg
        self.gdiclst[gnum]["legloc"] = loc
        self.gdiclst[gnum]["legloctype"] = loctype
        #input(self.gdiclst)

    def string_input(self, string, loc, loctype="view", gnum=0, charsize=1):
        self.decolst += [("string", string, loc, loctype, gnum, charsize)]

    def iterstr_input(self, lst, loc, loctype="view", gnum=0, charsize=1):
        cntlst = []
        i = 0
        while i < len(lst):
            if type(lst[i]) != str:
                lst[i] = [lst[i], 0]
            i += 1
        self.decolst += [("iterst", lst, loc, loctype, gnum, charsize)]
        
    def set_timestamp(self, string, loc=(0.03,0.03), font=None, charsize=1.0):
        self.decolst += [("tstamp", string, loc, font, charsize)]

    def box_input(self, loc, lstyle=1, lwidth=1, lcolor=1,  fcolor=1, fptn=0, loctype="view", gnum=0, xonly=False, yonly=False):
        self.gnum_check(gnum)
        self.snum_check(gnum, 0)
        self.decolst += [("box", loc, lstyle, lwidth, lcolor, fcolor, fptn, loctype, gnum, xonly, yonly)]
            
    def ellipse_input(self, loc, lstyle=1, lwidth=1, lcolor=1, fcolor=1, fptn=0, loctype="view", gnum=0):
        self.decolst += [("ellipse", loc, lstyle, lwidth, lcolor, fcolor, fptn, loctype, gnum)]

    def line_input(self, loc, lstyle=1, lwidth=1, lcolor=1, arrow=0, atype=0, alength=0, alayout=(1,1), loctype="view", gnum=0, xonly=False, yonly=False):
        self.decolst += [("line", loc, lstyle, lwidth, lcolor, arrow, atype, alength, alayout, loctype, gnum, xonly, yonly)]

    def xtickitvl_input(self, intvl, gnum=0):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["xtickitvl"] = intvl
        
    def ytickitvl_input(self, intvl, gnum=0):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["ytickitvl"] = intvl

    def show_prop(self, gnum=None):
        self.gnum_check(gnum)
        gdiclst = self.gdiclst if gnum else self.gnumlst[gnum]
        for  gdic in self.gdiclst:
            print "xlabel : %s" %sgdic["xlabel"]
            print "ylabel : %s" %sgdic["ylabel"]
    def set_axnum(self, axnum):
        self.axnumlst += [axnum]
    def get_axnum(self,):
        return self.axnumlst
 
class rootmacro(rootprop):
    def __init__(self):
        rootprop.__init__(self)
        self.papath = "/Users/yu/"  
        self.dfpath = self.papath + "tmpdata.txt"
        self.mpath = self.papath + "tmpmacro.c"
        self.cmd = "/Users/yu/Documents/progs/c_prog/ROOT/root-v5-34-00/bin/root"
        self.arrlst = None
        self.drawlst = []
        self.drawnlst = []
        self.cnum = 0
        self.pnum = 0
        self.abc = "abcdefghijklmnopqrstuvwxyz"
        self.write_lst= container()
        self.line_init()
    
    def set_xydata(self, x, y, gnum=0):
        self.gnum_check(gnum)
        self.dcnt()
        xmin, xmax = ascale(x)
        ymin, ymax = ascale(y)
        self.set_xlim(xmin, xmax)
        self.set_ylim(ymin, ymax)

        if x.ndim == 2:
            arrs = crush_arr([x,y])
        else:
            arrs = array([x,y])
        self.set_axnum(2)
        self.write_lst.stack_conca(*arrs.transpose().tolist())
        

    def set_xyzdata(self, x, y, z, colormap=False, gnum=0):
        self.gnum_check(gnum)
        self.dcnt()
        xmin, xmax = ascale(x)
        ymin, ymax = ascale(y)
        zmin, zmax = ascale(z)
        self.set_xlim(xmin, xmax)
        self.set_ylim(ymin, ymax)
        self.set_zlim(zmin, zmax)
        if x.ndim == 2:
            if (x[0][1] - x[0][0]) == 0:
                tmparr = x.transpose()
            else:
                tmparr = x
            self.set_xbin(self.bincalc(tmparr[0]))
            if (y[0][1] - y[0][0]) == 0:
                tmparr = y.transpose()
            else:
                tmparr = y
            self.set_ybin(self.bincalc(tmparr[0]))
        colormap = True
        if colormap:
            arrs =  array([append(x,[]), append(y,[]), append(z,[])])
        else:
            arrs = array(crush_lst([x,y,z]))
            
        self.set_axnum(3)
        self.write_lst.stack_conca(*arrs.tolist())
    

    def line_init(self):
        self.line = ""
        self.lput("{")
        self.lput("#include <vector>")
        self.lput("#include <fstream>")
    def ccnt(self):
        ret = self.cnum
        self.cnum += 1
        return ret

    def pcnt(self):
        ret = self.pnum
        self.pnum += 1
        return ret

    def add_canvas(self, name=None, title="", wtopx=0.5, wtopy=0.5, ww=500, wh=600):
        if name == None:
            name = "c%s" %self.cnum
        self.lput('TCanvas* c%s = new TCanvas("%s", "%s", %s, %s, %s, %s);' %(self.cnum, name, title, wtopx, wtopy, ww, wh))
        self.ccnt()

    def c_cd(self, cnum):
        #Canvas current display
        self.lput("c%s -> cd();" %cnum)
        
    def p_cd(self, pnum):
        #Pad current display
        self.lput("p%s -> cd();" %pnum)

    def lput(self, line):
        #line input
        self.line += line + "\n"
    
    def set_arrlst(self):
        self.arrlst = []
        axnumlst = array(append([],map(lambda x: range(x),self.get_axnum())),dtype=int)
        for n , i in zip(range(self.get_dnum()),self.get_axnum()):
                for t in range(i):
                    self.arrlst += ["%s%s" %(self.abc[n],axnumlst[t])]

    def dump_data(self):
        self.write_lst.trim()
        savetxt(self.dfpath, array(self.write_lst.get()).transpose())
    def set_data(self):
        self.set_arrlst()
        self.lput("vector <Double_t> %s;" %concatanate(self.arrlst,",").strip(","))
        self.lput("vector <Double_t> %s;" %concatanate(self.arrlst,",").strip(","))
        self.lput('ifstream ifs("%s");' %self.dfpath)
        self.lput("while(!ifs.eof()){")
        self.lput("Double_t %s;" %concatanate(self.arrlst, "_tmp,").strip(","))
        self.lput("ifs >> %s;" %concatanate(self.arrlst,"_tmp >> ").strip(" >> "))
        self.lput(concatanate(map(lambda x: "%s.push_back(%s_tmp)" %(x,x), self.arrlst), ";\n").strip("\n"))
        self.lput("}")
        self.lput("ifs.close();")
   
    def tgraph(self, snum, gnum=0):
        xmin, xmax, ymin, ymax, zmin, zmax = self.get_lim(gnum)
        self.lput(concatanate(map(lambda x,y: "Double_t *%sp=&(%s.at(0))" %(x,y), self.arrlst,self.arrlst), ";\n").strip("\n"))
        if type(snum) != list: snum = [snum]
        for n in snum:
            self.lput("TGraph *g%s = new TGraph(%s0.size(), %s0p, %s1p);" %(str(gnum)+self.abc[n], self.abc[n], self.abc[n], self.abc[n]))
            self.lput('g%s -> GetXaxis() -> SetTitle("%s");' %(str(gnum)+self.abc[n], "test"))
            self.lput('g%s -> GetYaxis() -> SetTitle("%s");' %(str(gnum)+self.abc[n], "test"))
            self.set_simple2d(str(gnum)+self.abc[n])
        
    def th2(self, gnum=0):
        xmin, xmax, ymin, ymax, zmin, zmax = self.get_lim()
        xbin = self.get_xbin()
        ybin = self.get_ybin()
        if type(xbin) == list: 
            xlim = "{" + concatanate(xbin, ",") + "}"
            ylim = "{" + concatanate(ybin, ",") + "}"
            xbin = len(xbin) - 1
            ybin = len(ybin) - 1
            self.lput("Double_t xlim[%s+1] = %s;" %(xbin, xlim))
            self.lput("Double_t ylim[%s+1] = %s;" %(ybin, ylim))
            self.lput('TH2D *g%s = new TH2D("g%s", "", %s, xlim, %s, ylim);' %(gnum, gnum, xbin, ybin))
        else:
            xbin = str(xbin) - 1
            ybin = str(ybin) - 1 
            xlim = "%s, %s" %(xmin, xmax)
            ylim = "%s, %s" %(ymin, ymax)
            self.lput('TH2D *g%s = new TH2D("title", "tmp", %s, %s, %s, %s, );' %(gnum, xbin, xlim, ybin, ylim))
        self.lput("g%s -> SetMinimum(%s);" %(gnum, zmin))
        self.lput("g%s -> SetMaximum(%s);" %(gnum, zmax))
        #self.lput("TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);")
        #self.lput("gStyle->SetNumberContours(NCont);")
        #self.lput('TH3D *g%s = new TH3D("title", "tmp", %s, %s, %s, %s, %s, %s,%s,%s,%s);' %(gnum, 100, xmin, xmax, 100, ymin, ymax, 100, zmin, zmax))
        #self.lput('TH2D *g%s = new TH2D("title", "tmp", %s, %s, %s, %s)' %(gnum, self.bincalc(), self.get_xmin(gnum), self.get_xmax(gnum), self.get_ymin(gnum), self.get_ymax(gnum)))
        
    def set_colmap(self, gnum=0):
        self.drawlst += ['g%s.Draw("cont4z");' %gnum]

    def set_simple2d(self, gnum):
        if self.drawn_check(int(gnum[:-1])):
            self.drawlst += ['g%s.Draw("AP");' %gnum]
        else:
            self.drawlst += ['g%s.Draw("SAME");' %gnum]

    def drawn_check(self, gnum):
        try:
            self.drawnlst.index(gnum)
            return False
        except:
            self.drawnlst += [gnum]
            return True

    def Fill(self):
        self.lput("int i;")
        axit = iter(self.get_axnum())
        for gnum in range(self.get_gnum()): 
            self.lput("for(i = 0; i <= a0.size(); ++i){")
            arg = concatanate(map(lambda x: self.abc[gnum] + str(x) + "[i]"  , range(axit.next())), ",").strip(",")
            self.lput("g%s -> Fill(%s);" %(gnum, arg))
            self.lput("}")
            #self.lput(concatanate(map(lambda x: "g%s -> Fill(%s)" %(gnum arg), self.arrlst), ";\n").strip("\n"))

    def set_xaxis(self, gnum, font="Helvatica", offset=0.005, color=1, lsize=0.04, ndiv=510, optim="ktrue", noexp="kTRUE", tlen=0.03, toffset=1, tsize=0.02):
       self.lput(" TAxis *xaxis = g%->GetXaxis();" %gnum)
       self.lput(" xaxis->SetAxisColor(Color_t color = %s);" %color)
       self.lput(" xaxis->SetLabelColor(Color_t color = %s);" %color)
       self.lput(" xaxis->SetLabelFont(Style_t font = %s);" %font)
       self.lput(" xaxis->SetLabelOffset(Float_t offset = %s);" %offset)
       self.lput(" xaxis->SetLabelSize(Float_t size = %s);" %lsize)
       self.lput(" xaxis->SetNdivisions(Int_t n = %s, Bool_t optim = %s);" %(ndiv, optim))
       self.lput(" xaxis->SetNoExponent(Bool_t noExponent = %s);" %noexp)
       self.lput(" xaxis->SetTickLength(Float_t length = %s);" %tlen)
       self.lput(" xaxis->SetTitleOffset(Float_t offset = %s);" %offset)
       self.lput(" xaxis->SetTitleSize(Float_t size = %s);" %tsize)

    def set_yaxis(self, gnum, font="Helvatica", offset=0.005, color=1, lsize=0.04, ndiv=510, optim="ktrue", noexp="kTRUE", tlen=0.03, toffset=1, tsize=0.02):
       self.lput(" TAxis *yaxis = g%->GetXaxis();" %gnum)
       self.lput(" yaxis->SetAxisColor(Color_t color = %s);" %color)
       self.lput(" yaxis->SetLabelColor(Color_t color = %s);" %color)
       self.lput(" yaxis->SetLabelFont(Style_t font = %s);" %font)
       self.lput(" yaxis->SetLabelOffset(Float_t offset = %s);" %offset)
       self.lput(" yaxis->SetLabelSize(Float_t size = %s);" %lsize)
       self.lput(" yaxis->SetNdivisions(Int_t n = %s, Bool_t optim = %s);" %(ndiv, optim))
       self.lput(" yaxis->SetNoExponent(Bool_t noExponent = %s);" %noexp)
       self.lput(" yaxis->SetTickLength(Float_t length = %s);" %tlen)
       self.lput(" yaxis->SetTitleOffset(Float_t offset = %s);" %offset)
       self.lput(" yaxis->SetTitleSize(Float_t size = %s);" %tsize)

    def set_zaxis(self, gnum, font="Helvatica", offset=0.005, color=1, lsize=0.04, ndiv=510, optim="ktrue", noexp="kTRUE", tlen=0.03, toffset=1, tsize=0.02):
       self.lput(" TAxis *zaxis = g%->GetXaxis();" %gnum)
       self.lput(" zaxis->SetAxisColor(Color_t color = %s);" %color)
       self.lput(" zaxis->SetLabelColor(Color_t color = %s);" %color)
       self.lput(" zaxis->SetLabelFont(Style_t font = %s);" %font)
       self.lput(" zaxis->SetLabelOffset(Float_t offset = %s);" %offset)
       self.lput(" zaxis->SetLabelSize(Float_t size = %s);" %lsize)
       self.lput(" zaxis->SetNdivisions(Int_t n = %s, Bool_t optim = %s);" %(ndiv, optim))
       self.lput(" zaxis->SetNoExponent(Bool_t noExponent = %s);" %noexp)
       self.lput(" zaxis->SetTickLength(Float_t length = %s);" %tlen)
       self.lput(" zaxis->SetTitleOffset(Float_t offset = %s);" %offset)
       self.lput(" zaxis->SetTitleSize(Float_t size = %s);" %tsize)

    def ctable(self, Stops, Red, Green, Blue, NColors, alpha = 1.):
        Number = len(Red)
        self.lput("UInt_t Number = %s;" %Number)
        self.lput("UInt_t NColors = %s;" %NColors)
        self.lput("Float_t alpha = %s;" %alpha)
        self.lput("Double_t Stops[%s] = {%s};" %(Number, concatanate(Stops,",")))
        self.lput("Double_t Red[%s] = {%s};" %(Number, concatanate(Red,",")))
        self.lput("Double_t Green[%s] = {%s};" %(Number, concatanate(Green,",")))
        self.lput("Double_t Blue[%s] = {%s};" %(Number, concatanate(Blue,",")))
        self.lput("TColor::CreateGradientColorTable(Number, Stops, Red, Green, Blue, NColors );")

    def set_cont(self, nlevels, levels=0, gnum=0):
        self.lput("Int_t nlevels = %s;" %nlevels)
        self.lput("Int_t levels = %s;" %levels)
        self.lput("g%s.SetContour(nlevels, levels);" %gnum)


    
    def duallayout(self,):
        self.add_canvas()
        n = 0
        self.add_pad(0.0,0,1,0.5)
        self.lput(self.drawlst[0])
        for draw in self.drawlst[1:]:
            try:
                draw.index("SAME")
                n += 1
                self.lput(draw)
            except:
                self.add_pad(0.0,0.5,1,1)
                self.lput(draw)
        self.lput("}")
        
    def simplelayout(self,):
        self.add_canvas()
        #self.add_pad(0.0,0,0.5,0.5)
        #self.ccd(0)
        for draw in self.drawlst:
            self.lput(draw)
        self.lput("}")

    def unset_stat(self):
        self.lput('gStyle->SetOptStat(kFALSE) ;')

    def ldump(self):
        self.set_arrlst()
        self.set_data()
        #self.colormap()
        self.tgraph()
        #self.Fill()
        self.ctable([0.,0.5,1],[1, 1, 0], [0,1,0],[0,1,1],1000)
        self.duallayout()
        w = open(self.mpath, "w")
        w.write(self.line)
        w.close()

    def dump_macro(self):
        w = open(self.mpath, "w")
        w.write(self.line)
        w.close()

    def bincalc(self, arr, gnum=0):
        bak = arr[:-1]
        fow = arr[1:]
        lst = map(lambda x, y: ((y - x) / 2) + x, bak, fow) 
        retlst = [bak[0] - (bak[1] - bak[0])/2] + lst + [fow[-1] + (fow[-1] - fow[-2])/2]
        return retlst

    def add_pad(self, xlow, ylow,  xup, yup, color=-1, bordersize=-1, bordermode=-2, cnum=0):
        n = self.pcnt()
        self.lput('TPad *p%s = new TPad("pad%s","This is pad%s",%s,%s,%s,%s,%s,%s,%s);' %(n,n,n, xlow, ylow, xup, yup, color, bordersize, bordermode))
        self.c_cd(cnum)
        self.lput("p%s.Draw();" %n)
        self.p_cd(n) 

    
    def open_macro(self, gnum=0, snum=0):
        cmd = "%s -l -x %s" %(self.cmd, self.mpath) 
        call(cmd.split())

class prop_handle():
    def __init__(self):
        self.myname = "self"
        self.dic = {}
    def input(self, key, val):
        self.dic.update({key:val})
    
    def get(self, key):
        return self.dic[key]
    
class graph_handle():
    def __init__(self):
        self.gdic = {}


class s_handle():
    def __init__(self):
        self.sdic = {}
#from calc import *
#from numpy import *
#from pylab import *
#
#[[x,y],[a,b]] = calc("pc",80000)
#a=gracemanage()
#a.set_xydata(x,y, gnum=0)
#a.set_xlabel("hello")
#a.set_ylabel("B")
#a.columnlayout(7)
#a.set_autoscale(x,y,0)
#a.dumpfig()
#a.multigraph(2,2)
#a.set_xydata(x,y, gnum=1)
#a.set_xydata(x,y, gnum=2)
#a.set_xydata(x,y, gnum=3)
#a.set_autoscale(x,y, 0)
#a.set_autoscale(x,y, 1)
#a.set_autoscale(x,y, 2)
#a.set_autoscale(x,y, 3, margin=0.1)
#a.open_grace()
#[[x,y],[c,b]] = calc("pb",80000)
#a.set_xydata(x,y, gnum=2)
#a.set_autoscale(x,y, 2)
#a.open_grace()
#input()
#
#[[x,y],[xn,yn]] = calc("pc", 80888, int=0.01)
#l = ones(len(x)) * 10
#dlst = array([x,l,y])
#dlst = array([dlst,[x,l*2,y]])
#tmp = graphmanage()
##tmp.setpdf()
#tmp.terminal("x11")
##tmp.xrange(0,30)
##tmp.yrange(0,-0.001)
##tmp.multiplot(2,2)
#tmp.prof_evo("tmp")
#d = [[x,y],[x,y]]
##tmp.complot(d)
