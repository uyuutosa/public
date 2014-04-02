class loaddat_util():
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

def loaddat(fpath, comments="#", delim=None):
    from numpy import array,append
    o = open(fpath, "r")
    cnt = True
    for  line in o:
        if line[0] == comments:
            continue
        if len(line) == 0:
            continue
        line = line.strip()
        if delim == None:
            try:
                line.index(",")
                delim = ","
            except ValueError:
                delim = " "
        if line[-len(delim):] == delim: line = line[:-len(delim)]
        lst = map(lambda x: float(x.strip()),line.split(delim))
        #lst = line.split(delim)
        if cnt:
            retlsts = []
            cnt = False
            for tmp in range(len(lst)):
                retlsts += [array([])]
       
        #retlsts = map(lambda x,y: x.append(y), retlsts, lst)
        retlsts = map(lambda x,y: append(x, y), retlsts, lst)
    return array(retlsts)

class writedat_util():
    def __init__(self):
        self.history = []
        self.id = None
        self.dirpath = "tmp"
        self.tevopath = "tmp"
        self.tevoname = "tmp"
        self.tag = "tmp"
    
    def mkdir(self, path= None):
        import os
        if path == None: path = self.dirpath
        os.mkdir(path)
        
    def simpledump(self, path, datlst, tag="tag", delimiter=", "):
        wfile = open(path,"w")
        
        arrs = []
        for arr in datlst:
            if arr != None:
                arrs += [arr]
        arrs = array(arrs)

        writeline = "#%s\n"%tag
        for arr in arrs.transpose():
            writeline += "%s\n" %(concatanate(arr, delimiter))
        
        wfile.write(writeline)
        wfile.close()
        return "Done"


    def writedat(self, path,datlst,tag="tag",delimiter=", "):
        """
        this function generates a data file from any data list(or tupple).
        The variable "tag" is written above the file after "#". 
        
        Where, a lists is inputed into 'writedat' function.
        
        >>> import os
        >>> path = os.environ["HOME"] + "/Desktop/test_writedat.txt"
        >>> done = writedat(path,[[0,1,2,3,4,5],[2,3,4,5,6,7],[3,4,65,6,7,5]],"xtag")
        """
        wlines = map((lambda x:""),range(len(datlst[0])))
        wfile = open(path,"w")
        #print datlst
        #print "datlst"
        for dat in datlst:
        
        
            n=0
            #print dat
            #print "dat"
            for line in dat:
                #print line
                if str == type(line):
                    wlines[n] += "%20.20s%s"%(line, delimiter)
                else:
                    wlines[n] += "%16.4e%s"%(line, delimiter)
                    
    #            print str(line) + delimiter
    #            wlines[n] += str(line) + delimiter
                n += 1
        
        wfile.write("#%s\n"%tag)
        for wline in wlines:
            wline = wline[:-1]
#            print wline
            wfile.write(wline+"\n")
        
        wfile.close()
        return "Done"

#    def writeprofs(self, paradatalst, tag="", writepath=None, namelst=None, leglst=None):
#        """
#            pradatalst contains,
#                paradatalst = [[paralst, datarrs],...]
#
#                paralst : self inputed parameter. ex) radial position, vertical position, angle and so on...
#                datarrs : series multiple data. ex) timedata, currentdata and so on...
#        """
#        #self.mkdir(writepath if writepath else self.writepath)
#        dlsts = []
#        for paralst, datarrs in paradatalst:
#            dlsts += [self.add_param(paralst, datarrs)]
#            
#        for i, dlst in enumerate(dlsts):
#            for dl in dlst:
#                self.writedat("%s/x%s_leg%s.txt" %(self.writepath, dl[1,0], leglst[i] if leglst else "dat%s" %i), dl, tag=namelst)
#        print "Done."

    def write_tevo(self, dcls, tevopath=None, tevoname=None, tag=None):

        if tevopath == None: tevopath = self.tevopath
        if tevoname == None: tevoname = self.tevoname
        if tag == None: tag = self.tag
        if dcls.T:
            dcls.transpose()
        dirpath = fcnt(tevopath)
        self.mkdir(dirpath)
        n = 0
        while n < len(dcls.x):
            dlst = []
            if dcls.x != None: dlst += [dcls.x[n]]
            if dcls.y != None: dlst += [dcls.y[n]]
            if dcls.z != None: dlst += [dcls.z[n]]
            self.writedat(fcnt(dirpath, tevoname, "txt"), dlst, tag)
            n += 1
        #map(lambda x,y,z: self.writedat(fcnt(dirpath, tevoname, "txt"), (x,y,z), tag), dcls.x, dcls.y, dcls.z)
        
#import calc
#[[a,b],[g,g]]=calc.calc("pc",80000)
#[[a,c],[g,g]]=calc.calc("pc",80000)
#d.writeprofs([[[12,13],array([[a,b,c],[a,b,c]])]])

def fcnt(path, name=None, extension=None):
    """
    This function add count on a filename.
    
    >>> import os;path = os.environ["HOME"];name="asd";ext="dat"; a=open(path+"/"+name+"."+ext,"w"); a.close()
    
    >>> type(fcnt(path,name,ext)) == str
    
    """
    from obj_util import zeropad

    if extension != None:
        extension = "." + extension
    else:
        extension = ""
    
    import glob as g
    if name != None:
        tmp = path + "/" + name + "_" + zeropad(1,4) + extension
    else:
        tmp = path + "_" + zeropad(1,4) 
    for n in range(2,10000):
        file = g.glob(tmp)
        if len(file) == 0:
            if n==2:
                if name != None:
                    tmp = path + "/" + name + "_" + zeropad(1,4) + extension  
                else:
                    tmp = path + "_" + zeropad(1,4) 
            return tmp
            break
        else:
            if name != None:
                tmp = path + "/" + name + "_" + zeropad(n,4) + extension  
            else:
                tmp = path + "_" + zeropad(n,4) + extension
