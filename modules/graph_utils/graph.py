#_*_ coding:utf-8 _*_
def graph1(DATAPATH,xrange="*:*",yrange="*:*",xname="",yname="",xunit="",yunit="",using="1:2",PICPATH=0):
    import Gnuplot
    g=Gnuplot.Gnuplot(debug=1)
    g("set term x11 enhanced")
    XRANGE="set xrange ["+xrange+"]"
    YRANGE="set yrange ["+yrange+"]"
    g(XRANGE)
    g(YRANGE)
    xlabel="set xlabel '{/Helvetica-Oblique "+xname+"} ["+xunit+"]' font 'Helvetica,25'"
    g(xlabel)
    ylabel="set ylabel '{/Helvetica-Oblique "+yname+"} ["+yunit+"]' font 'Helvetica,25'"
    g(ylabel)
    pcmd="p '"+DATAPATH+"' u "+using+" w p"
    g(pcmd)
    input("return to close this picture")
    if type(PICPATH)==str:    
        g("set term postscript eps enhanced color 'Helvetica,20'")
        piccmd="set output '"+PICPATH+"'"
        g(piccmd)
        g("set pointsize 2")
        g("set key right top")
        g("set key box")
        g("set bor lw 3")
        g("set ytics 0.2")
        g("set ytics('0.6'-0.6,'0.4'-0.4,'0.2'-0.2)")
        g("set tics font 'Helvetica,25'")
        g("set tics scale 3")
        g("set style line 1 lt 1 lw 25 lc 1")
        g("set style line 2 lt 1 lw 20 lc 3")
        g("set size ratio 1")
        g("rep")
        

def graph2(DATAPATH,xrange,yrange,xname,yname,xunit,yunit,using,PICPATH,n):
    set="set term x11 enhanced "+str(n)
    XRANGE="set xrange ["+xrange+"]"
    YRANGE="set yrange ["+yrange+"]"
    g(XRANGE)
    g(YRANGE)
    xlabel="set xlabel '{/Helvetica-Oblique "+xname+"} ["+xunit+"]' font 'Helvetica,25'"
    g(xlabel)
    ylabel="set ylabel '{/Helvetica-Oblique "+yname+"} ["+yunit+"]' font 'Helvetica,25'"
    g(ylabel)
    pcmd="p '"+DATAPATH+"' u "+using+" w p"
    g(pcmd)
    input("return to close this picture")
    if type(PICPATH)==str:    
        g("set term postscript eps enhanced color 'Helvetica,20'")
        piccmd="set output '"+PICPATH+"'"
        g(piccmd)
        g("set pointsize 2")
        g("set key right top")
        g("set key box")
        g("set bor lw 3")
        g("set ytics 0.2")
        g("set ytics('0.6'-0.6,'0.4'-0.4,'0.2'-0.2)")
        g("set tics font 'Helvetica,25'")
        g("set tics scale 3")
        g("set style line 1 lt 1 lw 25 lc 1")
        g("set style line 2 lt 1 lw 20 lc 3")
        g("set size ratio 1")
        g("rep")
        
def graph3(xdata,ydata,xname,yname,xmin,xmax,ymin,ymax):
    import pylab as pl
    pl.plot(xdata,ydata)
    pl.xlabel(xname)
    pl.ylabel(yname)
    pl.show()

#グラフを4個描く
def graph4(shot,xy1,xy2,xy3,xy4,xname="",y1name="",y2name="",y3name="",y4name="",fignum=1,PDFPATH="/Users/yu/test.pdf"):
    from pylab import plot,show,figure,subplot,suptitle,xlim,xlabel,ylabel,savefig,ylim,save,grid
    figure(figsize=(9,12))
    subplot(411)
    plot(xy1[0],xy1[1])
    grid(True)
    suptitle("#"+shot,fontsize=20)
    xlim(20,40)
    ylabel(y1name)
    subplot(412)
    plot(xy2[0],xy2[1])
    grid(True)
    xlim(20,40)
#    ylim(-0.001,0.005)
    ylabel(y2name)
    subplot(413)
    xlim(20,40)
    plot(xy3[0],xy3[1])
    grid(True)
    ylabel(y3name)
    subplot(414)
    plot(xy4[0],xy4[1])
    grid(True)
    xlim(20,40)
    ylabel(y4name)
    xlabel(xname)
    savefig(PDFPATH)

    
def graph5(shot,xy1,xy2,xy3,xy4,xname="",y1name="",y2name="",y3name="",y4name="",fignum=1,PDFPATH="/Users/yu/test.pdf"):
    from pylab import plot,show,figure,subplot,suptitle,xlim,xlabel,ylabel,savefig,twinx,grid
    figure(fignum,figsize=(9,12))
    subplot(211)
    grid(True)
    plot(xy1[0],xy1[1],"r")
    suptitle("#"+shot)
    xlim(20,40)
    ylabel(y1name)
    twinx()
    plot(xy2[0],xy2[1])
    xlim(20,40)
    ylabel(y2name)
    subplot(212)
    grid(True)
    xlim(20,40)
    plot(xy3[0],xy3[1],"r")
    ylabel(y3name)
    twinx()
    plot(xy4[0],xy4[1])
    xlim(20,40)
    ylabel(y4name)
    xlabel(xname)
    savefig(PDFPATH)
#    show()
    

def graph6(shot,xy1,xy2,xy3,xy4,xname="",y1name="",y2name="",y3name="",y4name="",PDFPATH="/Users/yu/test.pdf"):
    from pylab import plot,show,figure,subplot,suptitle,xlim,xlabel,ylabel,savefig,twinx
    figure(figsize=(9,12))
    subplot(211)
    plot(xy1[0],xy1[1],"r")
    suptitle("#"+shot)
    xlim(20,40)
    ylabel(y1name)
    twinx()
    plot(xy2[0],xy2[1])
    xlim(20,40)
    ylabel(y2name)
    subplot(212)
    xlim(20,40)
    plot(xy3[0],xy3[1],"r")
    ylabel(y3name)
    twinx()
    plot(xy4[0],xy4[1])
    xlim(20,40)
    ylabel(y4name)
    xlabel(xname)
    savefig(PDFPATH)
    show()
    
def graph7(shot,xy1,xy2,xname="",y1name="",y2name="",PDFPATH="/Users/yu/test.pdf"):
    from pylab import plot,show,figure,subplot,suptitle,xlim,xlabel,ylabel,savefig,grid,text
    from numpy import array
    figure(figsize=(9,5))
    ax1=subplot(111)
    grid(True)
    MPCratio=((1.24*xy1[1]-xy2[1])/(1.24*xy1[1]+xy2[1]))
    plot(xy1[0],MPCratio,"r")
    ax1.text(23,0,"#"+str(shot),bbox=dict(fc="w",alpha=1),horizontalalignment="center",verticalalignment="center",fontsize=30)
    xlim(20,40)
    ylabel(r"$(I_{\rm{s1}}-I_{\rm{s2}})/(I_{\rm{s1}}+I_{\rm{s2}})$",fontsize=20)
    xlabel(r"$\rm Time [msec]$",fontsize=20)
    savefig(PDFPATH)
    
def graph8(shots,xylst,xrange=[26,36],yrange=None,leglst=None,
           PICPATH="/Users/yu/test.pdf",figsize=(9,12),log=0,dress=0,
           collst=None, minus=None, loc="best"):
    from pylab import plot,show,figure,subplot,suptitle,xlim,ylim,xlabel,ylabel,savefig,grid,setp,subplots_adjust,rc,legend,semilogy,draw
    rc("font",family="Helvetica")
    from numpy import array,sqrt
    import itertools as i
    
    if type(collst) == list:
        colgen = i.cycle(collst) 
    else:
        colgen = i.cycle(["r"])
    
    index=len(shots)
    fig=figure(figsize=figsize)
    subplots_adjust(hspace=0.001)
    grid(True)
    ax1=subplot(index,1,1)
    fs=30/sqrt(index)
#    ax1.text("upper left","#"+str(shots[0]),bbox=dict(fc="w",alpha=1),horizontalalignment="center",verticalalignment="center",fontsize=fs)
    grid(True)
    if type(yrange) == list:
        ylim(yrange)
    fig.text(0.03,0.5,xylst[0][1][1],fontsize=20,horizontalalignment="center",verticalalignment="center",rotation=90)
    if type(leglst) == list:
        label=leglst[0]
    else:
        label="#"+str(shots[0])
    if log == 1:
        if minus == 1:
            semilogy(xylst[0][0][0],xylst[0][0][1],"r",label=label,c=colgen.next())
        else:
            semilogy(xylst[0][0][0],xylst[0][0][1],"r",label=label,c=colgen.next())
    else:
        if minus == 1:
            plot(xylst[0][0][0],xylst[0][0][1],"r",label=label,c=colgen.next())
        else:
            plot(xylst[0][0][0],xylst[0][0][1],"r",label=label,c=colgen.next())
    legend(loc="best")
    xticklabels=ax1.get_xticklabels()
    a=range(index)
    num=2
    xylst2=xylst[1:]
    if index != 1:
        for xy in xylst2:
            a[num-2]=subplot(index,1,num,sharex=ax1)
#            a[num-2].text(26.5,0.15,"#"+str(shots[num-1]),bbox=dict(fc="w",alpha=1),horizontalalignment="center",verticalalignment="center",fontsize=fs)
            grid(True)
            if type(yrange) == list:
                ylim(yrange)
            if type(leglst) == list:
                label=leglst[num-1]
            else:
                label="#"+str(shots[num-1])
            if log == 1:
                if minus == 1:
                    semilogy(xy[0][0],-xy[0][1],"r",label=label,c=colgen.next())
                else:
                    semilogy(xy[0][0],xy[0][1],"r",label=label,c=colgen.next())
            else:
                if minus == 1:
                    plot(xy[0][0],-xy[0][1],"r",label=label,c=colgen.next())
                else:
                    plot(xy[0][0],xy[0][1],"r",label=label,c=colgen.next())
            if num != index:
                xticklabels+=a[num-2].get_xticklabels()
            num+=1
            legend()
        setp(xticklabels,Visible=False)
        
    
    
    xlim(xrange) 
    xlabel(r"$Time\ \rm{[ms]}$",fontsize=20)
    draw()
    savefig(PICPATH)
    
def graph9(shot,xylst,xrange=[26,36],yrangelst=None,
           PICPATH="/Users/yu/test.pdf",figsize=(9,12),log=None,
           collst=None, dress=0):
    from pylab import semilogy,plot,show,figure,subplot,suptitle,xlim,ylim,xlabel,ylabel,savefig,grid,setp,subplots_adjust,rc,semilogy,draw
    rc("font",family="Helvetica")
    from numpy import array,sqrt
    from useful import dress
    import itertools as i
#    colgen=iter(["r","b","g","y","k","c"])
    if type(collst) == list:
        colgen = i.cycle(collst) 
    else:
        colgen = i.cycle(["r"])
    index=len(xylst)
    fig=figure(figsize=figsize)
    if dress == 1:
        dress(fig,xlabel,ylabel,)
    suptitle("#"+str(shot),fontsize=30)
    subplots_adjust(hspace=0.001)
    grid(True)
    ax1=subplot(index,1,1)
    fs=30/sqrt(index)
    if type(yrangelst) == list:
        if type(yrangelst[0])== list:
            ylim(yrangelst[0])
    ylabel(str(xylst[0][1][1]),fontsize=fs,fontproperties="Helvetica")
    grid(True)
    if log == 1:
        semilogy(xylst[0][0][0],-xylst[0][0][1],colgen.next())
    else:
        plot(xylst[0][0][0],xylst[0][0][1],colgen.next())
    xticklabels=ax1.get_xticklabels()
    a=range(index)
    num=2
    xylst2=xylst[1:]
    if index != 1:
        for xy in xylst2:
            a[num-2]=subplot(index,1,num,sharex=ax1)
            ylabel(xy[1][1],fontsize=fs)
            if type(yrangelst) == list:
                if type(yrangelst[num-1])== list:
                    ylim(yrangelst[num-1])
            grid(True)
            if log == 1:
                semilogy(xy[0][0],-xy[0][1],colgen.next())
            else:
                plot(xy[0][0],xy[0][1],colgen.next())
            if num != index:
                xticklabels+=a[num-2].get_xticklabels()
            num+=1
        setp(xticklabels,Visible=False)
    xlim(xrange)
    xlabel(r"$Time\ \rm{[ms]}$",fontsize=20)
    draw()
    savefig(PICPATH)

def graph10(shot,xylst,xrange=[26,36],yrangelst=None,
            PICPATH="/Users/yu/test.pdf",figsize=(9,12),log=None,
            collst=None, dress=0, minus=None):
    from pylab import plot,show,figure,subplot,suptitle,xlim,ylim,xlabel,ylabel,twinx,savefig,grid,setp,subplots_adjust,rc,legend,semilogy,draw
    rc("font",family="Helvetica")
    from numpy import array,sqrt
    import itertools as i
    
    index=len(xylst)
    
    if type(collst) == list:
        colgen = i.cycle(collst)
    else:
        colgen=i.cycle(["r","b","g","y","k","c"])

    fig=figure(figsize=figsize)
    suptitle("#"+str(shot),fontsize=30)
    grid(True)
    fs=30/sqrt(index)
    if type(yrangelst) == list:
        if type(yrangelst[0])== list:
            ylim(yrangelst[0])
    leglst=[xylst[0][1][1]]
    ylabel(str(xylst[0][1][1]),fontsize=20,fontproperties="Helvetica")
    grid(True)
    axlst=range(index)
    if log == 1:
        if minus ==1:
            axlst[0]=semilogy(xylst[0][0][0],-xylst[0][0][1],colgen.next())
        else:
            axlst[0]=semilogy(xylst[0][0][0],xylst[0][0][1],colgen.next()) 
    else:
        if minus == 1:
            axlst[0]=plot(xylst[0][0][0],-xylst[0][0][1],colgen.next())
        else:
            axlst[0]=plot(xylst[0][0][0],xylst[0][0][1],colgen.next())
    a=range(index)
    num=2
    xylst2=xylst[1:]
    if index != 1:
        for xy in xylst2:
            twinx()
            leglst+=[xy[1][1]]
            ylabel(xy[1][1],fontsize=20,fontproperties="Helvetica")
            if type(yrangelst) == list:
                if type(yrangelst[num-1])== list:
                    ylim(yrangelst[num-1])
            grid(True)
            if log == 1:
                if minus == 1:
                    axlst[num-1]=semilogy(xy[0][0],-xy[0][1],colgen.next())
                else:
                    axlst[num-1]=semilogy(xy[0][0],xy[0][1],colgen.next())
            else:
                if minus == 1:
                    axlst[num-1]=plot(xy[0][0],-xy[0][1],colgen.next())
                else:
                    axlst[num-1]=plot(xy[0][0],xy[0][1],colgen.next())
            num+=1
    
    legend(axlst,leglst,"upper left")
    xlim(xrange)
    xlabel(r"$\rm Time [msec]$",fontsize=20)
    draw()
    savefig(PICPATH)
    
def graph11(shots,xylst,xrange=[26,36],yrange=None,leglst=None,mark=None,
            PICPATH="/Users/yu/test.pdf",figsize=(12,8),log=0,minus=None,
            collst=None, loc="best"):
    from pylab import semilogy,plot,show,figure,subplot,suptitle,xlim,ylim,xlabel,ylabel,savefig,grid,setp,subplots_adjust,rc,twinx,legend,draw
    rc("font",family="Helvetica")
    from numpy import array,sqrt
    import itertools as i

    if type(collst) == list:
        colgen = i.cycle(collst)
    else:
        colgen=i.cycle(["r","y","g","b","black","c","m","pink"])
    index=len(shots)
    fig=figure(figsize=figsize)
    grid(True)
    fs=30/sqrt(index)
    shotgen=iter(shots)
    leglst2=["#"+str(shotgen.next())]
    grid(True)
    if type(yrange) == list:
        ylim(yrange)
    ylabel(xylst[0][1][1],fontsize=20)
    if log == 1 :
        if minus == 1:
            axlst=[semilogy(xylst[0][0][0],-xylst[0][0][1],colgen.next())]
        else:
            axlst=[semilogy(xylst[0][0][0],xylst[0][0][1],colgen.next())]
    else :
        if minus == 1:
            axlst=[plot(xylst[0][0][0],-xylst[0][0][1],colgen.next())]
        else:
            axlst=[plot(xylst[0][0][0],xylst[0][0][1],colgen.next())]
    xlabel(r"$Time\ \rm{[ms]}$",fontsize=20)
    a=range(index)
    num=2
    xylst2=xylst[1:]
    if index != 1:
        for xy in xylst2:
            grid(True)
            if type(yrange) == list:
                ylim(yrange)
            if log == 1:
                if minus == 1:
                    axlst+=[semilogy(xy[0][0],-xy[0][1],colgen.next())]
                else:
                    axlst+=[semilogy(xy[0][0],xy[0][1],colgen.next())]
            else:
                if minus == 1:
                    axlst+=[plot(xy[0][0],-xy[0][1],colgen.next())]
                else:
                    axlst+=[plot(xy[0][0],xy[0][1],colgen.next())]
            leglst2+=["#"+str(shotgen.next())]
            num+=1
    xlim(xrange)
    if leglst == None:
        leglst = leglst2
    legend(axlst,leglst,loc=loc)
    xlabel(r"$\rm Time [ms]$",fontsize=20)
    draw()
    savefig(PICPATH)
    
def pl3d(x,y,z,xrange,yrange,zrange,xname,yname,zname,pstyle="-",pointsize=3,color="r"):
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import matplotlib.pyplot as plt
    colgen=iter(["r","y","g","b","black","c","m","pink","b","b","white"])
    mpl.rcParams['legend.fontsize'] = 20
    
    
    ax = plt.gca(projection='3d')
    
    ax.plot(x, y, z,pstyle,markersize=pointsize,c=color)
    ax.set_xlim3d(xrange)
    ax.set_ylim3d(yrange)
    ax.set_zlim3d(zrange)
    ax.set_xlabel(xname)
    ax.set_ylabel(yname)
    ax.set_zlabel(zname)
   

    
    
    
        