#!/usr/bin/env python
#-*- coding:utf-8 -*-
from numpy import *
from writedatmanage import *
#from trimdata import *
from gracemanage import * 
from graphmanage import * 
from calctools import *
import os 
import itertools as it
import pickle
import ana_spec as spec


class graphhandler():
    def set_errorbar(self, gnum=0, snum=0, color=1, patn=1, size=1, lwidth=2, lstyle=1, rlwidth=1, rlstyle=1):
        self.grace.prop.errorbar_input(gnum, snum, color, patn, size, lwidth, lstyle, rlwidth, rlstyle)

    def set_xtickitvl(self, itvl, gnum=0):
        self.grace.prop.xtickitvl_input(itvl, gnum)
        
    def set_ytickitvl(self, itvl, gnum=0):
        self.grace.prop.ytickitvl_input(itvl, gnum)

    def set_xlabel(self, xname, gnum=0):
        self.grace.prop.xlabel_input(xname, gnum)
        
    def set_ylabel(self, yname, gnum=0):
        self.grace.prop.ylabel_input(yname, gnum)

    def set_lim(self, xmin, xmax, ymin, ymax, gnum=0, tnum=6):
        self.grace.prop.lim_input(xmin, xmax, ymin, ymax, gnum, tnum)

    def set_leg(self, yname, gnum=0, snum=0, loc="rightup", loctype="view"):
        self.grace.prop.leg_input(yname, gnum, snum, loc, loctype)
    
    def set_style_line(self, width=1, color=0, lstyle=1, gnum=0, snum=0):
        self.grace.prop.style_line_input(width, color, lstyle, gnum, snum)

    def set_mk(self, size=1, color=0, mstyle=1, fcolor=None, fptn=1, lwidth=1, lstyle=1, gnum=0, snum=0):
        self.grace.prop.mk_input(size, color, mstyle, fcolor, fptn, lwidth, lstyle, gnum, snum)

    def set_lineall(self, select=0, size=1, color=1, lstyle=1):
        self.grace.prop.lineall_input(select, size, color, lstyle)

    def set_mkall(self, size=1, color=1, mstyle=1, fptn=[1], lwidth=[1], lstyle=[1]):
        self.grace.prop.mkall_input(size, color, mstyle, fptn, lwidth, lstyle)

    def set_string(self, line, loc, loctype="view", gnum=0, charsize=1):
        self.grace.prop.string_input(line, loc, loctype, gnum, charsize)
        
    def set_iterstr(self, lst, loc, loctype="view", gnum=0, charsize=1):
        self.grace.prop.iterstr_input(lst, loc, loctype, gnum, charsize)

    def set_box(self, loc, lstyle=1, lwidth=1, lcolor=1,  fcolor=1, fptn=0, loctype="view", gnum=0):
        self.grace.prop.box_input(loc, lstyle, lwidth, lcolor,  fcolor, fptn, loctype, gnum)

    def set_ellipse(self, loc, lstyle=1, lwidth=1, lcolor=1,  fcolor=1, fptn=0, loctype="view", gnum=0):
        self.grace.prop.ellipse_input(loc, lstyle, lwidth, lcolor,  fcolor, fptn, loctype, gnum)

    def set_box(self, loc, lstyle=1, lwidth=1, lcolor=1,  fcolor=1, fptn=0, loctype="view", gnum=0, xonly=False, yonly=False):
        self.grace.prop.box_input(loc, lstyle, lwidth, lcolor,  fcolor, fptn, loctype, gnum, xonly, yonly)
    def set_line(self, loc, lstyle=1, lwidth=1, lcolor=1, arrow=0, atype=0, alength=0, alayout=(1,1), loctype="view", gnum=0, xonly=False, yonly=False):
        self.grace.prop.line_input(loc, lstyle, lwidth, lcolor, arrow, atype, alength, alayout, loctype, gnum, xonly, yonly)
    
        
class processdata(graphhandler):
    def __init__(self, x=None,y=None, z=None, xname="x", yname="y", zname="z", err=None):
        self.x = x 
        self.y = y 
        self.z = z
        self.err = err
        self.xname = xname
        self.yname = yname
        self.zname = zname
        self.grace = gracemanage()
        self.write = writedatmanage()
        self.load = loaddatmanage()
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
        if picklepath == None: picklepath = self.picklepath
        o = open(picklepath, "w")
        pickle.dump(self, o)
        o.close()

    def load_pickle(self, picklepath=None):
        if picklepath == None: picklepath = self.picklepath
        o = open(picklepath)
        tmp = pickle.load(o)
        self.err = tmp.err
        self.dinput(tmp.getdata())
        self.hist.hlst = tmp.hist.hlst
        o.close()

    def backup(self):
        self.hist.input()
        s = TemporaryFile()
        pickle.dump(self, s)
        s.seek(0)
        self.bkuplst += [s]

    def crosscorr(self, tau, point, abcs=0, lgtd=1):
        arrs = self.getdata()
        parrs = point.getdata()
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
        self.ccor = processdata()
        self.ccor.dinput(arrs)

    def autocorr(self, tau, abcs=0, lgtd=1):
        # calc Autocorrelation.
        arrs = self.getdata()
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
        self.acor = processdata()
        self.acor.dinput(arrs)

    def autocorr_wf(self, tau, abcs=0, lgtd=1):
        # calc Autocorrelation.
        arrs = self.getdata()
        x = arrs[abcs]
        y = arrs[lgtd]
        dx = x[1] - x[0]


        x, y = spec.autocorr(tau, x, y)

        arrs[abcs] = x
        arrs[lgtd] = y
        self.acor = processdata()
        self.acor.dinput(arrs)

    def crosscorr_wf(self, tau, point, abcs=0, lgtd=1):
        # calc Autocorrelation.
        arrs = self.getdata()
        x1 = arrs[abcs]
        y1 = arrs[lgtd]
        arrs = point.getdata()
        y2 = arrs[lgtd]

        x, y = spec.crosscorr(tau, x1, y1, y2)

        arrs[abcs] = x
        arrs[lgtd] = y
        self.ccor = processdata()
        self.ccor.dinput(arrs)

    def crosscorr_func_wf(self, tau, point, abcs=0, lgtd=1):
        # calc Autocorrelation.
        arrs = self.getdata()
        x1 = arrs[abcs]
        y1 = arrs[lgtd]
        arrs = point.getdata()
        y2 = arrs[lgtd]

        x, y, z= spec.crosscorr_func(tau, x1, y1, y2)

        arrs[abcs] = x
        arrs[lgtd] = y
        arrs[3-abcs-lgtd] = z
        self.ccor = multiprocess()
        self.ccor.dinput(arrs)

    def view_2d(self, abcs=0, lgtd=1):
        arrs = self.getdata()
        z = arrs[3 - abcs - lgtd]
        x = arrs[abcs]
        y = arrs[lgtd]

        a = rootmacro()
        a.set_xyzdata(x,y,z)
        a.ldump()
        a.open_macro()

    def view_col(self, abcs=2, lgtd=1):
        arrs = self.getdata()
        x = arrs[3 - abcs - lgtd]
        y = arrs[abcs]
        z = arrs[lgtd]

        a = rootmacro()
        a.set_xyzdata(x,y,z,colormap=True)
        a.ldump()
        a.open_macro()

    def average(self, INT, AVE):
        self.hist.input()
        from numpy import array, mean
        from decimal import Decimal
        x = self.x 
        y = self.y 

        dt = (x[1] - x[0])
        intelm = int(Decimal(str(INT / dt)))
        averange = int(Decimal(str(AVE / (2 * dt))))
    
        x_ave = []
        y_ave = []
    
        l = len(x)
        n = 0
        while n < l:
            print n
            x_ave += [x[n]]
            elmin = n - averange
            elmax = n + averange
            if elmin < 0:
                elmin = 0
            if elmax > l:
                elmax = l-1
            y_ave  += [mean(y[elmin : elmax])]
            n += intelm
        self.ave = processdata(array(x_ave), array(y_ave))

    def slice_arr(self, slst, xyz=0):
        self.hist.input()
        arrs = self.getdata()
        arr = arrs[xyz]
        arrs = array([x[where((slst[0] <= arr) == (arr <= slst[1]))[0]] if x != None else None for x in arrs])
        self.slice = processdata()
        self.slice.dinput(arrs)
        
    def zero_adj(self, plst, abcs=0, lgtd=1, inv=True):
        self.hist.input()
        arrs = self.getdata()
        x = arrs[abcs]
        y = arrs[lgtd]
        y -= y[where((plst[0] <= x) == (x <= plst[1]))[0]].mean()
        arrs[abcs] = x
        arrs[lgtd] = y
        self.zadj = processdata()
        self.zadj.dinput(arrs)

    def punch_out(self, plst, pxyz=0, inv=False):
        self.hist.input()
        x,y,z = self.getdata()
        dlst = [x,y,z]
        for pmin, pmax in plst: 
            numarr = where( inv == ((pmin <= dlst[pxyz]) * (pmax >= dlst[pxyz])))[0]
            x = x[numarr] if x != None else None
            y = y[numarr] if y != None else None
            z = z[numarr] if z != None else None
            dlst = [x,y,z]
        self.pout = processdata(x,y,z)
        return x,y,z if z != None else x,y

    def polyfit(self, M=8, stnum=None, ennum=None, itvl=0.1, abcs=0, lgtd=1, show=False):
        self.hist.input()
        arrs = self.getdata()
        x = arrs[abcs]
        y = arrs[lgtd]
        sen = [stnum, ennum, itvl]
        if stnum == None:
            sen[0] = x[0]    
        if ennum == None:
            sen[1] = x[-1]    
        x,y = pfit(x, y, M, sen) 
        arrs[abcs] = x
        arrs[lgtd] = y
        self.pfit = processdata()
        self.pfit.dinput(arrs)
        if show:
            tmp = self + self.pfit
            tmp.view()

    def gnufit(self, function, fitparalst, stnum=None, ennum=None, itvl=1, show=False, abcs=0, lgtd=1):
        self.hist.input()
        import Gnuplot as gp
#        from subprocess import call

        arrs = self.getdata()
        x = arrs[abcs]
        y = arrs[lgtd]

        tmppath = home() + "/tmp.txt"
        tmppath2 = home() + "/tmp2.txt"
        #savetxt(tmppath,transpose(array([self.x, self.y])))
        writedat(tmppath,array([x, y]))
        
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
        if stnum == None:
            stnum = x[0]    
        if ennum == None:
            ennum = x[-1]    
        x = arange(stnum, ennum, itvl)

        for para, val in zip(paras, paravals):
            exe = "%s = %s" %(para, val)
            exec exe
        exe = "y = %s" %function
        exec exe
        arrs[abcs] = x
        arrs[lgtd] = y
        self.gnu = processdata()
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
        arrlst = self.getdata()
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
        
        self.pcnv = processdata()
        arrlst[xyz] = array(retlst)
        self.pcnv.dinput(arrlst)
        #return retlst

    def pow_spec(self, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.getdata()
        x = arrs[abcs]
        y = arrs[lgtd]

        d = float(x[1] - x[0]) 
        t = (x[-1] - x[0]) 

        X = fft.fft(y)
        #X = fft.fft(y, pnum)
        dnum = X.size
        freq = (1 /(d * dnum)) * arange(dnum)
        #freq = abs(fft.fftfreq(dnum,d))
        dfreq = freq[1] - freq [0]
    
        pow =  abs(X/x.size) ** 2 / dnum
        #pow =  t * (X.real ** 2 + X.imag ** 2) / (( dnum))
       
        arrs[abcs] = freq
        arrs[lgtd] = pow
        self.pow = processdata()
        self.pow.dinput(arrs)
        
    def wig_spec(self, n=None, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.getdata()
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
        self.wig = processdata()
        self.wig.dinput(arrs)

    def run_wig(self, wid, n=None, pnum=False, abcs=0, lgtd=1):
        self.hist.input()
        #self.bindup(wid)
        arrs = self.getdata()
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

        self.rwig = multiprocess()
        self.rwig.T = False
        self.rwig.dinput([tarr, warr, freq])
    
    def fft(self, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.getdata()
        x = array(arrs[abcs])
        y = array(arrs[lgtd])

        d = (x[1] - x[0])# * 1e-3
        dnum = x.size

        X = myfft(y)
        freq = myfftfreq(dnum,X.size)
        dfreq = freq[1] - freq [0]
    
        arrs[abcs] = freq
        arrs[lgtd] = X
        self.wspec = processdata()
        self.wspec.st_ab = x[0]
        self.wspec.en_ab = X.size * d - x[0]
        self.wspec.d_ab = d 
        self.wspec.dinput(arrs)

        #return freq, pow

    def ifft(self, abcs=0, lgtd=1):
        self.hist.input()
        arrs = self.getdata()
        arrs[abcs] = arange(self.st_ab, self.en_ab, self.d_ab)
        arrs[lgtd] = myifft(arrs[lgtd], arrs[abcs].size).real
        self.iffted = processdata()
        self.iffted.dinput(arrs)

        #return freq, pow

    def bindup( self, width, retnum=None):
        self.hist.input()
        width = float(width)
        
        xdata,ydata,zdata = (self.x, self.y, self.z)
        d = xdata[1] - xdata[0]
        #num = num_dcml(d)
        #tmp = xdata
        #xdata = arange(xdata[0],xdata[-1]+num, 10**(-d))
        #wharr = where()
        #xdata[]
        num = int(width/d)
        xarrs = [xdata[0:-num]] if xdata != None else None
        yarrs = [ydata[0:-num]] if ydata != None else None
        zarrs = [zdata[0:-num]] if zdata != None else None
        for n in range(1,num):
            xarrs = append(xarrs, [xdata[n:-num+n]], axis=0) if xdata != None else None
            yarrs = append(yarrs, [ydata[n:-num+n]], axis=0) if ydata != None else None
            zarrs = append(zarrs, [zdata[n:-num+n]], axis=0) if zdata != None else None

        xarrs = transpose(xarrs) if xarrs != None else None
        yarrs = transpose(yarrs) if yarrs != None else None
        zarrs = transpose(zarrs) if zarrs != None else None
        self.bind = processdata(xarrs, yarrs, zarrs)
        
        if retnum:
            return num
        else:
            return xarrs, yarrs, zarrs if zarrs != None else xarrs, yarrs

    def gradient( self, width, retnum=None, abcs=0, lgtd=1):
        self.hist.input()
        
        num = self.bindup(width, retnum=True)
        if num == 1:
            raise ValueError, "Arg 'width' is wider than the data interval of 'abcs'."
        arrs = self.bind.getdata()
        xarrs = arrs[abcs]
        yarrs = arrs[lgtd]

        sumx = sum(xarrs, axis=1)
        sumy = sum(yarrs, axis=1)
        sumxy = sum(xarrs*yarrs, axis=1)
        sumxx = sum(xarrs*xarrs, axis=1)
        retarr = (( num * sumxy) - sumx * sumy ) / ( num * sumxx  - sumx ** 2 )
        
        arrs[abcs] = mean(xarrs, axis=1)
        arrs[lgtd] = retarr
        x,y,z = arrs
        self.grad = processdata(x, y, z)
        if retnum:
            return num
        else:
            return arrs[abcs], arrs[lgtd]
            
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
        arrs = self.bind.getdata()

        for n in range(3):
            if xyz == n:
                arrs[n] = arrs[n].std(axis=1) if arrs[n] != None else None
            else:
                arrs[n] = arrs[n].mean(axis=1) if arrs[n] != None else None

        self.bstd = processdata(arrs[0], arrs[1], arrs[2])
        if retnum:
            return num
        else:
            return self.bstd.getdata()
    def bind_std_arb(self, itvl=0.01, width=0.1, retnum=None, abcs=0, lgtd=1):
        self.hist.input()
        #num = self.bindup(width, retnum=True)
        arrs = self.getdata()
        abcsarr = arrs[abcs]

        for n in range(3):
            if lgtd == n:
                arrs[n] = std_arb(abcsarr, arrs[lgtd], itvl, width )[1] if arrs[n] != None else None
            else:
                arrs[n] = ave_arb(abcsarr, arrs[n], itvl, width )[1] if arrs[n] != None else None

        self.bstd = processdata(arrs[0], arrs[1], arrs[2])
        if retnum:
            return len(arrs[abcs])
        else:
            return self.bstd.getdata()

    def bind_mean(self, width, retnum=None, dname="raw"):
        self.hist.input()
        num = self.bindup(width, retnum=True)
        arrs = self.bind.getdata()
        
        for n in range(3):
            arrs[n] = arrs[n].mean(axis=1) if arrs[n] != None else None
            
        self.mean = processdata(arrs[0], arrs[1], arrs[2])
        if retnum:
            return num


    def getdata(self):
        lst = [self.x, self.y, self.z]
        if self.err != None:
            lst += [self.err]
        return [array(x) if x != None else None for x in lst]

    def dinput(self, lst):
        self.x = array(lst[0]) if lst[0] != None else None
        self.y = array(lst[1]) if lst[1] != None else None
        self.z = array(lst[2]) if lst[2] != None else None
        if len(lst) == 4: self.err = lst[3]

    def __add__(self, other):
        return multiprocess([self, other])



    def dumpdata(self, wpath=None):
        self.hist.input()
        wpath = wpath if wpath else self.wpath 
        self.write.simpledump(wpath, self.getdata(), tag="%s, %s, %s"%(self.xname, self.yname, self.zname))
        
    def view(self, abcs=0, lgtd=1):
        self.hist.input()
        self.grace.simplelayout()
        arrs = self.getdata()
        if self.err == None:
            #arrs[abcs], arrs[lgtd] = self.grace.set_xydata(array(arrs[abcs]), array(arrs[lgtd]))
            self.grace.set_xydata(array(arrs[abcs]), array(arrs[lgtd]))
        else:
            arrs[abcs], arrs[lgtd] = self.grace.set_xydy(array(arrs[abcs]), array(arrs[lgtd]), self.err)
            
        ##############################
        #arrsを代入すると
        #set_xydataのあとarrsのデータ
        #がめちゃくちゃになる。
        #なぜか返り値はそうならない。
        #そのため、返り値でもう一度代入させて対処。
        #要検証。
        ##############################
#        if self.grace.prop.gdiclst[0]["xlabel"] == None:
#            self.grace.set_xlabel("No name")
#        else:
#            self.grace.set_xlabel(self.grace.prop.gdiclst[0]["xlabel"])
#        
#        if self.grace.prop.gdiclst[0]["ylabel"] == None:
#            self.grace.set_ylabel("No name")
#        else:
#            self.grace.set_ylabel(self.grace.prop.gdiclst[0]["ylabel"])
#
        if self.grace.prop.gdiclst[0]["lim"] == None:
            self.grace.set_autoscale(arrs[abcs], arrs[lgtd])
        else:
            (xmin, xmax, ymin, ymax, gnum) = self.grace.prop.gdiclst[0]["lim"]
#            self.grace.set_lim(xmin, xmax, ymin, ymax, gnum)
        if self.grace.prop.decolst != None:
            self.grace.set_ornament()
        if len(self.grace.prop.gdiclst): self.grace.set_graphitems()

        self.grace.open_grace()
        self.grace.initialize()
        self.dinput(arrs)

    def playback(self, index=0):
        self.hist.execute(index=index)
           
            
class multiprocess(graphhandler):
    def __init__(self, dlst=None):
        self.x = None
        self.y = None
        self.z = None
        self.err = None
        self.T = False
        self.dumppath = "."
        self.grace = gracemanage()
        self.load = loaddatmanage()
        self.write = writedatmanage()
        self.bkuplst = []
        self.picklepath = "tmp"
        self.hist = method_history(self)
        if dlst != None:
            self.setmulti(dlst)
    
    def setmulti(self, dlst):
        self.T = False
        sublst = [[],[],[]]
        for dcls in dlst:
             for n in range(3):
                sublst[n] += [dcls.getdata()[n]]
          
        self.dinput(map(lambda x: array(x).transpose() if x[0] != None else None, sublst))

    def transpose(self):
        self.dinput(map(lambda x: x.transpose() if x != None else None, self.getdata()))
        self.T = False if self.T else True
    
    def sort(self):
        if self.T == False:
            self.transpose()
        
        self.dinput(map(lambda x: sorted(x) if x != None else None, self.getdata()))

    def dinput(self, lst):
        self.x = array(lst[0]) if lst[0] != None else None
        self.y = array(lst[1]) if lst[1] != None else None
        self.z = array(lst[2]) if lst[2] != None else None
        if len(lst) == 4: self.err = lst[3]

    def getdata(self):
        lst = [self.x, self.y, self.z]
        if self.err != None:
            lst += [self.err]
        #input(lst)
        #input([array(x) if x != None else None for x in lst])
        #input("ood_0")
        return [array(x) if x != None else None for x in lst]
    
    def dump_txt(self, path=None, conca=False, tag=None):
        if path: path = self.dumppath
        if self.T:
            tmplst = self.getdata()

            if conca:
                # Note: Only refer to x and y array. 
                datlst = append([tmplst[0][0]], tmplst[1], axis=0)
                self.write.writedat(fcnt(path, "tmp", "txt"), datlst, tag)
            else:
                n = 0
                while n < len(tmplst[0]):
                    datlst = []
                    for tmp in tmplst:
                        if tmp != None: datlst += [tmp[n]]
                    self.write.writedat(fcnt(path, "tmp", "txt"), datlst, tag)
                    n += 1
        else:
            self.write.write_tevo(self)

    def dump_pickle(self, picklepath=None):
        if picklepath == None: picklepath = self.picklepath
        o = open(picklepath, "w")
        pickle.dump(self, o)
        o.close()

    def load_pickle(self, picklepath=None):
        if picklepath == None: picklepath = self.picklepath
        o = open(picklepath)
        tmp = pickle.load(o)
        self.T = tmp.T
        self.dinput(tmp.getdata())
        self.err = tmp.err
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

    def view_col(self,  T=False, gtime=5, sepnum=1, abcs=2, lgtd=1):

        a = rootmacro()
        arrs = self.getdata()
        x = arrs[3 - abcs - lgtd]
        y = arrs[abcs]
        z = arrs[lgtd]
        a.set_xyzdata(x,y,z)
        a.dump_data()
        a.set_data()
        a.th2()
        a.set_colmap()
        a.Fill()
        a.set_cont(99)
                
        a.unset_stat()
        a.simplelayout()   
        a.dump_macro()
        a.open_macro()
    def view_root(self, modelst, T=False, gtime=5, sepnum=1, abcs=2, lgtd=1):

        a = rootmacro()
        for m in modelst:
            if m == "color":
                arrs = self.getdata()
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
                    arrs = tmp.getdata()
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
        arrs = self.getdata()
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
            #tmp1 = processdata(arr1)
            #tmp2 = processdata(arr2)
            tmp1.crosscorr(tau, tmp2, abcs, lgtd)
            con.stack(*tmp1.ccor.getdata())
            
        #con.ndarr()
        self.pcnv = multiprocess()
        self.pcnv.T = self.T
        self.pcnv.dinput(con.get())

    def pow_spec(self, pnum=False, abcs=0, lgtd=1):
        pass

    def prmconv(self, cnvlst, xyz=0, comments="#", delim=","):
        #if self.T: self.transpose()
        arrlst = self.getdata()
        arrs = arrlst[xyz]
        tmparr = []
        for arr in arrs:
            tmp = processdata(arr)
            tmp.prmconv(cnvlst, 0, comments, delim)
            tmparr += [tmp.pcnv.getdata()[0]]
        arrlst[xyz] = tmparr
        self.pcnv = multiprocess()
        self.pcnv.T = self.T
        self.pcnv.dinput(arrlst)

    def punch_out(self, plst, xyz=0, inv=False, T=False):
        if self.T != T: self.transpose()
        arrlst = self.getdata()
        tmplst = []
        n = 0
        xtlst = []
        ytlst = []
        ztlst = []
        while n < len(arrlst[xyz]):
            x = arrlst[0][n] if arrlst[0] != None else None
            y = arrlst[1][n] if arrlst[1] != None else None
            z = arrlst[2][n] if arrlst[2] != None else None
            tmp = processdata(x, y, z)
            tmp.punch_out(plst, xyz, inv)
            xtmp,ytmp,ztmp = tmp.pout.getdata()
            xtlst += [xtmp]
            ytlst += [ytmp]
            ztlst += [ztmp]
            n += 1

        tmparr = [array(xtlst), array(ytlst), array(ztlst)]
        self.pout = multiprocess()
        self.pout.T = self.T
        self.pout.dinput(tmparr)


    def prof_ave(self, abcs=2, lgtd=1,  errb=False):
        if self.T == False:
            self.transpose()

        #self.sort(abcs)
        #arrs = self.sorted.getdata()
        arrs = self.getdata()
        
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
                if retxarr != None:
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
        self.pave = multiprocess()
        self.pave.T = True
        self.pave.dinput(array(retlst))    
        print "processed data is inputed into 'pave' instance."
            
        


    def slice_arr(self, slst, xyz=0, T=True):
        if self.T != T: self.transpose()
            
        arrs = self.getdata()
        arr = arrs[xyz]
        retlst = [[],[],[]]
        for i in range(len(arr)):
            n = max([find_dec_place(x) for x in arr[i]])
            tmp = array([x[i][where((slst[0] <= arr[i].round(n)) == (arr[i].round(n) <= slst[1]))[0]] if x != None else None for x in arrs])
            map(lambda x,y: x.append(y) if y != None else None, retlst, tmp)
            
        self.slice = multiprocess()
        self.slice.dinput(retlst)
        self.slice.T = self.T

    def dump_txt_select(self, index, T=True, path=None, conca=False, tag=None, trans=False):
        ret = self.release(index, multi=True, T=T, trans=trans)
        ret.dump_txt(path, conca, tag)
        
        
    def release(self, index, multi=False, T=True, trans=None):
        if self.T != T: self.transpose()
        arrs = self.getdata()
        elm = None
        err = []

        try:
            index.index(":")
            i = [int(x) for x in index.split(":")]
            if trans != False:
                i = val2index(arrs[trans], i)
            xlst = arrs[0][i[0]:i[-1]] if  arrs[0] != None else None
            ylst = arrs[1][i[0]:i[-1]] if  arrs[1] != None else None
            zlst = arrs[2][i[0]:i[-1]] if  arrs[2] != None else None
            if self.err != None:
                err = self.err[i[0]:i[-1]]
        except (AttributeError, ValueError):
            xlst = []
            ylst = []
            zlst = []

            if trans != None:
                if type(index) == str:
                    index = [float(x) for x in str(index).split(",")]
                index = val2index(arrs[trans][0], index)
            else:
                if type(index) == str:
                    index = [int(x) for x in str(index).split(",")]

            self.transpose()
            arrs = self.getdata()
            elm = len(index)
            for num in index:
                if  arrs[0] != None: 
                    xlst += [arrs[0][num]]  
                else:
                    xlst += [None]
                if  arrs[1] != None: 
                    ylst += [arrs[1][num]]  
                else:
                    ylst += [None]

                if  arrs[2] != None: 
                    zlst += [arrs[2][num]]  
                else:
                    zlst += [None]

                if self.err != None:
                    err += [self.err[num]]
        
        if len(err) == 0: err = None
        if multi:
            if xlst[0] == None: xlst = None
            if ylst[0] == None: ylst = None
            if zlst[0] == None: zlst = None
            ret = multiprocess()
            ret.T = self.T
            ret.dinput([xlst, ylst, zlst, err])
            return ret
        else:
            if elm == 1:
                if err != None:
                    return map(lambda x,y,z,err: processdata(x,y,z, err=err), xlst, ylst, zlst, err)[0]
                else:
                    return map(lambda x,y,z: processdata(x,y,z), xlst, ylst, zlst)[0]
            else:
                return map(lambda x,y,z,err: processdata(x,y,z, err=err), xlst, ylst, zlst, err)
                
        


    def extract(self, para, xyz=0, T=False):
        if self.T == T:
            self.transpose()

        lst = self.getdata()
        
        x = lst[xyz]
        d = x[0][1] - x[0][0]
        i = int((para - x[0][0])/ d)

        self.transpose()
        lst = self.getdata()
        x = lst[0][i] if lst[0] != None else None
        y = lst[1][i] if lst[1] != None else None
        z = lst[2][i] if lst[2] != None else None
        return processdata(x, y, z)

    def zero_adj(self, plst, abcs=0, lgtd=1, inv=True):
        if self.T == False:
            self.transpose()

        arrs = self.getdata()
        x = arrs[abcs]
        y = arrs[lgtd]
        for i in range(len(x)):
            y[i] -= y[i][where((plst[0] <= x[i]) == (x[i] <= plst[1]))[0]].mean()
            arrs[abcs][i] = x[i]
            arrs[lgtd][i] = y[i]
        self.zadj = multiprocess()
        self.zadj.dinput(arrs)
        self.zadj.T = True

    def bindup( self, width, retnum=None):
        if self.T == False:
            self.transpose()
        arrlst = self.getdata()
        xretlst = []
        yretlst = []
        zretlst = []
        width = float(width)
        for n in range(len(arrlst[0])):
            tmp = processdata(arrlst[0][n] if arrlst != None else None,
                              arrlst[1][n] if arrlst != None else None,
                              arrlst[2][n] if arrlst != None else None)
            num = tmp.bindup(width, retnum=True)
            xret, yret, zret = tmp.bind.getdata()
            xretlst = xretlst + [xret] if xret != None else None
            yretlst = yretlst + [yret] if yret != None else None
            zretlst = zretlst + [zret] if zret != None else None
            
        self.bind = multiprocess()
        self.bind.dinput([array(xretlst),array(yretlst),array(zretlst)])
        if retnum:
            return num
    
    def bind_std(self, width, xyz=2):
        self.bindup(width)
        retlsts = []
        for i, arrs in enumerate(self.bind.getdata()):
            retlst = []
            for arr in arrs:
                if i == xyz:
                    ret = map(lambda x: x.std(), arr)
                else:
                    ret = map(lambda x: x.mean(), arr)
                retlst += [ret]
            retlsts += [retlst]
        retlsts = array(retlsts)
        self.bstd = multiprocess()
        self.bstd.dinput(retlsts)
        return retlsts
        
    def bind_std_arb(self, itvl=0.01, wid=0.1, abcs=0, lgtd=1):
        #self.bindup(width)
        retlsts = [[],[],[]]
        arrlst = self.getdata()
        length = len(arrlst[abcs]) 
        for i in range(length):
            for n in range(3):
                if n == lgtd:
                    retlsts[n] += [std_arb(arrlst[abcs][i],arrlst[lgtd][i], itvl, wid)[1]] if arrlst[n] != None else None
                    #input(std_arb(arrlst[abcs][i],arrlst[lgtd][i], itvl, wid) if arrlst[n] != None else None)
                else:
                    #input(arrlst[abcs][i])
                    #input(arrlst[n][i])
                    retlsts[n] += [ave_arb(arrlst[abcs][i],arrlst[n][i], itvl, wid)[1]] if arrlst[n] != None else None
                #input(retlsts)
        retlsts = array(retlsts)
        self.bstd = multiprocess()
        self.bstd.dinput(retlsts)

    def grad_arb(self, itvl=0.01, wid=0.1, abcs=2, lgtd=1, T=True):
        if self.T != T: self.transpose()
        retlsts = [[],[],[]]
        arrlst = self.getdata()
        length = len(arrlst[abcs]) 
        for i in range(length):
            abarr, lgarr = grad_arb(arrlst[abcs][i], arrlst[lgtd][i], itvl, wid) 
            retlsts[abcs] += [abarr]
            retlsts[lgtd] += [lgarr]
            retlsts[3-abcs-lgtd] += [arrlst[3-abcs-lgtd][i][0]*ones(len(abarr))]  if arrlst[3-abcs-lgtd] != None else [None]
        self.grad = multiprocess()
        self.grad.T = self.T
        self.grad.dinput(retlsts)
    def gnufit(self, function, fitparalst, stnum=None, ennum=None, itvl=1, abcs=2, lgtd=1, T=False):
        if self.T != T: self.transpose()
        retlsts = [[],[],[]]
        arrlst = self.getdata()
        length = len(arrlst[abcs]) 
        tmplst = []
        for i in range(length):
            tmp = processdata(arrlst[abcs][i], arrlst[lgtd][i])
            tmp.gnufit(function, fitparalst, stnum, ennum, itvl)
            abarr, lgarr, noval = tmp.gnu.getdata()
            tmplst += [tmp.gnu.fitpara]
            retlsts[abcs] += [abarr]
            retlsts[lgtd] += [lgarr]
            retlsts[3-abcs-lgtd] += [arrlst[3-abcs-lgtd][i][0]*ones(len(abarr))] if arrlst[3-abcs-lgtd] != None else [None]
        self.gnu = multiprocess()
        self.gnu.T = self.T
        self.gnu.dinput(retlsts)
        self.gnu.fitpara = tmplst

    def polyfit(self, M=8, stnum=None, ennum=None, itvl=1, abcs=2, lgtd=1, T = False):
        if self.T != T: self.transpose()
        retlsts = [[],[],[]]
        arrlst = self.getdata()
        length = len(arrlst[abcs]) 
        sen = [stnum, ennum, itvl]
        for i in range(length):
            if stnum == None:
                sen[0] = arrlst[abcs][i][0]    
            if ennum == None:
                sen[1] = arrlst[abcs][i][-1]    
            abarr, lgarr = pfit(arrlst[abcs][i], arrlst[lgtd][i], M, sen) 
            retlsts[abcs] += [abarr]
            retlsts[lgtd] += [lgarr]
            retlsts[3-abcs-lgtd] += [arrlst[3-abcs-lgtd][i][0]*ones(len(abarr))] if arrlst[3-abcs-lgtd] != None else [None]
        self.pfit = multiprocess()
        self.pfit.T = self.T
        self.pfit.dinput(retlsts)

    def bind_mean(self, width):
        self.bindup(width)
        retlsts = []
        for arrs in self.bind.getdata():
            retlst = []
            for arr in arrs:
                ret = map(lambda x: x.mean(), arr)
                retlst += [ret]
            retlsts += [retlst]
        retlsts = array(retlsts)
        self.bmean = multiprocess()
        self.bmean.dinput(retlsts)
        return retlsts

    def gradient( self, width, retnum=None, abcs=0, lgtd=1):
        num = self.bindup(width, retnum=True)
        if num == 1:
            raise ValueError, "Arg 'width' is wider than the data interval of 'abcs'."
        arrs = self.bind.getdata()
        xarrs = arrs[abcs]
        yarrs = arrs[lgtd]
        remarrs = arrs[3-(abcs+lgtd)]
        arrs = map(lambda x:array(map(lambda y: median(y)*ones(len(xarrs)), x)), arrs)
        retx = []
        rety = []
        ret_remain = []
        for n in range(len(xarrs)):
            sumx = sum(xarrs[n], axis=1)
            sumy = sum(yarrs[n], axis=1)
            sumxy = sum(xarrs[n]*yarrs[n], axis=1)
            sumxx = sum(xarrs[n]*xarrs[n], axis=1)
            retarr = (( num * sumxy) - sumx * sumy ) / ( num * sumxx  - sumx ** 2 )
        
            retx += [mean(xarrs[n], axis=1)]
            rety += [retarr]
            ret_remain += [mean(remarrs[n], axis=1)]
        arrs[abcs] = array(retx)
        arrs[lgtd] = array(rety)
        arrs[3-(abcs+lgtd)] = array(ret_remain)
        
        self.grad = multiprocess()
        self.grad.dinput(arrs)
            
        if retnum:
            return num
        else:
            return arrs[abcs], arrs[lgtd]

    def loaddata(self, path):
        x,y,z = self.load.loadprofdat(path)
        self.dinput([x,y,z])

    def loaddata_wg(self, path):
        x,y,z = self.load.loadprofdat_wg(path)
        self.dinput([x,y,z])

    def columnview(self, abcs=0, lgtd=1):
        if self.T == False:
            self.transpose()
        arrs = self.getdata()
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

    def view(self, layout="simple", abcs=0,lgtd=1, T=True, sepnum=None, dirname="tmpdir", filename="tmp", device="pdf", dump=False, hgrid=1, vgrid=1):
        self.hist.input()
        layoutdic = {"simple" : self.grace.simplelayout,
                          "column" : self.grace.columnlayout,
                          "dual" : self.grace.duallayout,
                          "triple"   : self.grace.triplelayout,
                          "quad"   : self.grace.quadlayout,
                          "hepta"   : self.grace.heptalayout,
                          "octo"   : self.grace.octolayout,
                          "octo2"   : self.grace.octolayout2,
                          "penta"   : self.grace.pentalayout,
                          }
        if self.T != T:
            self.transpose()

        arrs = self.getdata()

        sepnum = sepnum if sepnum != None else len(arrs[abcs])
        arrs[abcs] = lstsplit(arrs[abcs], sepnum) if None != arrs[abcs] else None
        arrs[lgtd] = lstsplit(arrs[lgtd], sepnum) if None != arrs[lgtd] else None
        arrs[3-abcs-lgtd] = lstsplit(arrs[3-abcs-lgtd], sepnum) if None != arrs[3-abcs-lgtd] else None
        err = lstsplit(self.err, sepnum) if None != self.err else None
        plotnumlim = 1
        snumlim_tmp = sepnum if type(sepnum) == int else iter(sepnum)
        gnumlim = len(arrs[abcs])
        if dump:
            dirpath =  fcnt(self.dumppath+"/"+dirname)       
            os.mkdir(dirpath)
        plotnum = 0
        snum = 0
        gnum = 0
        fnames = ""
#        while plotnum < plotnumlim:
        if layout == "column":
            layoutdic[layout](gnumlim, hgrid=hgrid, vgrid=vgrid)
        else:
            layoutdic[layout](hgrid=hgrid, vgrid=vgrid)
        while gnum < gnumlim: 
        
            snumlim = snumlim_tmp if type(sepnum) == int else snumlim_tmp.next()
            while snum < snumlim:
                if self.err == None:
                    self.grace.set_xydata(arrs[abcs][gnum][snum], arrs[lgtd][gnum][snum], gnum=gnum, snum=snum+self.grace.inisnum)
                else:
                    self.grace.set_xydy(arrs[abcs][gnum][snum], arrs[lgtd][gnum][snum], err[gnum][snum], gnum=gnum, snum=snum+self.grace.inisnum)

                self.grace.prop.snum_check(gnum,snum)
                if self.grace.prop.gdiclst[gnum]["snum"][snum]["legend"] != None:
                    self.grace.set_leg(self.grace.prop.gdiclst[gnum]["snum"][snum]["legend"], gnum, snum, loc=self.grace.prop.gdiclst[gnum]["legloc"])
                else:
                    pass
                snum += 1
            snum = 0
            if self.grace.prop.gdiclst[gnum]["lim"] != None:
                xmin, xmax, ymin, ymax, tnum = self.grace.prop.gdiclst[gnum]["lim"]
                self.grace.set_lim(xmin,xmax,ymin,ymax,gnum, tnum)
            else:
                self.grace.set_autoscale(arrs[abcs][gnum][snum], arrs[lgtd][gnum][snum], gnum=gnum)
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
            
    def tevo(self, layout="simple", abcs=0,lgtd=1, T=False, sepnum=None, dirname="tmpdir", filename="tmp", device="pdf", hgrid=1, vgrid=1):
        self.hist.input()
        layoutdic = {
                          "simple" : self.grace.simplelayout,
                          "column" : self.grace.columnlayout,
                          "dual"   : self.grace.duallayout,
                          "triple"   : self.grace.triplelayout,
                          "quad"   : self.grace.quadlayout,
                          "hepta"   : self.grace.heptalayout,
                          "octo"   : self.grace.octolayout,
                          "octo2"   : self.grace.octolayout2,
                          "penta"   : self.grace.pentalayout,
                          }
        if self.T != T:
            self.transpose()
        arrs = self.getdata()
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
            else:
                layoutdic[layout](hgrid=hgrid, vgrid=vgrid)
            while gnum < gnumlim: 
                while snum < snumlim:
                    self.grace.set_xydata(arrs[abcs][plotnum], arrs[lgtd][plotnum], gnum=gnum, snum=snum)
                    self.grace.prop.snum_check(gnum,snum)
                    if self.grace.prop.gdiclst[gnum]["snum"][snum]["legend"] != None:
                        self.grace.set_leg(self.grace.prop.gdiclst[gnum]["snum"][snum]["legend"], gnum, snum, loc=self.grace.prop.gdiclst[gnum]["legloc"])
                    else:
                        pass
                    snum += 1
                snum = 0
                if self.grace.prop.gdiclst[gnum]["lim"] != None:
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
            self.grace.initialize()
            plotnum += 1

    def boxview(self, abcs=0, lgtd=1):
        if self.T == False:
            self.transpose()
        arrs = self.getdata()
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


class comparison(graphhandler):
    def __init__(self, datlst=None):
        self.datlst = datlst
        self.grace = gracemanage()
        self.dumppath = "."
        self.hist = method_history(self)

    def set_data(self, datlst=None):
        self.datlst = datlst
    def T_align(self,tof = True):
        self.hist.input()
        map(lambda x: x.transpose() if x.T != tof else None, self.datlst)

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

            a_arrs = a.getdata()
            b_arrs = b.getdata()
            
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
            tmp = multiprocess()
            tmp.T = True
            tmp.dinput(array(retlst))
            retlsts += [tmp]
        self.sbt = comparison(retlsts)
        print "processed data is inputed into 'sbt' instance."

      
    def view(self, layout="simple", abcs=0,lgtd=1, transpose=False, T=False, sepnum=1, dirname="tmpdir", filename="tmp", device="pdf", hgrid=1, vgrid=1, glim=None):
        self.hist.input()
        layoutdic = {"simple" : self.grace.simplelayout,
                          "column" : self.grace.columnlayout,
                          "column4" : self.grace.columnlayout_4grid,
                          "dual"   : self.grace.duallayout,
                          "triple"   : self.grace.triplelayout,
                          "quad"   : self.grace.quadlayout,
                          "hepta"   : self.grace.heptalayout,
                          "octo"   : self.grace.octolayout,
                          "octo2"   : self.grace.octolayout2,
                          "penta"   : self.grace.pentalayout,
                          }
        self.T_align(T)
        arrs = []
        for dcls in self.datlst:
            arrs += [dcls.getdata()]
                
        arrs = lstsplit(arrs, sepnum)
        plotnumlim = 1
        #plotnumlim = len(arrs[0][0][abcs])
        snumlim = sepnum 
        gnumlim = len(arrs)
        dirpath =  fcnt(self.dumppath+"/"+dirname)       
        os.mkdir(dirpath)
        plotnum = 0
        snum = 0
        snum2 = 0
        gnum = 0
        cnt = it.cycle(self.datlst)
        fnames = ""
        while plotnum < plotnumlim:
            snumlim_tmp = sepnum if type(sepnum) != list else iter(sepnum) 
            if layout == "column" or layout == "column4":
                if glim != None:
                    layoutdic[layout](glim, hgrid=hgrid, vgrid=vgrid)
                else:
                    layoutdic[layout](gnumlim, hgrid=hgrid, vgrid=vgrid)
            else:
                layoutdic[layout]()
            while gnum < gnumlim: 
                while snum < snumlim:
                    snum2lim = len(arrs[gnum][snum][abcs])
                    while snum2 < snum2lim:
                        if len(arrs[gnum][snum]) != 4:
                            self.grace.set_xydata(arrs[gnum][snum][abcs][snum2], arrs[gnum][snum][lgtd][snum2], gnum=gnum)
                        else:
                            self.grace.set_xydy(arrs[gnum][snum][abcs][snum2], arrs[gnum][snum][lgtd][snum2], arrs[gnum][snum][3][snum2], gnum=gnum, snum=snum)
                        snum2 += 1
                    snum2 = 0
                    snum += 1
                snum = 0
                if len(self.grace.prop.gdiclst): self.grace.set_graphitems()
                #if self.grace.prop.gdiclst[gnum]["lim"] == None:
                #    self.grace.set_autoscale(arrs[gnum][snum][abcs][snum2], arrs[gnum][snum][lgtd][snum2], gnum=gnum)
                gnum += 1
            gnum = 0
            fnames += " "  + fcnt(dirpath, filename,device)
            self.grace.set_ornament() 
            #self.grace.dumpfig(fcnt(dirpath, filename,device))
            self.grace.open_grace()
            self.grace.initialize()
            plotnum += 1

    def tevo(self, layout="simple", abcs=0,lgtd=1, transpose=False, sepnum=1, dirname="tmpdir", filename="tmp", device="pdf", hgrid=1, vgrid=1):
        self.hist.input()
        layoutdic = {"simple" : self.grace.simplelayout,
                          "column" : self.grace.columnlayout,
                          "dual"   : self.grace.duallayout,
                          "triple"   : self.grace.triplelayout,
                          "quad"   : self.grace.quadlayout,
                          "hepta"   : self.grace.heptalayout,
                          "octo"   : self.grace.octolayout,
                          "octo2"   : self.grace.octolayout2,
                          "penta"   : self.grace.pentalayout,
                          }
        self.grace.prop.plot_init()
        self.T_align(False)
        arrs = []
        for dcls in self.datlst:
            if  transpose:
                dcls.transpose()
            arrs += [dcls.getdata()]
                
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
                    if len(arrs[gnum][snum]) != 4:
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
            self.grace.initialize()
            plotnum += 1

#    def show_graph(self):
#        self.grace.open_grace()        
#        self.grace.initialize()
        
    def dump_pickle(self, picklepath=None):
        self.hist.input()
        if picklepath == None: picklepath = self.picklepath
        o = open(picklepath, "w")
        pickle.dump(self, o)
        o.close()

    def load_pickle(self, picklepath=None):
        if picklepath == None: picklepath = self.picklepath
        o = open(picklepath)
        tmp = pickle.load(o)
        self.hist.hlst = tmp.hist.hlst
        self.datlst = tmp.datlst
        self.grace.prop.gdiclst = tmp.grace.prop.gdiclst
        self.grace.prop.decolst = tmp.grace.prop.decolst
        self.grace.prop.mkall = tmp.grace.prop.mkall
        o.close()
        
    def playback(self, index=0):
        self.hist.execute(index=index)
#from calc import *
#from pylab import *
#ion()
#[x,y],[xn,yn] = calc("ilab", 86543, int=0.1, ave=2)
#dat=1000
#x = pi*arange(dat)/180
#y = sin(pi*arange(dat)/180.)
#c = cos(x)
#a = processdata(x,y)
#wid = 16
#a.punch_out([[0,2],[3,8]])
#d=[a,a,a]
#s=processdata(dlst=d)
#f,g,h=s.get_data("multi")
#for e in f:
#    input(e)
#    plot(e);draw()
#input()
#a.punch_out([[0,2],[3,8]])
##num = a.punch_out([[10,20],[30,40]],retnum=True)
##print a.punch_out([[21,22],[23,24]])
##plot(x,y)
##input()
#num=20
#xlabel(r"$\theta$ [rad]", fontsize=20)
##ylabel(r"sin($\theta$)", fontsize=20)
#per = num/float(dat)
#xdata,ydata,gg = a.get_data("raw")
#xgrad,ygrad,gg = a.get_data("pout")
##input(xdata)
##input(ygrad)
#suptitle(r"Thie gradient calculated using %s data(a ratio to all data is %.2f)included %s rad" %(num,per,wid), fontsize=15)
#plot(xdata, ydata,"b",label=r"sin($\theta$)", linewidth=3)
#plot(xdata, c,"g", label=r"cos($\theta$)", linewidth=3)
#plot(xgrad, ygrad,"r",label=r"grad sin($\theta$)", linewidth=3)
#legend()
#show();input()



#[[x,y],[ss,dd]]=calc("pc", 80000,int=0.1,ave=0.1)
#>>a=processdata(x,y)
#a.punch_out([[1,5],[7,9]])
#a.gradient(5)
#input(a.grad.getdata())
#a.bind_std(3)
##print a.pout.getdata()
##print a.bstd.getdata()
#d=multiprocess([a,a,a,a,a])
#d.yname=["one","two", "three","four","five"]
#d.tevo()
#print d.x
#d.transpose()
#input()
#print d.x
#a.view()
#a=multiprocess()
#a.loaddata("testdata4")
#a.tevo(abcs=1,lgtd=2, xmin=80.,xmax=140,ymin=0.,ymax=6.)
#input()
#a.transpose()
#a.gradient(1, abcs=0,lgtd=2)
#a.grad.transpose()
#a.transpose()
#a.grad.tevo(abcs=1,lgtd=2, xmin=80.,xmax=140,ymin=-1.,ymax=1input(dcls.x)
