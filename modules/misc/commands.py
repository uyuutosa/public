
def profile(abbchname,dlsts,xrange=None,yrange=None,xname=r"R [mm]"
            ,yname=None,leglst=0,gtime=35.5,figsize=(9,9),loc="best",tick=0,bor=None,fitting=0,data=None,sdev=None,pointsize=3,
            int=0.1,ave=0.2,RAW=0,eleint=None,eleave=None,sen = 1000,fit_path=None):
    from calc import calc,ele_field,pfit
    from useful import abbchan,grep,writedat
    from numpy import where,array,arange,polyfit,polyval,savetxt,transpose,mean,std,append, linspace
    from pylab import plot,xticks,yticks,xlim,ylim,xlabel,ylabel,figure,plot,savefig,rc,annotate,legend,rcParams,axes,draw,errorbar

    def profread(num):
        o = open("/")
#    print abbchname != "ele" and abbchname != "velo"
#    print abbchname == "ele"
#    input()
    ###########CONFIG AREA##################
#    rc("text",usetex=True)

    rcParams["legend.fontsize"]=20
    rcParams["axes.linewidth"]=2
    rcParams["xtick.major.pad"]=12
    rcParams["ytick.major.pad"]=12
    mk = "o"
    
        
    colgen=iter(["r","y","g","b","black","c","m","pink","b","b","white"])
    if type(data)== list:
        datagen=iter(data)
    
    gylst=[]
    shotlst=[]
    
    ax=figure(figsize=figsize).add_axes([0.15,0.15,0.8,0.8])

    ##########CALC AREA################
    if tick == 1:
        if type(xrange) == list:
            if len(xrange)==3:
                xdivision=xrange[2]
            else:
                xdivision=None
            xlimit=arange(xrange[0],xrange[1],xdivision)
            
            xticks(xlimit,xlimit,fontsize=30)
        
        if type(yrange) == list:
            if len(yrange)==3:
                ydivision=yrange[2]
            else:
                ydivision=None
            
            ylimit=arange(yrange[0],yrange[1],ydivision)
            yticks(ylimit,ylimit,fontsize=30)
            
    if xrange != None:
        xlim(xrange[0],xrange[1])
    if yrange != None:
        ylim(yrange[0],yrange[1])
        
#        ylim(yrange)
    if type(leglst) == list:
        label=iter(leglst)
    elif leglst == 0:
        pass
    else:
        a=range(len(dlsts))
        b=map((lambda x: "datalist%s" %(x+1)),a)
        label=iter(b)
        
        
    paralst=array([])
    std_paralst = array([])
    xlst=array([])
    num=0
    a=[]
    glst=None
    if type(gtime)==list:
        glst=gtime
        ggen=iter(glst)
    
    tmp_xy = []
    xylst = []
    tmp_shot = []
    shots = []
    tes = []
    for dlst in dlsts:
#        print dlst
        dlst = sorted(dlst, key = lambda x:x[1])
#        print dlst
#        input()
        for dl in dlst:
            para = dl[1]
            if len(where(std_paralst==para)[0]) == 0:
                std_paralst=append(std_paralst,para)
            
            tmp_shot += [dl[0]]
            if abbchname == "ele" or abbchname == "velo" or abbchname == "Mp":
                tmp_xy += [calc("vf",dl[0],int=int,ave=ave,RAW=RAW)]
                if abbchname == "Mp":
                    tes += [calc("te",dl[0],int=int,ave=ave,RAW=RAW)]
            else:
                tmp_xy += [calc(abbchname,dl[0],int=int,ave=ave,RAW=RAW)]
        xylst += [tmp_xy]
        shotlst += [tmp_shot]
        tmp_shot = []
        tmp_xy = []


    cnt = 0
    cnt_fit = 0
    cnt1 = 0
    cnt2 = 0
    for dlst in dlsts:
        dlst = sorted(dlst, key = lambda x:x[1])
        if type(glst)==list:
            gtime=ggen.next()
        gylst=[]    
        for dl in dlst:
            para = dl[1]
#            if len(where(paralst==para)[0]) == 0:
            paralst=append(paralst,para)
            
            xy=xylst[cnt1][cnt2]
            cnt2 += 1
            #gylst=append(gylst,[grep(gtime,xy[0][0],xy[0][1])])
            gylst += [grep(float(gtime),xy[0][0],xy[0][1])]
#            print [a for a in xy[0][1]]
#            print [a for a in xy[0][0]]
#            
##            plot(xy[0][0],xy[0][1]) 
#            draw()
#            print xy[0][1][155]
#            print gtime
#            input()
            xlst=append(xlst,dl[1])
        gylst=array(gylst)
        
        if abbchname == "ele" or abbchname == "velo" or abbchname == "Mp":
            mk = "-"
            a=pfit(paralst,gylst,fitting,(paralst[0],paralst[-1],sen)) 
#            plot(a[0],a[1])
            paralst, gylst ,blst= ele_field(a[0],a[1], int=eleint, ave=eleave)
#            plot(arange(0,200,0.01),gylst[50]*arange(0,200,0.01)+blst[50])
            xy[1][1] = "E [kV/m]"
            if abbchname == "velo" or abbchname == "Mp":
                B_phi = 0.3 #* 82 / paralst
                gylst = gylst / B_phi
                xy[1][1] = "V_phi [km/s]"
            
                if abbchname == "Mp":
                    iotas=array(profread(profpath,2))
                    reffs=array(profread(profpath,1))
                    elms = []
                    te_greped = []
                    para_greped = []
                    
                    for reff in reffs: 
                        elms += [grep(reff, paralst, gylst)]
                        te_greped += [grep(reff, paralst, tes)]
                        
                    
                    m_i = 1.67262e-27
                    k = 1.380658e-23
                    vp = array([elms])
                    te = array([te_greped])
                    Theta = iotas*reffs/0.82
                    vt = sqrt(2*k*0.1*tes/mi) #assumption Te = 10Ti 
                    paralst = reff
                    gylst = vp/(Theta * vt)
                    xy[1][1] = "$M_p$"
                
#                

            

        mdatlst=array([])
        stdatlst=array([])
#        print paralst
#        print gylst
#        print xlst
#        print gylst
#        print shotlst
#        print xylst
#        input()

        
        
        if cnt == 0:
            datlst = [paralst]
            cnt += 1

        if sdev == 1:
            for para in std_paralst:
                dat=gylst[where(xlst==para)[0]]
                mdat=mean(dat)
                stdat=std(dat)
                mdatlst=append(mdatlst,mdat)
                stdatlst=append(stdatlst,stdat)
                if cnt == 0:
                    datlst = [std_paralst]
                    cnt += 1
                    
        
                
        
        
        #################PLOT AREA######################
        if sdev == 1:
            if leglst == 0:
                ax.errorbar(std_paralst,mdatlst,stdatlst,fmt=mk,markersize=pointsize,c=colgen.next())
            else:
                ax.errorbar(std_paralst,mdatlst,stdatlst,fmt=mk,markersize=pointsize,c=colgen.next(),label=label.next())
            if fitting != 0:
                a=pfit(std_paralst,mdatlst,fitting,(std_paralst[0],std_paralst[-1],500)) 
                ax.plot(a[0],a[1])
            
            datlst += [mdatlst,stdatlst]
#            if type(data) == list:
#                writedat(datagen.next(),[std_paralst,mdatlst,stdatlst],xy[1][0]+", "+xy[1][1])#,stdatlst)))
                
        
        else:                
            if leglst == 0:
                ax.plot(paralst,gylst,mk,markersize=pointsize,c=colgen.next())
            else:
                ax.plot(paralst,gylst,mk,markersize=pointsize,c=colgen.next(),label=label.next())
#           
            if fitting !=0:
                if abbchname != "ele" and abbchname != "velo":
                    a=pfit(paralst,gylst,fitting,(paralst[0],paralst[-1],sen))
                    ax.plot(a[0],a[1])
#                    fit_paralst, fit_gylst ,blst= ele_field(a[0],a[1], int=eleint, ave=eleave)
#                    plot(linspace(paralst[0],paralst[-1],sen),-fit_gylst[1020]*linspace(paralst[0],paralst[-1],sen)+blst[1020])
#                    print fit_paralst[1020]#*arange(0,200,0.01)+blst[50]
                    if cnt_fit == 0:
                        fit_datlst = [a[0]]
                        cnt_fit += 1
#                    fit_datlst += [-fit_gylst[1020]*linspace(paralst[0],paralst[-1],sen)+blst[1020]]
                    fit_datlst += [a[1]]
                    
            datlst += [gylst] 
#            print len(datlst[0])
#            print len(datlst[1])
#            print len(datlst[2])


                    
        xlst,gylst,paralst,mdatlst,stdatlst=array([]),array([]),array([]),array([]),array([])       
        cnt1 +=1
        cnt2 = 0
#    
    if type(data) == list:
        writedat(datagen.next(),datlst,xy[1][0]+", "+xy[1][1])
#    if fitting != 0:
#        writedat(fit_path,fit_datlst,"Rtp [mm], w/ Bias [V], w/o Bias [V]")
        
        
        
      

    xlabel(xname,fontsize=30)
    if type(yname) == str:
        ylabel(yname,fontsize=30)
    else:
        ylabel(xy[1][1],fontsize=30,fontproperties="Helvetica")
    
    if leglst != 0:
        legend(shadow=True,loc=loc,numpoints=1)
        
    draw()