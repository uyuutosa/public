#!/usr/bin/env python
#-*- coding:utf-8 -*-
from copy import deepcopy
class grace_prop():
    allpropdic = {
        "xlabelall" : None,
        "ylabelall" : None,
        "layout" : "simple",
    }
    def __init__(self):
        self.tmpdic = {"snum" : [],
                          "gtype" : "normal",
                          "xaxes" : None,
                          "yaxes" : None,
                          "xtics" : None,
                          "ytics" : None,
                          "xtickitvl" : None,
                          "ytickitvl" : None,
                          "xlabel" : None,
                          "ylabel" : None,
                          "lim" : None,
                          "xlim" : None,
                          "ylim" : None,
                          "legloc" : "rightup",
                          "legloctype" : "wratio",
                          }
        self.mkall = None
        self.lineall = None
        self.initialize()

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

    def xaxes_input(self, scale="Normal", invert="off", gnum=0):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["xaxes"] = (scale, invert)

    def yaxes_input(self, scale="Normal", invert="off", gnum=0):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["yaxes"] = (scale, invert)

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

    def xlim_input(self, xmin, xmax, gnum, tnum=6):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["xlim"] = (xmin, xmax, tnum)

    def ylim_input(self, ymin, ymax, gnum, tnum=6):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["ylim"] = (ymin, ymax, tnum)

    def autolim_input(self,xarr,yarr, margin=0.1, gnum=0):
        xmin,xmax = self.autoscale(xarr, margin)
        ymin,ymax = self.autoscale(yarr, margin)
        self.prop.lim_input(xmin,xmax,ymin,ymax,gnum)

    def xlabel_input(self, xname, gnum):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["xlabel"] = xname

    def xlabel_all_input(self, xname, gnumlim):
        self.allpropdic["xlabelall"] = [xname, gnumlim]

    def ylabel_input(self, yname, gnum):
        self.gnum_check(gnum)
        self.gdiclst[gnum]["ylabel"] = yname
            
    def ylabel_all_input(self, yname, gnumlim):
        self.allpropdic["ylabelall"] = [yname, gnumlim]

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

    def layout_input(self, name):
        self.allprop["layout"] = name


    def show_prop(self, gnum=None):
        self.gnum_check(gnum)
        gdiclst = self.gdiclst if gnum else self.gnumlst[gnum]
        for  gdic in self.gdiclst:
            print "xlabel : %s" %sgdic["xlabel"]
            print "ylabel : %s" %sgdic["ylabel"]

