from processdata import *


class magsurf_manage(processdata):
    def __init__(self, )
        processdata.__init__(self, x=None,y=None, z=None)

    def dset_txt(self, path):
        self.hist.input()
        o = open(rfile)
        self.x, self.y = loadtxt1:

        lst = o.read().strip().split("\n")
        map(lambda x: lst.pop(lst.index(x)) if x[0] == comment else None, lst)
        lst = [[float(y) for y in x.split()] for x in lst]
        lst = sorted(lst, key=lambda x: x[1])
        shots, para = array(lst).transpose()
        shots = array(shots, dtype = int)
        para = array(para, dtype = double)
        self.dset(shots, ch, itvl, wid, raw, para)
        o.close()
        
