def gnufit(datlst, function, fitparalst, stnum, ennum, interval, retpara=False):
 import Gnuplot as gp
 from subprocess import call
 tmppath = home() + "/tmp.txt"
 tmppath2 = home() + "/tmp2.txt"
 savetxt(tmppath,transpose(datlst))
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
 g = gp.Gnuplot(debug=1)
 o = open(tmppath2)
 paravals = []
 for line in o:
  paravals += [float(line)]
  print line
 o.close()
 call(["rm",tmppath,tmppath2])
 
 #making index area
 x = linspace(stnum, ennum, interval)
 for para, val in zip(paras, paravals):
     exe = "%s = %s" %(para, val)
     exec exe
 exe = "y = %s" %function
 exec exe
 print exe
 if retpara:
    return [x, y, paravals]
 else:
    return [x, y]
def linear_fit( xlst, ylst, itvl=None, ave=None):
    from numpy import array,sum,where

    xlst = array(xlst)
    ylst = array(ylst)

    if len(xlst) != len(ylst):
        print "The number of X low is different with the number of y low !!"
    elif itvl == None: 
        n = len(xlst)
        x = sum(xlst)
        y = sum(ylst)
        xy = sum(xlst * ylst)
        xsqua = sum(xlst ** 2)
        
        a = ( n * xy- x * y ) / ( n * xsqua - x ** 2 )
        b = ( xsqua * y- xy * x ) / ( n * xsqua - x ** 2 )
    
        return a,b
    
    elif type(itvl) != None:
        itvl = float(itvl)
        wid = float(ave)
        cnt = float(xlst[0])
        xmax = float(xlst[-1]) 
        cntlst = []
        alst = []
        blst = []
        avelst=[]
        while cnt < xmax: 
            widmin = cnt - wid/2
            widmax = cnt + wid/2
            xlst_min = xlst[where(xlst >= widmin)[0]]
            ylst_min = ylst[where(xlst >= widmin)[0]]
            xlst_len = where(xlst_min <= widmax )[0]
            

            if len(xlst_len) != 0:
                xlst_tmp=xlst_min[xlst_len]
                ylst_tmp=ylst_min[xlst_len]

                n = len(xlst_tmp)
                x = sum(xlst_tmp)
                y = sum(ylst_tmp)
                xy = sum(xlst_tmp * ylst_tmp)
                xsqua = sum(xlst_tmp ** 2)
            
                a = ( n * xy- x * y ) / ( n * xsqua - x ** 2 )
                b = ( xsqua * y- xy * x ) / ( n * xsqua - x ** 2 )
                
                cntlst += [cnt]
                alst += [a]
                blst += [b]
                
            cnt += itvl
        return cntlst,alst,blst
        
def pfit(xlist,ylist,M=8,sen=(82,123,1)):
    import numpy as np
    xlist = np.array(xlist)
    ylist = np.array(ylist)
    def y(x, wlist):
        ret = wlist[0]
        for i in range(1, M+1):
            ret += wlist[i] * (x ** i)
        return ret
    
    def estimate(xlist, tlist):
        A = []
        for i in range(M+1):
            for j in range(M+1):
                temp = (xlist**(i+j)).sum()
                A.append(temp)
        A = np.array(A).reshape(M+1, M+1)
     
        T = []
        for i in range(M+1):
            T.append(((xlist**i) * tlist).sum())
        T = np.array(T)
        wlist = np.linalg.solve(A, T)
        return wlist
    
    wlist = estimate(xlist, ylist)

    xs = np.arange(sen[0], sen[1] + sen[2], sen[2])
    model = [y(x, wlist) for x in xs]
    
    return xs, model
