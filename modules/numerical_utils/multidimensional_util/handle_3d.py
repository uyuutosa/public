#!/usr/bin/env python
#-*- coding:utf-8 -*-
from numpy import *
from modules.essential_utils.obj_util import *
from modules.essential_utils.convert_util import *
from modules.essential_utils.file_util import *
from modules.essential_utils.search_util import *
from modules.essential_utils.dir_util import *
from modules.numerical_utils.fit_util import pfit
from modules.numerical_utils.tensor_utils.tensor import *
#import modules.numerical_utils.ana_spec as spec
from modules.numerical_utils.speana_util import *
from modules.graph_utils.grace_util.grace_util import * 
from modules.graph_utils.grace_util.grace_prop import * 
#from modules.graph_utils.root_util.root_util import * 

import os 
import itertools as it
import cPickle as pickle
from handle_graph import handle_graph, root_prop
import handle_4d as h4d

        
class handle_3d(handle_graph):
    """Handle x, y, and z dimenzion data.

    Description
        This class is multidimensional but mainly handles x and y of 2D data.

    """
    def __init__(self, x=None,y=None, z=None, xname="x", yname="y", zname="z", xerr=None, yerr=None, zerr=None, aerr=None):
        self.x = array(x) if not x is None else None 
        self.y = array(y) if not y is None else None  
        self.z = array(z) if not z is None else None 
        self.a = None
        self.xerr = xerr
        self.yerr = yerr
        self.zerr = zerr
        self.aerr = aerr
        self.xname = xname
        self.yname = yname
        self.zname = zname
        self.grace = grace_util()
        self.root = root_prop()
        self.write = writedat_util()
        self.load = loaddat_util()
        self.wpath = "tmp.txt"
        self.picklepath = "tmp"
        self.hist = method_history(self)
    
    def set_data(self, x=None, y=None, z=None):
        self.x = x 
        self.y = y 
        self.z = z
        
    def add_param(self, paralst, arrs, transpose=True):
        self.hist.input()
        arrlst = []
        n = 0
        for para in paralst:
            tmp  = para * ones(len(arrs[0][0]))
            arrlst += [concatenate(([tmp], arrs[n]), axis=0)]
            n += 1
        return array(arrlst).transpose() if transpose else array(arrlst)
    

    def dump_pickle(self, picklepath=None):
        self.hist.input()
        if type(picklepath) == type(None): picklepath = self.picklepath
        o = open(picklepath, "w")
        pickle.dump(self, o)
        o.close()

    def load_pickle(self, picklepath=None):
        if type(picklepath) == type(None): picklepath = self.picklepath
        o = open(picklepath)
        tmp = pickle.load(o)
        self.dinput(*tmp.get_data(reterr=True))
        self.hist.hlst = tmp.hist.hlst
        self.grace = tmp.grace
        o.close()

    #def load_pickle(self, txtpath=None):
    #    if type(txtpath) == type(None): txtpath = self.txtpath
    #    o = open(txtpath)
    #    tmp = txt.load(o)
    #    self.dinput(tmp.get_data(reterr=True))
    #    self.hist.hlst = tmp.hist.hlst
    #    self.grace = tmp.grace
    #    o.close()

    def backup(self):
        self.hist.input()
        s = TemporaryFile()
        pickle.dump(self, s)
        s.seek(0)
        self.bkuplst += [s]

    def combine(self, obj, slst=[26, 36], xy=True, abcs=0, lgtd=1):
        self.slice_arr(slst, abcs)
        obj.slice_arr(slst, abcs)
        self.cmb = handle_3d()
        
        arrs1 = self.slice.get_data()
        arrs2 = obj.slice.get_data()
        if xy:
            self.cmb.x = arrs1[lgtd]
            self.cmb.y = arrs2[lgtd]
        else:
            self.cmb.x = arrs2[lgtd]
            self.cmb.y = arrs1[lgtd]

    def crosscorr(self, obj, abcs=0, lgtd=1):
        self.hist.input()
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3-abcs-lgtd]
        if not x.size % 2:
            x = x[:-1]
            y = y[:-1]
            z = z[:-1] if not z is None else None

        arrs2,errs2 = obj.get_data(reterr=True)
        x2 = arrs2[abcs]
        y2 = arrs2[lgtd]
        z2 = arrs2[3-abcs-lgtd]
        dt = (x[1] - x[0])
        if not x2.size % 2:
            x2 = x2[:-1]
            y2 = y2[:-1]
            z2 = z2[:-1] if not z2 is None else None
        
#        st = x[0]
#        y_cut = y[(lim[0]-st)/dt:(lim[1]-st)/dt]
#        L = y_cut.size
#        T = lim[1] - lim[0]





        cor_y = convolve(y,y2[::-1])
        L = cor_y.size


        arrs[abcs] = dt * arange(-L/2+1, L/2+1)
        arrs[lgtd] = cor_y
        arrs[3-abcs-lgtd] = z[L/2:-(L/2-1)] if not z is None else None
        obj = handle_3d()
        obj.dinput(arrs, errs)
        T = max(obj.x)
        k = T / (T - abs(obj.x))
        k[k != k] = 1
        k[k == inf] = 1
        obj.y *= k
        #obj.slice_arr([x[0], x[-1] - wid], xyz=abcs)
        self.ccor = obj

    def crosscorr2(self, tau, point, abcs=0, lgtd=1):
        arrs = self.get_data()
        parrs = point.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        py = parrs[lgtd]
        dx = x[1] - x[0]

        if type(tau) == list:
            x = arange(tau[0], tau[1], dx) 
            num = abs(int((max(tau)) / dx))
            numarr = range(int(tau[0]/dx), int(tau[1]/dx)) 
        else:
            x = arange(0, tau, dx) if tau > 0 else arange(tau, 0, dx)
            num = abs(int(tau / dx))
            numarr = range(num) if tau > 0 else range(-num,1)
        y = array(map(lambda a: mean(y[(num + a): - (num - a)] * py[num: - num]) / (mean(y[num: - num] ** 2)**0.5 * mean(py[num: - num] ** 2)**0.5), numarr))

        arrs[abcs] = x
        arrs[lgtd] = y
        self.ccor = handle_3d()
        self.ccor.dinput(arrs)

    def autocorr(self, abcs=0, lgtd=1):
        self.hist.input()
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3-abcs-lgtd]
        dt = (x[1] - x[0])
        if not x.size % 2:
            x = x[:-1]
            y = y[:-1]
            z = z[:-1] if not z is None else None
        
#        st = x[0]
#        y_cut = y[(lim[0]-st)/dt:(lim[1]-st)/dt]
#        T = lim[1] - lim[0]


        cor_y = convolve(y,y[::-1])
        L = cor_y.size


        arrs[abcs] = dt * arange(-L/2+1, L/2+1)
        arrs[lgtd] = cor_y
        arrs[3-abcs-lgtd] = z[L/2:-(L/2-1)] if not z is None else None
        obj = handle_3d()
        obj.dinput(arrs, errs)
        T = max(obj.x)
        #input(T / (T - abs(obj.x)))
        k = T / (T - abs(obj.x))
        k[k != k] = 1
        k[k == inf] = 1
        obj.y *= k
        #obj.slice_arr([x[0], x[-1] - wid], xyz=abcs)
        self.acor = obj

    def autocorr2(self, tau, abcs=0, lgtd=1):
        # calc Autocorrelation.
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        dx = x[1] - x[0]

        if type(tau) == list:
            x = arange(tau[0], tau[1], dx) 
            num = abs(int((max(tau)) / dx))
            numarr = range(int(tau[0]/dx), int(tau[1]/dx)) 
        else:
            x = arange(0, tau, dx) if tau > 0 else arange(tau, 0, dx)
            num = abs(int(tau / dx))
            numarr = range(num) if tau > 0 else range(-num,1)
        y = array(map(lambda a: mean(y[(num + a): - (num - a)] * y[num: - num]) / mean(y[num: - num] ** 2), numarr))

        arrs[abcs] = x
        arrs[lgtd] = y
        self.acor = handle_3d()
        self.acor.dinput(arrs)

    def trapezoid(self, abcs=0, lgtd=1):
        from modules.numerical_utils.basic_util import trapezoid
        arrs = self.get_data()
        self.trap = trapezoid(arrs[abcs], arrs[lgtd])

#    def autocorr_wf(self, tau, abcs=0, lgtd=1):
#        # calc Autocorrelation.
#        arrs = self.get_data()
#        x = arrs[abcs]
#        y = arrs[lgtd]
#        dx = x[1] - x[0]
#
#
#        x, y = spec.autocorr(tau, x, y)
#
#        arrs[abcs] = x
#        arrs[lgtd] = y
#        self.acor = handle_3d()
#        self.acor.dinput(arrs)
#
#    def crosscorr_wf(self, tau, point, abcs=0, lgtd=1):
#        # calc Autocorrelation.
#        arrs = self.get_data()
#        x1 = arrs[abcs]
#        y1 = arrs[lgtd]
#        arrs = point.get_data()
#        y2 = arrs[lgtd]
#
#        x, y = spec.crosscorr(tau, x1, y1, y2)
#
#        arrs[abcs] = x
#        arrs[lgtd] = y
#        self.ccor = handle_3d()
#        self.ccor.dinput(arrs)
#
#    def crosscorr_func_wf(self, tau, point, abcs=0, lgtd=1):
#        # calc Autocorrelation.
#        arrs = self.get_data()
#        x1 = arrs[abcs]
#        y1 = arrs[lgtd]
#        arrs = point.get_data()
#        y2 = arrs[lgtd]
#
#        x, y, z= spec.crosscorr_func(tau, x1, y1, y2)
#
#        arrs[abcs] = x
#        arrs[lgtd] = y
#        arrs[3-abcs-lgtd] = z
#        self.ccor = h4d.handle_4d()
#        self.ccor.dinput(arrs)
    def round(self, n):
        self.x = self.x.round(n) if not self.x is None else None
        self.y = self.y.round(n) if not self.y is None else None
        self.z = self.z.round(n) if not self.z is None else None

    def view_2d(self, abcs=0, lgtd=1):
        arrs = self.get_data()
        z = arrs[3 - abcs - lgtd]
        x = arrs[abcs]
        y = arrs[lgtd]

        a = rootmacro()
        a.set_xyzdata(x,y,z)
        a.ldump()
        a.open_macro()

    def view_col(self, layout="simple", opt="cont3z", abcs=2, lgtd=1):
        arrs = self.get_data()
        x = arrs[3 - abcs - lgtd]
        y = arrs[abcs]
        z = arrs[lgtd]
        self.root.set_xyzdata(tuple(append(array([]),x)), tuple(append(array([]),y)), tuple(append(array([]),z)));
        self.root.simplelayout(opt)
        self.root.view_graph()

    def parzen_window(self, wid, abcs=0, lgtd=1,check=False):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal
        arrs,errs = self.get_data(reterr=True)
        obj = handle_3d(arrs[abcs], arrs[lgtd], arrs[3-abcs-lgtd])
        dt = (obj.x[1] - obj.x[0])
        obj.fft()
        N = (obj.x.size)
        k = arange(0, 1., 1./obj.ffted.x.size)
        f = obj.ffted.x 
        fs = 1. / dt
        #k = obj.ffted.x * dt * N
        #L = wid
        L = int(wid / dt)
        A = pi *  f * L / fs / 2
        H = (sin(A) / A) **4 * exp(-1j * pi * f * (L-1) / fs)# / L
        H[0] = 1.
        obj.ffted.y *= H
        obj.ffted.ifft()

        #ave_x = convolve(x, conv_arr)[inum:-(inum-1)]
        #ave_y = convolve(y, conv_arr)[inum:-(inum-1)]
        #if check:
        #    conv_x = arange(0, dt*inum, dt)
        #    obj = handle_3d(conv_x, conv_arr)
        #    obj.pow_spec()
        #    obj.pow.view()

        arrs = obj.ffted.iffted.get_data()
        #input(len(arrs))

#        self.parzen.x = self.parzen.x[L:] - wid / 2. #Maybe... This convolution is started at right and ended at right.
#        self.parzen.y = self.parzen.y[L:]
        
        arrs[abcs] = arrs[abcs][L:] - wid / 2.
        arrs[lgtd] = arrs[lgtd][L:]
        if arrs[3-abcs-lgtd] is not None: arrs[3-abcs-lgtd] = arrs[3-abcs-lgtd][L:]
        self.parzen = handle_3d()
        self.parzen.dinput(arrs, errs)

    def mov_ave2(self, wid, abcs=0, lgtd=1,check=False):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal
        arrs,errs = self.get_data(reterr=True)
        obj = handle_3d(arrs[abcs], arrs[lgtd])
        dt = (obj.x[1] - obj.x[0])
        obj.fft()
        N = (obj.x.size)
        k = arange(0, 1., 1./obj.ffted.x.size)
        f = obj.ffted.x 
        fs = 1. / dt
        #k = obj.ffted.x * dt * N
        #L = wid
        L = int(wid / dt)
        H = ((sin(pi *  f * L / fs) / sin(pi * f / fs)) * exp(-1j * pi * f * (L-1) / fs)) / L
        H[0] = 1.
        obj.ffted.y *= H
        obj.ffted.ifft()

        #ave_x = convolve(x, conv_arr)[inum:-(inum-1)]
        #ave_y = convolve(y, conv_arr)[inum:-(inum-1)]
        #if check:
        #    conv_x = arange(0, dt*inum, dt)
        #    obj = handle_3d(conv_x, conv_arr)
        #    obj.pow_spec()
        #    obj.pow.view()

        self.mave = obj.ffted.iffted

        self.mave.x = self.mave.x[L:] - wid / 2. #Maybe... This convolution is started at right and ended at right.
        self.mave.y = self.mave.y[L:]
        if check:
            t2 = handle_3d(f, abs(obj.ffted.y/f.size/2)**2)
            t3= handle_3d(f, abs(H/N)**2)
            t4= handle_3d(f, abs(H)**2)
            #t4.view()
            self.mave.pow_spec()
            t = handle_3d(f, abs(obj.ffted.y/f.size/2)**2)
            lst = [t,t2,t3,self.mave.pow]
            c = h4d.handle_4d()
            c.set_multi(lst)
            c.view("1_2", logy=True)


    def mov_pow(self, wid, abcs=0, lgtd=1,check=False):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        z = arrs[lgtd]
        y = arrs[3-abcs-lgtd]


        dt = (x[1] - x[0])
        L = abs(int(wid/dt))

        conv_arr = ones(L, dtype=float) / L

        X = fft.fft(bindup(z, L))[:,0:L/2]
        tile_n = len(X[0])
        freq = tile(fft.fftfreq(z.size, dt)[0:L/2], (len(X), 1))
        z = abs(X/L) ** 2
        x = tile(bindup(x, L).mean(axis=1), (tile_n,1)).transpose()[:,0:L/2]
        y = tile(bindup(y, L).mean(axis=1), (tile_n,1)).transpose()[:,0:L/2] if not y is None else None
        arrs[abcs] = x
        arrs[lgtd] = z
        arrs[3-abcs-lgtd] = y
        self.mpow = h4d.handle_4d()
        self.mpow.T = True
        self.mpow.dinput(arrs)
        self.mpow.a = freq

        if check:
            conv_x = arange(0, dt*L, dt)
            #obj = handle_3d(conv_x, conv_arr)
            #obj.pow_spec()
            #obj.pow.view()
            obj = handle_3d(x,y)
            obj.fft()
            #o1 = handle_3d(conv_x, conv_arr)
            #o1.pow_spec()
            N = (x.size)
            k = obj.ffted.x * dt * N
            L = int(wid / dt)
            H = ((sin(pi * k * L / N) / sin(pi * k / N)) * exp(-1j * pi * k * (L-1) / N)) / L
            H[0] = 1.
            o1= handle_3d(k, abs(H/N)**2)
            self.pow_spec()
            self.mpow.pow_spec()
            c = h4d.handle_4d()
            c.set_multi([self.pow, o1,self.mpow.pow])
            c.view()
    def mov_ave(self, wid, abcs=0, lgtd=1,check=False):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3-abcs-lgtd]


        dt = (x[1] - x[0])
        L = abs(wid/dt)
        L = abs(int(wid/dt))

        conv_arr = ones(L, dtype=float) / L
        #input(L)
        #input(x.dtype)
        #input(x[L/2:-(L/2-1)].dtype)
        ave_x = x[L/2:-(L/2-1)]
        #print "aw"
        #input(x[1] - x[0])
        #input(ave_x[1] - ave_x[0])
        import scipy.signal as s
        ave_y = s.fftconvolve(y, conv_arr)[L-1:len(y)]
        ave_z = z[L/2:-(L/2-1)] if not z is None else None
        if ave_y.size != ave_x.size:
            ave_x = ave_x[0:ave_y.size]
        #ave_x = convolve(x, conv_arr)[L:-(L-1)]
        #ave_y = convolve(y, conv_arr)[L:-(L-1)]
        #ave_z = convolve(z, conv_arr)[L:-(L-1)] if not z is None else None

        arrs[abcs] = ave_x
        arrs[lgtd] = ave_y
        arrs[3-abcs-lgtd] = ave_z
        self.mave = handle_3d()
        self.mave.dinput(arrs, errs)

        if check:
            conv_x = arange(0, dt*L, dt)
            #obj = handle_3d(conv_x, conv_arr)
            #obj.pow_spec()
            #obj.pow.view()
            obj = handle_3d(x,y)
            obj.fft()
            #o1 = handle_3d(conv_x, conv_arr)
            #o1.pow_spec()
            N = (x.size)
            k = obj.ffted.x * dt * N
            L = int(wid / dt)
            H = ((sin(pi * k * L / N) / sin(pi * k / N)) * exp(-1j * pi * k * (L-1) / N)) / L
            H[0] = 1.
            o1= handle_3d(k, abs(H/N)**2)
            self.pow_spec()
            self.mave.pow_spec()
            c = h4d.handle_4d()
            c.set_multi([self.pow, o1,self.mave.pow])
            c.view()

    def mov_grad(self, wid, abcs=0, lgtd=1, retL=False):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3-abcs-lgtd]
        xy = x * y
        dt = (x[1] - x[0])
        L = abs(int(wid/dt)) 
        h = ones(L)

        conv_x = convolve(h, x)
        a = (L * convolve(h, xy) - conv_x * convolve(h, y)) / (L * convolve(h, x ** 2) - conv_x ** 2)


            
        arrs[abcs] = x[L/2:-(L/2-1)]
        arrs[lgtd] = a[L-1:-(L-1)] 
        arrs[3-abcs-lgtd] = z[L/2:-(L/2-1)] if not z is None else None
        
        #align

        obj = handle_3d()
        obj.dinput(arrs, errs)
        N = obj.y.size
        if obj.x is not None: obj.x = obj.x[0:N]
        if obj.z is not None: obj.z = obj.z[0:N]
        #input(x[0])
        #input(x[-1] - wid)
        #input(obj.z)
        #input(obj.x)
        #input(obj.y)
        #print obj.x
        #print obj.y
        #print obj.z
        #print dt 
        
        #####obj.slice_arr([x[0], x[-1] - wid], xyz=abcs)
        #input(obj.x)
        #input(obj.z)
        self.mgrad = obj#.slice
        if retL: return L

    def mov_grad2(self, wid, abcs=0, lgtd=1, retL=False):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3-abcs-lgtd]
        xy = x * y
        dt = (x[1] - x[0])
        L = abs(int(wid/dt)) 
        h = ones(L)
        

        x2 = x[L/2:-(L/2-1)]

        conv_x = convolve(h, x)
        numerator = (L * convolve(h, xy) - conv_x * convolve(h, y))[L-1:-(L-1)] 
        denominator = (L ** 2. * (x2 - x2**2. + dt**2. * (2.*L-1.)*(L-1.)/6. - dt ** 2. * (L -1.) ** 2. / 4.))
        a = numerator / denominator


            
        arrs[abcs] = x2
        arrs[lgtd] = a
        arrs[3-abcs-lgtd] = z[L/2:-(L/2-1)] if not z is None else None
        
        #align

        obj = handle_3d()
        obj.dinput(arrs, errs)
        N = obj.y.size
        if obj.x is not None: obj.x = obj.x[0:N]
        if obj.z is not None: obj.z = obj.z[0:N]
        #input(x[0])
        #input(x[-1] - wid)
        #input(obj.z)
        #input(obj.x)
        #input(obj.y)
        #print obj.x
        #print obj.y
        #print obj.z
        #print dt 
        
        #####obj.slice_arr([x[0], x[-1] - wid], xyz=abcs)
        #input(obj.x)
        #input(obj.z)
        self.mgrad = obj#.slice
        if retL: return L

    def sort_theta(self, ):
        self.hist.input()
        x0 = self.x.max() - (self.x.max() - self.x.min()) / 2
        y0 = self.y.max() - (self.y.max() - self.y.min()) / 2

        x = self.x - x0
        y = self.y - y0
        r = sqrt(x**2 + y**2)
        t = angle((x+y*1.j)/r)
        narr = argsort(t)
        r = r[narr]
        t = t[narr]
        x = r * cos(t)
        y = r * sin(t)
        self.theta = handle_3d(x+x0,y+y0)

    def mov_var(self, wid, abcs=0, lgtd=1):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3-abcs-lgtd]
        dt = (x[1] - x[0])
        L = int(wid/dt)  
        h = ones(L)

        var_y = convolve(h, (convolve(h, y)[L-1:-L+1] / L - y[L/2-1:-(L/2)]) ** 2) / L

        arrs[abcs] = x[L/2:-(L/2-1)]
        arrs[lgtd] = var_y
        arrs[3-abcs-lgtd] = z[L/2:-(L/2-1)] if not z is None else None
        obj = handle_3d()
        obj.dinput(arrs, errs)
        obj.slice_arr([x[0], x[-1] - wid], xyz=abcs)
        self.mvar = obj.slice

    def cross_spec(self, obj, abcs=0, lgtd=1, check=False):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        arrs2 = obj.get_data()
        y2 = arrs[lgtd]

        d = float(x[1] - x[0]) 
        X = (fft.fft(y) * fft.fft(y2).conj()/y.size)[0:y.size/2]
        freq = fft.fftfreq(X.size*2, d)[0:y.size]

        
        n = freq.size

       
        arrs[abcs] = freq
        arrs[lgtd] = (abs(X) ** 2)
        if not z is None: arrs[3 - abcs - lgtd] = z[0:z.size/2] 
        self.cspec = handle_3d()
        self.cspec.dinput(arrs)
        
    def coherence(self, obj, abcs=0, lgtd=1, check=False):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        self.crosscorr(obj)
        self.autocorr()
        obj.autocorr()
        self.acor.fft();Sxx = self.acor.ffted
        obj.acor.fft() ;Syy = obj.acor.ffted
        self.ccor.fft();Sxy = self.ccor.ffted

        
        n = Sxx.x.size

        #coh = abs(Sxy.y) ** 2 / (Syy.y.real * Sxx.y.real)
        coh = abs(Sxy.y) ** 2 / (abs(Syy.y) * abs(Sxx.y))
        
        #input(abs(X * Y.conj())==sqrt(abs(X) ** 2 * abs(Y) ** 2))

        #K = 0.5 * (Sxy + Syx)
        #Q = 1j * 0.5 * (Sxy - Syx)

        #coh = sqrt((K ** 2 + Q ** 2) / (abs(Sxx) ** 2 * abs(Syy) ** 2))
        #coh = sqrt((Sxy.real ** 2 + Sxy.imag ** 2) / (abs(X) ** 2 * abs(Y) ** 2))
        #coh = sqrt(abs(Sxy) ** 2 / (abs(X) ** 2 * abs(Y) ** 2))
        #input(coh)
        #coh = abs(X * Y.conj()) ** 2 / (abs(X) ** 2 * abs(Y) ** 2)
        #pow =  abs(X/X.size) ** 2 * d
        #pow =  abs(X/x.size) ** 2 / dnum
        #pow =  t * (X.real ** 2 + X.imag ** 2) / (( dnum))
       
        arrs[abcs] = Sxx.x[0:n/2]
        arrs[lgtd] = coh[0:n/2]
        if not z is None: arrs[3 - abcs - lgtd] = z[0:z.size/2] 
        self.coh = handle_3d()
        self.coh.dinput(arrs)
        
        if check:
            c = h4d.handle_4d()
            self.pow_spec()
            obj.pow_spec()

            c.set_multi([self, obj, self.pow, obj.pow, self.coh])
            c.view("3", sepnum=[2,2,1])

    def cross_phase(self, obj, abcs=0, lgtd=1, check=False):
        self.hist.input()
        arrs = self.get_data()
        z = arrs[3 - abcs - lgtd]

        #self.crosscorr(obj)
        #self.autocorr()
        #self.autocorr()
        #self.acor.fft();Sxx = self.acor.ffted
        #obj.acor.fft();Syy = obj.acor.ffted
        #self.ccor.fft();Sxy = self.ccor.ffted

        self.fft();Sxx = self.ffted
        obj.fft();Syy = obj.ffted

        
        phase = angle(Sxx.y) - angle(Syy.y)
        
        n = Sxx.x.size
        #n = Sxy.x.size

        #amp = sqrt(abs(Sxx.y) * abs(Syy.y))
        #phase = angle(Sxy.y/amp)
        
       
        arrs[abcs] = Sxx.x[0:n/2]
        arrs[lgtd] = phase[0:n/2]
        if not z is None: arrs[3 - abcs - lgtd] = z[0:z.size/2] 
        self.cphase = handle_3d()
        self.cphase.dinput(arrs)
        num = self.cphase.y == self.cphase.y
        self.cphase.x = self.cphase.x[num]
        self.cphase.y = self.cphase.y[num]
        
        
        if check:
            c = h4d.handle_4d()
            self.pow_spec()
            obj.pow_spec()

            c.set_multi([self, obj, self.pow, obj.pow, self.coh])
            c.view("3", sepnum=[2,2,1])

    def euler_method(self, abcs=0, lgtd=1, st=None, en=None, d=None):
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        if d is None: d = x[1] - x[0]
        if st is None: st = x[0]
        if en is None: en = x[-1] + d

        lst = []
        v = 0
        for i in y:
            v = v + d * i
            lst += [v]

        arrs[abcs] = arange(st, en, d)
        arrs[lgtd] = array(lst)
        obj = handle_3d()
        obj.dinput(arrs, errs)
        self.euler = obj

    def runge_kutta_4th(self, abcs=0, lgtd=1, st=None, en=None, h=None, ini_val=None):
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        if h is None: h = x[1] - x[0] 
        if st is None: st = x[0]
        if en is None: en = x[-1] + h
        if ini_val is None: ini_val = y[0]

        lst = []
        v = ini_val
        i = 0

        dx = x[1] - x[0]
        dn = int(dx / h)
        parr = arange(st, en, h)
        for i in xrange(len(parr) - dn):
            k0 = h * y[i]
            k1 = h * y[i-dn/2]
            k2 = h * y[i+dn/2]
            k3 = h * y[i+dn]
            v = v + (k0 + 2 * k1 + 2 * k2 + k3) / 6.
            lst += [v]

        arrs[abcs] = arange(st, en, h)
        arrs[lgtd] = array(lst)
        obj = handle_3d()
        obj.dinput(arrs, errs)
        self.rk4 = obj
        
    def eval_cond(self, cond):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal

        x = self.x
        y = self.y
        z = self.z
        xerr = self.xerr
        yerr = self.yerr
        zerr = self.zerr

        exec "tof = " + cond
        self.cond = handle_3d()
        self.cond.x = x[tof] if not x is None else None
        self.cond.y = y[tof] if not y is None else None
        self.cond.z = z[tof] if not z is None else None
        self.cond.xerr = xerr[tof] if not xerr is None else None
        self.cond.yerr = yerr[tof] if not yerr is None else None
        self.cond.zerr = zerr[tof] if not zerr is None else None



    def iterp_ave(self, itvl, wid, abcs=0, lgtd=1):
        self.hist.input()
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3-abcs-lgtd]

        dt = (x[1] - x[0])
        itvlelm = int(Decimal(str(itvl / dt)))
        averange = int(Decimal(str(wid / (2 * dt))))
    
        x_ave = []
        y_ave = []
        y_err = []
    
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
            #y_err  += [std(y[elmin : elmax])]
            n += itvlelm
        arrs[abcs] = array(x_ave)
        arrs[lgtd] = array(y_ave)
        arrs[3-abcs-lgtd] = z[0:len(x_ave)] if not z is None else None
        #errs[lgtd] = array(y_err)
        self.iave = handle_3d()
        self.iave.dinput(arrs, errs)

    def iterp_ave(self, itvl, wid, abcs=0, lgtd=1):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal
        arrs,errs = self.get_data(reterr=True)
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3-abcs-lgtd]

        dt = (x[1] - x[0])
        itvlelm = int(Decimal(str(itvl / dt)))
        averange = int(Decimal(str(wid / (2 * dt))))
    
        x_ave = []
        y_ave = []
        y_err = []
    
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
            #y_err  += [std(y[elmin : elmax])]
            n += itvlelm
        arrs[abcs] = array(x_ave)
        arrs[lgtd] = array(y_ave)
        arrs[3-abcs-lgtd] = z[0:len(x_ave)] if not z is None else None
        #errs[lgtd] = array(y_err)
        self.iave = handle_3d()
        self.iave.dinput(arrs, errs)

    def slice_arr(self, slst, xyz=0, err=0):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[xyz]
        #input(where((slst[0] <= x) == (x <= slst[1])))
        #input(where((slst[0] <= x) == (x <= slst[1]))[0])
        args = where((slst[0] - err <= x) == (x <= slst[1] + err))[0]
        if len(args) == 0: 
            return False
        arrs = array([arr[args] if type(arr) != type(None) else None for arr in arrs])
        self.slice = handle_3d()
        self.slice.dinput(arrs)
        return True
        
    def zero_adj(self, plst, abcs=0, lgtd=1, inv=True):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        y -= y[where((plst[0] <= x) == (x <= plst[1]))[0]].mean()
        arrs[abcs] = x
        arrs[lgtd] = y
        self.zadj = handle_3d()
        self.zadj.dinput(arrs)

    def punch_out(self, plst, pxyz=0, inv=False, val=None, vxyz=1):
        self.hist.input()
        x,y,z,a = self.get_data()
        dlst = [x,y,z]
        numarr = array(ones(dlst[pxyz].size), dtype=bool)
        for pmin, pmax in plst: 
                
            numarr = numarr * where( inv == ((pmin <= dlst[pxyz]) * (pmax >= dlst[pxyz])), True, False)
            #numarr = where( inv == ((pmin <= dlst[pxyz]) * (pmax >= dlst[pxyz])))[0]
        if val is None:
            x = x[numarr] if type(x) != type(None) else None
            y = y[numarr] if type(y) != type(None) else None
            z = z[numarr] if type(z) != type(None) else None
            dlst = [x,y,z,a]
        else:
            dlst[vxyz][False == numarr] = val
        self.pout = handle_3d()
        self.pout.dinput(dlst)
        #return x,y,z if type(z) != type(None) else x,y

    def polyfit(self, M=8, stnum=None, ennum=None, itvl=0.1, abcs=0, lgtd=1, show=False):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        sen = [stnum, ennum, itvl]
        if type(stnum) == type(None):
            sen[0] = x[0]    
        if type(ennum) == type(None):
            sen[1] = x[-1]    
        x,y = pfit(x, y, M, sen) 
        arrs[abcs] = x
        arrs[lgtd] = y
        self.pfit = handle_3d()
        self.pfit.dinput(arrs)
        if show:
            tmp = self + self.pfit
            tmp.view()

    def gnufit(self, function, fitparalst, stnum=None, ennum=None, itvl=1, show=False, abcs=0, lgtd=1):
        self.hist.input()
        import Gnuplot as gp
#        from subprocess import call

        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]

        tmppath = home() + "/tmp.txt"
        tmppath2 = home() + "/tmp2.txt"
        savetxt(tmppath,transpose(array([x, y])))
        #writedat(tmppath,array([x, y]))
        
        g = gp.Gnuplot(debug=1)
        
        
        paranamelst = ["a", "b", "c", "d", "e", "f", "g", "h", "i",
                       "j", "k", "l", "m", "n", "o", "p", "q", "r", 
                       "s", "t", "u", "v", "w", "x", "y", "z"]
        i = iter(paranamelst)
    
        paratag = ""
        paras = []
        for para in fitparalst:
            name = i.next()
            paras += [name]
            paratag += "%s," %name
            g("%s = %s" %(name, para))
        paratag = paratag[:-1]
    
        g("f(x) = %s" %function)
        g("fit f(x) '%s' via %s" %(tmppath, paratag))
    
        g("set print '%s'" %tmppath2)
        for para in paras:
         #print para
            g("print %s" %para)
            #g = gp.Gnuplot(debug=1)
        g = gp.Gnuplot(debug=1) # initialize
        o = open(tmppath2)
        paravals = []
        for line in o:
            paravals += [float(line)]
            print line
        o.close()
        #call(["rm",tmppath,tmppath2])
        
        #making index area
        if type(stnum) == type(None):
            stnum = x[0]    
        if type(ennum) == type(None):
            ennum = x[-1]    
        x = arange(stnum, ennum, itvl)

        for para, val in zip(paras, paravals):
            exe = "%s = %s" %(para, val)
            exec exe
        exe = "y = %s" %function
        exec exe
        arrs[abcs] = x
        arrs[lgtd] = y
        self.gnu = handle_3d()
        self.gnu.dinput(arrs)
        self.gnu.fitpara = paravals
        if show:
            v = self + self.gnu
            v.view()
    
    def prmconv(self, cnvlst, xyz=0, comments="#", delim=","):
        self.hist.input()
        """ 
        'prmconv' convert a value as decline in 'paralst' 
        to new value baced on the config data as decline in 'cnvlst'.
        if a text file path name which has string type substitute 'cnvlst',
        convert data contained the file is read.
    
        """
        from numpy import array, where, ndarray
        arrlst = self.get_data()
        paralst = arrlst[xyz]
        if type(cnvlst) == str:
            cnv1, cnv2 = loaddat(cnvlst, comments, delim)
            cnvlst = [cnv1, cnv2]
    
        origlst, convlst = array(cnvlst,dtype=float)
        retlst = []
        for para in array(paralst,dtype=float):
            try:
                nummin = where(origlst <= para)[0][-1]
                nummax = where(origlst >= para)[0][0]
                orig_paramin = origlst[nummin]
                orig_paramax = origlst[nummax]
                orig_delta = orig_paramax - orig_paramin
                if orig_delta != 0:
                    ratio = (para - orig_paramin) / orig_delta
                    conv_paramin = convlst[nummin]
                    conv_paramax = convlst[nummax]
                    conv_delta = conv_paramax - conv_paramin
                    ret = conv_delta * ratio + conv_paramin
                else:
                    ret = convlst[nummin]
                retlst += [ret]
            except IndexError:
                retlst += [para]
        
        self.pcnv = handle_3d()
        arrlst[xyz] = array(retlst)
        self.pcnv.dinput(arrlst)
        #return retlst

    def interp(self, cnvlst, xyz=0, comments="#", delim=","):
        self.hist.input()
        from numpy import array, where, ndarray
        paralst = self.get_data()
        if type(cnvlst) == str:
            cnv1, cnv2 = loaddat(cnvlst, comments, delim)
            cnvlst = [cnv1, cnv2]
        paralst[xyz] = interp(paralst[xyz], cnvlst[0], cnvlst[1])
        self.itp = handle_3d()
        self.itp.dinput(paralst)
        #return retlst

    def slice_same(self, obj, xyz=0, err=0.001, round=None):
        self.hist.input()
        arrs = self.get_data()
        arrs2 = obj.get_data()
        x = arrs[xyz]
        x2 = arrs2[xyz]
        if round:
            x = x.round(round)
            x2 = x2.round(round)
        dx = x[1] - x[0]
        dx2 = x2[1] - x2[0]

        if str(dx) != str(dx2):
#            input(self.x)
#            input(obj.x)
#            input(dx)
#            input(dx2)
            raise ValueError, "Delta of series data is not same between 'self' (%s) and 'obj' (%s)." %(dx, dx2)
        if x2.size > x.size:
            raise ValueError, "'obj' size is exceed for 'self'. Can not treated."
        if str(arrs[xyz][0]) != str(x2[0]):
            arrs[xyz] += x2[0] - arrs[xyz][0] 

        # if delta and size hold, might that data is shifted between them. 
        # So it need to shift the arrs[xyz] as shown this. 
        slst = [x2[0], x2[-1]] if x2[0] < x2[-1] else [x2[-1], x2[0]]

        #input(where((slst[0] <= x) == (x <= slst[1])))
        #input(where((slst[0] <= x) == (x <= slst[1]))[0])
        #arrs = [arr[where((slst[0]-err <= x) == (x <= slst[1]+err))[0]] if not arr is None else None for arr in arrs]
        self.slice_arr(slst, xyz, err=err)
        if not self.x is None: self.slice.x = self.slice.x[0:obj.x.size]
        if not self.y is None: self.slice.y = self.slice.y[0:obj.y.size]
        if not self.z is None: self.slice.z = self.slice.z[0:obj.z.size]
        #self.slice = handle_3d()
        #self.slice.dinput(arrs)

    def pow_spec(self, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        d = float(x[1] - x[0]) 
#        t = (x[-1] - x[0]) 
#
#        X = fft.fft(y)
#        #X = fft.fft(y, pnum)
#        dnum = X.size
#        freq = (1 /(d * dnum)) * arange(dnum)
#        #freq = abs(fft.fftfreq(dnum,d))
#        dfreq = freq[1] - freq [0]
#    
        X = fft.fft(y)[0:y.size/2]
        freq = fft.fftfreq(X.size*2, d)[0:X.size]
        pow =  abs(X/X.size) ** 2
        #pow =  abs(X/X.size) ** 2 * d
        #pow =  abs(X/x.size) ** 2 / dnum
        #pow =  t * (X.real ** 2 + X.imag ** 2) / (( dnum))
       
        arrs[abcs] = freq
        arrs[lgtd] = pow
        if not z is None: arrs[3 - abcs - lgtd] = z[0:z.size/2] 
        self.pow = handle_3d()
        self.pow.dinput(arrs)


    def envelope(self, abcs=0, lgtd=1):
        import scipy.signal as s
        self.hist.input()
        arrs = self.get_data()
        y = arrs[lgtd]
       
        y = abs(s.hilbert(y))

        arrs[lgtd] = y
        self.env = handle_3d()
        self.env.dinput(arrs)
        

    def phase_difference(self, obj, abcs=0, lgtd=1):
        import scipy.signal as s
        self.hist.input()
        arrs = self.get_data()
        y = s.hilbert(arrs[lgtd])
        arrs2 = obj.get_data()
        y2 = s.hilbert(arrs2[lgtd])

        y = angle((y*y2.conj())/(abs(y)*abs(y2.conj())))

        arrs[lgtd] = y
        self.phd = handle_3d()
        self.phd.dinput(arrs)

    def mean_power(self, obj, abcs=0, lgtd=1):
        import scipy.signal as s
        self.hist.input()
        arrs = self.get_data()
        y = s.hilbert(arrs[lgtd])
        arrs2 = obj.get_data()
        y2 = s.hilbert(arrs2[lgtd])

        amp = abs(y) * abs(y2) / 2 
        ph = angle((y*y2.conj())/(abs(y)*abs(y2.conj())))
        y = amp * cos(ph)

        arrs[lgtd] = y
        self.mvi = handle_3d() #mean VI
        self.mvi.dinput(arrs)

    def bispectrum_ensemble(self, obj, wid, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        arrs2 = obj.get_data()
        x2 = arrs2[abcs]
        y2 = arrs2[lgtd]
        z2 = arrs2[3 - abcs - lgtd]

        d = float(x[1] - x[0]) 
        n = int(wid / d)

        if x is not None: x = x[0:x.size - x.size % n]
        if y is not None: y = y[0:y.size - y.size % n] 
        if z is not None: z = z[0:z.size - z.size % n]
        if x2 is not None: x2 = x2[0:x.size - x.size % n]
        if y2 is not None: y2 = y2[0:y.size - y.size % n] 
        if z2 is not None: z2 = z2[0:z.size - z.size % n]



        y = hsplit(y, y.size/n) 
        y2 = hsplit(y2, y2.size/n) 

        y_t = tensor(y, idx="ki", ud="d")
        y2_t = tensor(y2, idx="kj", ud="d")
        #y3_t = y_t * y2_t

        #y3_t.transpose("ij")
        #y3 = y3_t.arr

        freq = fft.fftfreq(len(y[0]), d) 
        N1 = freq.size
        freq = roll(freq, N1/2)
        freq_n = arange(N1)
        freq2 = fft.fftfreq(len(y2[0]), d)
        N2 = freq2.size
        freq2 = roll(freq2, N2/2)
        freq2_n = arange(N2)

        freq_t = tensor(freq, idx="i", ud="d")
        freq2_t = tensor(freq2, idx="j", ud="d")
        freq_n_t = tensor(freq_n, idx="i", ud="d")
        freq2_n_t = tensor(freq2_n, idx="j", ud="d")
        freq3_t = freq_t + freq2_t
        freq3_n_t = freq_n_t + freq2_n_t - N1/2

        freq3_t.transpose("ij")
        freq3_n_t.transpose("ij")
        freq3 = freq3_t.arr
        freq3_n = freq3_n_t.arr

        X = fft.fft(y)
        X = roll(X, N1/2)

        X_t = tensor(X, idx="ki", ud="dd")
        k_t = tensor(ones(len(X)), idx="k", ud="u")
        Y = fft.fft(y2)
        Y = roll(Y, N2/2)

        Y_t = tensor(Y, idx="kj", ud="dd")

        #Z = array([X[n, where(freq3_n >= freq.size, 0, freq3_n).astype(int)] for n in range(k_t.arr.size)]) * where(freq3_n >= freq.size, nan, freq3_n)
        Z = array([X[n, where((freq3_n>0) & (freq3_n < freq.size), freq3_n, 0).astype(int)] for n in range(k_t.arr.size)]) * where((freq3_n>0) & (freq3_n < freq.size), freq3_n, nan)
        Z = Z.conj()
        Z_t = tensor(Z, idx="kij", ud="ddd")

        XYZ = abs((X_t * Y_t * Z_t * k_t).arr) 
        XYZ[XYZ!=XYZ] = 0

        arrs[abcs] = tile(freq, (N2,1)).T
        arrs[lgtd] = XYZ
        arrs[3 - abcs - lgtd] = tile(freq2, (N1,1))

        self.besp = h4d.handle_4d()
        self.besp.dinput(arrs)

    def bicoherence_ensemble(self, obj, wid, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        arrs2 = obj.get_data()
        x2 = arrs2[abcs]
        y2 = arrs2[lgtd]
        z2 = arrs2[3 - abcs - lgtd]

        d = float(x[1] - x[0]) 
        n = int(wid / d)

        if x is not None: x = x[0:x.size - x.size % n]
        if y is not None: y = y[0:y.size - y.size % n] 
        if z is not None: z = z[0:z.size - z.size % n]
        if x2 is not None: x2 = x2[0:x.size - x.size % n]
        if y2 is not None: y2 = y2[0:y.size - y.size % n] 
        if z2 is not None: z2 = z2[0:z.size - z.size % n]



        y = hsplit(y, y.size/n) 
        y2 = hsplit(y2, y2.size/n) 

        y_t = tensor(y, idx="ki", ud="d")
        y2_t = tensor(y2, idx="kj", ud="d")
        #y3_t = y_t * y2_t

        #y3_t.transpose("ij")
        #y3 = y3_t.arr

        freq = fft.fftfreq(len(y[0]), d) 
        N1 = freq.size
        freq = roll(freq, N1/2)
        freq_n = arange(N1)
        freq2 = fft.fftfreq(len(y2[0]), d)
        N2 = freq2.size
        freq2 = roll(freq2, N2/2)
        freq2_n = arange(N2)

        freq_t = tensor(freq, idx="i", ud="d")
        freq2_t = tensor(freq2, idx="j", ud="d")
        freq_n_t = tensor(freq_n, idx="i", ud="d")
        freq2_n_t = tensor(freq2_n, idx="j", ud="d")
        freq3_t = freq_t + freq2_t
        freq3_n_t = freq_n_t + freq2_n_t - N1/2

        freq3_t.transpose("ij")
        freq3_n_t.transpose("ij")
        freq3 = freq3_t.arr
        freq3_n = freq3_n_t.arr

        X = fft.fft(y)
        X = roll(X, N1/2)

        X_t = tensor(X, idx="ki", ud="dd")
        k_t = tensor(ones(len(X)), idx="k", ud="u")
        Y = fft.fft(y2)
        Y = roll(Y, N2/2)

        Y_t = tensor(Y, idx="kj", ud="dd")

        Z = array([X[n, where((freq3_n>0) & (freq3_n < freq.size), freq3_n, 0).astype(int)] for n in range(k_t.arr.size)]) * where((freq3_n>0) & (freq3_n < freq.size), freq3_n, nan)
        Z = Z.conj()
        #Z = array([for i in X[where(freq3 >= freq.size, 0, freq3).astype(int)] * where(freq3 >= freq.size, nan, freq3)])
        Z_t = tensor(Z, idx="kij", ud="ddd")

        B_t = t_abs(X_t * Y_t * Z_t * k_t) ** 2
        denom_t = ((t_abs(X_t * Y_t )**2) * k_t) * ((t_abs(Z_t) ** 2) * k_t)
        bicoh_t = B_t / denom_t
        bicoh_t.transpose("ij")
        bicoh = bicoh_t.arr
        bicoh[bicoh!=bicoh] = 0

        arrs[abcs] = tile(freq, (N2,1)).T
        arrs[lgtd] = bicoh 
        arrs[3 - abcs - lgtd] = tile(freq2, (N1,1))
        #if not z is None: arrs[3 - abcs - lgtd] = z
        self.bech = h4d.handle_4d()
        self.bech.dinput(arrs)

    def biphase_ensemble(self, obj, wid, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        arrs2 = obj.get_data()
        x2 = arrs2[abcs]
        y2 = arrs2[lgtd]
        z2 = arrs2[3 - abcs - lgtd]

        d = float(x[1] - x[0]) 
        n = int(wid / d)

        if x is not None: x = x[0:x.size - x.size % n]
        if y is not None: y = y[0:y.size - y.size % n] 
        if z is not None: z = z[0:z.size - z.size % n]
        if x2 is not None: x2 = x2[0:x.size - x.size % n]
        if y2 is not None: y2 = y2[0:y.size - y.size % n] 
        if z2 is not None: z2 = z2[0:z.size - z.size % n]



        y = hsplit(y, y.size/n) 
        y2 = hsplit(y2, y2.size/n) 

        y_t = tensor(y, idx="ki", ud="d")
        y2_t = tensor(y2, idx="kj", ud="d")
        #y3_t = y_t * y2_t

        #y3_t.transpose("ij")
        #y3 = y3_t.arr

        freq = fft.fftfreq(len(y[0]), d)
        N1 = freq.size
        freq = roll(freq, N1/2)
        freq_n = arange(N1)
        freq2 = fft.fftfreq(len(y2[0]), d)
        N2 = freq2.size
        freq2 = roll(freq2, N2/2)
        freq2_n = arange(N2)

        freq_t = tensor(freq, idx="i", ud="d")
        freq2_t = tensor(freq2, idx="j", ud="d")
        freq_n_t = tensor(freq_n, idx="i", ud="d")
        freq2_n_t = tensor(freq2_n, idx="j", ud="d")
        freq3_t = freq_t + freq2_t
        freq3_n_t = freq_n_t + freq2_n_t - N1/2

        freq3_t.transpose("ij")
        freq3_n_t.transpose("ij")
        freq3 = freq3_t.arr
        freq3_n = freq3_n_t.arr

        X = fft.fft(y)
        X = roll(X, N1/2)


        X_t = tensor(X, idx="ki", ud="dd")
        k_t = tensor(ones(len(X)), idx="k", ud="u")
        Y = fft.fft(y2)
        Y_t = tensor(Y, idx="kj", ud="dd")

        #Z = array([X[n, where(freq3_n >= freq.size, 0, freq3_n).astype(int)] for n in range(k_t.arr.size)]) * where(freq3_n >= freq.size, nan, freq3_n)
        Z = array([X[n, where((freq3_n>0) & (freq3_n < freq.size), freq3_n, 0).astype(int)] for n in range(k_t.arr.size)]) * where((freq3_n>0) & (freq3_n < freq.size), freq3_n, nan)
        Z = Z.conj()
        #Z = array([for i in X[where(freq3 >= freq.size, 0, freq3).astype(int)] * where(freq3 >= freq.size, nan, freq3)])
        Z_t = tensor(Z, idx="kij", ud="ddd")

        B= (X_t * Y_t * Z_t * k_t).arr 
        biphase = angle(B.conj())
        biphase[biphase!=biphase] = 0

        arrs[abcs] = tile(freq, (N2,1)).T
        arrs[lgtd] = biphase
        arrs[3 - abcs - lgtd] = tile(freq2, (N1,1))
        #if not z is None: arrs[3 - abcs - lgtd] = z
        self.beph = h4d.handle_4d()
        self.beph.dinput(arrs)

    def coherence_ensemble(self, obj, wid, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        arrs2 = obj.get_data()
        x2 = arrs2[abcs]
        y2 = arrs2[lgtd]
        z2 = arrs2[3 - abcs - lgtd]

        d = float(x[1] - x[0]) 
        n = int(wid / d)

        if x is not None: x = x[0:x.size - x.size % n]
        if y is not None: y = y[0:y.size - y.size % n] 
        if z is not None: z = z[0:z.size - z.size % n]
        if x2 is not None: x2 = x2[0:x.size - x.size % n]
        if y2 is not None: y2 = y2[0:y.size - y.size % n] 
        if z2 is not None: z2 = z2[0:z.size - z.size % n]

        y = hsplit(y, y.size/n) 
        y2 = hsplit(y2, y2.size/n) 

        dlen = len(y[0])
        X = fft.fft(y)
        Y = fft.fft(y2)
        XY = (X * Y.conj()).transpose().mean(axis=1)[0:dlen/2]
        YX = (Y * X.conj()).transpose().mean(axis=1)[0:dlen/2]
        XX = (abs(X)**2).transpose().mean(axis=1)[0:dlen/2]
        YY = (abs(Y)**2).transpose().mean(axis=1)[0:dlen/2]
        #X = fft.fft(y)[0:y.size/2]
        freq = fft.fftfreq(dlen, d)[0:dlen/2]
        #ecoh =  sqrt((abs(X) * abs(Y))/abs(XY) )
        ecoh =  sqrt(abs(XY * YX) /(XX * YY))
       
        arrs[abcs] = freq
        arrs[lgtd] = ecoh
        if not z is None: arrs[3 - abcs - lgtd] = z[0:dlen/2] 
        self.ecoh = handle_3d()
        self.ecoh.dinput(arrs)

    def cross_phase_ensemble(self, obj, wid, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        arrs2 = obj.get_data()
        x2 = arrs2[abcs]
        y2 = arrs2[lgtd]
        z2 = arrs2[3 - abcs - lgtd]

        d = float(x[1] - x[0]) 
        n = int(wid / d)

        if x is not None: x = x[0:x.size - x.size % n]
        if y is not None: y = y[0:y.size - y.size % n] 
        if z is not None: z = z[0:z.size - z.size % n]
        if x2 is not None: x2 = x2[0:x.size - x.size % n]
        if y2 is not None: y2 = y2[0:y.size - y.size % n] 
        if z2 is not None: z2 = z2[0:z.size - z.size % n]
        y = hsplit(y, y.size/n) 
        y2 = hsplit(y2, y2.size/n) 

        X = fft.fft(y)
        Y = fft.fft(y2)
        
        dlen = len(y[0])
        XY = (X * Y.conj()).transpose().mean(axis=1)[0:dlen/2]
        freq = fft.fftfreq(dlen, d)[0:dlen/2]
        ecph =  angle(XY) 
       
        arrs[abcs] = freq
        arrs[lgtd] = ecph
        if not z is None: arrs[3 - abcs - lgtd] = z[0:dlen/2] 
        self.ecph = handle_3d()
        self.ecph.dinput(arrs)

    def cross_spec_ensemble(self, obj, wid, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        arrs2 = obj.get_data()
        x2 = arrs2[abcs]
        y2 = arrs2[lgtd]
        z2 = arrs2[3 - abcs - lgtd]

        d = float(x[1] - x[0]) 
        n = int(wid / d)

        if x is not None: x = x[0:x.size - x.size % n]
        if y is not None: y = y[0:y.size - y.size % n] 
        if z is not None: z = z[0:z.size - z.size % n]
        if x2 is not None: x2 = x2[0:x.size - x.size % n]
        if y2 is not None: y2 = y2[0:y.size - y.size % n] 
        if z2 is not None: z2 = z2[0:z.size - z.size % n]

        y = hsplit(y, y.size/n) 
        y2 = hsplit(y2, y2.size/n) 

        dlen = len(y[0])
        X = fft.fft(y)
        Y = fft.fft(y2)
        XY = (X * Y.conj()).transpose().mean(axis=1)[0:dlen/2]
        X = X.transpose().mean(axis=1)
        Y = Y.transpose().mean(axis=1)
        freq = fft.fftfreq(dlen, d)[0:dlen/2]
        ecross =  XY /(X.size * Y.size)
       
        arrs[abcs] = freq
        arrs[lgtd] = ecross
        #arrs[abcs] = roll(freq, freq.size/2)
        #arrs[lgtd] = roll(ecross, ecross.size/2)
        if not z is None: arrs[3 - abcs - lgtd] = z[0:dlen/2] 
        self.ecross = handle_3d()
        self.ecross.dinput(arrs)

    def pow_spec_ensemble(self, wid, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        d = float(x[1] - x[0]) 
        n = int(wid / d)

        if x is not None: x = x[0:x.size - x.size % n]
        if y is not None: y = y[0:y.size - y.size % n] 
        if z is not None: z = z[0:z.size - z.size % n]

        y = hsplit(y, y.size/n) 
        dlen = len(y[0])
#        t = (x[-1] - x[0]) 
#
#        X = fft.fft(y)
#        #X = fft.fft(y, pnum)
#        dnum = X.size
#        freq = (1 /(d * dnum)) * arange(dnum)
#        #freq = abs(fft.fftfreq(dnum,d))
#        dfreq = freq[1] - freq [0]
#    
        X = fft.fft(y).transpose().mean(axis=1)[0:dlen/2]
        #X = fft.fft(y)[0:y.size/2]
        freq = fft.fftfreq(dlen, d)[0:dlen/2]
        epow =  abs(X/X.size) ** 2
        #pow =  abs(X/X.size) ** 2 * d
        #pow =  abs(X/x.size) ** 2 / dnum
        #pow =  t * (X.real ** 2 + X.imag ** 2) / (( dnum))
       
        arrs[abcs] = freq
        arrs[lgtd] = epow
        if not z is None: arrs[3 - abcs - lgtd] = z[0:dlen/2] 
        self.epow = handle_3d()
        self.epow.dinput(arrs)

    def phase_spec(self, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd] 

        d = float(x[1] - x[0]) 
#        t = (x[-1] - x[0]) 
#
#        X = fft.fft(y)
#        #X = fft.fft(y, pnum)
#        dnum = X.size
#        freq = (1 /(d * dnum)) * arange(dnum)
#        #freq = abs(fft.fftfreq(dnum,d))
#        dfreq = freq[1] - freq [0]
#    
        X = fft.fft(y)[0:y.size/2]
        freq = fft.fftfreq(X.size*2, d)[0:X.size]
        phase =  angle(X)
        #pow =  abs(X/X.size) ** 2 * d
        #pow =  abs(X/x.size) ** 2 / dnum
        #pow =  t * (X.real ** 2 + X.imag ** 2) / (( dnum))
       
        arrs[abcs] = freq
        arrs[lgtd] = phase
        if z is not None: arrs[3 - abcs - lgtd] = z[0:X.size]

        self.phase = handle_3d()
        self.phase.dinput(arrs)

    def phase_spec_ensemble(self, wid, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        d = float(x[1] - x[0]) 
        n = int(wid / d)

        if x is not None: x = x[0:x.size - x.size % n]
        if y is not None: y = y[0:y.size - y.size % n] 
        if z is not None: z = z[0:z.size - z.size % n]

        y = hsplit(y, y.size/n) 
        dlen = len(y[0])

        X = fft.fft(y).transpose().mean(axis=1)[0:dlen/2]
        freq = fft.fftfreq(dlen, d)[0:dlen/2]
        epow =  abs(X/X.size) ** 2
        phase =  angle(X)
       
        arrs[abcs] = freq
        arrs[lgtd] = phase 
        if not z is None: arrs[3 - abcs - lgtd] = z[0:dlen/2] 
        self.ephase = handle_3d()
        self.ephase.dinput(arrs)

    def pow_spec_wm(self, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]
        z = arrs[3 - abcs - lgtd]

        d = float(x[1] - x[0]) 
#        t = (x[-1] - x[0]) 
#
#        X = fft.fft(y)
#        #X = fft.fft(y, pnum)
#        dnum = X.size
#        freq = (1 /(d * dnum)) * arange(dnum)
#        #freq = abs(fft.fftfreq(dnum,d))
#        dfreq = freq[1] - freq [0]
#    
        X = myfft(y)
        freq = myfftfreq(X.size, d)
        pow =  abs(X/X.size) ** 2
        #pow =  abs(X/X.size) ** 2 * d
        #pow =  abs(X/x.size) ** 2 / dnum
        #pow =  t * (X.real ** 2 + X.imag ** 2) / (( dnum))
       
        arrs[abcs] = freq[0:freq.size/2]
        arrs[lgtd] = pow[0:freq.size/2]

        arrs[3 - abcs - lgtd] = z
        self.pow = handle_3d()
        self.pow.dinput(arrs)

    def run_pow(self, itvl, wid, abcs=0, lgtd=1):
        self.hist.input()
        #self.bindup(wid)
        arrs = self.get_data()
        xarr = arrs[abcs]
        yarr = arrs[lgtd]

        wlst = []

        tstep = (xarr[1] - xarr[0])
#        wid_d = int(wid / tstep)
#        itvl_d = int(itvl / tstep)
        narr = arange(xarr[0], xarr[-1], itvl, dtype=double)
        st = (wid / 2) / itvl + 1
        en = -st
        #input(len(narr))
        #input(narr[st:en])

        obj_lst = []

        for n in narr[st:en]:
            self.slice_arr([n-wid/2., n+wid/2.])
            self.slice.pow_spec(abcs=abcs, lgtd=lgtd)
            obj = handle_3d()
            arr_lst = self.slice.pow.get_data()
            obj.a = array(arr_lst[3 - abcs - lgtd])[0:len(arr_lst[abcs])]
            arr_lst[3 - abcs - lgtd] = ones(shape(arr_lst[abcs])) * n
            obj.dinput(arr_lst)
            obj_lst += [obj]
        
        self.rpow = h4d.handle_4d()
        self.rpow.T = False
        self.rpow.set_multi(obj_lst)
        
    def wig_spec(self, n=None, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = arrs[abcs]
        y = arrs[lgtd]

        d = float(x[1] - x[0]) 
        t = (x[-1] - x[0]) 

        X = wig_spec(y, n, pnum)
        dnum = X.size
        freq = (1 /(2 * d * dnum)) * arange(dnum)
        #freq = abs(fft.fftfreq(dnum,d))
        dfreq = freq[1] - freq [0]
    
        w =  abs(X/X.size) ** 2 
        #pow =  t * (X.real ** 2 + X.imag ** 2) / (( dnum))
       
        arrs[abcs] = freq
        arrs[lgtd] = w.real
        self.wig = handle_3d()
        self.wig.dinput(arrs)

    def run_wig(self, wid, n=None, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        #self.bindup(wid)
        arrs = self.get_data()
        xarr = arrs[abcs]
        yarr = arrs[lgtd]

        wlst = []

        tstep = (xarr[1] - xarr[0])
        d = int(wid / tstep)
        narr = arange(d/2, xarr.size-d/2)

        for n in narr:
            w = wig_spec(yarr[n - d/2: n + d/2])
            wlst +=  [abs(w/w.size) ** 2]
        tstep = xarr[1] - xarr[0]        
        warr = array(wlst).real
        tarr = tile(arange(xarr[0]+wid/2, xarr[-1]-wid/2+tstep, tstep), (len(warr[0]),1)).transpose()
        freq = tile(myfftfreq(len(warr[0]), 2*tstep),(len(warr),1))

        self.rwig = h4d.handle_4d()
        self.rwig.T = False
        self.rwig.dinput([tarr, warr, freq])
    
    def fft(self, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = array(arrs[abcs])
        y = array(arrs[lgtd])

        d = (x[1] - x[0])# * 1e-3
        dnum = x.size

        X = fft.fft(y)
        #freq = myfftfreq(X.size,2.)
        freq = fft.fftfreq(X.size,d)
        dfreq = freq[1] - freq [0]
    
        arrs[abcs] = freq
        arrs[lgtd] = X
        self.ffted = handle_3d()
        self.ffted.st_ab = x[0]
        self.ffted.en_ab = X.size * d + x[0]
        #self.ffted.en_ab = X.size * d - x[0]
        self.ffted.d_ab = d 
        self.ffted.dinput(arrs)

        #return freq, pow

    def ifft(self, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()

        arrs[abcs] = arange(self.st_ab, self.en_ab, self.d_ab)
        tmp_size = len(arrs[lgtd])
        arrs[lgtd] = fft.ifft(arrs[lgtd])
        if tmp_size != arrs[lgtd].size:
            arrs[abcs] = linspace(self.st_ab, self.en_ab, arrs[lgtd].size)
        #arrs[lgtd] = myifft(arrs[lgtd], arrs[abcs].size).real
        self.iffted = handle_3d()
        self.iffted.dinput(arrs)

    def rfft(self, abcs=0, lgtd=1):
        #input(abcs)
        self.hist.input()
        arrs = self.get_data()
        x = array(arrs[abcs])
        y = array(arrs[lgtd])

        d = (x[1] - x[0])# * 1e-3
        dnum = x.size

        X = fft.rfft(y)
        #freq = myfftfreq(X.size,2.)
        freq = fft.rfftfreq(X.size,d)
        dfreq = freq[1] - freq [0]
    
        #input(freq)
        arrs[abcs] = freq
        arrs[lgtd] = X
        self.rffted = handle_3d()
        self.rffted.st_ab = x[0]
        self.rffted.en_ab = 2 * X.size * d + x[0]
        #self.ffted.en_ab = X.size * d - x[0]
        self.rffted.d_ab = d 
        #print "Helo"
        #print arrs
        #input("helo")
        self.rffted.dinput(arrs)

        #return freq, pow

    def irfft(self, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()

        arrs[abcs] = arange(self.st_ab, self.en_ab, self.d_ab)
        tmp_size = len(arrs[lgtd])
        arrs[lgtd] = fft.irfft(arrs[lgtd])
        if tmp_size != arrs[lgtd].size:
            arrs[abcs] = linspace(self.st_ab, self.en_ab, arrs[lgtd].size)
        #arrs[lgtd] = myifft(arrs[lgtd], arrs[abcs].size).real
        self.irffted = handle_3d()
        self.irffted.dinput(arrs)
        #return freq, pow

    def fft_wm(self, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()
        x = array(arrs[abcs])
        y = array(arrs[lgtd])

        d = (x[1] - x[0])# * 1e-3
        dnum = x.size

        X = myfft(y)
        #freq = myfftfreq(X.size,2.)
        freq = myfftfreq(X.size,d)
        dfreq = freq[1] - freq [0]
    
        arrs[abcs] = freq
        arrs[lgtd] = X
        self.ffted = handle_3d()
        self.ffted.st_ab = x[0]
        self.ffted.en_ab = X.size * d + x[0]
        #self.ffted.en_ab = X.size * d - x[0]
        self.ffted.d_ab = d 
        self.ffted.dinput(arrs)

        #return freq, pow

    def ifft_wm(self, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.get_data()

        arrs[abcs] = arange(self.st_ab, self.en_ab, self.d_ab)
        tmp_size = len(arrs[lgtd])
        arrs[lgtd] = myifft(arrs[lgtd]).real
        if tmp_size != arrs[lgtd].size:
            arrs[abcs] = linspace(self.st_ab, self.en_ab, arrs[lgtd].size)
        #arrs[lgtd] = myifft(arrs[lgtd], arrs[abcs].size).real
        self.iffted = handle_3d()
        self.iffted.dinput(arrs)

    def filter(self, plst, inv=False, abcs=0, lgtd=1, cut=False, weight=4):
        self.hist.input()    
        obj = handle_3d()
        obj.dinput(self.get_data())
        obj.fft(abcs=abcs,lgtd=lgtd)
        obj.ffted.punch_out(plst, abcs, inv, 0)
        obj.ffted.pout.st_ab = obj.ffted.st_ab
        obj.ffted.pout.en_ab = obj.ffted.en_ab
        obj.ffted.pout.d_ab = obj.ffted.d_ab
#        obj.rfft(abcs=abcs,lgtd=lgtd)
#        obj.rffted.punch_out(plst, abcs, inv, 0)
#        obj.rffted.pout.st_ab = obj.rffted.st_ab
#        obj.rffted.pout.en_ab = obj.rffted.en_ab
#        obj.rffted.pout.d_ab = obj.rffted.d_ab
        o = obj.ffted.pout
#        o.y[o.y.size/2:] = o.y[o.y.size/2:0:-1].conj()
        o.ifft()
        self.filt = o.iffted
        self.filt.y = self.filt.y.real
        if cut:
            wmax = plst[0][1]
            d = self.filt.x[1] - self.filt.x[0]
            #obj.x = obj.x[:: around(1./(d * (2 * wmax)))]
            self.filt.x = self.filt.x[:: around(1./(d * (weight * wmax)))]
            #input(o.x)
            self.filt.y = self.filt.y[:: around(1./(d * (weight * wmax)))]
            bj.y = obj.y[:: around(1./(d * (2 * wmax)))]


    def resample(self, fs, prec=10, abcs=0, lgtd=1):
        self.hist.input()    
        obj = handle_3d()
        obj.dinput(self.get_data())
        obj.rfft(abcs=abcs,lgtd=lgtd)
        obj.rffted.punch_out([[0,fs]], abcs, True, 0)
        obj.rffted.pout.st_ab = obj.rffted.st_ab
        obj.rffted.pout.en_ab = obj.rffted.en_ab
        obj.rffted.pout.d_ab = obj.rffted.d_ab
        o = obj.rffted.pout

        fs_old = 1./o.d_ab
        fs_new = fs
        fLCM = fs_old * fs_new
        df = o.x[1] - o.x[0]
        dn = prec * (fLCM - o.x[-1]) /  df
        #input(fs_old)
        #input(fs_new)
        #input(o.x[-1]  / fs_old)
        

        o.x = append(o.x, o.x[-1] + arange(1, dn + 1) * df)
        o.y = append(o.y, zeros(dn)) * o.x[-1]  / fs_old


        o.irfft()
        #input(o.x)
        #input(o.y)
        #input(o.view())
        #input(o.irffted.view())
        #input(o.irffted.x)
        self.rsmp = o.irffted

        weight = 2.
        wmax = fs
        d = self.rsmp.x[1] - self.rsmp.x[0]
        #obj.x = obj.x[:: around(1./(d * (2 * wmax)))]
        #input(1./(d * (weight * wmax)))
        #input(around(1./(d * (weight * wmax))))
        self.rsmp.x = self.rsmp.x[:: around(1./(d * (weight * wmax)))]
        #input(o.x)
        self.rsmp.y = self.rsmp.y[:: around(1./(d * (weight * wmax)))]
#        input(self.rsmp.view())
        #obj.y = obj.y[:: around(1./(d * (2 * wmax)))]



    def filter_decimation2(self, flst, abcs=0, lgtd=1):
        obj = deepcopy(self)
        obj.hist.input()    
        obj.rfft(abcs=abcs,lgtd=lgtd)
        obj.rffted.punch_out([flst], abcs, True)
        x = obj.rffted.pout.x 
        y = obj.rffted.pout.y 
        n = obj.rffted.y.size
        d = x[1] - x[0] 
        #obj.rffted.pout.x = append(x, x + x.max() + d)[:0:-1]
        #obj.rffted.pout.y = append(y, y[:0:-1].conj())
        #obj.ffted.pout.y = abs(append(y, y[-1:0:-1].conj())) ** 2
        obj.rffted.pout.st_ab = obj.rffted.st_ab
        obj.rffted.pout.en_ab = obj.rffted.en_ab
        obj.rffted.pout.d_ab = obj.rffted.d_ab
        o = obj.rffted.pout
        o.y = o.y * o.y.size / n
        #input(o.y)
        #o.y[o.y.size/2:] = o.y[o.y.size/2:0:-1].conj()
        o.irfft()
        self.dfilt = o.irffted

    def filter_decimation_old(self, flst, abcs=0, lgtd=1):
        obj = deepcopy(self)
        obj.hist.input()    
        obj.fft_wm(abcs=abcs,lgtd=lgtd)
        obj.ffted.punch_out([flst], abcs, True, 0)
        obj.ffted.pout.st_ab = obj.ffted.st_ab
        obj.ffted.pout.en_ab = obj.ffted.en_ab
        obj.ffted.pout.d_ab = obj.ffted.d_ab
        o = obj.ffted.pout
        o.y[o.y.size/2:] = o.y[o.y.size/2:0:-1].conj()
        o.ifft_wm()
        self.dfilt = o.iffted

        weight = 2.
        wmax = flst[1]
        d = self.dfilt.x[1] - self.dfilt.x[0]
        #obj.x = obj.x[:: around(1./(d * (2 * wmax)))]
        self.dfilt.x = self.dfilt.x[:: around(1./(d * (weight * wmax)))]
        #input(o.x)
        self.dfilt.y = self.dfilt.y[:: around(1./(d * (weight * wmax)))]
        #obj.y = obj.y[:: around(1./(d * (2 * wmax)))]

    def filter_smoothing(self, plst, abcs=0, lgtd=1, cut=False):
        obj = deepcopy(self)
        obj.hist.input()    
        obj.fft(abcs=abcs,lgtd=lgtd)
        dnum = float(obj.ffted.y.size)
        obj.ffted.punch_out(plst, abcs, True, None, lgtd)
        obj.ffted.pout.st_ab = obj.ffted.st_ab
        obj.ffted.pout.en_ab = obj.ffted.en_ab
        obj.ffted.pout.d_ab = 1. / (2*obj.ffted.pout.x[-1])
        o = obj.ffted.pout
        o.x = append(o.x, o.x + o.x[-1] + 1)
        o.y = append(o.y, o.y[:0:-1].conj()) * (2 * o.y.size / dnum)
        o.ifft()
        self.filt = o.iffted

    def filter2(self, slst, abcs=0, lgtd=1):
        obj = deepcopy(self)
        obj.hist.input()    
        obj.fft(abcs=abcs,lgtd=lgtd)
        obj.ffted.slice_arr(slst, abcs)
        #input(obj.ffted.slice.x)
        #input(obj.ffted.slice.y)
        obj.ffted.slice.st_ab = obj.ffted.st_ab
        obj.ffted.slice.en_ab = obj.ffted.en_ab
        obj.ffted.slice.d_ab = obj.ffted.d_ab
        obj.ffted.slice.ifft()
        self.filt = obj.ffted.slice.iffted

       

    def bindup( self, width, xyz=0, retnum=None):
        self.hist.input()
        width = float(width)
        
        arrs = self.get_data()
        xdata,ydata,zdata = (self.x, self.y, self.z)
        d = arrs[xyz][1] - arrs[xyz][0]
        #num = num_dcml(d)
        #tmp = xdata
        #xdata = arange(xdata[0],xdata[-1]+num, 10**(-d))
        #wharr = where()
        #xdata[]
        num = int(width/d)
        xarrs = [xdata[0:-num]] if type(xdata) != type(None) else None
        yarrs = [ydata[0:-num]] if type(ydata) != type(None) else None
        zarrs = [zdata[0:-num]] if type(zdata) != type(None) else None
        for n in range(1,num):
            xarrs = append(xarrs, [xdata[n:-num+n]], axis=0) if type(xdata) != type(None) else None
            yarrs = append(yarrs, [ydata[n:-num+n]], axis=0) if type(ydata) != type(None) else None
            zarrs = append(zarrs, [zdata[n:-num+n]], axis=0) if type(zdata) != type(None) else None

        xarrs = transpose(xarrs) if type(xarrs) != type(None) else None
        yarrs = transpose(yarrs) if type(yarrs) != type(None) else None
        zarrs = transpose(zarrs) if type(zarrs) != type(None) else None
        self.bind = handle_3d(xarrs, yarrs, zarrs)
        
        if retnum:
            return num
        else:
            return xarrs, yarrs, zarrs if type(zarrs) != type(None) else xarrs, yarrs

    def bindup2( self, width, xyz=0, retnum=None):
        import scipy.signal as s
        self.hist.input()
        width = float(width)
        arrs = self.get_data()
        
        d = arrs[xyz][1] - arrs[xyz][0]
        #num = num_dcml(d)
        #tmp = xdata
        #xdata = arange(xdata[0],xdata[-1]+num, 10**(-d))
        #wharr = where()
        #xdata[]
        wn = int(width/d)

        dn = arrs[xyz].size
        n = dn - (wn - 1)
        #input(wn)
        #idx = eye(n)
        #for i in xrange(1,wn):
        #    idx += eye(n,k=i)
        #idx = idx == True
        idx=s.fftconvolve(eye(n),ones((1,wn)), mode="valid") == True
        retlst = []
        for arr in arrs:
            if arr is not None:
                #arr = arr[0:n]
                a = tile(arr, (n, 1))
 
                retlst += [a[idx].reshape(n, wn)]
            else:
                retlst += [None]
            print "Done"

        
        self.bind = h4d.handle_4d()
        self.bind.dinput(retlst)

   # def gradient( self, width, retnum=None, abcs=0, lgtd=1):
   #     self.hist.input()
   #     
   #     num = self.bindup(width, retnum=True)
   #     if num == 1:
   #         raise ValueError, "Arg 'width' is wider than the data interval of 'abcs'."
   #     arrs = self.bind.get_data()
   #     xarrs = arrs[abcs]
   #     yarrs = arrs[lgtd]

   #     sumx = sum(xarrs, axis=1)
   #     sumy = sum(yarrs, axis=1)
   #     sumxy = sum(xarrs*yarrs, axis=1)
   #     sumxx = sum(xarrs*xarrs, axis=1)
   #     retarr = (( num * sumxy) - sumx * sumy ) / ( num * sumxx  - sumx ** 2 )
   #     
   #     arrs[abcs] = mean(xarrs, axis=1)
   #     arrs[lgtd] = retarr
   #     self.grad = handle_3d()
   #     self.grad.dinput(arrs)
   #     if retnum:
   #         return num
   #     else:
   #         return arrs[abcs], arrs[lgtd]

    def gradient( self, abcs=0, lgtd=1):
        self.hist.input()
        
        arrs = self.get_data()
        xarrs = arrs[abcs]
        yarrs = arrs[lgtd]

        sumx = sum(xarrs)
        sumy = sum(yarrs)
        sumxy = sum(xarrs*yarrs)
        sumxx = sum(xarrs*xarrs)
        num = xarrs.size
        ret = (( num * sumxy) - sumx * sumy ) / ( num * sumxx  - sumx ** 2 )
        
        self.grad = ret
            
    def average( self, abcs=0, lgtd=1):
        self.hist.input()
        
        arrs = self.get_data()
        xarrs = arrs[abcs]
        yarrs = arrs[lgtd]

        xarrs = xarrs.mean()
        yarrs = yarrs.mean()
        self.xmean = xarrs
        self.ymean = yarrs

    def show_select(self):
        self.hist.input()
        print """
            "select" can be substituted below character.

            raw  : raw xyz Data.
            gnu  : xyz Data caluculated by the method "gnufit" with LM fitting using gnuplot.
            grad : xyz Data caluculated by the method "grad".
            pout : xyz Data caluculated by the method "punch_out".
            pfit : xyz Data caluculated by the method "polyfit".
            pcnv : one of xyz Data caluculated by the method "prmconv" but other is raw data.
            bstd : one of xyz Data caluculated by the method "bind_std" but other is raw data.
            bmean : one of xyz Data caluculated by the method "bind_mean" but other is raw data.
        """
    def bind_std(self, width, retnum=None, xyz=1):
        self.hist.input()
        num = self.bindup(width, retnum=True)
        arrs = self.bind.get_data()

        for n in range(3):
            if xyz == n:
                arrs[n] = arrs[n].std(axis=1) if type(arrs[n]) != type(None) else None
            else:
                arrs[n] = arrs[n].mean(axis=1) if type(arrs[n]) != type(None) else None

        self.bstd = handle_3d(arrs[0], arrs[1], arrs[2])
        if retnum:
            return num
        else:
            return self.bstd.get_data()
    def bind_std_arb(self, itvl=0.01, width=0.1, retnum=None, abcs=0, lgtd=1):
        self.hist.input()
        #num = self.bindup(width, retnum=True)
        arrs = self.get_data()
        abcsarr = arrs[abcs]

        for n in range(3):
            if lgtd == n:
                arrs[n] = std_arb(abcsarr, arrs[lgtd], itvl, width )[1] if type(arrs[n]) != type(None) else None
            else:
                arrs[n] = ave_arb(abcsarr, arrs[n], itvl, width )[1] if type(arrs[n]) != type(None) else None

        self.bstd = handle_3d(arrs[0], arrs[1], arrs[2])
        if retnum:
            return len(arrs[abcs])
        else:
            return self.bstd.get_data()

    def bind_mean(self, width, retnum=None, dname="raw"):
        self.hist.input()
        num = self.bindup(width, retnum=True)
        arrs = self.bind.get_data()
        
        for n in range(3):
            arrs[n] = arrs[n].mean(axis=1) if type(arrs[n]) != type(None) else None
            
        self.mean = handle_3d(arrs[0], arrs[1], arrs[2])
        if retnum:
            return num

    def sort(self, xyz=0):
        self.hist.input()
        arrs = copy.deepcopy(self.get_data())
        idx = argsort(arrs[xyz])
        for i in xrange(len(arrs)):
            arr = arrs[i]
            if arr is not None:
                arr = arr[idx]
            arrs[i] = arr
        self.sorted = handle_3d()
        self.sorted.dinput(arrs)

        
        self.dinput(map(lambda x: sorted(x) if type(x) != type(None) else None, self.get_data()))

    def get_data(self, reterr=False):
        x = array(self.x) if type(self.x) != type(None) else None
        y = array(self.y) if type(self.y) != type(None) else None
        z = array(self.z) if type(self.z) != type(None) else None
        a = array(self.a) if type(self.a) != type(None) else None
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

    def dinput(self, arrlst, errlst=None):
        self.x = array(arrlst[0]) if type(arrlst[0]) != type(None) else None
        self.y = array(arrlst[1]) if type(arrlst[1]) != type(None) else None
        if arrlst[2] is not None : self.z = array(arrlst[2]) 
        #input(array(arrlst[0]))
        #input(self.x)
        if errlst:
            self.xerr = array(errlst[0]) if type(errlst[0]) != type(None) else None
            self.yerr = array(errlst[1]) if type(errlst[1]) != type(None) else None
            self.zerr = array(errlst[2]) if type(errlst[2]) != type(None) else None

    def __add__(self, other):
        return h4d.handle_4d([self, other])



    def dumpdata(self, wpath=None):
        self.hist.input()
        wpath = wpath if wpath else self.wpath 
        self.write.simpledump(wpath, self.get_data(), tag="%s, %s, %s"%(self.xname, self.yname, self.zname))
        
    def view(self, layout="1", abcs=0, lgtd=1, logx=False, logy=False, real=None):
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
        self.hist.input()
        #self.grace.layout_1()
        if layout == "column":
            layoutdic[layout](gnumlim)
        else:
            layoutdic[layout]()
        self.set_xaxes(1,0) if logx == True else self.set_xaxes(0,0)
        self.set_yaxes(1,0) if logy == True else self.set_yaxes(0,0)
        arrs,errs = self.get_data(reterr=True)
        if real is not None:
            arrs[lgtd] = arrs[lgtd].real if real else arrs[lgtd].imag
        if type(errs[lgtd]) == type(None):
            #arrs[abcs], arrs[lgtd] = self.grace.set_xydata(array(arrs[abcs]), array(arrs[lgtd]))
            self.grace.set_xydata(array(arrs[abcs]), array(arrs[lgtd]))
        else:
            self.grace.set_xydy(array(arrs[abcs]), array(arrs[lgtd]), array(errs[lgtd]))
            #arrs[abcs], arrs[lgtd] = self.grace.set_xydy(array(arrs[abcs]), array(arrs[lgtd]), array(errs[lgtd]))
            
        ##############################
        #arrsを代入すると
        #set_xydataのあとarrsのデータ
        #がめちゃくちゃになる。
        #なぜか返り値はそうならない。
        #そのため、返り値でもう一度代入させて対処。
        #要検証。
        ##############################
#        if type(self.grace.prop.gdiclst[0]["xlabel"]) == type(None):
#            self.grace.set_xlabel("No name")
#        else:
#            self.grace.set_xlabel(self.grace.prop.gdiclst[0]["xlabel"])
#        
#        if self.grace.prop.gdiclst[0]["ylabel"] == type(None):
#            self.grace.set_ylabel("No name")
#        else:
#            self.grace.set_ylabel(self.grace.prop.gdiclst[0]["ylabel"])
#
        if type(self.grace.prop.decolst) != type(None):
            self.grace.set_ornament()
        if self.grace.prop.gdiclst[0]["lim"] is None:
            self.grace.set_autoscale(arrs[abcs], arrs[lgtd],logx=logx, logy=logy)
        else:
            (xmin, xmax, ymin, ymax, gnum) = self.grace.prop.gdiclst[0]["lim"]
        if len(self.grace.prop.gdiclst): self.grace.set_graphitems()
#            self.grace.set_lim(xmin, xmax, ymin, ymax, gnum)

        self.grace.open_grace()
        self.grace.initialize()
        #self.dinput(arrs)

    def view_col(self,  layout="simple", axtpl=(0,1,2), device="png", opt="colz", palette="simple"):
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
        x = arrs[axtpl[0]]
        y = arrs[axtpl[1]]
        z = arrs[axtpl[2]]
        

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

    def playback(self, index=0):
        self.hist.execute(index=index)
           
