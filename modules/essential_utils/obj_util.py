def bindup(arr, wid):
    import numpy as np
    n = len(arr)
    a = np.arange(n)
    k = (np.tile(a,(n-wid+1,1)).transpose() - a[:-wid+1]).transpose()
    arr = np.tile(arr,(n-wid+1, 1))
    return arr[(k >= 0) == (k < wid) ].reshape(n-wid+1, wid)


class myiter():
    def __init__(self, lst):
        self.lst = lst
        self.iter = iter(self.lst)
        self.next()
    def next(self):
        self.curr = self.iter.next()
    def __repr__(self):
        return repr(self.curr)


def mywhere(condition):
    #wait numpypy upgrade.
    from numpy import where,array
    numlst = []
    for i,tof in enumerate(tuple(condition)):
        if tof: numlst += [i]

    return [array(numlst)]
        
    

    

class index_util(list):
    def __init__(self, index=None):
        if index: self.set_index(index)

    def set_index(self, index):
        if type(index) == str:
            if ":" in index: self.ilst = range(*[int(x) for x in index.split(":")])
            elif "," in index: self.ilst = [int(x) for x in index.split(",")] 
            else: self.ilst = [int(index)]
        elif type(index) == list:
            self.ilst = index
        else: 
            self.ilst = [index]

    def __getitem__(self, index): 
        return self.ilst[index]    



class container():
    def __init__(self, ctype="stack"):
        self.ctype = ctype
        self.luggage = None

    def stack_conca(self, *lst):
        #list is concatenated after stacking.
        if self.luggage == None:
            self.luggage = [[x] for x in list(lst)]
        else:
            self.luggage = map(lambda x, y: [x[0] + y], self.luggage, lst) 

    def trim(self):
        #Trim extra  [].
        self.luggage = map(lambda x: x[0], self.luggage) 

    def stack(self, *lst):
        if self.luggage == None:
            self.luggage = [[x] for x in list(lst)]
        else:
            self.luggage = map(lambda x, y: x + [y], self.luggage, lst) 

    def ndarr(self, whole=False):
        if whole:
            self.luggage = array(self.luggage)
        else:
            self.luggage = map(lambda x: array(x), self.luggage)

        self.dic = {}

    def keyval(self, key, val):
        if self.luggage == None:
            self.luggage = {key:val}
        self.luggage({key:val})
    
    def get_key(self, key):
        return self.dic[key]
    def get(self):
        return self.luggage

def crush_lst(lst):
    retlst = []
    n = 0
    while n < len(lst[0]):
        i = 0
        while i < len(lst):
            retlst += [lst[i][n]]
            i += 1
        n += 1
    return retlst

def crush_arr(arr):
    if type(arr) == list: arr = array(arr)
    arr = arr.transpose()
    return append(array([]), arr, axis=0)

def punch_out(x,y, plst , inv = False):
    x = array(x) if type(x) == list else x
    y = array(y) if type(y) == list else y
    for pmin, pmax in plst:
        numarr = where( inv == ((pmin <= x) * (pmax >= x)))[0]
        x = x[numarr]
        y = y[numarr]
    return x,y
    
def pullout(param, plst, glst, number=None):
    """
    'pullout' extracts a param from an array named as 'glst',
    The decision of extracted param in 'glst' is conducted by that
    an array number  coressponded with an 'param' of 'plst' is
    equivalent to those of this in 'glist'.

    Example:
    
    >>> print pullout(2, [2,3,4], [3,5,6])
    3

    >>> print pullout(3, [2,3,4], [3,5,6])
    5

    >>> print pullout(4, [2,3,4], [3,5,6])
    6
    """
    delta = float(plst[1]) - float(plst[0])
    lst_num = int(float(str((float(param) - float(plst[0]))/delta)))
    ret = glst[lst_num]
    confirm = plst[lst_num]
    if str(float(confirm)) == str(float(param)):
        if number:
            return lst_num
        else:
            return ret
    else:
        raise ValueError("'param' was not found in 'plst'")

def list_joint(lst, delim=", "):
    return "".join([str(x)+delim for x in lst]).strip(delim)
    
import inspect as i
import copy
class method_history():
    def __init__(self, obj):
        self.hlst = []
        self.obj = obj

    def deco_input(self,function):
        def _deco_input(*args, **kw):
            result = function(*args, **kw)
            self.input()
        return _deco_input

    def input(self):
        name = i.stack()[1][3]
        argdic = i.getargvalues(i.currentframe().f_back)[3]
        argdic.pop("self")
        self.hlst += [[name,argdic]]
    
    def execute(self, index=0):
        name, argdic = self.hlst[index]
        argdic = copy.deepcopy(argdic)
        for key, val in argdic.items():
            if type(val) == str:
                argdic[key] = "'%s'" %val
            
        mlst = i.getmembers(self.obj, i.ismethod)
        for mname, method in mlst:
            if mname == name:
                if argdic == {}:
                    args = ""
                else:
                    args = concatanate([concatanate(x,"=") for x in argdic.items()],", ")
                exec 'method(%s)' %args

    def execute_all(self):
        for n in range(len(self.hlst)):
            self.execute(n)

def alignment(xylst, gcolumn=0, void=0):
    import numpy as n
    initimes = map(lambda x: x[0][0], xylst)
    index = range(len(xylst))
    try:
        dts = map(lambda x: x[0][1] - x[0][0], xylst)
    except IndexError:
        retlst = xylst[0]
        return retlst
        
    retlst = []
    for time in xylst[gcolumn][0]:
        #input("time"+time)
        tmp = map(lambda p: time-p, initimes)
        #print str(initimes) + "initimes"
        #print str(tmp) + "tmp"
        g_num = map(lambda n,p: tmp[n]/p if 0 <= tmp[n] else None, index, dts)
        #print str(g_num)+"gnum"
        #print xylst[1][1]
        retlst += [map(lambda n,p: xylst[n][1][int(p)] if p != None and p < len(xylst[n][1]) else void, index, g_num)]
        #print retlst
    
    retlst = [xylst[gcolumn][0]] + n.transpose(n.array(retlst)).tolist()
    
    return retlst

def lstsplit(lst,sepnum, mod=False):
    tmplst = []
    retlst = []
    tof = False
    if type(sepnum) != int:
        sepgen = iter(sepnum) 
        tof = True

    if tof: sepnum = sepgen.next() 
    for string in lst:
        tmplst += [string]
        if len(tmplst) == sepnum:
            retlst += [tmplst]
            tmplst = []
            try:
                if tof: sepnum = sepgen.next() 
            except:
                break
    if mod: retlst += [tmplst]
    return retlst

def zeropad(num, digit):
    from numpy import zeros
    stnum = str(int(num))
    zeronum = digit - len(stnum)
    return "".join(map(lambda x: str(x), zeros(zeronum, dtype="int").tolist())) + stnum
