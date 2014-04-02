import Gnuplot
from subprocess import *
from datfilemanage import *
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
    
class gracemanage():
    def __init__(self,):
        self.x = None
        self.y = None
        self.xname = None
        self.yname = None
        self.xr = None
        self.yr = None
        self.size = None
        self.pagesize = (848,808)
        self.gdic = {}
        self.prop = self.graceprop()
        self.grace_init()

    def grace_init(self,):
        self.line = """
# Grace project file
#
@page size 848, 608
@page scroll 10%
@page inout 10%
@link page on
@map font 0 to "Times-Roman", "Times-Roman"
@map font 1 to "Times-Italic", "Times-Italic"
@map font 2 to "Times-Bold", "Times-Bold"
@map font 3 to "Times-BoldItalic", "Times-BoldItalic"
@map font 4 to "Helvetica", "Helvetica"
@map font 5 to "Helvetica-Oblique", "Helvetica-Oblique"
@map font 6 to "Helvetica-Bold", "Helvetica-Bold"
@map font 7 to "Helvetica-BoldOblique", "Helvetica-BoldOblique"
@map font 8 to "Courier", "Courier"
@map font 9 to "Courier-Oblique", "Courier-Oblique"
@map font 10 to "Courier-Bold", "Courier-Bold"
@map font 11 to "Courier-BoldOblique", "Courier-BoldOblique"
@map font 12 to "Symbol", "Symbol"
@map font 13 to "ZapfDingbats", "ZapfDingbats"
@map color 0 to (255, 255, 255), "white"
@map color 1 to (0, 0, 0), "black"
@map color 2 to (255, 0, 0), "red"
@map color 3 to (0, 255, 0), "green"
@map color 4 to (0, 0, 255), "blue"
@map color 5 to (255, 255, 0), "yellow"
@map color 6 to (188, 143, 143), "brown"
@map color 7 to (220, 220, 220), "grey"
@map color 8 to (148, 0, 211), "violet"
@map color 9 to (0, 255, 255), "cyan"
@map color 10 to (255, 0, 255), "magenta"
@map color 11 to (255, 165, 0), "orange"
@map color 12 to (114, 33, 188), "indigo"
@map color 13 to (103, 7, 72), "maroon"
@map color 14 to (64, 224, 208), "turquoise"
@map color 15 to (0, 139, 0), "green4"
@reference date 0
@date wrap off
@date wrap year 1950
@default linewidth 1.5
@default linestyle 1
@default color 1
@default pattern 1
@default font 6
@default char size 1.000000
@default symbol size 2.000000
@default sformat "%.8g"
@background color 0
@page background fill on
@timestamp off
@timestamp 0.03, 0.03
@timestamp color 1
@timestamp rot 0
@timestamp font 0
@timestamp char size 1.000000
@g0 on
@g0 hidden false
@g0 type XY
@g0 stacked false
@g0 bar hgap 0.000000
@g0 fixedpoint off
@g0 fixedpoint type 0
@g0 fixedpoint xy 0.000000, 0.000000
@g0 fixedpoint format general general
@g0 fixedpoint prec 6, 6
&
"""
#@with g0
#@    world 0, -100, 90, 449258950
#@    stack world 0, 0, 0, 0
#@    znorm 1
#@    view 0.167352, 0.525000, 0.671967, 0.712500
#@    title ""
#@    title font 6
#@    title size 1.500000
#@    title color 1
#@    subtitle ""
#@    subtitle font 6
#@    subtitle size 1.000000
#@    subtitle color 1
#@    xaxes scale Normal
#@    yaxes scale Normal
#@    xaxes invert off
#@    yaxes invert off
#@    xaxis  on
#@    xaxis  type zero false
#@    xaxis  offset 0.000000 , 0.000000
#@    xaxis  bar on
#@    xaxis  bar color 1
#@    xaxis  bar linestyle 1
#@    xaxis  bar linewidth 2.0
#@    xaxis  label ""
#@    xaxis  label layout para
#@    xaxis  label place auto
#@    xaxis  label char size 1.300000
#@    xaxis  label font 6
#@    xaxis  label color 1
#@    xaxis  label place normal
#@    xaxis  tick on
#@    xaxis  tick major 5
#@    xaxis  tick minor ticks 4
#@    xaxis  tick default 6
#@    xaxis  tick place rounded true
#@    xaxis  tick in
#@    xaxis  tick major size 1.000000
#@    xaxis  tick major color 1
#@    xaxis  tick major linewidth 2.0
#@    xaxis  tick major linestyle 1
#@    xaxis  tick major grid off
#@    xaxis  tick minor color 1
#@    xaxis  tick minor linewidth 2.0
#@    xaxis  tick minor linestyle 1
#@    xaxis  tick minor grid off
#@    xaxis  tick minor size 0.500000
#@    xaxis  ticklabel off
#@    xaxis  ticklabel format general
#@    xaxis  ticklabel prec 5
#@    xaxis  ticklabel formula ""
#@    xaxis  ticklabel append ""
#@    xaxis  ticklabel prepend ""
#@    xaxis  ticklabel angle 0
#@    xaxis  ticklabel skip 0
#@    xaxis  ticklabel stagger 0
#@    xaxis  ticklabel place normal
#@    xaxis  ticklabel offset auto
#@    xaxis  ticklabel offset 0.000000 , 0.010000
#@    xaxis  ticklabel start type auto
#@    xaxis  ticklabel start 0.000000
#@    xaxis  ticklabel stop type auto
#@    xaxis  ticklabel stop 0.000000
#@    xaxis  ticklabel char size 1.300000
#@    xaxis  ticklabel font 6
#@    xaxis  ticklabel color 1
#@    xaxis  tick place both
#@    xaxis  tick spec type none
#@    yaxis  on
#@    yaxis  type zero false
#@    yaxis  offset 0.000000 , 0.000000
#@    yaxis  bar on
#@    yaxis  bar color 1
#@    yaxis  bar linestyle 1
#@    yaxis  bar linewidth 2.0
#@    yaxis  label "(V)"
#@    yaxis  label layout para
#@    yaxis  label place auto
#@    yaxis  label char size 1.000000
#@    yaxis  label font 6
#@    yaxis  label color 1
#@    yaxis  label place normal
#@    yaxis  tick on
#@    yaxis  tick major 1000000000
#@    yaxis  tick minor ticks 4
#@    yaxis  tick default 6
#@    yaxis  tick place rounded true
#@    yaxis  tick in
#@    yaxis  tick major size 1.000000
#@    yaxis  tick major color 1
#@    yaxis  tick major linewidth 2.0
#@    yaxis  tick major linestyle 1
#@    yaxis  tick major grid off
#@    yaxis  tick minor color 1
#@    yaxis  tick minor linewidth 2.0
#@    yaxis  tick minor linestyle 1
#@    yaxis  tick minor grid off
#@    yaxis  tick minor size 0.500000
#@    yaxis  ticklabel on
#@    yaxis  ticklabel format general
#@    yaxis  ticklabel prec 5
#@    yaxis  ticklabel formula ""
#@    yaxis  ticklabel append ""
#@    yaxis  ticklabel prepend ""
#@    yaxis  ticklabel angle 0
#@    yaxis  ticklabel skip 0
#@    yaxis  ticklabel stagger 0
#@    yaxis  ticklabel place normal
#@    yaxis  ticklabel offset auto
#@    yaxis  ticklabel offset 0.000000 , 0.010000
#@    yaxis  ticklabel start type auto
#@    yaxis  ticklabel start 0.000000
#@    yaxis  ticklabel stop type auto
#@    yaxis  ticklabel stop 0.000000
#@    yaxis  ticklabel char size 1.000000
#@    yaxis  ticklabel font 6
#@    yaxis  ticklabel color 1
#@    yaxis  tick place both
#@    yaxis  tick spec type none
#@    altxaxis  off
#@    altyaxis  off
#@    legend on
#@    legend loctype view
#@    legend 0.192946868952, 0.694
#@    legend box color 1
#@    legend box pattern 1
#@    legend box linewidth 1.5
#@    legend box linestyle 0
#@    legend box fill color 0
#@    legend box fill pattern 0
#@    legend font 6
#@    legend char size 1.000000
#@    legend color 1
#@    legend length 0
#@    legend vgap 0
#@    legend hgap 0
#@    legend invert false
#@    frame type 0
#@    frame linestyle 0
#@    frame linewidth 1.5
#@    frame color 1
#@    frame pattern 1
#@    frame background color 0
#@    frame background pattern 0
#@    s0 hidden false
#@    s0 type xy
#@    s0 symbol 0
#@    s0 symbol size 2.000000
#@    s0 symbol color 2
#@    s0 symbol pattern 1
#@    s0 symbol fill color 2
#@    s0 symbol fill pattern 0
#@    s0 symbol linewidth 1.5
#@    s0 symbol linestyle 1
#@    s0 symbol char 65
#@    s0 symbol char font 6
#@    s0 symbol skip 0
#@    s0 line type 1
#@    s0 line linestyle 1
#@    s0 line linewidth 1.5
#@    s0 line color 2
#@    s0 line pattern 1
#@    s0 baseline type 0
#@    s0 baseline off
#@    s0 dropline off
#@    s0 fill type 0
#@    s0 fill rule 0
#@    s0 fill color 1
#@    s0 fill pattern 1
#@    s0 avalue off
#@    s0 avalue type 2
#@    s0 avalue char size 1.000000
#@    s0 avalue font 6
#@    s0 avalue color 1
#@    s0 avalue rot 0
#@    s0 avalue format general
#@    s0 avalue prec 3
#@    s0 avalue prepend ""
#@    s0 avalue append ""
#@    s0 avalue offset 0.000000 , 0.000000
#@    s0 errorbar on
#@    s0 errorbar place both
#@    s0 errorbar color 2
#@    s0 errorbar pattern 1
#@    s0 errorbar size 1.000000
#@    s0 errorbar linewidth 1.5
#@    s0 errorbar linestyle 1
#@    s0 errorbar riser linewidth 1.5
#@    s0 errorbar riser linestyle 1
#@    s0 errorbar riser clip off
#@    s0 errorbar riser clip length 0.100000
#@    s0 comment "stdin"
#@    s0 legend  "V_electrode_LaB6"
#&
#\n
#        """
        #self.line += "@page size 848, 999\n"
        #self.line += "@with g0\n"
        #self.line += "@page size %s, %s\n" %self.pagesize
        #self.line += "@world 20088888888000, -3806991100, 40, 449258950\n"
        #self.line += "@view 0.2, 0.2, 0.8, 0.8\n"
        #self.set_xlabel("ahaha")
        #self.set_xlabel("shsh",1)
        #self.set_ylabel("uyhhi")
        #self.set_leg("ohho",0,0)
        #self.multigraph(1, 1, hpad = 0, vpad=0, hmargin=0.1,vmargin=0.1)
        #print self.line

    def graph_prop(self):
        self.line += """
@    title ""
@    title font 6
@    title size 1.500000
@    title color 1
@    subtitle ""
@    subtitle font 6
@    subtitle size 1.000000
@    subtitle color 1
@    xaxes scale Normal
@    yaxes scale Normal
@    xaxes invert off
@    yaxes invert off
@    xaxis  on
@    xaxis  type zero false
@    xaxis  bar on
@    xaxis  bar color 1
@    xaxis  bar linestyle 1
@    xaxis  bar linewidth 2.0
@    xaxis  tick on
@    xaxis  tick major 3
@    xaxis  tick in
@    xaxis  tick major size 1.000000
@    xaxis  tick major color 1
@    xaxis  tick major linewidth 2.0
@    xaxis  tick major linestyle 1
@    xaxis  tick major grid off
@    xaxis  tick minor size 0
@    xaxis  ticklabel on
@    xaxis  ticklabel char size 1.300000
@    xaxis  ticklabel font 6
@    xaxis  ticklabel color 1
@    xaxis  tick place both
@    xaxis  tick spec type none
@    yaxis  on
@    yaxis  type zero false
@    yaxis  offset 0.000000 , 0.000000
@    yaxis  bar on
@    yaxis  bar color 1
@    yaxis  bar linestyle 1
@    yaxis  bar linewidth 2.0
@    yaxis  label layout para
@    yaxis  label place auto
@    yaxis  label char size 1.000000
@    yaxis  label font 6
@    yaxis  label color 1
@    yaxis  label place normal
@    yaxis  tick on
@    yaxis  tick in
@    yaxis  tick major size 1.000000
@    yaxis  tick major color 1
@    yaxis  tick major linewidth 2.0
@    yaxis  tick major linestyle 1
@    yaxis  tick major grid off
@    yaxis  tick minor size 0
@    yaxis  ticklabel on
@    yaxis  ticklabel char size 1.000000
@    yaxis  ticklabel font 6
@    yaxis  ticklabel color 1
@    yaxis  tick place both
@    yaxis  tick spec type none
        """
    def set_pagesize(self, width, hight):
        self.pagesize=(width,hight) 
        self.line += "@page size %s, %s\n" %self.pagesize
    def set_xtick(self, itvl, size=2, width=2, gnum=0):
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    xaxis  tick major %s\n" %itvl
        self.line += "@    xaxis  tick major size %s\n" %size
        self.line += "@    xaxis  tick major linewidth %s\n" %width
        self.prop.xtick_input(itvl, size, width, gnum)
        
    def set_ytick(self, itvl, size=2, width=2, gnum=0):
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    yaxis  tick major %s\n" %itvl
        self.line += "@    yaxis  tick major size %s\n" %size
        self.line += "@    yaxis  tick major linewidth %s\n" %width
        self.prop.xtick_input(itvl, size, width, gnum)

    def multigraph(self, row, col, auto=True, wid=0.1, hight=0.1, hmargin=0.1, vmargin=0.05, hpad=0.0, vpad=0.0):
            hd = 1. / col 
            vd = 1. / row 
            if auto:
                wid = hd
                hight = vd
            gnum = 0
            for r in arange(row)+1:
                vmin = (vd * r - hight + vpad) * (1 - 2*vmargin) + vmargin
                vmax = (vd * r + - vpad) * (1 - 2*vmargin) + vmargin
                for c in arange(col)+1:
                    hmin = (hd * c - wid + hpad) * (1 - 2*hmargin) + hmargin
                    hmax = (hd * c - hpad) * (1 - 2*hmargin) + hmargin
                    self.line += "@g%s on\n" %(gnum)
                    self.line += "@with g%s\n" %(gnum)
                    self.line += "@    view %s,%s,%s,%s\n" %(hmin, vmin, hmax, vmax)
                    self.prop.g_add()
                    gnum += 1

    def set_leg(self, leg, gnum, snum):
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    s%s legend\"%s\"\n" %(snum, leg)
        self.prop.leg_input(leg, gnum, snum)

    def set_lim(self,xmin, xmax, ymin, ymax, gnum=0):
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    world %s, %s, %s, %s\n" %(xmin, ymin, xmax, ymax)
        self.prop.lim_input(xmin, xmax, ymin, ymax, gnum)
        
    def set_xlabel(self,name, gnum=0):
        self.xname = name
        self.line += "@with g%s\n" %gnum
        #self.line += "@    yaxis  on\n"
        self.line += "@    xaxis  label \"%s\"\n" %name
    
    def set_ylabel(self,name, gnum=0):
        self.yname = name
        self.line += "@with g%s\n" %gnum
        #self.line += "@    yaxis  on\n"
        self.line += "@    yaxis  label \"%s\"\n" %name

    def gcnt(self, gnum):
        gnum = str(gnum)
        if gnum in self.gdic:
            self.gdic[gnum] += 1
        else:
            self.gdic.update({gnum:0})

        return self.gdic[gnum]

        
    def set_xydata(self, x, y, gnum=0):
        self.prop.gnum_check(gnum)
        self.line += "@target g%s.S%s\n" %(gnum, self.gcnt(gnum))
        self.line += "@type xy\n"
        self.line += "".join(map(lambda a,b: "%s %s\n" %(a,b), x,y))
        self.prop.s_add(gnum)
        

        

    def open_grace(self, auto=None):

        p=Popen(["xmgrace", "-free", "none", "-pipe"], stdin=PIPE) 
        #p=Popen(["xmgrace", "-free", "-autoscale", "none", "-pipe"], stdin=PIPE) 
        p.communicate(self.line)
        p.stdin.close()

    def autoscale(self, arr, margin=0.1):
        r = 1. / arr.ptp()
        retmin = (r * arr.min() - margin) / r
        retmax = (r * arr.max() + margin) / r
        return retmin, retmax
        
    def set_autoscale(self, xarr, yarr, gnum=0, margin=0.1):
        xmin,xmax = self.autoscale(xarr, margin)
        ymin,ymax = self.autoscale(yarr, margin)
        self.set_lim(xmin,xmax,ymin,ymax, gnum)
        self.set_xtick(sig_fig(xarr.ptp()/6,1),gnum=gnum)
        self.set_ytick(sig_fig(yarr.ptp()/6,1),gnum=gnum)

    def set_xautoscale(self, xarr, gnum=0, margin=0.1):
        xmin,xmax = self.autoscale(xarr, margin)
        self.set_lim(xmin,xmax,ymin,ymax, gnum)
        self.set_xtick(sig_fig(xarr.ptp()/6,1),gnum=gnum)
    
    class graceprop():
        def __init__(self):
            self.tmpdic = {"snum" : None,
                              "gtype" : "normal",
                              "xtics" : None,
                              "ytics" : None,
                              "xlabel" : None,
                              "ylabel" : None,
                              "lim" : None,
                              "legend" : None,}
            self.g_add() 

        def g_add(self):
            try:
                self.gdiclst += [self.tmpdic]
            except (IndexError, AttributeError):
                self.gdiclst = [self.tmpdic]

        def s_add(self,gnum):
            sdic = {"legend" : None}
            if self.gdiclst[gnum]["snum"] == None:
                self.gdiclst[gnum]["snum"] = [sdic]
            else:
                self.gdiclst[gnum]["snum"] += [sdic]

#        def scnt(self, gnum):
#            gnum = str(gnum)
#            if gnum in self.gdic:
#                self.gdiclst[gnum]["snum"] += 1
#            else:
#                self.gupdate()
#                self.gdiclst.update({gnum:{"snum" : 0}})
#
#            return self.gdiclst[gnum]["snum"]

        def gnum_check(self, gnum):
            try:
                self.gdiclst[gnum]
            except IndexError:
                raise IndexError, "Graph number %s is not defineded." %gnum
        
        def lim_input(self, xmin, xmax, ymin, ymax, gnum):
            self.gnum_check(gnum)
            self.gdiclst[gnum]["lim"] = (xmin, xmax, ymin, ymax)

        def xlabel_input(self, xname, gnum):
            self.gnum_check(gnum)
            self.gdiclst[gnum]["xlabel"] = xname

        def ylabel_input(self, xname, gnum):
            self.gnum_check(gnum)
            self.gdiclst[gnum]["ylabel"] = yname
                
        def leg_input(self, leg, gnum, snum):
            self.gnum_check(gnum)
            self.gdiclst[gnum]["snum"][snum]["legend"] = leg
                
        def xtick_input(self, intvl, size, width, gnum):
            self.gnum_check(gnum)
            self.gdiclst[gnum]["xtick"] = (intvl, size, width, gnum)
            
        def ytick_input(self, intvl, size, width, gnum):
            self.gnum_check(gnum)
            self.gdiclst[gnum]["ytick"] = (intvl, size, width, gnum)

        def show_prop(self, gnum=None):
            self.gnum_check(gnum)
            gdiclst = self.gdiclst if gnum else self.gnumlst[gnum]
            for  gdic in self.gdiclst:
                print "xlabel : %s" %sgdic["xlabel"]
                print "ylabel : %s" %sgdic["ylabel"]
            
             

#from calc import *
#from numpy import *
#from pylab import *
#
#[[x,y],[a,b]] = calc("pc",80000)
#a=gracemanage()
#a.multigraph(2,2)
#a.set_xydata(x,y, gnum=0)
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
