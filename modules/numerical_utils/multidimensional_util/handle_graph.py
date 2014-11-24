#!/usr/bin/env python
#-*- coding:utf-8 -*-
from numpy import *
from modules.essential_utils.obj_util import *
from modules.essential_utils.convert_util import *
from modules.essential_utils.file_util import *
from modules.essential_utils.search_util import *
from modules.numerical_utils.fit_util import pfit
#import modules.numerical_utils.ana_spec as spec
#from modules.heliac_utils.speana_util import *
from modules.graph_utils.grace_util.grace_util import * 
from modules.graph_utils.grace_util.grace_prop import * 

import os 
import itertools as it
import pickle

class root_prop():
    def __init__(self):
        self.tmp_gdic = {"xname" : "Nonea",
                      "yname" : "None",
                      "zname" : "None",
                      "xlim" : None,
                      "ylim" : None,
                      "zlim" : None,
                      }
        self.tmp_decodic = {"box" : []}
        self.initialize()

    def initialize(self):
        self.glst = [deepcopy(self.tmp_gdic)]
        self.decolst = [deepcopy(self.tmp_decodic)]

    def glst_check(self, gnum):
        while len(self.glst) <= gnum:
            self.glst += [deepcopy(self.tmp_gdic)]
            self.decolst += [deepcopy(self.tmp_decodic)]

    def input_xname(self, xname, gnum=0):
        self.glst_check(gnum)
        self.glst[gnum]["xname"] = xname

    def input_yname(self, yname, gnum=0):
        self.glst_check(gnum)
        self.glst[gnum]["yname"] = yname

    def input_zname(self, zname, gnum=0):
        self.glst_check(gnum)
        self.glst[gnum]["zname"] = zname

    def input_xlim(self, xmin, xmax, gnum=0):
        self.glst_check(gnum)
        self.glst[gnum]["xlim"] = [xmin, xmax]

    def input_ylim(self, ymin, ymax, gnum=0):
        self.glst_check(gnum)
        self.glst[gnum]["ylim"] = [ymin, ymax]

    def input_zlim(self, zmin, zmax, gnum=0):
        self.glst_check(gnum)
        self.glst[gnum]["zlim"] = [zmin, zmax]
      
    def input_box(self, loc, lstyle=1, lwidth=1, lcolor=1,  fcolor=1, fptn=0, loctype="view", gnum=0, xonly=False, yonly=False, gtpl=()):
        self.glst_check(gnum)
        xmin, xmax, ymin, ymax = loc
        self.decolst[gnum]["box"] += [[xmin, xmax, ymin, ymax, lstyle, lwidth, lcolor,  fcolor, fptn, loctype, gnum, xonly, yonly, gtpl]]

    def get_xname(self, gnum):
        self.glst_check(gnum)
        return self.glst[gnum]["xname"]

    def get_yname(self, gnum):
        self.glst_check(gnum)
        return self.glst[gnum]["yname"]

    def get_zname(self, gnum):
        self.glst_check(gnum)
        return self.glst[gnum]["zname"]

    def get_xlim(self, gnum):
        self.glst_check(gnum)
        return self.glst[gnum]["xlim"]

    def get_ylim(self, gnum):
        self.glst_check(gnum)
        return self.glst[gnum]["ylim"]

    def get_zlim(self, gnum):
        self.glst_check(gnum)
        return self.glst[gnum]["zlim"]

    def get_box(self, gnum):
        return self.decolst[gnum]["box"] 

class handle_graph():
    grace = grace_util()
    def set_xlabel_all(self, name, gnumlim):
        self.grace.prop.xlabel_all_input(name, gnumlim)
        for i in range(gnumlim): self.root.input_xname(name, i)

    def set_ylabel_all(self, name, gnumlim):
        self.grace.prop.ylabel_all_input(name, gnumlim)
        for i in range(gnumlim): self.root.input_yname(name, i)

    def set_zlabel_all(self, name, gnumlim):
        for i in range(gnumlim): self.root.input_zname(name, i)

    def set_errorbar(self, gnum=0, snum=0, color=1, patn=1, size=1, lwidth=2, lstyle=1, rlwidth=1, rlstyle=1):
        self.grace.prop.errorbar_input(gnum, snum, color, patn, size, lwidth, lstyle, rlwidth, rlstyle)

    def set_xtickitvl(self, itvl, gnum=0):
        self.grace.prop.xtickitvl_input(itvl, gnum)
        
    def set_ytickitvl(self, itvl, gnum=0):
        self.grace.prop.ytickitvl_input(itvl, gnum)

    def set_xaxes(self, scale="Nomal", invert="off", gnum=0):
        self.grace.prop.xaxes_input(scale, invert, gnum)

    def set_yaxes(self, scale="Nomal", invert="off", gnum=0):
        self.grace.prop.yaxes_input(scale, invert, gnum)

    def set_xlabel(self, xname, gnum=0):
        self.grace.prop.xlabel_input(xname, gnum)
        self.root.input_xname(xname, gnum)
        
    def set_ylabel(self, yname, gnum=0):
        self.grace.prop.ylabel_input(yname, gnum)
        self.root.input_yname(yname, gnum)

    def set_zlabel(self, zname, gnum=0):
        self.root.input_zname(zname, gnum)

    def set_lim(self, xmin, xmax, ymin, ymax, gnum=0, tnum=6):
        self.grace.prop.lim_input(xmin, xmax, ymin, ymax, gnum, tnum)
        self.root.input_xlim(xmin, xmax, gnum)
        self.root.input_ylim(ymin, ymax, gnum)

    def set_xylim_all(self, xmin, xmax, ymin, ymax, glim=10, tnum=6):
        for gnum in range(glim):
            self.grace.prop.lim_input(xmin, xmax, ymin, ymax, gnum, tnum)
            self.root.input_xlim(xmin, xmax, gnum)
            self.root.input_ylim(ymin, ymax, gnum)

    def set_xlim(self, xmin, xmax, gnum=0, tnum=6):
        self.root.input_xlim(xmin, xmax, gnum)

    def set_ylim(self, ymin, ymax, gnum=0, tnum=6):
        self.root.input_ylim(ymin, ymax, gnum)
        
    def set_zlim(self, zmin, zmax, gnum=0, tnum=6):
        self.root.input_zlim(zmin, zmax, gnum)

    def set_leg(self, yname, gnum=0, snum=0, loc="rightup", loctype="view"):
        self.grace.prop.leg_input(yname, gnum, snum, loc, loctype)
    
    def set_style_line(self, width=1, color=0, lstyle=1, gnum=0, snum=0):
        self.grace.prop.style_line_input(width, color, lstyle, gnum, snum)

    def set_mk(self, size=1, color=0, mstyle=1, fcolor=None, fptn=1, lwidth=1, lstyle=1, gnum=0, snum=0):
        self.grace.prop.mk_input(size, color, mstyle, fcolor, fptn, lwidth, lstyle, gnum, snum)

    def set_lineall(self, size=1, color=1, lstyle=1):
        self.grace.prop.lineall_input(size, color, lstyle)

    def set_mkall(self, size=1, color=1, mstyle=1, fptn=[1], lwidth=[1], lstyle=[1]):
        self.grace.prop.mkall_input(size, color, mstyle, fptn, lwidth, lstyle)

    def set_string(self, line, loc, loctype="view", gnum=0, charsize=1):
        self.grace.prop.string_input(line, loc, loctype, gnum, charsize)
        
    def set_iterstr(self, lst, loc, loctype="view", gnum=0, charsize=1):
        self.grace.prop.iterstr_input(lst, loc, loctype, gnum, charsize)

#    def set_box(self, loc, lstyle=1, lwidth=1, lcolor=1,  fcolor=1, fptn=0, loctype="view", gnum=0):
#        self.grace.prop.box_input(loc, lstyle, lwidth, lcolor,  fcolor, fptn, loctype, gnum)
#        self.grace.root.input_box(loc, lstyle, lwidth, lcolor,  fcolor, fptn, loctype, gnum)

    def set_ellipse(self, loc, lstyle=1, lwidth=1, lcolor=1,  fcolor=1, fptn=0, loctype="view", gnum=0):
        self.grace.prop.ellipse_input(loc, lstyle, lwidth, lcolor,  fcolor, fptn, loctype, gnum)

    def set_box(self, loc, lstyle=1, lwidth=1, lcolor=1,  fcolor=1, fptn=0, loctype="view", gnum=0, xonly=False, yonly=False):
        self.grace.prop.box_input(loc, lstyle, lwidth, lcolor,  fcolor, fptn, loctype, gnum, xonly, yonly)
        #gtpl = tuple(self.root.get_xlim(gnum) + self.root.get_ylim(gnum))
        #self.root.input_box(loc, lstyle, lwidth, lcolor,  fcolor, fptn, loctype, gnum, xonly, yonly, gtpl)

    def set_line(self, loc, lstyle=1, lwidth=1, lcolor=1, arrow=0, atype=0, alength=0, alayout=(1,1), loctype="view", gnum=0, xonly=False, yonly=False):
        self.grace.prop.line_input(loc, lstyle, lwidth, lcolor, arrow, atype, alength, alayout, loctype, gnum, xonly, yonly)
    

    def view_colmap(self,  arrs, layout="simple", device="png", opt="colz", palette="simple", serial=False):
        from modules.graph_utils.root_util.root_util import root_util
        r = root_util()
        layoutdic = {"single": r.single_layout,
                     "dual": r.dual_layout,
                     "sextuple" : r.sextuple_layout}
        palettedic = {"simple": r.mypalette1,
                      "simple3": r.mypalette3,
                      "simple4": r.mypalette4,
                      "rainbow": r.palette_rainbow,
                      "r2b": r.palette_red2blue}

        arrs = self.get_data()
        x,y,z = arrs
        
        if serial:
            bin_xtpl = tuple(x[0]) if x[0][1] != x[0][0] else tuple(x.transpose()[0]) # check the greater direction.
            bin_ytpl = tuple(y[0]) if y[0][1] != y[0][0] else tuple(y.transpose()[0])
            r.set_xyzdata(tuple(x.reshape(x.size).tolist()),  tuple(y.reshape(y.size).tolist()), tuple(z.reshape(z.size).tolist()), bin_xtpl, bin_ytpl, 0, 0)
        else:
            r.set_xyzdata_tgraph(tuple(x.reshape(x.size).tolist()),  tuple(y.reshape(y.size).tolist()), tuple(z.reshape(z.size).tolist()), 0, 0)
        xlim = self.root.get_xlim(0)
        ylim = self.root.get_ylim(0)
        zlim = self.root.get_zlim(0)
        if type(xlim) != type(None): r.set_xlim(xlim[0], xlim[1], 0)
        if type(ylim) != type(None): r.set_ylim(ylim[0], ylim[1], 0)
        if type(zlim) != type(None): r.set_zlim(zlim[0], zlim[1], 0)
        r.set_xname(self.root.get_xname(0), 0)
        r.set_yname(self.root.get_yname(0), 0)
        r.set_zname(self.root.get_zname(0), 0)
        layoutdic[layout](opt)
        palettedic[palette]()
        r.view_graph()
