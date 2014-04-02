#!/usr/bin/env python
#-*- coding:utf-8 -*-
from numpy import *

#Single, dual, triple, quadruple, quintuple, sextuple, septuple, octuple, nonuple, decuple, undecuple, duodecuple...
class grace_layout():
    def layout_1(self, linewidth=4, hgrid=1, vgrid=1):
        gridnum = hgrid * vgrid
        self.set_font(4)
        self.set_pagesize(600,600)
        self.multigraph(1,1, hmargin=0.18, vmargin=0.18, hoffset=0.09, voffset=0.02, hgrid=hgrid, vgrid=vgrid)
        for n in range(gridnum):
            self.set_xaxis(0.1,2,4, fsnum=2, gnum=n)
            self.set_yaxis(0.1,2,4, fsnum=2, gnum=n)
            
    def layout_1_2(self, linewidth=4, hgrid=1, vgrid=1):
        gridnum = hgrid * vgrid
        self.set_font(4)
        self.set_pagesize(848, 600)
        self.multigraph(1,1, hmargin=0.18, vmargin=0.18, hoffset=0.09, voffset=0.02, hgrid=hgrid, vgrid=vgrid)
        for n in range(gridnum):
            self.set_leg_prop(gnum=n, blwid=2, csize=2)
            self.set_xaxis(0.1,2,4, fsnum=2, gnum=n)
            self.set_yaxis(0.1,2,4, fsnum=2, gnum=n)
    
    def layout_2(self, hgrid=1, vgrid=1):
        self.set_font(4)
        self.set_pagesize(566,800)
        self.multigraph(2,1, hmargin=0.14, vmargin=0.02, hpad=0.04, vpad=0.05,hoffset=0.09, voffset=0.01, hgrid=hgrid, vgrid=vgrid)
        for num in range(2):
            
            self.set_xaxis(0.1,1.2,3, fsnum=1.5, gnum=num)
            self.set_yaxis(0.1,1.2,3, fsnum=1.5, gnum=num)


    def layout_3(self, hgrid=1, vgrid=1):
        self.layout_4(hgrid=hgrid, vgrid=vgrid)
        self.unset_graph(3)

    def layout_4(self, hgrid=1, vgrid=1):
        self.set_font(4)
        self.set_pagesize(1000,800)
        self.multigraph(2,2, hmargin=0.04, vmargin=0.02, hpad=0.07, vpad=0.05,hoffset=0.03, voffset=0.01, hgrid=hgrid, vgrid=vgrid)
        for num in range(4):
            self.set_xaxis(0.1,1,2, fsnum=1, gnum=num)
            self.set_yaxis(0.1,1,2, fsnum=1, gnum=num)
        

    def layout_5(self, hgrid=1, vgrid=1):
        self.set_font(4)
        self.set_pagesize(1131,800)
        self.multigraph(2,3, hmargin=0.02, vmargin=0.02, hpad=0.045, vpad=0.045,hoffset=0.03, voffset=0.01, hgrid=hgrid, vgrid=vgrid)
        for num in range(5):
            self.set_xaxis(0.1,1,2, fsnum=0.8, gnum=num)
            self.set_yaxis(0.1,1,2, fsnum=0.8, gnum=num)
        self.unset_graph(5)

    def layout_6(self, hgrid=1, vgrid=1):
        self.set_font(4)
        self.set_pagesize(1131,800)
        self.multigraph(2,3, hmargin=0.02, vmargin=0.02, hpad=0.04, vpad=0.05,hoffset=0.03, voffset=0.01, hgrid=hgrid, vgrid=vgrid)
        for num in range(6):
            self.set_xaxis(0.1,1,2, fsnum=0.8, gnum=num)
            self.set_yaxis(0.1,1,2, fsnum=0.8, gnum=num)

    def layout_7(self, hgrid=1, vgrid=1):
        self.set_font(4)
        self.set_pagesize(800,800)
        self.multigraph(3,3, hmargin=0.01, vmargin=0.0, hpad=0.04, vpad=0.04,hoffset=0.03, voffset=0.03)
        #self.multigraph(3,3, hmargin=0.02, vmargin=0.1, hpad=0.05, vpad=0.02,hoffset=0.03, voffset=0.01)
        for num in range(9):
            self.set_xaxis(0.1,0.5,1, fsnum=0.5, gnum=num, tl=True)
            self.set_yaxis(0.1,0.5,1, fsnum=0.5, gnum=num, tl=True)
        self.unset_graph(7)
        self.unset_graph(8)

    def layout_8(self, hgrid=1, vgrid=1):
        self.set_font(4)
        self.set_pagesize(paper ="hl", psize=800)
        self.multigraph(4,2, hmargin=0.02, vmargin=0.1, hpad=0.06, vpad=0,hoffset=0.03, voffset=0.01, hgrid=hgrid, vgrid=vgrid)
        for num in range(8):
            self.set_xaxis(0.1,1,2, fsnum=1, gnum=num, tl=False)
            self.set_yaxis(0.1,1,2, fsnum=1, gnum=num, tl=True)
        self.set_xaxis(0.1,1,2, fsnum=1, gnum=0, tl=True)
        self.set_xaxis(0.1,1,2, fsnum=1, gnum=1, tl=True)

    def layout_8_2(self, hgrid=1, vgrid=1):
        self.set_font(4)
        self.set_pagesize(800,800)
        self.multigraph(3,3, hmargin=0.01, vmargin=0.0, hpad=0.04, vpad=0.04,hoffset=0.03, voffset=0.03, hgrid=hgrid, vgrid=vgrid)
        #self.multigraph(3,3, hmargin=0.02, vmargin=0.1, hpad=0.05, vpad=0.02,hoffset=0.03, voffset=0.01)
        for num in range(9):
            self.set_xaxis(0.1,0.5,1, fsnum=0.5, gnum=num, tl=True)
            self.set_yaxis(0.1,0.5,1, fsnum=0.5, gnum=num, tl=True)
        self.unset_graph(8)

    def layout_column(self, num, hgrid=1, vgrid=1):
        gridnum = hgrid * vgrid
        gr = 1. /(num)**(0.35)
        #gr = 1. /(num)**(0.75/gridnum)
        self.set_font(4)
        self.set_pagesize(600,849)
        self.multigraph(num/gridnum, 1, hmargin=0.15, vmargin=0.1, hpad=0.0, vpad=0.,hoffset=0.1, voffset=0.08*gr, hgrid=hgrid, vgrid=vgrid)
        #self.multigraph(num,1, hmargin=0.2/(num*gridnum)**(1/3), vmargin=0.1/(num*gridnum)**(1/3), hpad=0.0, vpad=0.,hoffset=0.1/sqrt(num*gridnum), voffset=0.03/sqrt(num*gridnum), hgrid=hgrid, vgrid=vgrid)
        for gn in xrange(num):
            print gn % gridnum
            self.set_xaxis(0.1*gr,1*gr,2*gr, fsnum=gr*2.5, gnum=gn, tl=True if not gn % (num / gridnum) else False)
            self.set_yaxis(0.1*gr,1*gr,2*gr, fsnum=gr*2.5, gnum=gn)
            
    def layout_column_4grid(self, num, hgrid=1, vgrid=1, logx=False, logy=False):
        gr = 1./sqrt(num/4)
        self.layout_column(num/4, hgrid=2, vgrid=2)
        #for n in xrange(num):
        #    if n%(num/4) != 0:
        #        tl = False
        #    else:
        #        tl = True
        #    if logx: self.set_xaxes(1, 0, n)
        #    if logy: self.set_yaxes(1, 0, n)
        #    self.set_xaxis(1*gr,0.5*gr,1*gr,gnum=n, tl=tl)
        #    self.set_yaxis(1*gr,0.5*gr,1*gr,gnum=n)
