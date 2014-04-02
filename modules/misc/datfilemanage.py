from useful import *

class loaddatmanage():
    def __init__(self):
        self.dat = None
        self.history = []

    def detainput(self, key, val):
        self.datdic

    def get_contents(self, dirpath):
        import glob as g
        ret = g.glob(dirpath + "/*")
        return ret
    
    def get_multicontents(self, dirpath, taglst):
        import glob as g
        retlst = []
        for tag in taglst:
            retlst += [g.glob(dirpath + "/*" + tag  + "*")]

        self.history += [retlst]
        return retlst

    def loadmultiprof_wg(self, dirpath, taglst):     
        # This method can be used in a data outputed by graphmake.
        datpathlsts = self.get_multicontents(dirpath, taglst)
        arrlsts = []
        for datpathlst in datpathlsts:
            time = float(datpathlst[0].split("/")[-1][2:datpathlst[0].index("_")])
            arrlst = [loaddat(datpathlst[0])]
            tmp = ones(len(arrlst))
            arrlst = [tmp*time] + arrlst
            for datpath in datpathlst[1:]:
                time = float(datpath.split("/")[-1][2:dathpath.index("_")])
                arrlst += [ [tmp*time] + loaddat(datpath)]
            arrlsts += [arrlst]
        self.history += [arrlsts]
        return arrlsts

    def loadprofdat_wg(self, dirpath):
        # This method can be used in a data outputed by graphmake.
        datpathlst = self.get_contents(dirpath)
        xarrs = []
        yarrs = []
        zarrs = []
        for datpath in datpathlst[1:]:
            yarr , zarr = loaddat(datpath)
            yarrs += [yarr]
            zarrs += [zarr]
            tmp = ones(len(yarr))
            line = datpath.split("/")[-1]
            xarrs += [float(line[2:line.index("_")]) * tmp]

        return array([array(xarrs),array(yarrs),array(zarrs)])

    def loadprofdat(self, dirpath):
        datpathlst = self.get_contents(dirpath)
        xarrs = []
        yarrs = []
        zarrs = []
        for datpath in datpathlst[1:]:
            tmparr = loaddat(datpath)
            xarrs += [tmparr[0]]
            yarrs += [tmparr[1]]
            if len(tmparr) == 3: zarrs += [tmparr[2]]  

        #return array([array(xarrs),array(yarrs),array(zarrs)])
        retlst = [xarrs, yarrs, zarrs]
        return map(lambda x: array(x) if len(x) != 0 else None, retlst)
     
    def loadmultiprof(self, dirpath, taglst):     
        datpathlsts = self.get_multicontents(dirpath, taglst)
        arrlsts = []
        for datpathlst in datpathlsts:
            line = datpathlst[0][datpathlst[0].index("/")+1:]
            time = float(line[2:line.index("_")])
            arr = loaddat(datpathlst[0])
            tmp = ones(len(arr[0]))
            xyz = append([tmp*time], arr, axis=0)
            arrs = array([xyz])
            for datpath in datpathlst[1:]:
                arr = loaddat(datpath)
                line = datpath[datpath.index("/")+1:]
                time = float(line[2:line.index("_")])
                tmp = ones(len(arr[0]))
                xyz = append([tmp*time], arr, axis=0)
                arrs = append(arrs, [xyz], axis=0)
            arrlsts += [arrs]
        self.history += [arrlsts]
        return arrlsts

        

#a = loaddatmanage()
#arr=a.loadmultiprof("testdir",["1.txt","_2.txt"])
##arr=a.loadprofdat("testdir")
##from pylab import *
#ion()
#n = 0
#input(a.history)
#while len(arr[0]) > n:
#    ylim(-0.2,0.2)
#    plot(arr[0][n][0], arr[0][n][1], "ro")
#    plot(arr[1][n][0], arr[1][n][1], "bo")
#    draw()
#    clf()
#    n += 1
##input()
