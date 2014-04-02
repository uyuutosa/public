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
import cPickle as pickle

from handle_graph import handle_graph, root_prop
import handle_4d as h4d

class handle_5d(handle_graph):
    def __init__(self, datlst=[]):
        self.x = None
        self.y = None
        self.z = None
        self.a = None
        self.b = None
        self.xerr = None
        self.yerr = None
        self.zerr = None
        self.aerr = None
        self.berr = None
        self.T = None
        self.datlst = datlst
        self.grace = grace_util()
        self.root = root_prop()
        self.dumppath = "."
        self.hist = method_history(self)

    def set_data(self, datlst=None):
        self.datlst = datlst

    def set_multi(self, datlst):
        xlst = []
        ylst = []
        zlst = []
        alst = []
        for obj in datlst:
            xlst += [obj.x]
            ylst += [obj.y]
            zlst += [obj.z]
            alst += [obj.a]
        self.x = array(xlst) if type(xlst[0]) != type(None) else None
        self.y = array(ylst) if type(ylst[0]) != type(None) else None
        self.z = array(zlst) if type(zlst[0]) != type(None) else None
        self.a = array(alst) if type(alst[0]) != type(None) else None
            
    def reshape(self, shtpl):
        self.dinput([None if type(x) == type(None) else x.reshape(shtpl) for x in self.get_data()])
        #x, y, z = self.get_data()
        #if type(x) != type(None): x = x.reshape(shtpl)
        #if type(y) != type(None): y = y.reshape(shtpl)
        #if type(z) != type(None): z = z.reshape(shtpl)

    def transpose(self, trtpl=(0,2,1)):
        self.dinput([None if type(x) == type(None) else x.transpose(trtpl) for x in self.get_data()])

    def dinput(self, arrlst, errlst=None):
        num = len(arrlst)
        
        self.x = arrlst[0]
        self.y = arrlst[1]
        self.z = arrlst[2]
        if num >= 4: self.a = arrlst[3]
        if type(errlst) != type(None):
            self.xerr = errlst[0]
            self.yerr = errlst[1]
            self.zerr = errlst[2]
            if num >= 4: self.aerr = errlst[3]

    def get_data(self, reterr=False):
        x = array(self.x) if type(self.x) != type(None) else None
        y = array(self.y) if type(self.y) != type(None) else None
        z = array(self.z) if type(self.z) != type(None) else None
        a = array(self.a) if type(self.a) != type(None) else None
        b = array(self.a) if type(self.b) != type(None) else None
        xerr = array(self.xerr) if type(self.xerr) != type(None) else None
        yerr = array(self.yerr) if type(self.yerr) != type(None) else None
        zerr = array(self.zerr) if type(self.zerr) != type(None) else None
        aerr = array(self.aerr) if type(self.aerr) != type(None) else None
        berr = array(self.berr) if type(self.berr) != type(None) else None
        arrlst = [x, y, z, a, b]
        errlst = [xerr, yerr, zerr, aerr, b]

        if reterr: 
            return [arrlst, errlst]
        else:
            return arrlst
            
    def T_align(self, T):
        """
            
        """
        self.hist.input()
        map(lambda x: x.transpose() if x.T != T else None, self.datlst)

    def release(self):
        self.hist.input()
        return self.datlst

    def subtract(self, abcs=2, lgtd=1, absolute=True):
        self.hist.input()
        lsts = lstsplit(self.datlst,2)
        retlsts= []
        for a,b in lsts:
                
            if a.T == False:
                a.transpose()
            if b.T == False:
                b.transpose()

            a_arrs = a.get_data()
            b_arrs = b.get_data()
            
            retlst = [[], [], []]
            for n, a_y in enumerate(a_arrs[lgtd]):
                flag = False
                a_tmpx = a_arrs[abcs][n][0]
                for i, b_y in enumerate(b_arrs[lgtd]):
                    b_tmpx = b_arrs[abcs][i][0]
                    if a_tmpx == b_tmpx:
                        if absolute:
                            a_y = abs(a_y) - abs(b_y)
                        else:
                            a_y -= b_y
                        flag = True
                        break
                    else:
                        continue
                    
                if flag:
                    a_x = a_arrs[abcs][n]
                    a_z = a_arrs[3-abcs-lgtd][n]
                    retlst[abcs] += [a_x]
                    retlst[lgtd] += [a_y]
                    retlst[3-abcs-lgtd] += [a_z]
            tmp = h4d.handle_4d()
            tmp.T = True
            tmp.dinput(array(retlst))
            retlsts += [tmp]
        self.sbt = h4d.handle_5d(retlsts)

    def prof_ave(self, abcs=2, lgtd=1,  errb=False):
        if self.T == False:
            self.transpose()

        #self.sort(abcs)
        #arrs = self.sorted.get_data()
        arrs = self.get_data()
        
        retlst = [[], [], []]
        currx = nan
        retxarr = None
        retzarr = None
        for n, y in enumerate(arrs[lgtd]):
            tmpx = arrs[abcs][n][0]
            tmpxarr = arrs[abcs][n]
            tmpzarr = arrs[3-abcs-lgtd][n]

            if tmpx == currx:
                sumy += y
                i += 1
            else:
                if type(retxarr) != type(None):
                    retlst[abcs] += [retxarr]
                    retlst[lgtd] += [sumy / i]
                    retlst[3-abcs-lgtd] += [retzarr]
                
                retxarr = tmpxarr
                sumy = y
                retzarr = tmpzarr
                currx = tmpx 
                i = 1
        
        retlst[abcs] += [retxarr]
        retlst[lgtd] += [sumy / i]
        retlst[3-abcs-lgtd] += [retzarr]
        self.pave = h4d.handle_4d()
        self.pave.T = True
        self.pave.dinput(array(retlst))    
      
    def trapezoid(self, abcs=0,lgtd=1, T=False):
        from modules.numerical_utils.basic_util import trapezoid
        tmplst = []
        for obj in self.datlst:
            obj.trapezoid(abcs, lgtd, T)
            tmplst += [obj.trap]
        self.trap = h4d.handle_4d()
        self.trap.set_multi(tmplst, T=True)

    def view(self, layout="simple", abcs=0,lgtd=1, transpose=False, T=False, sepnum=1, filename="tmp", device="PDF", hgrid=1, vgrid=1, glim=None, dump=False):
        self.hist.input()
        layout = str(layout)
        layoutdic = {
                     "1"      : self.grace.layout_1,
                     "1_2"      : self.grace.layout_1_2,
                     "2"      : self.grace.layout_2,
                     "3"      : self.grace.layout_3,
                     "4"      : self.grace.layout_4,
                     "5"      : self.grace.layout_5,
                     "6"      : self.grace.layout_6,
                     "7"      : self.grace.layout_7,
                     "8"      : self.grace.layout_8,
                     "8_2"    : self.grace.layout_8_2,
                     "column" : self.grace.layout_column,
                     "column4": self.grace.layout_column_4grid,
                    }
        self.T_align(T)
        arrs = []
        errs = []
        for dcls in self.datlst:
            arr, err = dcls.get_data(reterr=True)
            arrs += [arr]
            errs += [err]
                
        arrs = lstsplit(arrs, sepnum)
        plotnumlim = 1
        #plotnumlim = len(arrs[0][0][abcs])
        snumlim = sepnum 
        gnumlim = len(arrs)
        plotnum = 0
        snum = 0
        snum2 = 0
        gnum = 0
        cnt = it.cycle(self.datlst)
        fnames = ""
        while plotnum < plotnumlim:
            snumlim_tmp = sepnum if type(sepnum) != list else iter(sepnum) 
            if layout == "column" or layout == "column4":
                if type(glim) != type(None):
                    layoutdic[layout](glim, hgrid=hgrid, vgrid=vgrid)
                else:
                    layoutdic[layout](gnumlim, hgrid=hgrid, vgrid=vgrid)
            else:
                layoutdic[layout]()
            while gnum < gnumlim: 
                while snum < snumlim:
                    snum2lim = len(arrs[gnum][snum][abcs])
                    while snum2 < snum2lim:
                        if type(errs[gnum][lgtd]) == type(None):
                            self.grace.set_xydata(arrs[gnum][snum][abcs][snum2], arrs[gnum][snum][lgtd][snum2], gnum=gnum)
                        else:
                            self.grace.set_xydy(arrs[gnum][snum][abcs][snum2], arrs[gnum][snum][lgtd][snum2], arrs[gnum][snum][3][snum2], gnum=gnum, snum=snum)
                        snum2 += 1
                    snum2 = 0
                    snum += 1
                snum = 0
                if len(self.grace.prop.gdiclst): self.grace.set_graphitems()
                #if type(self.grace.prop.gdiclst[gnum]["lim"]) == type(None):
                #    self.grace.set_autoscale(arrs[gnum][snum][abcs][snum2], arrs[gnum][snum][lgtd][snum2], gnum=gnum)
                gnum += 1
            gnum = 0
            #fnames += " "  + fcnt(dirpath, filename,device)
            self.grace.set_ornament() 
            if dump: 
                self.grace.dumpfig(fcnt(self.dumppath, filename,extension=device), device)
            self.grace.open_grace()
            self.grace.initialize()
            plotnum += 1

    def tevo(self, layout="simple", abcs=0,lgtd=1, T=False, sepnum=1, dirname="tmpdir", filename="tmp", device="PDF", hgrid=1, vgrid=1, show=False):
        self.hist.input()
        layout = str(layout)
        layoutdic = {
                     "1"      : self.grace.layout_1,
                     "1_2"      : self.grace.layout_1_2,
                     "2"      : self.grace.layout_2,
                     "3"      : self.grace.layout_3,
                     "4"      : self.grace.layout_4,
                     "5"      : self.grace.layout_5,
                     "6"      : self.grace.layout_6,
                     "7"      : self.grace.layout_7,
                     "8"      : self.grace.layout_8,
                     "8_2"    : self.grace.layout_8_2,
                     "column" : self.grace.layout_column,
                     "column4": self.grace.layout_column_4grid,
                    }
        self.grace.prop.plot_init()
        self.T_align(T)

        arrs = []
        errs = []
        for dcls in self.datlst:
            arr, err = dcls.get_data(reterr=True)
            arrs += [arr]
            errs += [err]
                
        arrs = lstsplit(arrs, sepnum)
        plotnumlim = len(arrs[0][0][abcs])
        gnumlim = len(arrs)
        dirpath =  fcnt(self.dumppath+"/"+dirname)       
        os.mkdir(dirpath)
        plotnum = 0
        snum = 0
        gnum = 0
        cnt = it.cycle(self.datlst)
        fnames = ""
        while plotnum < plotnumlim:
            snumlim_tmp = sepnum if type(sepnum) != list else iter(sepnum) 
            if layout == "column":
                layoutdic[layout](gnumlim, hgrid=hgrid)
            else:
                layoutdic[layout](hgrid=hgrid, vgrid=vgrid)
            while gnum < gnumlim: 
                snumlim = snumlim_tmp if type(snumlim_tmp) == int else snumlim_tmp.next()
                while snum < snumlim:
                    if type(errs[gnum][lgtd]) == type(None):
                        #input(arrs[gnum][snum][abcs][plotnum])
                        #input(arrs[gnum][snum][lgtd][plotnum])
                        self.grace.set_xydata(arrs[gnum][snum][abcs][plotnum], arrs[gnum][snum][lgtd][plotnum], gnum=gnum )
                    else:
                        self.grace.set_xydy(arrs[gnum][snum][abcs][plotnum], arrs[gnum][snum][lgtd][plotnum], arrs[gnum][snum][3][plotnum], gnum=gnum, snum=snum)
                    snum += 1
                snum = 0
                #if len(self.grace.prop.gdiclst): self.grace.set_graphitems()
                gnum += 1
            gnum = 0
            fnames += " "  + fcnt(dirpath, filename,device)
            self.grace.set_ornament() 
            if len(self.grace.prop.gdiclst): self.grace.set_graphitems()
            self.grace.dumpfig(fcnt(dirpath, filename,device))
            if show: 
                self.grace.open_grace()
            self.grace.initialize()
            plotnum += 1

        os.system("pdftk %s/*.PDF output %s" %(dirpath, fcnt(self.dumppath, "tevo", device)))
        print "pdftk %s/*.PDF output %s" %(dirpath, fcnt(self.dumppath, "tevo", device))

    def show_graph(self):
        self.grace.open_grace()        
        self.grace.initialize()

    def view_col(self,  layout="single", T=None, axtpl=(0,2,1), xlim=None, ylim=None, zlim=None, device="png", opt="colz", palette="simple"):
        from modules.graph_utils.root_util.root_util import root_util
        self.T_align(T)
        r = root_util()
        layoutdic = {"single": r.single_layout,
                     "dual": r.dual_layout,
                     "sextuple" : r.sextuple_layout,
                     "1logz" : r.layout1_logz}
        palettedic = {"simple": r.mypalette1,
                      "simple3": r.mypalette3,
                      "simple4": r.mypalette4,
                      "rainbow": r.palette_rainbow,
                      "r2b": r.palette_red2blue}
        if type(T) != type(None) and T != self.T: self.transpose()
        for i, obj in enumerate(self.datlst):

            arrs = obj.get_data()
            x = arrs[axtpl[0]]
            y = arrs[axtpl[1]]
            z = arrs[axtpl[2]]
        
            bin_xtpl = tuple(x[0]) if x[0][1] != x[0][0] else tuple(x.transpose()[0]) # check the greater direction for multiarray.
            bin_ytpl = tuple(y[0]) if y[0][1] != y[0][0] else tuple(y.transpose()[0])
            if bin_xtpl[1] - bin_xtpl[0] < 0: bin_xtpl = bin_xtpl[::-1]  # check the greater direction for array.
            if bin_ytpl[1] - bin_ytpl[0] < 0: bin_ytpl = bin_ytpl[::-1] 

            r.set_xyzdata(tuple(x.reshape(x.size).tolist()),  tuple(y.reshape(y.size).tolist()), tuple(z.reshape(z.size).tolist()), bin_xtpl, bin_ytpl, i, 0)
            #r.show_prop()
            #r.dump_fig(fcnt(dirpath, filename, device))
            xlim = self.root.get_xlim(i)
            ylim = self.root.get_ylim(i)
            zlim = self.root.get_zlim(i)
            if type(xlim) != type(None): r.set_xlim(xlim[0], xlim[1], i)
            if type(ylim) != type(None): r.set_ylim(ylim[0], ylim[1], i)
            if type(zlim) != type(None): r.set_zlim(zlim[0], zlim[1], i)
            r.set_xname(self.root.get_xname(i), i)
            r.set_yname(self.root.get_yname(i), i)
            r.set_zname(self.root.get_zname(i), i)
        layoutdic[layout](opt)
        palettedic[palette]()
        for i in range(len(self.datlst)):
            for lst in self.root.get_box(i):
                #input(lst)
                #input(lst)
                r.set_box(*lst)
        r.view_graph()
#    def view_col(self,  layout="simple", T=None, axtpl=(0,2,1), xlim=None, ylim=None, zlim=None, device="png", opt="colz", palette="simple"):
#        self.T_align(T)
#        layoutdic = {"single": self.root.single_layout,
#                     "dual": self.root.dual_layout,
#                     "sextuple" : self.root.sextuple_layout}
#        palettedic = {"simple": self.root.mypalette1,
#                      "rainbow": self.root.rainbow_palette}
#        if type(T) != type(None) and T != self.T: self.transpose()
#        for i, obj in enumerate(self.datlst):
#
#            arrs = obj.get_data()
#            x = arrs[axtpl[0]]
#            y = arrs[axtpl[1]]
#            z = arrs[axtpl[2]]
#        
#            bin_xtpl = tuple(x[0]) if x[0][1] != x[0][0] else tuple(x.transpose()[0]) # check the greater direction.
#            bin_ytpl = tuple(y[0]) if y[0][1] != y[0][0] else tuple(y.transpose()[0])
#
#            self.root.set_xyzdata(tuple(x.reshape(x.size).tolist()),  tuple(y.reshape(y.size).tolist()), tuple(z.reshape(z.size).tolist()), bin_xtpl, bin_ytpl, i, 0)
#            #self.root.show_prop()
#            #self.root.set_prop()
#            #self.root.dump_fig(fcnt(dirpath, filename, device))
#        self.root.set_prop()
#        layoutdic[layout](opt)
#        palettedic[palette]()
#        self.root.view_graph()
    def get_seq(self):
        lst = []
        arrs = self.get_data()
        for a in arrs:
            if a is None:
                lst += [None]
                continue
            
            if (a[1,0,0] - a[0,0,0] == 0) and (a[0,1,0] - a[0,0,0] == 0) and (a[0,0,1] - a[0,0,0] != 0):
                lst += [2]
            elif (a[1,0,0] - a[0,0,0] == 0) and (a[0,1,0] - a[0,0,0] != 0) and (a[0,0,1] - a[0,0,0] == 0):
                lst += [1]
            elif (a[1,0,0] - a[0,0,0] != 0) and (a[0,1,0] - a[0,0,0] == 0) and (a[0,0,1] - a[0,0,0] == 0):
                lst += [0]
            else:
                lst += [None]
        return lst

                

    def tevo_col(self, layout="single", palette="simple",dirname="tmpdir", filename="tmp", T=(0,1,2), axtpl=(0,2,1), device="png", opt="colz", show=False):
        from modules.graph_utils.root_util.root_util import root_util
        self.transpose(T)
        dirpath = fcnt(self.dumppath+"/"+dirname)       
        os.mkdir(dirpath)
        #seqlst = self.get_seq()
        #for x,y,z,a in zip(self.x, self.y, self.z, self.a):
        
        arrs = self.get_data()
        xarr = arrs[axtpl[0]]
        yarr = arrs[axtpl[1]]
        zarr = arrs[6-array(axtpl).sum()] 
        aarr = arrs[axtpl[2]] if not arrs[axtpl[2]] is None else None

        seq = self.get_seq()
        
        xseq = [0,0,0]; xseq[seq[axtpl[0]]] = ":"; xseq = "[%s,%s,%s]" %tuple(xseq)
        
        exec "bin_xtpl = tuple(xarr%s)" %xseq
        yseq = [0,0,0]; yseq[seq[axtpl[1]]] = ":"; yseq = "[%s,%s,%s]" %tuple(yseq)
        exec "bin_ytpl = tuple(yarr%s)" %yseq
        #bin_xtpl = tuple(xarr[0][0] if xarr[0][0][0] != xarr[0][0][1] else xarr.transpose(0,2,1)[0][0])
        #bin_ytpl = tuple(yarr[0][0] if yarr[0][0][0] != yarr[0][0][1] else yarr.transpose(0,2,1)[0][0])
        i = 0
        n = len(arrs[0])
        while i < n:
            x = xarr[i]
            y = yarr[i]
            z = zarr[i]
            if not aarr is None: a = aarr[i]
            #input(x)
            #input(y)
            #input(z)
            #input(a)
            
            r = root_util()
            layoutdic = {"single": r.single_layout,
                         "dual": r.dual_layout,
                         "sextuple" : r.sextuple_layout,
                         "1logz" : r.layout1_logz}
            palettedic = {"simple": r.mypalette1,
                      "simple3": r.mypalette3,
                      "simple4": r.mypalette4,
                      "rainbow": r.palette_rainbow,
                      "r2b": r.palette_red2blue}
            #r.root_init()
            #r.set_xlim(0)
            #bin_xtpl = (1,2,3)
            #bin_ytpl = (1,2,3)
            #input(bin_xtpl)
            #input(bin_ytpl)
            #input(shape(x))
            #input(shape(a))
            xtpl = tuple(x.reshape(x.size).tolist())
            ytpl = tuple(y.reshape(y.size).tolist())
            ztpl = tuple(z.reshape(z.size).tolist())
            if not(len(xtpl) == len(ytpl) == len(ztpl)):
                raise ValueError, "Not mutch for data size between x, y and z (x = %s, y = %s and z = %s)." %(len(xtpl), len(ytpl), len(ztpl))
            
            r.set_xyzdata(tuple(x.reshape(x.size).tolist()),  tuple(y.reshape(y.size).tolist()), tuple(z.reshape(z.size).tolist()), bin_xtpl, bin_ytpl, 0, 0)
            xlim = self.root.get_xlim(0)
            ylim = self.root.get_ylim(0)
            zlim = self.root.get_zlim(0)
            if type(xlim) != type(None): r.set_xlim(xlim[0], xlim[1], 0)
            if type(ylim) != type(None): r.set_ylim(ylim[0], ylim[1], 0)
            if type(zlim) != type(None): r.set_zlim(zlim[0], zlim[1], 0)
            r.set_xname(self.root.get_xname(0), 0)
            r.set_yname(self.root.get_yname(0), 0)
            r.set_zname(self.root.get_zname(0), 0)

            #r.set_xlim(bin_xtpl[0], bin_xtpl[-1], 0)
            #r.set_ylim(bin_ytpl[0], bin_ytpl[-1], 0)
            #r.set_zlim(0, 1e-18, 0)
            #input(fcnt(dirpath, filename, device))
            layoutdic[layout](opt)
            palettedic[palette]()
            r.dump_fig(fcnt(dirpath, filename, device))
            if show: r.view_graph()
            i += 1
        
    def dump_pickle(self, picklepath=None):
        #for obj in self.datlst: obj.root = None
        self.hist.input()
        if type(picklepath) == type(None): picklepath = self.picklepath
        o = open(picklepath, "w")
        pickle.dump(self, o)
        o.close()

    def load_pickle(self, picklepath=None):
        if type(picklepath) == type(None): picklepath = self.picklepath
        o = open(picklepath)
        tmp = pickle.load(o)
        self.x = tmp.x
        self.y = tmp.y
        self.z = tmp.z
        self.a = tmp.a
        self.hist.hlst = tmp.hist.hlst
        self.datlst = tmp.datlst
        self.grace.prop.gdiclst = tmp.grace.prop.gdiclst
        self.grace.prop.decolst = tmp.grace.prop.decolst
        self.grace.prop.mkall = tmp.grace.prop.mkall
        o.close()
        
    def playback(self, index=0):
        self.hist.execute(index=index)
