#!/usr/bin/env python
#-*- coding:utf-8 -*-

from grace_layout import *
from grace_aliases import *
from grace_style import *
from grace_prop import *
from numpy import *

from modules.essential_utils.convert_util import *

from tempfile import TemporaryFile
from subprocess import Popen

class grace_util(grace_layout,):
    def __init__(self, pagesize=(848,808)):
        self.prop = grace_prop()
        self.initialize(pagesize)

    def initialize(self, pagesize=(848,808)):
#        self.x = None
#        self.y = None
#        self.xname = None
#        self.yname = None
#        self.xr = None
#        self.yr = None
        self.size = None
        self.gdic = {}
        self.gdic_box = {}
        self.pagesize = pagesize
        self.inisnum = 10
        self.grace_init()

    def grace_init(self,):
        """Initilaize grace_util.

        Description:
            All attributes of this class are initiarized by this method.
            This method also called by constractor.
    
        Argments:
            None
    """
#version は　boxやellipse の背景色表示に必要
        self.line = """
# Grace project file
#
@version 50123
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
"""
#@reference date 0
#@date wrap off
#@date wrap year 1950
#@default linewidth 1.5
#@default linestyle 1
#@default color 1
#@default pattern 1
#@default font 6
#@default char size 1.000000
#@default symbol size 2.000000
#@default sformat "%.8g"
#@background color 0
#@page background fill on
#@timestamp off
#@timestamp 0.03, 0.03
#@timestamp color 1
#@timestamp rot 0
#@timestamp font 0
#@timestamp char size 1.000000
#@g0 on
#@g0 hidden false
#@g0 type XY
#@g0 stacked false
#@g0 bar hgap 0.000000
#@g0 fixedpoint off
#@g0 fixedpoint type 0
#@g0 fixedpoint xy 0.000000, 0.000000
#@g0 fixedpoint format general general
#@g0 fixedpoint prec 6, 6
#&
#"""

    def graph_prop(self):
        self.line += """
@    title ""
@    title size 1.500000
@    title color 1
@    subtitle ""
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
@    xaxis  bar linewidth 4.0
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
@    yaxis  ticklabel color 1
@    yaxis  tick place both
@    yaxis  tick spec type none
        """


    def set_title(self, name, size=1.5):
        """ Set graph title.
            
            Argments
                title -- title name
                size  -- size of title name
        
        """
        self.line += "@    title \"%s\"" %line
        self.line += "@    title size %s" %size

    def set_font(self, fnum):
        """ Set graph global and legend font.
            
            Argments
                fnum  -- The number of font. Correspondence of the number and font name is as follows.

            0  Times-Roman
            1  Times-Italic
            2  Times-Bold
            3  Times-BoldItalic
            4  Helvetica
            5  Helvetica-Oblique
            6  Helvetica-Bold
            7  Helvetica-BoldOblique
            8  Courier
            9  Courier-Oblique
            10  Courier-Bold
            11  Courier-BoldOblique
            12  Symbol
            13  ZapfDingbats
        
        """
        self.line += "@default font %s\n" %fnum
        self.line += "@legend font %s\n" %fnum

    def set_errorbar(self, gnum=0, snum=0, color=1, patn=1, size=1, lwidth=2, lstyle=1, rlwidth=1, rlstyle=1):
        """Setting for errorbar

        Argumants:
            gnum -- Graph number.
            snum -- Symbol number.
            color -- Color number.# You can also set list of color numbar to this arguments. 
            patn -- The number of error bar pattarn. 
            size -- The error bar size. 
            lwidth -- The line width.
            lstyle -- The line style.
            rlwidth -- The errorbar riser line width.
            rlstyle -- The errorbar riser line style.
        """

        self.line += "@with g%s\n" %gnum
        self.line += "@    s%s errorbar on\n" %snum
        self.line += "@    s%s errorbar place both\n" %snum
        self.line += "@    s%s errorbar color %s\n" %(snum, color)
        self.line += "@    s%s errorbar pattern %s\n" %(snum, patn)
        self.line += "@    s%s errorbar size %s\n" %(snum, size)
        self.line += "@    s%s errorbar linewidth %s\n" %(snum, lwidth)
        self.line += "@    s%s errorbar linestyle %s\n" %(snum, lstyle)
        self.line += "@    s%s errorbar riser linewidth %s\n" %(snum, rlwidth)
        self.line += "@    s%s errorbar riser linestyle %s\n" %(snum, rlstyle)
        self.line += "@    s%s errorbar riser clip off\n" %snum 
        self.line += "@    s%s errorbar riser clip length 0.100000\n" %snum
    

    def set_pagesize(self, width=800, hight=1131.37, paper=None, psize=800):
        """Set gage size.

        Arguments:
            width -- The width of pagesize. The unit is pixel.
            hight -- The hight of pagesize. The unit is pixel.
            paper -- if you set 'vl' or 'hl' to paper and set a number to psize,
                     you get the pagesize as follows,
                     
                     vl: width = psize and hight = psize * (2 ** 0.5)
                     vl: width = psize  * (2 ** 0.5) and hight = psize
        """
        if paper == "vl":
            self.pagesize=(int(psize),int(psize * (2 ** 0.5))) 
        elif paper == "hl":
            self.pagesize=(int(psize * (2 ** 0.5)), int(psize)) 
        else:
            self.pagesize=(width,hight) 
        self.line += "@page size %s, %s\n" %self.pagesize

    def set_xaxes(self, scale="Nomal", invert="off", gnum=0):
        if type(scale) == int: scale = ["Normal", "Logarithmic"][scale]
        if type(invert) == int: invert = ["off", "on"][invert]
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    xaxes  scale %s\n" %scale
        self.line += "@    xaxes  invert %s\n" %invert

    def set_yaxes(self, scale="Nomeal", invert="off", gnum=0):
        if type(scale) == int: scale = ["Normal", "Logarithmic"][scale]
        if type(invert) == int: invert = ["off", "on"][invert]
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    yaxes  scale %s\n" %scale
        self.line += "@    yaxes  invert %s\n" %invert

    def set_xaxis(self, itvl, size=2, width=2, gnum=0, minsize=0, minwidth=0, fnum=4, fsnum=1, tl=True):
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    xaxis  tick major %s\n" %itvl
        self.line += "@    xaxis  tick major size %s\n" %size
        self.line += "@    xaxis  tick major linewidth %s\n" %width
        self.line += "@    xaxis  tick minor size %s\n" %minsize
        self.line += "@    xaxis  tick minor linewidth %s\n" %minwidth
        self.line += "@    xaxis  bar linewidth %s\n" %width
        self.line += "@    xaxis  ticklabel font %s\n" %fnum
        self.line += "@    xaxis  label font %s\n" %fnum
        self.line += "@    xaxis  ticklabel char size %s\n" %fsnum
        self.line += "@    xaxis  label char size %s\n" %fsnum
        self.line += "@    xaxis  ticklabel %s\n" %("on" if tl else "off")
        #self.prop.xtick_input(itvl, size, width, gnum)
        
    def set_yaxis(self, itvl, size=2, width=2, gnum=0, minsize=0, minwidth=0, fnum=4, fsnum=1, tl=True):
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    yaxis  tick major %s\n" %itvl
        self.line += "@    yaxis  tick major size %s\n" %size
        self.line += "@    yaxis  tick major linewidth %s\n" %width
        self.line += "@    yaxis  tick minor size %s\n" %minsize
        self.line += "@    yaxis  tick minor linewidth %s\n" %minwidth
        self.line += "@    yaxis  bar linewidth %s\n" %width
        self.line += "@    yaxis  ticklabel font %s\n" %fnum
        self.line += "@    yaxis  label font %s\n" %fnum
        self.line += "@    yaxis  ticklabel char size %s\n" %fsnum
        self.line += "@    yaxis  label char size %s\n" %fsnum
        self.line += "@    yaxis  ticklabel offset 0.000000 , 0.020000\n"
        self.line += "@    yaxis  ticklabel %s\n" %("on" if tl else "off")
        #self.prop.xtick_input(itvl, size, width, gnum)

        
    def unset_graph(self, gnum):
        self.line += "@g%s hidden true\n" %gnum

    def multigraph(self, row, col, auto=True, wid=0.1, hight=0.1, hmargin=0.1, vmargin=0.05, hpad=0.0, vpad=0.0,hoffset=0, voffset=0, hgrid=1, vgrid=1):
            hd = 1. / col 
            vd = 1. / row 
            if auto:
                wid = hd
                hight = vd

            gnum = 0
            ratio = float(self.pagesize[1]) / float(self.pagesize[0])
            for vnum in range(vgrid):
                for hnum in range(hgrid):
                    for r in arange(row)+1:
                        for c in arange(col)+1:
                            hmin = ((hd * c - wid + hpad) * (1 - 2*hmargin) + hmargin + hoffset) * ( 1./ratio if ratio < 1 else 1)
                            hmax = ((hd * c - hpad) * (1 - 2*hmargin) + hmargin + hoffset) * (1./ratio if ratio < 1 else 1)
                            vmin = ((vd * r - hight + vpad) * (1 - 2*vmargin) + vmargin + voffset) * ( ratio if ratio > 1 else 1)
                            vmax = ((vd * r + - vpad) * (1 - 2*vmargin) + vmargin + voffset) * ( ratio if ratio > 1 else 1)
                            hmin = float(hnum) / hgrid * (1./ratio if ratio < 1 else 1) + hmin / hgrid
                            hmax = float(hnum) / hgrid * (1./ratio if ratio < 1 else 1) + hmax / hgrid
                            vmin = float(vnum) / vgrid * ( ratio if ratio > 1 else 1) + vmin / vgrid
                            vmax = float(vnum) / vgrid * ( ratio if ratio > 1 else 1) + vmax / vgrid

                            self.line += "@g%s on\n" %(gnum)
                            self.line += "@with g%s\n" %(gnum)
                            self.line += "@    view %s,%s,%s,%s\n" %(hmin, vmin, hmax, vmax)
                            #self.prop.g_add()
                            gnum += 1

    def conv_wratio(self, loc, gnum, xonly=False, yonly=False):
            loc = tuple(loc)
            xmin, xmax, ymin, ymax, tnum = self.prop.gdiclst[gnum]["lim"]
            xd = xmax - xmin
            yd = ymax - ymin
            if type(loc) == tuple:
                loc = list(loc)

            if len(loc) == 4:
                if yonly == False:
                    loc[0] = xd * loc[0] + xmin
                    loc[1] = xd * loc[1] + xmin

                if xonly == False:
                    loc[2] = yd * loc[2] + ymin
                    loc[3] = yd * loc[3] + ymin
            else:
                if yonly == False: loc[0] = xd * loc[0] + xmin
                if xonly == False: loc[1] = yd * loc[1] + ymin
            return tuple(loc)
            
    def set_leg_prop(self, gnum, **kwargs):
        self.line += "@with g%s\n" %(gnum)
        if "loctype" in kwargs:
            self.line += "@    legend loctype %s\n" %kwargs["loctype"]
        if "loc" in kwargs:
            self.line += "@    legend %s\n" %kwargs["loc"]
        if "bcolor" in kwargs:
            self.line += "@    legend box color %s\n" %kwargs["bcolor"]
        if "bptn" in kwargs:
            self.line += "@    legend box pttern %s\n" %kwargs["bptn"]
        if "blwid" in kwargs:
            self.line += "@    legend box linewidth %s\n" %kwargs["blwid"]
        if "blstyle" in kwargs:
            self.line += "@    legend box linestyle %s\n" %kwargs["blstyle"]
        if "bfcolor" in kwargs:
            self.line += "@    legend box fill color %s\n" %kwargs["bfcolor"]
        if "bfptn" in kwargs:
            self.line += "@    legend box fill pattern %s\n" %kwargs["bfptn"]
        if "font" in kwargs:
            self.line += "@    legend font %s\n" %kwargs["font"]
        if "csize" in kwargs:
            self.line += "@    legend char size %s\n" %kwargs["csize"]
        if "color" in kwargs:
            self.line += "@    legend color %s\n" %kwargs["color"]
        if "length" in kwargs:
            self.line += "@    legend length %s\n" %kwargs["length"]
        if "vgap" in kwargs:
            self.line += "@    legend vgap %s\n" %kwargs["vgap"]
        if "hgap" in kwargs:
            self.line += "@    legend hgap %s\n" %kwargs["hgap"]
        if "inv" in kwargs:
            self.line += "@    legend invert %s\n" %kwargs["inv"]

    def set_leg(self, leg, gnum, snum, loc=None, loctype="wratio", xonly=False, yonly=False):
        """
        Set legends for legend name and location. For Other setting for legends,
        use 'set_leg_prop'

        Parameters
        ----------
        leg : legend name in str
        gnum : graph number
        snum : symbol number
        loc : location of legends
        loctype : assign type of legends location
            loctype has three types, 'view', 'world' and 'wratio'.
                - 'view' is assign of location as canvas. min is 0 and max is 1.
                  0 is left(down) and 1 is right(up).
                - 'world' is assign of location as graph which you assign by 'gnum'.
                  You need to set the range of graph before use this method.
                - 'wratio' is assign of location as graph along with avobe. However, min is 0 and max is 1.
                  0 is left(down) and 1 is right(up).
        xonly : This argment is valid when loctype is 'wratio'.
                if True is set, 'wratio' is valid only x-axis.
        yonly : This argment is valid when loctype is 'wratio'.
                if True is set, 'wratio' is valid only y-axis.
        """

        self.line += "@with g%s\n" %(gnum)
        self.line += "@    s%s legend \"%s\"\n" %(snum+self.inisnum, leg)
        if loctype == "wratio":
            if type(loc) == str:
                xmin, xmax, ymin, ymax, tnum = self.prop.gdiclst[gnum]["lim"]
                xd = xmax - xmin
                yd = ymax - ymin
                if loc == "center":
                    loc = self.conv_wratio((0.5, 0.5), gnum, xonly, yonly)
                elif loc == "leftup":
                    loc = self.conv_wratio((0.2, 0.8), gnum, xonly, yonly)
                elif loc == "leftdown":
                    loc = self.conv_wratio((0.2, 0.2), gnum, xonly, yonly)
                elif loc == "rightup":
                    loc = self.conv_wratio((0.8, 0.8), gnum, xonly, yonly)
                elif loc == "rightdown":
                    loc = self.conv_wratio((0.8, 0.2), gnum, xonly, yonly)
                else:
                    raise ValueError, "Wrong location alias \"%s\" inputed. Now support alias name is \n\"center\"\n\"leftup\"\n\"leftdown\"\n\"rightup\"\n\"rightup\"\n\"rightdown\"." %loc
            else:
                loc = self.conv_wratio(loc, gnum, xonly, yonly)
            loctype = "world"
            self.line += "@    legend loctype %s\n" %loctype
            self.line += "@    legend %s, %s\n" %loc
        #self.prop.leg_input(leg, gnum, snum)

    def set_lim(self, xmin, xmax, ymin, ymax, gnum=0, tnum=6):
        xmin, xmax, ymin, ymax = map(lambda x: float(x),(xmin, xmax, ymin, ymax))
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    world %s, %s, %s, %s\n" %(xmin, ymin, xmax, ymax)
        #self.prop.lim_input(xmin, xmax, ymin, ymax, gnum)
        self.set_xtickitvl(sig_fig((xmax - xmin)/tnum,1), gnum=gnum)
        self.set_ytickitvl(sig_fig((ymax - ymin)/tnum,1), gnum=gnum)

    def set_xlim(self, xmin, xmax, gnum=0, tnum=6):
        xmin, xmax = map(lambda x: float(x),(xmin, xmax))
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    world xmin %s\n" %(xmin)
        self.line += "@    world xmax %s\n" %(xmax)
        #self.prop.lim_input(xmin, xmax, ymin, ymax, gnum)
        self.set_xtickitvl(sig_fig((xmax - xmin)/tnum,1), gnum=gnum)

    def set_ylim(self, ymin, ymax, gnum=0, tnum=6):
        ymin, ymax = map(lambda x: float(x),(ymin, ymax))
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    world ymin %s\n" %(ymin)
        self.line += "@    world ymax %s\n" %(ymax)
        #self.prop.lim_input(xmin, xmax, ymin, ymax, gnum)
        self.set_ytickitvl(sig_fig((ymay - ymin)/tnum,1), gnum=gnum)

    def set_xlabel(self,name, gnum=0):
        self.xname = name
        self.line += "@with g%s\n" %gnum
        #self.line += "@    yaxis  on\n"
        self.line += "@    xaxis  label \"%s\"\n" %name
    
    def set_xlabel_all(self,name, gnumlim):
        for gnum in range(gnumlim):
            self.xname = name
            self.line += "@with g%s\n" %gnum
            #self.line += "@    yaxis  on\n"
            self.line += "@    xaxis  label \"%s\"\n" %name
        

    def set_ylabel(self,name, gnum=0):
        self.yname = name
        self.line += "@with g%s\n" %gnum
        #self.line += "@    yaxis  on\n"
        self.line += "@    yaxis  label \"%s\"\n" %name

    def set_ylabel_all(self,name, gnumlim):
        for gnum in range(gnumlim):
            self.yname = name
            self.line += "@with g%s\n" %gnum
            #self.line += "@    yaxis  on\n"
            self.line += "@    yaxis  label \"%s\"\n" %name

    def gcnt_box(self, gnum):
        gnum = str(gnum)
        if gnum in self.gdic_box:
            self.gdic_box[gnum] += 1 
        else:
            self.gdic_box.update({gnum:0})

        return self.gdic_box[gnum]

    def gcnt(self, gnum):
        gnum = str(gnum)
        if gnum in self.gdic:
            self.gdic[gnum] += 1 
        else:
            self.gdic.update({gnum:self.inisnum})

        return self.gdic[gnum]

        
    def set_xydy(self, x, y, dy, gnum=0, snum=0, ptype="line",):
        #self.prop.gnum_check(gnum)
        x = deepcopy(x)
        y = deepcopy(y)
        dy = deepcopy(dy)
        snum = self.gcnt(gnum)
        self.line += "@with g%s\n" %gnum
        #self.line += "@    s0 legend \"pose1 rmsd\"\n"
        #self.line += "@    s1 legend \"pose1 rmsd\"\n"
        if ptype == "line":
            self.line += "@     s%s symbol size 0\n" %snum
        else:
            self.line += "@     s%s line linestyle 0\n" %snum
            self.line += "@     s%s symbol %s\n" %(snum, snum + 1)
            self.line += "@     s%s symbol size 1\n" %snum

        self.line += "@target g%s.S%s\n" %(gnum, snum)
        self.line += "@type xydy\n"
        x, tmpy = rm_naninf(array(x), array(y))
        dy, y = rm_naninf(array(dy), array(y))
        self.line += "".join(map(lambda a,b,c: "%s %s %s\n" %(a,b,c), array(x),array(y),array(dy)))#arrsがめちゃくちゃになる原因
        return x, y, dy

    def set_xydata(self, x, y, gnum=0, snum=None, ptype="line", box=False):
        #self.prop.gnum_check(gnum)
        x = deepcopy(x)
        y = deepcopy(y)
        if box:
            snum = self.gcnt_box(gnum)
        else:
            snum = self.gcnt(gnum)
#        if snum == None: 
#            if box:
#                snum = self.gcnt_box(gnum)
#            else:
#                snum = self.gcnt(gnum)
        self.line += "@with g%s\n" %gnum
        #self.line += "@    s0 legend \"pose1 rmsd\"\n"
        #self.line += "@    s1 legend \"pose1 rmsd\"\n"
        if ptype == "line":
            self.line += "@     s%s symbol size 0\n" %snum
        else:
            self.line += "@     s%s line linestyle 0\n" %snum
            self.line += "@     s%s symbol %s\n" %(snum, snum + 1)
            self.line += "@     s%s symbol size 1\n" %snum

        self.line += "@target g%s.S%s\n" %(gnum, snum)
        self.line += "@type xy\n"
        x, y = rm_naninf(array(x), array(y))
        self.line += "".join(map(lambda a,b: "%s %s\n" %(a,b), array(x),array(y)))#arrsがめちゃくちゃになる原因
        return snum
        #self.prop.s_add(gnum)
        
    def set_style_line(self, width=1, color=0, lstyle=1, gnum=0, snum=0):
        snum = self.inisnum + snum
        self.line += "@with g%s\n" %gnum
        self.line += "@     s%s line linestyle %s\n" %(snum, lstyle)
        self.line += "@     s%s line linewidth %s\n" %(snum, width)
        self.line += "@     s%s line color %s\n" %(snum, color)

    def set_mk(self, size=1, color=0, mstyle=1, fcolor=None, fptn=1, lwidth=1, lstyle=1, gnum=0, snum=0):
        snum = self.inisnum + snum
        self.line += "@with g%s\n" %gnum
        self.line += "@     s%s symbol %s\n" %(snum, mstyle)
        self.line += "@     s%s symbol size %s\n" %(snum, size)
        self.line += "@     s%s symbol color %s\n" %(snum, color)
        self.line += "@     s%s symbol fill color %s\n" %(snum, fcolor if fcolor != None else color) 
        self.line += "@     s%s symbol fill pattern %s\n" %(snum, fptn) 
        self.line += "@     s%s symbol linewidth %s\n" %(snum, lwidth) 
        self.line += "@     s%s symbol linestyle %s\n" %(snum, lstyle) 

    def dumpfig(self, picpath="gracedump.pdf", hdev="PDF", view=False):
        from subprocess import Popen, PIPE
        #s = TemporaryFile()
        #s.write(self.line)
        #s.seek(0)

        p=Popen(["xmgrace", "-autoscale", "none", "-hdevice", hdev, "-hardcopy", "-printfile", picpath, "-geometry", "%sx%s"%self.pagesize,"-free", "-pipe"], stdin=PIPE) 
        #p=Popen(["xmgrace", "-free", "-autoscale", "none", "-pipe"], stdin=PIPE) 
        p.communicate(self.line)
        #s.close()
        p.stdin.close()
        

    def open_grace(self, auto=None):
        s = TemporaryFile()
        s.write(self.line)
        s.seek(0)
        #cmd = "xmgrace -autoscale none -geometry %sx%s -free -pipe << %s &" %(self.pagesize[0], self.pagesize[1], self.line)
        #os.system(cmd)
        p=Popen(["xmgrace", "-autoscale", "none", "-noask", "-geometry",  "%sx%s"%self.pagesize,"-free", "-pipe" ], stdin=s) 
        #p=Popen(["xmgrace", "-free", "-autoscale", "none", "-pipe"], stdin=PIPE) 
        s.close()
        #p.stdin.write(self.line)

    def autoscale(self, arr, margin=0.1, log=False):
        amax = arr.max()
        amin = arr.min()
        r = 1. / arr.ptp()
        if log:
            if (amax > 0 and  amin > 0) and (amax < 0 and  amin < 0) :
                retmin = (r * amin / 10**10) / r
                retmax = (r * amax * 10**10) / r

            else:
                pom = abs(arr.max()) - abs(arr.min()) > 0 #pom stands for plus or minus.
                if pom:
                    retmin = 1e-18
                    retmax = (r * amax * 10**10) / r
                else:
                    retmin = (r * amin / 10**10) / r
                    retmax = -1e-18
        else:                
            retmin = (r * arr.min() - margin) / r
            retmax = (r * arr.max() + margin) / r
            retmin = (r * arr.min() - margin) / r
            retmax = (r * arr.max() + margin) / r
        return retmin, retmax

    def set_mkall(self, size=1, color=1, mstyle=1, fptn=[1], lwidth=[1], lstyle=[1]):
        from itertools import cycle
    
        for gnum in self.gdic.keys():
            if type(color) != int: colgen = cycle(color)
            if type(mstyle) != int: msgen = cycle(mstyle)
            if type(fptn) != int: fpgen = cycle(fptn)
            if type(lwidth) != int: lwgen = cycle(lwidth)
            if type(lstyle) != int: lsgen = cycle(lstyle)
        #for gnum in range(len(self.prop.gdiclst)):
            self.line += "@with g%s\n" %gnum
            snumlim = self.gdic[gnum] + 1
            if type(color) == int: colgen = count(color)
            if type(mstyle) == int: msgen = count(mstyle)
            if type(fptn) == int: fpgen = count(fptn)
            if type(lwidth) == int: lwgen = count(lwidth)
            if type(lstyle) == int: lsgen = count(lstyle)
            #for snum in range(snumlim):
            for snum in range(self.inisnum, snumlim):
                tmp = colgen.next()
                self.line += "@     s%s line linestyle 0\n" %snum
                self.line += "@     s%s symbol %s\n" %(snum, msgen.next())
                self.line += "@     s%s symbol color %s\n" %(snum, tmp)
                self.line += "@     s%s symbol fill color %s\n" %(snum, tmp) 
                self.line += "@     s%s symbol fill pattern %s\n" %(snum, fpgen.next()) 
                self.line += "@     s%s symbol linewidth %s\n" %(snum, lwgen.next())
                self.line += "@     s%s symbol linestyle %s\n"  %(snum, lsgen.next())
                #if select == 0:
                #    self.line += "@     s%s symbol %s\n" %(snum, msgen.next())
                #    self.line += "@     s%s symbol color %s\n" %(snum, colgen.next())
                #elif select == 1:
                #    self.line += "@     s%s symbol %s\n" %(snum, msgen.next())
                #    self.line += "@     s%s symbol color %s\n" %(snum, color)
                #else:
                #    self.line += "@     s%s symbol %s\n" %(snum, msgen.next()) 
                #    self.line += "@     s%s symbol color %s\n" %(snum, colgen.next())
                self.line += "@     s%s symbol size %s\n" %(snum, size)
        
    def set_lineall(self, select=0, size=1, color=1, lstyle=1):
        for gnum in range(len(self.prop.gdiclst)):
            self.line += "@with g%s\n" %gnum
            for snum in arange(len(self.prop.gdiclst[gnum]["snum"])):
                if select == 0:
                    self.line += "@     s%s line linestyle %s\n" %(snum, lstyle)
                    self.line += "@     s%s line color %s\n" %(snum+self.inisnum, snum + 1)
                elif select == 1:
                    self.line += "@     s%s line linestyle %s\n" %(snum+self.inisnum, snum + 1)
                    self.line += "@     s%s line color %s\n" %(snum+self.inisnum, color)
                else:
                    self.line += "@     s%s line linestyle %s\n" %(snum+seif.inisnum, snum + 1)
                    self.line += "@     s%s line color %s\n" %(snum+self.inisnum, snum + 1)
                self.line += "@     s%s line linewidth %s\n" %(snum+self.inisnum, size)

    def set_xtickitvl(self, itvl, gnum=0, ):
        self.line += "@with g%s\n" %(gnum)
        #self.line += "@    xaxis  major on\n" 
        self.line += "@    xaxis  tick major %s\n" %itvl
        
    def set_ytickitvl(self, itvl, gnum=0):
        self.line += "@with g%s\n" %(gnum)
        self.line += "@    yaxis  tick major %s\n" %itvl
       
#    def set_autoscale(self, xarr, yarr, gnum=0, margin=0.1):
#        xarr = array(xarr)
#        yarr = array(yarr)
#        xmin,xmax = self.autoscale(xarr, margin)
#        ymin,ymax = self.autoscale(yarr, margin)
#        self.set_lim(xmin,xmax,ymin,ymax, gnum, tnum=6)

    def set_xautoscale(self, xarr, gnum=0, margin=0.1):
        xarr = array(xarr)
        xmin,xmax = self.autoscale(xarr, margin)
        self.set_lim(xmin,xmax,ymin,ymax, gnum)
        self.set_xtickitvl(sig_fig(xarr.ptp()/6,1),gnum=gnum)
    
    def set_autoscale(self, xarr, yarr, gnum=0, margin=0.1, tl=6, logx=False, logy=False):
        xarr = array(xarr, dtype=double)
        yarr = array(yarr, dtype=double)
        xarr, yarr = rm_naninf(xarr, yarr)
        #for x in xarr:
        #    print x
        #input()
        xmin,xmax = self.autoscale(xarr, margin, log=logx)
        ymin,ymax = self.autoscale(yarr, margin, log=logy)
        
        #input((xmin,xmax,ymin,ymax, gnum))
        self.set_lim(xmin,xmax,ymin,ymax, gnum)
        #self.prop.lim_input(xmin,xmax,ymin,ymax, gnum)
        self.set_xtickitvl(sig_fig(xarr.ptp()/tl,1),gnum=gnum)
        self.set_ytickitvl(sig_fig(yarr.ptp()/tl,1),gnum=gnum)


    def set_xautoscale(self, xarr, gnum=0, margin=0.1):
        xmin,xmax = self.autoscale(xarr, margin)
        self.set_lim(xmin,xmax,ymin,ymax, gnum)
        self.set_xtickitvl(sig_fig(xarr.ptp()/6,1),gnum=gnum)
    
    def set_line(self, loc, lstyle=1, lwidth=1, lcolor=1, arrow=0, atype=0, alength=0, alayout=(1,1), loctype="view", gnum=0, xonly=False, yonly=False):
        if loctype == "wratio":
            loctype = "world"
            loc = self.conv_wratio(loc, gnum, xonly, yonly)
            
        self.line += "@with line\n"
        self.line += "@     line on\n"
        self.line += "@     line loctype %s\n" %loctype
        if loctype == "world":
            self.line += "@     line g%s\n" %gnum
        self.line += "@     line %s, %s, %s, %s\n" %(loc[0], loc[2], loc[1], loc[3])
        self.line += "@     line linestyle %s\n" %lstyle
        self.line += "@     line linewidth %s\n" %lwidth
        self.line += "@     line color %s\n" %lcolor
        self.line += "@     line arrow %s\n" %arrow
        self.line += "@     line arrow type %s\n" %atype
        self.line += "@     line arrow length %s\n" %alength
        self.line += "@     line arrow layout %s, %s\n" %alayout
        self.line += "@line def\n"

    def set_ellipse(self, loc, lstyle=1, lwidth=1, lcolor=1, fcolor=1, fptn=0, loctype="view", gnum=0):
        self.line += "@with ellipse\n"
        self.line += "@     ellipse on\n"
        self.line += "@     ellipse loctype %s\n" %loctype
        if loctype == "world":
            self.line += "@     ellipse g%s\n" %gnum 
        self.line += "@     ellipse %s, %s, %s, %s\n" %(loc[0], loc[2], loc[1], loc[3])
        self.line += "@     ellipse linestyle %s\n" %lstyle
        self.line += "@     ellipse linewidth %s\n" %lwidth
        self.line += "@     ellipse color %s\n" %lcolor
        self.line += "@     ellipse fill color %s\n" %fcolor
        self.line += "@     ellipse fill pattern %s\n" %fptn
        self.line += "@ellipse def\n"


    def set_box(self, loc, lstyle=1, lwidth=1, lcolor=1,  fcolor=1, fptn=0, loctype="view", gnum=0, xonly=False, yonly=False):
        if loctype == "wratio":
            loctype = "world"
            loc = self.conv_wratio(loc, gnum, xonly, yonly)

        xmin,xmax,ymin,ymax = loc
        xdata = array([xmin,xmin,xmax,xmax,xmin])
        ydata = array([ymin,ymax,ymax,ymin,ymin])
        #self.push_snum(0)
        snum = self.set_xydata(xdata, ydata, gnum=gnum, box=True)
        self.line += "@with g%s\n" %gnum
        self.line += "@    s%s line linestyle %s\n" %(snum, lstyle)
        self.line += "@    s%s line linewidth %s\n" %(snum, lwidth)
        self.line += "@    s%s line linewidth %s\n" %(snum, lwidth)
        self.line += "@    s%s line color %s\n" %(snum, lcolor)
        self.line += "@    s%s fill type 1\n" %snum
        self.line += "@    s%s fill rule 0\n" %snum
        self.line += "@    s%s fill color %s\n" %(snum, fcolor)
        self.line += "@    s%s fill pattern %s\n" %(snum, fptn)


    def set_box2(self, loc, lstyle=1, lwidth=1, lcolor=1,  fcolor=1, fptn=0, loctype="view", gnum=0):
        self.line += "@with box\n"
        self.line += "@     box on\n"
        self.line += "@     box loctype %s\n" %loctype
        if loctype == "world":
            self.line += "@     box g%s\n" %gnum
        self.line += "@     box %s, %s, %s, %s\n" %(loc[0], loc[2], loc[1], loc[3])
        self.line += "@     box linestyle %s\n" %lstyle
        self.line += "@     box linewidth %s\n" %lwidth
        self.line += "@     box color %s\n" %lcolor
        self.line += "@     box fill color %s\n" %fcolor
        self.line += "@     box fill pattern %s\n" %fptn
        self.line += "@box def\n"

    def set_string(self, string, loc, loctype="view", gnum=0, charsize=1):
        if loctype == "wratio":
            loctype = "world"
            loc = self.conv_wratio(loc, gnum)
        self.line += "@with string\n" 
        self.line += "@     string on\n" 
        self.line += "@     string loctype %s\n" %loctype
        if loctype == "world":
            self.line += "@     string g%s\n" %gnum 
        self.line += "@     string char size %s\n" %charsize
        self.line += "@     string %s, %s\n" %loc 
        self.line += "@     string def \"%s\"\n" %string

    def set_iterstr(self, lst, loc, loctype="view", gnum=0, charsize=1):
        
        #lst = map(lambda x: iter(x) if type(x) != str else x, lst)
        #input(i)
        # Make iterator object.
        
        cntlst = []
        cnt = 0
        wline = ""
        for line in lst:
            if type(line) == str:
                wline += line
            else:
                arr, n = line 
                wline += "%.3f" %arr[n]
                cntlst += [cnt]
                #wline += "%.3f" %line[self.iter_n]
            cnt += 1
        for cnt in cntlst:
            lst[cnt][1] += 1

        self.set_string(wline, loc, loctype, gnum, charsize)
                

    def set_timestamp(self, string, loc=(0.03,0.03), font=None, charsize=1.0):
        self.line += "@timestamp on\n" 
        self.line += "@timestamp %s, %s\n" %loc 
        if font != None:
            self.line += "@timestamp font %s\n" %font
        self.line += "@timestamp char size %s\n" %charsize

    def set_allprop(self):
        for gnum, gdic in enumerate(self.prop.gdiclst):
            self.set_xlabel(gdic["xlabel"], gnum=gnum) 
            self.set_ylabel(gdic["ylabel"], gnum=gnum) 
            self.set_xtics(gdic["xticks"], gnum=gnum) 
            self.set_ytics(gdic["yticks"], gnum=gnum) 
            self.set_lim(gdic["lim"], gnum=gnum) 
            for snum,sdic in enumerate(gdic["snum"]):
                self.set_legend(sdic["legend"], gnum=gnum, snum=snum) 
                self.set_mk(m[0], m[1], m[2], m[3], m[4], m[5]) 

    def set_lim_prop(self):
        for gnum, gdic in enumerate(self.prop.gdiclst):
            self.set_lim(gdic["lim"], gnum=gnum) 
            
    def set_xlabel_prop(self):
        for gnum, gdic in enumerate(self.prop.gdiclst):
            self.set_xlabel(gdic["xlabel"], gnum=gnum) 
    
    def set_ylabel_prop(self):
        for gnum, gdic in enumerate(self.prop.gdiclst):
            self.set_ylabel(gdic["ylabel"], gnum=gnum) 
    
    def set_labels_prop(self):
        for gnum, gdic in enumerate(self.prop.gdiclst):
            self.set_xlabel(gdic["xlabel"], gnum=gnum) 
            self.set_ylabel(gdic["ylabel"], gnum=gnum) 
    
    def set_ornament(self):
        for d in self.prop.decolst:
            if d[0] == "string":
                self.set_string(d[1], d[2], d[3], d[4], d[5])
            elif d[0] == "tstamp":
                self.set_timestamp(d[1], d[2], d[3], d[4])
            elif d[0] == "box":
                self.set_box(d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9],d[10])
            elif d[0] == "ellipse":
                self.set_ellipse(d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8])
            elif d[0] == "line":
                self.set_line(d[1], d[2], d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10], d[11],d[12])
            elif d[0] == "iterst":
                self.set_iterstr(d[1], d[2], d[3], d[4], d[5])

    def set_graphitems(self):
        #layoutdic = {"simple" : self.simplelayout,
        #                  "column" : self.columnlayout,
        #                  "dual"   : self.duallayout,
        #                  "triple"   : self.triplelayout,
        #                  "quad"   : self.quadlayout,
        #                  "hepta"   : self.heptalayout,
        #                  "octo"   : self.octolayout,
        #                  "octo2"   : self.octolayout2,
        #                  "penta"   : self.pentalayout}
        #layoutdic[self.prop.allpropdic["layout"]]()
        for key, val in self.prop.allpropdic.items():
            if key == "xlabelall" and val != None: self.set_xlabel_all(*val)
            if key == "ylabelall" and val != None: self.set_ylabel_all(*val)

        if self.prop.mkall != None: 
            v = self.prop.mkall
            self.set_mkall(v[0], v[1], v[2], v[3], v[4], v[5])
        if self.prop.lineall != None: 
            v = self.prop.lineall
            self.set_lineall(v[0], v[1], v[2], v[3])

        for gnum, gdic in enumerate(self.prop.gdiclst):
            for item, v in gdic.items():
                if item == "lim" and v != None:
                    self.set_lim(v[0], v[1], v[2], v[3], gnum, v[4])
                elif item == "xaxes" and v != None:
                    self.set_xaxes(*list(v) + [gnum])
                elif item == "yaxes" and v != None:
                    self.set_yaxes(*list(v) + [gnum])
                elif item == "xlabel" and v != None:
                    self.set_xlabel(v, gnum)
                elif item == "ylabel" and v != None:
                    self.set_ylabel(v, gnum)
                elif item == "xtickitvl" and v != None:
                    self.set_xtickitvl(v, gnum)
                elif item == "snum":
                    for snum, sdic in enumerate(v):
                        for sitem, sv in sdic.items():
                            if sitem == "legend" and sv != None:
                                self.set_leg(sv, gnum, snum, gdic["legloc"], gdic["legloctype"])
                                #self.set_leg(leg, gnum, snum, loc="rightup", loctype="wratio")
                            if sitem == "marker" and sv != None:
                                self.set_mk(sv[0], sv[1], sv[2], sv[3], sv[4], sv[5], sv[6], gnum, snum) 
                            if sitem == "line" and sv != None:
                                self.set_style_line(sv[0], sv[1], sv[2], gnum, snum) 
                            if sitem == "err" and sv != None:
                                self.set_errorbar(gnum, snum, sv[0], sv[1], sv[2], sv[3], sv[4], sv[5], sv[6])


                    


    
