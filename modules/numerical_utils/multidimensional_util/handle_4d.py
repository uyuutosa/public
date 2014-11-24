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
#from modules.graph_utils.root_util.root_util import * 

import os 
import itertools as it
import cPickle as pickle
            
from handle_graph import handle_graph, root_prop
import handle_3d as h3d
import handle_5d as h5d

def align_T(objlst, T):
    for obj in objlst:
        if obj.T != T: obj.transpose()


## Handle 4 dimension(Max).
#
# Description\n
#  handle_4d handle x, y, z and a that contain
#  the 2d numpy ndarray.\n
#  handle means that data can be manupulated and plotted easily.\n
#  Array is desired at least three and these of two has a serial 
#  in direction to an axis.\n In addtion, each direction of serial 
#  is needed to differ from each other.
class handle_4d(handle_graph):
    ## Initilize.
    #
    # Initilize object. dlst a list object which
    # include handle_3d objects.
    def __init__(self, dlst=None):
        self.x = None
        self.y = None
        self.z = None
        self.a = None
        self.xerr = None
        self.yerr = None
        self.zerr = None
        self.aerr = None
        self.T = False
        self.dumppath = "."
        self.grace = grace_util()
        self.root = root_prop()
        self.load = loaddat_util()
        self.write = writedat_util()
        self.bkuplst = []
        self.picklepath = "tmp"
        self.hist = method_history(self)
        if type(dlst) != type(None):
            self.set_multi(dlst)
    
    ## Set multiple object of handle_3d
    #
    # Description
    #  Make the handle_4d from multiple handle_3d object.
    #  
    def set_multi(self, objlst, T=True):
        self.T = T
        xarr_lst = []
        yarr_lst = []
        zarr_lst = []
        aarr_lst = []
        xerr_lst = []
        yerr_lst = []
        zerr_lst = []
        aerr_lst = []
        for obj in objlst:
            xarr_lst += [obj.x]
            yarr_lst += [obj.y]
            zarr_lst += [obj.z]
            aarr_lst += [obj.a]
            xerr_lst += [obj.xerr]
            yerr_lst += [obj.yerr]
            zerr_lst += [obj.zerr]
            aerr_lst += [obj.aerr]
        self.x = array(xarr_lst) if type(xarr_lst[0]) != type(None) else None
        self.y = array(yarr_lst) if type(yarr_lst[0]) != type(None) else None
        self.z = array(zarr_lst) if type(zarr_lst[0]) != type(None) else None
        self.a = array(aarr_lst) if type(aarr_lst[0]) != type(None) else None
        self.xerr = array(xerr_lst) if type(xerr_lst[0]) != type(None) else None
        self.yerr = array(yerr_lst) if type(yerr_lst[0]) != type(None) else None
        self.zerr = array(zerr_lst) if type(zerr_lst[0]) != type(None) else None
        self.aerr = array(aerr_lst) if type(aerr_lst[0]) != type(None) else None


    ## Transpose all array.
    #
    # Description\n
    #  Transpose all of attributed array. T is a sign whther the transpose occoured.\n
    # 
    # Argments\n
    #  T -- It may be three value.\n
    #    - If T is True or False and T equals self.T, transpose is occurred.\n
    #    - If T is None, transpose is occured.\n
    def transpose(self, T=None):
        arrs, errs = self.get_data(True)
        if T is None or T != self.T:
            self.dinput(
                [x.transpose() if not x is None else None for x in arrs],
                [x.transpose() if not x is None else None for x in errs]
                )
            self.T = False if self.T else True
    
    def sort(self):
        if self.T == False:
            self.transpose()
        
        self.dinput(map(lambda x: sorted(x) if type(x) != type(None) else None, self.get_data()))

    def dinput(self, arrlst, errlst=None):
        num = len(arrlst)
        
        self.x = array(arrlst[0]) if type(arrlst[0]) != type(None) else None
        self.y = array(arrlst[1]) if type(arrlst[1]) != type(None) else None
        self.z = array(arrlst[2]) if type(arrlst[2]) != type(None) else None
        if num >= 4: self.a = arrlst[3]
        if type(errlst) != type(None):
            self.xerr = array(errlst[0]) if type(errlst[0]) != type(None) else None
            self.yerr = array(errlst[1]) if type(errlst[1]) != type(None) else None
            self.zerr = array(errlst[2]) if type(errlst[2]) != type(None) else None
            if num >= 4: self.aerr = errlst[3]

    def get_data(self, reterr=False):
        x = array(self.x) if type(self.x) != type(None) else None
        y = array(self.y) if type(self.y) != type(None) else None
        z = array(self.z) if type(self.z) != type(None) else None
        a = array(self.a) if type(self.a) != type(None) else None
        arrlst = [x, y, z, a]
        xerr = array(self.xerr) if type(self.xerr) != type(None) else None
        yerr = array(self.yerr) if type(self.yerr) != type(None) else None
        zerr = array(self.zerr) if type(self.zerr) != type(None) else None
        aerr = array(self.aerr) if type(self.aerr) != type(None) else None
        arrlst = [x, y, z, a]
        errlst = [xerr, yerr, zerr, aerr]
        if reterr: 
            return [arrlst, errlst]
        else:
            return arrlst
    
    def rid_diff(self, obj, xyz, T=None):
        """
        """
        
        self.transpose(T)
        obj.transpose(T)

        arrs = self.get_data()
        arrs2 = obj.get_data()
        x_arr = arrs[xyz]
        x2_arr = arrs2[xyz]

        Tlst = []
        for x in x_arr:
            if x in x2_arr:
                Tlst += [True]
            else:
                Tlst += [False]
        arrs = [x[array(Tlst)] if not x is None else None for x in arrs]
        self.rdiff = handle_4d()
        self.rdiff.dinput(arrs)
        self.rdiff.T = T

            
        
    def dump_txt(self, path=None, conca=False, tag=None):
        if path: path = self.dumppath
        if self.T:
            tmplst = self.get_data()

            if conca:
                # Note: Only refer to x and y array. 
                datlst = append([tmplst[0][0]], tmplst[1], axis=0)
                self.write.writedat(fcnt(path, "tmp", "txt"), datlst, tag)
            else:
                n = 0
                while n < len(tmplst[0]):
                    datlst = []
                    for tmp in tmplst:
                        if type(tmp) != type(None): datlst += [tmp[n]]
                    self.write.writedat(fcnt(path, "tmp", "txt"), datlst, tag)
                    n += 1
        else:
            self.write.write_tevo(self)

    def dump_pickle(self, picklepath=None):
        if type(picklepath) == type(None): picklepath = self.picklepath
        o = open(picklepath, "w")
        pickle.dump(self, o)
        o.close()

    def load_pickle(self, picklepath=None):
        if type(picklepath) == type(None): picklepath = self.picklepath
        o = open(picklepath)
        tmp = pickle.load(o)
        self.T = tmp.T
        self.dinput(tmp.get_data())
        self.hist.hlst = tmp.hist.hlst
        self.grace.prop.gdiclst = tmp.grace.prop.gdiclst
        self.grace.prop.decolst = tmp.grace.prop.decolst
        self.grace.prop.mkall = tmp.grace.prop.mkall
        o.close()

    def backup(self):
        s = TemporaryFile()
        pickle.dump(self, s)
        s.seek(0)
        self.bkuplst += [s]

    def restore(self, num):
        s = self.bkuplst[num]
        ret = pickle.load(s)
        s.seek(0)
        return ret

    def view_col(self,  layout="simple", T=None, axtpl=(0,2,1), xlim=None, ylim=None, zlim=None, device="png", opt="colz", palette="simple", serial=False):
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
        if type(T) != type(None) and T != self.T: self.transpose()

        arrs = self.get_data()
        x = arrs[axtpl[0]]
        y = arrs[axtpl[1]]
        z = arrs[axtpl[2]]
        
        if serial:
            bin_xtpl = tuple(x[0]) if x[0][1] != x[0][0] else tuple(x.transpose()[0]) # check the greater direction.
            bin_ytpl = tuple(y[0]) if y[0][1] != y[0][0] else tuple(y.transpose()[0])
            r.set_xyzdata(tuple(x.reshape(x.size).tolist()),  tuple(y.reshape(y.size).tolist()), tuple(z.reshape(z.size).tolist()), bin_xtpl, bin_ytpl, 0, 0)
        else:
            input("asdf")
            r.set_xyzdata_tgraph(tuple(x.reshape(x.size).tolist()),  tuple(y.reshape(y.size).tolist()), tuple(z.reshape(z.size).tolist()), 0, 0)
        #r.set_xlim(bin_xtpl[0], bin_xtpl[-1], 0)
        #r.set_ylim(bin_ytpl[0], bin_ytpl[-1], 0)
        #r.show_prop()
        #r.set_prop()
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
        #r.dump_fig(fcnt(dirpath, filename, device))
        r.view_graph()

    def view_root(self, modelst, T=False, gtime=5, sepnum=1, abcs=2, lgtd=1):

        a = rootmacro()
        for m in modelst:
            if m == "color":
                arrs = self.get_data()
                x = arrs[3 - abcs - lgtd]
                y = arrs[abcs]
                z = arrs[lgtd]
                a.set_xyzdata(x,y,z)
                a.th2()
                a.set_colmap()
                a.Fill()
                a.set_cont(99)
            elif m == "tgraph":
                tmplst = self.release(gtime, T=T, trans=None)
                #tmp = self.release([gtime], trans=3-abcs-lgtd)
                #a.modelst()
                if type(tmplst) != list: tmpslt = [tmplst]
                xlst = []
                ylst = []
                for i,tmp in enumerate(tmplst):
                    arrs = tmp.get_data()
                    a.set_xydata(arrs[abcs], arrs[lgtd], gnum=i)
                a.dump_data()
                a.set_data()
                for num in range(len(gtime)):
                    a.tgraph([num], gnum=num)
                        
        a.simplelayout()   
        a.unset_stat()
        a.dump_macro()
        a.open_macro()
       

    def view_tmp(self, abcs=2, lgtd=1):
        arrs = self.get_data()
        x = arrs[3 - abcs - lgtd]
        y = arrs[abcs]
        z = arrs[lgtd]

        a = rootmacro()
        a.set_xyzdata(x,y,z)
        a.ldump()
        a.open_macro()
        
    def crosscorr(self, tau, cmpcls, abcs=0, lgtd=1, T=True):
#        point = self.release(point_val, trans=True)
        if T != self.T: self.transpose()
        if T != cmpcls.T: cmpcls.transpose()

        con = container()
        for n in range(len(self.x)):
            tmp1 = self.release([n], multi=False, T=T)
            tmp2 = cmpcls.release([n], multi=False, T=T)
            #tmp1 = handle_3d(arr1)
            #tmp2 = handle_3d(arr2)
            tmp1.crosscorr(tau, tmp2, abcs, lgtd)
            con.stack(*tmp1.ccor.get_data())
            
        #con.ndarr()
        self.pcnv = handle_4d()
        self.pcnv.T = self.T
        self.pcnv.dinput(con.get())

    def envelope(self, pnum=False, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        xarr = arrs[0]
        yarr = arrs[1]
        zarr = arrs[2]
        arrs2 = obj.get_data()
        xarr2 = arrs2[0]
        yarr2 = arrs2[1]
        zarr2 = arrs2[2]

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            x2 = xarr2[i] if not xarr2 is None else None
            y2 = yarr2[i] if not yarr2 is None else None
            z2 = zarr2[i] if not zarr2 is None else None
            a = h3d.handle_3d(x, y, z)
            b = h3d.handle_3d(x2, y2, z2)
            a.envelope(b, abcs=abcs, lgtd=lgtd)
            lst += [a.env]

        self.env = handle_4d()
        self.env.set_multi(lst)
        self.env.T = self.T

    def phase_difference(self, obj, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        xarr = arrs[0]
        yarr = arrs[1]
        zarr = arrs[2]
        obj.transpose(T)
        arrs2 = obj.get_data()
        xarr2 = arrs2[0]
        yarr2 = arrs2[1]
        zarr2 = arrs2[2]

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            x2 = xarr2[i] if not xarr2 is None else None
            y2 = yarr2[i] if not yarr2 is None else None
            z2 = zarr2[i] if not zarr2 is None else None
            a = h3d.handle_3d(x, y, z)
            b = h3d.handle_3d(x2, y2, z2)
            a.phase_difference(b, abcs=abcs, lgtd=lgtd)
            lst += [a.phd]

        self.phd = handle_4d()
        self.phd.set_multi(lst)
        self.phd.T = self.T

    def mean_axis(self, T=False):
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        xarr = arrs[0]
        yarr = arrs[1]
        zarr = arrs[2]

        if xarr is not None: xarr = xarr.mean(axis=0)
        if yarr is not None: yarr = yarr.mean(axis=0)
        if zarr is not None: zarr = zarr.mean(axis=0)

        self.mean = h3d.handle_3d(xarr, yarr, zarr)


        

    def mean_power(self, obj, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        xarr = arrs[0]
        yarr = arrs[1]
        zarr = arrs[2]
        obj.transpose(T)
        arrs2 = obj.get_data()
        xarr2 = arrs2[0]
        yarr2 = arrs2[1]
        zarr2 = arrs2[2]

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            x2 = xarr2[i] if not xarr2 is None else None
            y2 = yarr2[i] if not yarr2 is None else None
            z2 = zarr2[i] if not zarr2 is None else None
            a = h3d.handle_3d(x, y, z)
            b = h3d.handle_3d(x2, y2, z2)
            a.mean_power(b, abcs=abcs, lgtd=lgtd)
            lst += [a.mvi]

        self.mvi = handle_4d()
        self.mvi.set_multi(lst)
        self.mvi.T = self.T

    def reverse(self, T=None):
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        self.rev = handle_4d()
        self.rev.dinput([x[:,::-1] if x is not None else None for x in arrs])
        self.rev.T = self.T


    def pow_spec_ensemble(self, wid, pnum=False, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        xarr = arrs[0]
        yarr = arrs[1]
        zarr = arrs[2]

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            obj.pow_spec_ensemble(wid, abcs=abcs, lgtd=lgtd)
            lst += [obj.epow]

        self.epow = handle_4d()
        self.epow.set_multi(lst)
        self.epow.T = self.T

    def cross_phase_ensemble(self, obj, wid, pnum=False, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        arrs2 = obj.get_data()
        xarr = arrs[0]
        yarr = arrs[1]
        zarr = arrs[2]
        xarr2 = arrs2[0]
        yarr2 = arrs2[1]
        zarr2 = arrs2[2]

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            x2 = xarr2[i] if not xarr2 is None else None
            y2 = yarr2[i] if not yarr2 is None else None
            z2 = zarr2[i] if not zarr2 is None else None
            obj = h3d.handle_3d(x, y, z)
            obj2 = h3d.handle_3d(x2, y2, z2)
            obj.cross_phase_ensemble(obj2, wid, abcs=abcs, lgtd=lgtd)
            lst += [obj.ecph]

        self.ecph = handle_4d()
        self.ecph.set_multi(lst)
        self.ecph.T = self.T

    def phase_spec_ensemble(self, wid, pnum=False, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        xarr = arrs[0]
        yarr = arrs[1]
        zarr = arrs[2]

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            obj.phase_spec_ensemble(wid, abcs=abcs, lgtd=lgtd)
            lst += [obj.ephase]

        self.ephase = handle_4d()
        self.ephase.set_multi(lst)
        self.ephase.T = self.T

    def pow_spec(self, pnum=False, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        xarr = arrs[0]
        yarr = arrs[1]
        zarr = arrs[2]

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            obj.pow_spec(abcs=abcs, lgtd=lgtd)
            lst += [obj.pow]

        self.pow = handle_4d()
        self.pow.set_multi(lst)
        self.pow.T = self.T

    def phase_spec(self, pnum=False, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        xarr = arrs[0]
        yarr = arrs[1]
        zarr = arrs[2]

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            obj.phase_spec(abcs=abcs, lgtd=lgtd)
            lst += [obj.phase]

        self.phase = handle_4d()
        self.phase.set_multi(lst)
        self.phase.T = self.T

    def iterp_ave(self, itvl, wid, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        xarr,yarr,zarr, a = self.get_data()

        objlst = []
        for i in range(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            
            obj = h3d.handle_3d(x, y, z)
            obj.iterp_ave(itvl, wid, abcs, lgtd)
            objlst += [obj.iave]

        self.iave = handle_4d()
        self.iave.set_multi(objlst)
        self.iave.T = self.T

    def slice_same(self, obj, xyz=0, err=0, T=None, round=None):
        self.transpose(T)
        if obj.__module__.split(".")[-1] == "handle_4d":
            obj.transpose(T)
        self.hist.input()
        xarr,yarr,zarr,aarr = self.get_data()
        arrs2 = obj.get_data()
        xarr2 = arrs2[xyz]
        
        if len(xarr2.shape) == 1:
            #if x2[0][1] - x2[0][0] == 0: x2 = x2.transpose()
            xarr2 = tile(xarr2,(len(xarr),1))
            
        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj1 = h3d.handle_3d(x,y,z)
            obj2 = h3d.handle_3d(xarr2[0],xarr2[0],xarr2[0])
            obj1.slice_same(obj2,xyz, err, round=round)
            lst += [obj1.slice]
        self.slice = handle_4d()
        self.slice.T = self.T
        self.slice.set_multi(lst)

    def round(self, n):
        self.x = self.x.round(n) if not self.x is None else None
        self.y = self.y.round(n) if not self.y is None else None
        self.z = self.z.round(n) if not self.z is None else None

    def interp(self, cnvlst, xyz=0, comments="#", delim=","):
        #if self.T: self.transpose()
        arrlst = self.get_data()
        arrs = arrlst[xyz]
        tmparr = []
        for arr in arrs:
            tmp = h3d.handle_3d(arr)
            tmp.interp(cnvlst, 0, comments, delim)
            tmparr += [tmp.itp.get_data()[0]]
        arrlst[xyz] = tmparr
        self.itp = handle_4d()
        self.itp.T = self.T
        self.itp.dinput(arrlst)

    def prmconv(self, cnvlst, xyz=0, comments="#", delim=","):
        #if self.T: self.transpose()
        arrlst = self.get_data()
        arrs = arrlst[xyz]
        tmparr = []
        for arr in arrs:
            tmp = h3d.handle_3d(arr)
            tmp.prmconv(cnvlst, 0, comments, delim)
            tmparr += [tmp.pcnv.get_data()[0]]
        arrlst[xyz] = tmparr
        self.pcnv = handle_4d()
        self.pcnv.T = self.T
        self.pcnv.dinput(arrlst)

    def punch_out(self, plst, xyz=0, inv=False, T=False):
        if self.T != T: self.transpose()
        arrlst = self.get_data()
        tmplst = []
        n = 0
        xtlst = []
        ytlst = []
        ztlst = []
        while n < len(arrlst[xyz]):
            x = arrlst[0][n] if type(arrlst[0]) != type(None) else None
            y = arrlst[1][n] if type(arrlst[1]) != type(None) else None
            z = arrlst[2][n] if type(arrlst[2]) != type(None) else None
            tmp = h3d.handle_3d(x, y, z)
            tmp.punch_out(plst, xyz, inv)
            xtmp,ytmp,ztmp = tmp.pout.get_data()
            xtlst += [xtmp]
            ytlst += [ytmp]
            ztlst += [ztmp]
            n += 1

        tmparr = [array(xtlst), array(ytlst), array(ztlst)]
        self.pout = handle_4d()
        self.pout.T = self.T
        self.pout.dinput(tmparr)


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
        self.pave = handle_4d()
        self.pave.T = True
        self.pave.dinput(array(retlst))    
            
        

    def slice_arr(self, slst, xyz=0, T=None, err=0):
        self.transpose(T)
            
        arrs,errs = self.get_data(reterr = True)
        arr = arrs[xyz]
        retlst = []
        for i in xrange(len(arr)):
            xarr = arrs[0][i] if not arrs[0] is None else None
            yarr = arrs[1][i] if not arrs[1] is None else None
            zarr = arrs[2][i] if not arrs[2] is None else None
            obj = h3d.handle_3d(xarr, yarr, zarr)
            if not obj.slice_arr(slst, xyz, err=err):
                raise ValueError, "Can not sliced"
            retlst += [obj.slice]
        
        self.slice = handle_4d()
        self.slice.set_multi(retlst)
        self.slice.T = self.T

#    def slice_arr(self, slst, xyz=0, T=True):
#        if self.T != T: self.transpose()
#            
#        arrs,errs = self.get_data(reterr = True)
#        arr = arrs[xyz]
#        retlst = [[],[],[],[]]
#        retlst_err = [[],[],[],[]]
#        for i in range(len(arr)):
#            n = max([find_dec_place(x) for x in arr[i]])
#            tmparr = array([x[i][where((slst[0] <= arr[i].round(n)) == (arr[i].round(n) <= slst[1]))[0]] if type(x) != type(None) else None for x in arrs])
#            map(lambda x,y: x.append(y) if type(y) != type(None) else None, retlst, tmparr)
#            tmperr = array([x[i][where((slst[0] <= arr[i].round(n)) == (arr[i].round(n) <= slst[1]))[0]] if type(x) != type(None) else None for x in errs])
#            map(lambda x,y: x.append(y) if type(y) != type(None) else None, retlst_err, tmperr)
#        
#        self.slice = handle_4d()
#        retlst = [x if len(x) != 0 else None for x in retlst]
#        retlst_err = [x if len(x) != 0 else None for x in retlst_err]
#        self.slice.dinput(retlst, retlst_err)
#        self.slice.T = self.T

    def dump_txt_select(self, index, T=True, path=None, conca=False, tag=None, trans=None):
        ret = self.release(index, multi=True, T=T, trans=trans)
        ret.dump_txt(path, conca, tag)
        
        
    def release(self, index, multi=False, trans=None):
        elm = None
        err = None

        if ":" in index:
            arrs = self.get_data()
            i = [int(x) for x in index.split(":")]
            if not trans is None:
                i = val2index(arrs[trans], i)
            xlst = arrs[0][i[0]:i[-1]] if not arrs[0] is None else None
            ylst = arrs[1][i[0]:i[-1]] if not arrs[1] is None else None
            zlst = arrs[2][i[0]:i[-1]] if not arrs[2] is None else None
            if not self.zerr is None:
                err = self.zerr[i[0]:i[-1]]
        else:
            xlst = []
            ylst = []
            zlst = []

            if not trans is None:
                if type(index) == str:
                    index = [float(x) for x in str(index).split(",")]
                arrs = self.get_data()
                if arrs[trans][1][1] == arrs[trans][1][0]:
                    self.transpose()
                    arrs = self.get_data()
                index = val2index(arrs[trans][0], index)
            else:
                if type(index) == str:
                    index = [int(x) for x in str(index).split(",")]
            #'index' as string is transform as list as above.
            self.transpose()
            arrs = self.get_data()
            elm = len(index)
            # Get array if  array[0] == num.
            for num in index:
                if  type(arrs[0]) != type(None): 
                    xlst += [arrs[0][num]]  
                else:
                    xlst += [None]
                if  type(arrs[1]) != type(None): 
                    ylst += [arrs[1][num]]  
                else:
                    ylst += [None]

                if  type(arrs[2]) != type(None): 
                    zlst += [arrs[2][num]]  
                else:
                    zlst += [None]

                if type(self.zerr) != type(None):
                    err += [self.zerr[num]]
        
        if err is None: zerr = None
        if multi:
            if type(xlst[0]) == type(None): xlst = None
            if type(ylst[0]) == type(None): ylst = None
            if type(zlst[0]) == type(None): zlst = None
            ret = handle_4d()
            ret.T = self.T
            ret.dinput([xlst, ylst, zlst])
            return ret
        else:
            if elm == 1:
                if type(err) != type(None):
                    return map(lambda x,y,z,err: h3d.handle_3d(x,y,z, err=err), xlst, ylst, zlst, err)[0]
                else:
                    return map(lambda x,y,z: h3d.handle_3d(x,y,z), xlst, ylst, zlst)[0]
            else:
                if type(xlst) == type(None) and type(ylst) == type(None) and type(zlst) == type(None): raise ValueError, "No match index. By any chance, didn't you miss T setting?"
                if type(xlst) == type(None): xlst = [None for n in xrange(len(index))]     
                if type(ylst) == type(None): ylst = [None for n in xrange(len(index))]     
                if type(zlst) == type(None): zlst = [None for n in xrange(len(index))]     
                
                return map(lambda x,y,z: h3d.handle_3d(x,y,z), xlst, ylst, zlst)
                
        


    def extract(self, para, xyz=0, T=False):
        if self.T == T:
            self.transpose()

        lst = self.get_data()
        
        x = lst[xyz]
        d = x[0][1] - x[0][0]
        i = int((para - x[0][0])/ d)

        self.transpose()
        lst = self.get_data()
        x = lst[0][i] if type(lst[0]) != type(None) else None
        y = lst[1][i] if type(lst[1]) != type(None) else None
        z = lst[2][i] if type(lst[2]) != type(None) else None
        return h3d.handle_3d(x, y, z)

    def zero_adj(self, plst, abcs=0, lgtd=1, inv=True):
        if self.T == False:
            self.transpose()

        arrs, errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        for i in range(len(x)):
            if x[i][0] > plst[0] or x[i][-1] < plst[1]:
                raise ValueError, "Inputed range exeeds data range." \
                "(Inputed min, max = %s, %s. Data min, max = %s, %s" %(plst[0], plst[1], x[i][0], x[i][-1])
            obj = h3d.handle_3d(x[i], y[i])
            obj.slice_arr(plst)
            y[i] -= obj.slice.y.mean()
            #y[i] -= y[i][where((plst[0] <= x[i]) == (x[i] <= plst[1]))[0]].mean()
            arrs[abcs][i] = x[i]
            arrs[lgtd][i] = y[i]
        self.zadj = handle_4d()
        self.zadj.dinput(arrs, errs)
        self.zadj.T = True

    def get_xyz(self, abcs, lgtd):
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3-abcs-lgtd]
        return x, y, z

    def resample(self, flst, prec=10, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        xarr,yarr,zarr, a = self.get_data()

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            obj.resample(flst, prec=prec, abcs=abcs, lgtd=lgtd)
            lst += [obj.rsmp]

        self.rsmp = handle_4d()
        self.rsmp.set_multi(lst)
        self.rsmp.T = self.T

    def filter_decimation2(self, flst, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        xarr,yarr,zarr, a = self.get_data()

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            obj.filter_decimation2(flst, abcs, lgtd)
            lst += [obj.dfilt]

        self.dfilt = handle_4d()
        self.dfilt.set_multi(lst)
        self.dfilt.T = self.T

    def runge_kutta_4th(self, abcs=0, lgtd=1, st=None, en=None, h=None, ini_val=None, T=None):
        from numpy import array, mean
        from decimal import Decimal
        self.hist.input()
        self.transpose(T)
        xarr,yarr,zarr, a = self.get_data()

        lst = []
        for i in range(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            tmp_ini_val = ini_val[i] if type(ini_val) == list or not ini_val is None else ini_val
            obj = h3d.handle_3d(x, y, z)
            obj.runge_kutta_4th(abcs, lgtd, st, en, h, tmp_ini_val)
            lst += [obj.rk4]

        self.rk4 = handle_4d()
        self.rk4.set_multi(lst)
        self.rk4.T = self.T

    def runge_kutta_4th_tmp(self, abcs=0, lgtd=1, st=0, en=100, h=1, ini_val=None, T=None):
        from numpy import array, mean
        from decimal import Decimal
        self.hist.input()
        self.transpose(T)
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]

        lst = []


        if ini_val is None: ini_val = array(x)

        parr = arange(st, en, h)

     
        f = array(y)
        y = ini_val
        xlst = []
        ylst = []
        for i in xrange(len(parr)):
            y = y + h * f
            xlst += [x[80][80]]
            ylst += [y[80][80]]

        arrs[abcs] = append(array([]),array(xlst))
        arrs[lgtd] = append(array([]),array(ylst))

        self.rk4 = h3d.handle_3d()
        self.rk4.dinput(arrs)
        self.rk4.T = self.T

    def euler_method(self, abcs=0, lgtd=1, st=None, en=None, d=None, T=None):
        from numpy import array, mean
        from decimal import Decimal
        self.hist.input()
        self.transpose(T)
        xarr,yarr,zarr, a = self.get_data()

        lst = []
        for i in range(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            obj.euler_method(abcs, lgtd, st, en, d)
            lst += [obj.euler]

        self.euler = handle_4d()
        self.euler.set_multi(lst)
        self.euler.T = self.T


    def mov_ave(self, wid, abcs=0, lgtd=1, T=None):
        from numpy import array, mean
        from decimal import Decimal
        self.hist.input()
        self.transpose(T)
        xarr,yarr,zarr, a = self.get_data()

        lst = []
        for i in range(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            obj.mov_ave(wid, abcs, lgtd)
            lst += [obj.mave]

        self.mave = handle_4d()
        self.mave.set_multi(lst)
        self.mave.T = self.T

    def mov_grad(self, wid, abcs=0, lgtd=1, T=None, retL=False):
        from numpy import array, mean
        from decimal import Decimal
        self.hist.input()
        self.transpose(T)
        xarr,yarr,zarr, a = self.get_data()

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            L = obj.mov_grad(wid, abcs, lgtd, retL=retL)
            lst += [obj.mgrad]

        self.mgrad = handle_4d()
        self.mgrad.set_multi(lst)
        self.mgrad.T = self.T
        if retL: return L

    def sort_theta(self, wid, abcs=0, lgtd=1, T=None):
        from numpy import array, mean
        from decimal import Decimal
        self.hist.input()
        self.transpose(T)
        xarr,yarr,zarr, a = self.get_data()

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            obj.sort_theta()
            lst += [obj.theta]

        self.theta = handle_4d()
        self.theta.set_multi(lst)
        self.theta.T = self.T
        
    def mov_var(self, wid, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        xarr,yarr,zarr, a = self.get_data()

        lst = []
        for i in xrange(len(xarr)):
            x = xarr[i] if not xarr is None else None
            y = yarr[i] if not yarr is None else None
            z = zarr[i] if not zarr is None else None
            obj = h3d.handle_3d(x, y, z)
            obj.mov_var(wid, abcs, lgtd)
            lst += [obj.mvar]

        self.mvar = handle_4d()
        self.mvar.set_multi(lst)
        self.mvar.T = self.T

    def eval_cond(self, cond, val_F="nan"):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal

        x = self.x
        y = self.y
        z = self.z
        a = self.a
        xerr = self.xerr
        yerr = self.yerr
        zerr = self.zerr
        aerr = self.aerr

        exec "arr = where(%s, %s, x)" %(cond, val_F)
        self.cond = handle_4d()
        self.cond.T = self.T
        exec "x = where(%s, %s, x)" %(cond, val_F)
        self.cond.x = x[tof] if not x is None else None
        exec "x = where(%s, %s, x)" %(cond, val_F)
        self.cond.y = y[tof] if not y is None else None
        exec "x = where(%s, %s, x)" %(cond, val_F)
        self.cond.z = z[tof] if not z is None else None
        exec "x = where(%s, %s, x)" %(cond, val_F)
        self.cond.a = a[tof] if not a is None else None
        exec "x = where(%s, %s, x)" %(cond, val_F)
        self.cond.xerr = xerr[tof] if not xerr is None else None
        exec "x = where(%s, %s, x)" %(cond, val_F)
        self.cond.yerr = yerr[tof] if not yerr is None else None
        exec "x = where(%s, %s, x)" %(cond, val_F)
        self.cond.zerr = zerr[tof] if not zerr is None else None
        exec "x = where(%s, %s, x)" %(cond, val_F)
        self.cond.aerr = aerr[tof] if not aerr is None else None

    def bindup( self, width, xyz=0, retnum=None, T=False):
        if self.T != T: self.transpose()
        arrlst = self.get_data()
        xretlst = []
        yretlst = []
        zretlst = []
        aretlst = []
        width = float(width)
        for n in range(len(arrlst[0])):
            tmp = h3d.handle_3d(array(arrlst[0][n]) if type(arrlst[0]) != type(None) else None,
                              array(arrlst[1][n]) if type(arrlst[1]) != type(None) else None,
                              array(arrlst[2][n]) if type(arrlst[2]) != type(None) else None)
            num = tmp.bindup(width, xyz=xyz, retnum=True)
            retarrlst  = tmp.bind.get_data()
            xret, yret, zret, aret = retarrlst

            xret, yret, zret, aret = tmp.bind.get_data()
            xretlst = xretlst + [xret] if type(xret) != type(None) else None
            yretlst = yretlst + [yret] if type(yret) != type(None) else None
            zretlst = zretlst + [zret] if type(zret) != type(None) else None
            aretlst = aretlst + [aret] if type(aret) != type(None) else None
            
        self.bind = handle_4d()
        self.bind.dinput([xretlst,yretlst,zretlst,aretlst])
        if retnum:
            return num
    
    def bind_std(self, width, xyz=2):
        self.bindup(width)
        retlsts = []
        for i, arrs in enumerate(self.bind.get_data()):
            retlst = []
            for arr in arrs:
                if i == xyz:
                    ret = map(lambda x: x.std(), arr)
                else:
                    ret = map(lambda x: x.mean(), arr)
                retlst += [ret]
            retlsts += [retlst]
        retlsts = array(retlsts)
        self.bstd = handle_4d()
        self.bstd.dinput(retlsts)
        return retlsts
        
    def bind_std_arb(self, itvl=0.01, wid=0.1, abcs=0, lgtd=1):
        #self.bindup(width)
        retlsts = [[],[],[]]
        arrlst = self.get_data()
        length = len(arrlst[abcs]) 
        for i in range(length):
            for n in range(3):
                if n == lgtd:
                    retlsts[n] += [std_arb(arrlst[abcs][i],arrlst[lgtd][i], itvl, wid)[1]] if type(arrlst[n]) != type(None) else None
                    #input(std_arb(arrlst[abcs][i],arrlst[lgtd][i], itvl, wid) if type(arrlst[n]) != type(None) else None)
                else:
                    #input(arrlst[abcs][i])
                    #input(arrlst[n][i])
                    retlsts[n] += [ave_arb(arrlst[abcs][i],arrlst[n][i], itvl, wid)[1]] if type(arrlst[n]) != type(None) else None
                #input(retlsts)
        retlsts = array(retlsts)
        self.bstd = handle_4d()
        self.bstd.dinput(retlsts)

    def grad_arb(self, itvl=0.01, wid=0.1, abcs=2, lgtd=1, T=True):
        if self.T != T: self.transpose()
        retlsts = [[],[],[]]
        arrlst = self.get_data()
        length = len(arrlst[abcs]) 
        for i in range(length):
            abarr, lgarr = grad_arb(arrlst[abcs][i], arrlst[lgtd][i], itvl, wid) 
            retlsts[abcs] += [abarr]
            retlsts[lgtd] += [lgarr]
            retlsts[3-abcs-lgtd] = retlsts[3-abcs-lgtd] + [arrlst[3-abcs-lgtd][i][0]*ones(len(abarr))]  if type(arrlst[3-abcs-lgtd]) != type(None) else None
        self.grad = handle_4d()
        self.grad.T = self.T
        self.grad.dinput(retlsts)

    def run_pow(self, itvl, wid, abcs=0, lgtd=1):
        self.hist.input()
        #self.bindup(wid)
        arrs = self.get_data()
        xarr = arrs[abcs]
        yarr = arrs[lgtd]
        zarr = arrs[3 - abcs - lgtd]

        lst = []
        for x, y, z in zip(xarr, yarr, zarr):
            obj = h3d.handle_3d(x, y, z)
            obj.run_pow(itvl, wid, abcs, lgtd)
            #for i in obj.rpow.a: print len(i)
            lst += [obj.rpow]

        self.rpow = h5d.handle_5d()
        self.rpow.set_multi(lst)

    def mov_pow(self, wid, abcs=0, lgtd=1, T=None):
        self.hist.input()
        self.transpose(T)
        #self.bindup(wid)
        arrs = self.get_data()
        xarr = arrs[abcs]
        yarr = arrs[lgtd]
        zarr = arrs[3 - abcs - lgtd]

        lst = []
        for x, y, z in zip(xarr, yarr, zarr):
            obj = h3d.handle_3d(x, y, z)
            obj.mov_pow(wid, abcs, lgtd)
            #for i in obj.rpow.a: print len(i)
            lst += [obj.mpow]

        self.mpow = h5d.handle_5d()
        self.mpow.set_multi(lst)

    def gnufit(self, function, fitparalst, stnum=None, ennum=None, itvl=1, abcs=2, lgtd=1, T=False):
        if self.T != T: self.transpose()
        retlsts = [[],[],[]]
        arrlst = self.get_data()
        length = len(arrlst[abcs]) 
        tmplst = []
        for i in range(length):
            tmp = h3d.handle_3d(arrlst[abcs][i], arrlst[lgtd][i])
            tmp.gnufit(function, fitparalst, stnum, ennum, itvl)
            abarr, lgarr, noval = tmp.gnu.get_data()
            tmplst += [tmp.gnu.fitpara]
            retlsts[abcs] += [abarr]
            retlsts[lgtd] += [lgarr]
            retlsts[3-abcs-lgtd] += [arrlst[3-abcs-lgtd][i][0]*ones(len(abarr))] if type(arrlst[3-abcs-lgtd]) != type(None) else [None]
        self.gnu = handle_4d()
        self.gnu.T = self.T
        self.gnu.dinput(retlsts)
        self.gnu.fitpara = tmplst

    def polyfit(self, M=8, stnum=None, ennum=None, itvl=1, abcs=2, lgtd=1, T = None, show=False):
        self.transpose(T)
        retlsts = [[],[],[]]
        arrlst, errlst = self.get_data(reterr=True)
        length = len(arrlst[abcs]) 
        sen = [stnum, ennum, itvl]
        for i in xrange(length):
            if type(stnum) == type(None):
                sen[0] = arrlst[abcs][i][0]    
            if type(ennum) == type(None):
                sen[1] = arrlst[abcs][i][-1]    
            
            try:
                abarr, lgarr = pfit(arrlst[abcs][i], arrlst[lgtd][i], M, sen) 
            except IndexError:
                input(arrlst[lgtd])
                input(len(arrlst[lgtd]))
                input(i)
                input(arrlst[abcs][i])
                input(arrlst[lgtd][i])
            if show:
                a = h3d.handle_3d(arrlst[abcs][i],arrlst[lgtd][i])
                b = h3d.handle_3d(abarr, lgarr)
                c = a + b
                c.view(abcs=0, lgtd=1)
                fin = raw_input("View next graph. if you finish confirm, type 'end'")
                if len(fin) == 0: pass
                elif fin[0] == "e": show = False
            retlsts[abcs] += [abarr]
            retlsts[lgtd] += [lgarr]
            retlsts[3-abcs-lgtd] = retlsts[3-abcs-lgtd] + [arrlst[3-abcs-lgtd][i][0]*ones(len(abarr))] if type(arrlst[3-abcs-lgtd]) != type(None) else None
        self.pfit = handle_4d()
        self.pfit.T = self.T
        self.pfit.dinput(retlsts, errlst)

    def bind_mean(self, width):
        self.bindup(width)
        retlsts = []
        for arrs in self.bind.get_data():
            retlst = []
            for arr in arrs:
                ret = map(lambda x: x.mean(), arr)
                retlst += [ret]
            retlsts += [retlst]
        retlsts = array(retlsts)
        self.bmean = handle_4d()
        self.bmean.dinput(retlsts)
        return retlsts

    def gradient( self, width, retnum=None, abcs=0, lgtd=1, T=False):
        num = self.bindup(width, xyz=abcs, retnum=True, T=T)
        if num == 1:
            raise ValueError, "Arg 'width' is narrower than the data interval of 'abcs'."
        arrs = self.bind.get_data()
        xarrs = arrs[abcs]
        yarrs = arrs[lgtd]
        remarrs = arrs[3-(abcs+lgtd)]
        arrs = map(lambda x:array(map(lambda y: median(y)*ones(len(xarrs)), x)) if type(x) != type(None) else None, arrs)
        retx = []
        rety = []
        ret_remain = []
        for n in xrange(len(xarrs)):
            sumx = sum(xarrs[n], axis=1)
            sumy = sum(yarrs[n], axis=1)
            sumxy = sum(xarrs[n]*yarrs[n], axis=1)
            sumxx = sum(xarrs[n]*xarrs[n], axis=1)
            retarr = (( num * sumxy) - sumx * sumy ) / ( num * sumxx  - sumx ** 2 )
        
            retx += [mean(xarrs[n], axis=1)]
            rety += [retarr]

            ret_remain = ret_remain + [mean(remarrs[n], axis=1)] if type(remarrs) != type(None) else None
        arrs[abcs] = retx
        arrs[lgtd] = rety
        arrs[3-(abcs+lgtd)] = ret_remain
        
        self.grad = handle_4d()
        self.grad.dinput(arrs)
        self.grad.T = T
        self.grad.transpose()
            
        if retnum:
            return num
        else:
            return arrs[abcs], arrs[lgtd]
    
    def poly_integral(self, abcs=2, lgtd=1 ,T=None):
        from modules.numerical_utils.basic_util import trapezoid
        if not T is None:
            if self.T != T: self.transpose()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]

        ylst = []
        for i in xrange(len(y)):
            ylst += [(x[i], y[i])]
        arrs[abcs] = None
        #arrs[lgtd] = array(ylst)

        #input(transpose(arrs[3-abcs-lgtd]))
        #input(ylst)
        self.trap = h3d.handle_3d(transpose(arrs[3-abcs-lgtd])[0],array(ylst))

    def trapezoid(self, abcs=2, lgtd=1 ,T=None):
        from modules.numerical_utils.basic_util import trapezoid
        if not T is None:
            if self.T != T: self.transpose()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]

        ylst = []
        for i in xrange(len(y)):
            ylst += [trapezoid(x[i], y[i])]
        arrs[abcs] = None
        #arrs[lgtd] = array(ylst)

        #input(transpose(arrs[3-abcs-lgtd]))
        #input(ylst)
        self.trap = h3d.handle_3d(transpose(arrs[3-abcs-lgtd])[0],array(ylst))

    def loaddata(self, path):
        x,y,z = self.load.loadprofdat(path)
        self.dinput([x,y,z])

    def loaddata_wg(self, path):
        x,y,z = self.load.loadprofdat_wg(path)
        self.dinput([x,y,z])

    def columnview(self, abcs=0, lgtd=1):
        if self.T == False:
            self.transpose()
        arrs = self.get_data()
        names = self.getlabel()
        n = len(arrs[abcs])
        self.grace.columnlayout(n)
        for i in range(n):
            self.grace.set_ylabel(names[lgtd][i] if type(names[lgtd]) == list else names[lgtd] ,i)
            self.grace.set_xydata(arrs[abcs][i], arrs[lgtd][i],i)
            self.grace.set_autoscale(arrs[abcs][i], arrs[lgtd][i],i)
        self.grace.set_xlabel(names[abcs][0] if type(names[abcs]) == list else names[abcs] ,0)
        self.grace.open_grace()
        self.grace.initialize()

    def slice_view(self, index, trans=False, layout="1", abcs=0,lgtd=1, T=True, sepnum=None, dirname="tmpdir", filename="tmp", device="pdf", dump=False, hgrid=1, vgrid=1):
        obj = self.release(index, multi=True, trans=trans)
        obj.view(layout, abcs,lgtd, T, sepnum, dirname, filename, device, dump, hgrid, vgrid)
        
        

    def view(self, layout=1, abcs=0,lgtd=1, T=True, sepnum=None, dirname="tmpdir", filename="tmp", device="pdf", dump=False, hgrid=1, vgrid=1, logx=False, logy=False):
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
        if self.T != T:
            self.transpose()

        arrs,errs = self.get_data(reterr=True)
        
        if type(logx) == list : logx = iter(logx)
        if type(logy) == list : logy = iter(logy)

        sepnum = sepnum if type(sepnum) != type(None) else len(arrs[abcs])
        arrs[abcs] = lstsplit(arrs[abcs], sepnum) if None != arrs[abcs] else None
        errs[abcs] = lstsplit(errs[abcs], sepnum) if None != errs[abcs] else None
        arrs[lgtd] = lstsplit(arrs[lgtd], sepnum) if None != arrs[lgtd] else None
        errs[lgtd] = lstsplit(arrs[lgtd], sepnum) if None != errs[lgtd] else None
        arrs[3-abcs-lgtd] = lstsplit(arrs[3-abcs-lgtd], sepnum) if None != arrs[3-abcs-lgtd] else None
        errs[3-abcs-lgtd] = lstsplit(arrs[3-abcs-lgtd], sepnum) if None != errs[3-abcs-lgtd] else None
        plotnumlim = 1
        snumlim_tmp = sepnum if type(sepnum) == int else iter(sepnum)
        gnumlim = len(arrs[abcs])
        if dump:
            dirpath =  fcnt(self.dumppath+"/"+dirname)       
            dirpath = "/Users/yu/tmpdir199"
            if not os.path.exists(dirpath): os.mkdir(dirpath)
        plotnum = 0
        snum = 0
        gnum = 0
        fnames = ""
#        while plotnum < plotnumlim:
        if layout == "column":
            layoutdic[layout](gnumlim, hgrid=hgrid, vgrid=vgrid)
        elif layout == "column4":
            layoutdic[layout](gnumlim, hgrid=hgrid, vgrid=vgrid)
        else:
            layoutdic[layout](hgrid=hgrid, vgrid=vgrid)
        while gnum < gnumlim: 
        
            snumlim = snumlim_tmp if type(sepnum) == int else snumlim_tmp.next()
            while snum < snumlim:
                if type(errs[lgtd]) == type(None):
                    self.grace.set_xydata(arrs[abcs][gnum][snum], arrs[lgtd][gnum][snum], gnum=gnum, snum=snum+self.grace.inisnum)
                else:
                    self.grace.set_xydy(arrs[abcs][gnum][snum], arrs[lgtd][gnum][snum], errs[lgtd][gnum][snum], gnum=gnum, snum=snum+self.grace.inisnum)

                self.grace.prop.snum_check(gnum,snum)
                #if type(self.grace.prop.gdiclst[gnum]["snum"][snum]["legend"]) != type(None):
                #    self.grace.set_leg(self.grace.prop.gdiclst[gnum]["snum"][snum]["legend"], gnum, snum, loc=self.grace.prop.gdiclst[gnum]["legloc"])
                #else:
                #    pass
                snum += 1
            snum = 0
            #logscale setting--------------
            if type(logx) != bool : 
                tmp_logx = logx.next()
            else:
                tmp_logx = logx
            if type(logy) != bool : 
                tmp_logy = logy.next()
            else:
                tmp_logy = logy
            if tmp_logx: self.set_xaxes(1,0,gnum)
            if tmp_logy: self.set_yaxes(1,0,gnum)
            #------------------------------
            if type(self.grace.prop.gdiclst[gnum]["lim"]) != type(None):
                xmin, xmax, ymin, ymax, tnum = self.grace.prop.gdiclst[gnum]["lim"]
                self.grace.set_lim(xmin,xmax,ymin,ymax,gnum, tnum)
            else:
                self.grace.set_autoscale(arrs[abcs][gnum][snum], arrs[lgtd][gnum][snum], gnum=gnum, logx=tmp_logx, logy=tmp_logy)
            #self.grace.set_ylabel(self.grace.prop.gdiclst[gnum]["ylabel"], gnum)
            gnum += 1
        gnum = 0
        self.grace.set_ornament() 
        self.grace.set_lineall()
        #self.grace.set_xlabel(self.grace.prop.gdiclst[gnum]["xlabel"], gnum)
        if len(self.grace.prop.gdiclst): 
            self.grace.set_graphitems()
        self.grace.open_grace()
        if dump: self.grace.dumpfig(fcnt(dirpath, filename,device))
        self.grace.initialize()
        plotnum += 1
            
    def tevo(self, layout="1", abcs=0,lgtd=1, T=False, sepnum=None, dirname="tmpdir", filename="tmp", device="pdf", hgrid=1, vgrid=1, show=False):
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
        if self.T != T: self.transpose()
        arrs = self.get_data()
        sepnum = 1 
        plotnumlim = len(arrs[abcs])
        snumlim = sepnum 
        gnumlim = 1
        dirpath =  fcnt(self.dumppath+"/"+dirname)       
        os.mkdir(dirpath)
        plotnum = 0
        snum = 0
        gnum = 0
        fnames = ""
        while plotnum < plotnumlim:
            if layout == "column":
                layoutdic[layout](gnumlim, hgrid=hgrid)
            elif layout == "column4":
                layoutdic[layout](gnumlim, hgrid=hgrid, vgrid=vgrid)
            else:
                layoutdic[layout](hgrid=hgrid, vgrid=vgrid)
            while gnum < gnumlim: 
                while snum < snumlim:
                    self.grace.set_xydata(arrs[abcs][plotnum], arrs[lgtd][plotnum], gnum=gnum, snum=snum)
                    self.grace.prop.snum_check(gnum,snum)
                    if type(self.grace.prop.gdiclst[gnum]["snum"][snum]["legend"]) != type(None):
                        self.grace.set_leg(self.grace.prop.gdiclst[gnum]["snum"][snum]["legend"], gnum, snum, loc=self.grace.prop.gdiclst[gnum]["legloc"])
                    else:
                        pass
                    snum += 1
                snum = 0
                if type(self.grace.prop.gdiclst[gnum]["lim"]) != type(None):
                    xmin, xmax, ymin, ymax, gnum = self.grace.prop.gdiclst[gnum]["lim"]
                    self.grace.set_lim(xmin,xmax,ymin,ymax,gnum)
                else:
                    self.grace.set_autoscale(arrs[abcs][gnum][snum], arrs[lgtd][gnum][snum], gnum=gnum)
                #self.grace.set_ylabel(self.grace.prop.gdiclst[gnum]["ylabel"], gnum)
                gnum += 1
            gnum = 0
            if len(self.grace.prop.gdiclst): self.grace.set_graphitems()
            self.grace.set_ornament() 
            self.grace.set_lineall()
            #self.grace.set_xlabel(self.grace.prop.gdiclst[gnum]["xlabel"], gnum)
            self.grace.dumpfig(fcnt(dirpath, filename,device))
            if show:
                self.grace.open_grace()
                input()
            self.grace.initialize()
            plotnum += 1

    def boxview(self, abcs=0, lgtd=1):
        if self.T == False:
            self.transpose()
        arrs = self.get_data()
        names = self.getlabel()
        n = len(arrs[abcs])
        self.grace.simplelayout()
        for i in range(n):
            self.grace.set_ylabel("Value")
            #self.grace.set_ylabel(names[lgtd][0] if type(names[lgtd]) == list else names[lgtd] ,i)
            self.grace.set_xydata(arrs[abcs][i], arrs[lgtd][i],snum=i)
        self.grace.set_autoscale(arrs[abcs][i], arrs[lgtd][i])
        self.grace.set_xlabel(names[abcs][0] if type(names[abcs]) == list else names[abcs] ,0)
        self.grace.open_grace()
        self.grace.initialize()

    def playback(self, index=0):
        self.hist.execute(index=index)


