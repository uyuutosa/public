from numpy import *
from modules.essential_utils.numerical_util import * 
from handle_tensor import *


    
## Manipulate array as tensor.
#
# Description\n
#  tensor class manipulates the numpy ndarray as tensor.
#  tensor has some calculation rule. User follow this 
#  calculation rule, User's numerical code is more reduced
#  and more clear than using the regular array.
#  For detail information, visit address.
#  
class tensor(handle_tensor):
    ## Initialization of tensor.
    #
    # tensor has four attributes as follows,\n
    # arr -- list, tuple or numpy ndarray\n
    # ud -- index location. up or down indicates super or sub 
    # script.\n
    def __init__(self, arr, *args, **kwargs):
        tmpidx = "ijklmopqrstu"
        tmpud =  "dddddddddddd"
        idx = kwargs["idx"] if "idx" in kwargs.keys() else tmpidx
        ud =  kwargs["ud"] if "ud" in kwargs.keys() else tmpud
        name = kwargs["name"] if "name" in kwargs.keys() else "a"

        if len(args) != 0:
            idx = args[0]
            ud = args[1]

        if isinstance(arr, tensor):
            self.set_tensor(arr)
            return

        if isinstance(arr, list):
            if all([isinstance(x, tensor) for x in arr]):
                idx0 = arr[0].idx
                self.idx = idx + idx0
                self.ud =  ud + arr[0].ud
                self.name = name

                lst = []
                for obj in arr:
                    obj.transpose(idx0)
                    lst += [obj.arr]
                self.arr = array(lst)
                return 

        self.arr = array(arr) 
        self.idx = idx[0:self.arr.ndim]
        self.ud = ud[0:self.arr.ndim]
        self.name = name 
        
        
    ## \brief View the contens of tensor.
    # 
    # Description\n
    # view shows follow values,\n
    #  value -- content of array
    #  form -- tensor form (sub or super script)
    #  shape -- number of index
    def view(self):#, ndic=globals()):

        sup = ""
        sub = ""
        sup_shape = []
        sub_shape = []
        lst = []

        for n,i in enumerate(self.arr.shape):
            if self.ud[n] == "u": 
                sup += self.idx[n]
                sup_shape += [i]
            else:
                sub += self.idx[n]
                sub_shape += [i]


        lst +=  ["value----------"]
        lst +=  ["%s" %self.arr]
        lst +=  [""]
        lst +=  ["form----------"]
        lst +=  ["   " + sup]
        lst +=  [" %s " %self.name]
        lst +=  ["   " + sub]
        lst +=  [""]


        lst += ["shape---------"]
        shape = self.arr.shape
        for n in range(len(self.idx)):
            lst += ["%s : %s" %(self.idx[n], shape[n])]
        
        return "\n".join(lst)

    def __repr__(self,):
        return self.view()



    def __add__(self, obj):
        n,rdic = self.check_type(obj)
        #print n
        if n == 0:
            arr = self.arr + obj
        elif n == 1:
            arr = self.arr +  obj.arr
        elif n == 2:
            arr = self.arr +  obj.arr
            return tensor(arr, idx=obj.idx, ud=obj.ud)
        elif n == 3:
            arr = self.arr +  obj.arr
            return tensor(arr, idx=self.idx, ud=self.ud)
        elif n == 4 or n == 6:
            arr = rdic["tmp"] + obj.arr
            return tensor(arr, idx=rdic["idx"], ud=rdic["ud"])

        else:
            raise ValueError, "arr.ndim miss much."
        return tensor(arr, idx=self.idx, ud=self.ud)

    def __radd__(self, obj):
        return self + obj

    def __sub__(self, obj):
        n,rdic = self.check_type(obj)
        if n == 0:
            arr = self.arr - obj
        elif n == 1:
            arr = self.arr -  obj.arr
        elif n == 2:
            arr = self.arr -  obj.arr
            return tensor(arr, idx=obj.idx, ud=obj.ud)
        elif n == 3:
            arr = self.arr -  obj.arr
            return tensor(arr, idx=self.idx, ud=self.ud)
        elif n == 4 or n == 6:
            arr = rdic["tmp"] - obj.arr
            return tensor(arr, idx=rdic["idx"], ud=rdic["ud"])

        else:
            raise ValueError, "arr.ndim miss much."
        return tensor(arr, idx=self.idx, ud=self.ud)

    def __rsub__(self, obj):
        return -(self - obj)

    def __pow__(self, obj):
        n,rdic = self.check_type(obj)
        if n == 0:
            arr = self.arr ** obj
        elif n == 1:
            arr = self.arr **  obj.arr
        elif n == 2:
            arr = self.arr **  obj.arr
            return tensor(arr, idx=obj.idx, ud=obj.ud)
        elif n == 3:
            arr = self.arr **  obj.arr
            return tensor(arr, idx=self.idx, ud=self.ud)
        elif n == 4 or n == 6:
            arr = rdic["tmp"] ** obj.arr
            return tensor(arr, idx=rdic["idx"], ud=rdic["ud"])
        else:
            raise ValueError, "arr.ndim miss much."
        return tensor(arr, idx=self.idx, ud=self.ud)

    def __rpow__(self, obj):
        n,rdic = self.check_type(obj)
        if n == 0:
            arr = obj ** self.arr
        elif n == 1:
            arr = obj.arr **  self.arr
        elif n == 2:
            arr = obj.arr **  self.arr
            return tensor(arr, idx=self.idx, ud=self.ud)
        elif n == 3:
            arr = obj.arr **  self.arr
            return tensor(arr, idx=obj.idx, ud=obj.ud)
        elif n == 4 or n == 6:
            arr = rdic["tmp"] ** self.arr
            return tensor(arr, idx=rdic["idx"], ud=rdic["ud"])
        else:
            raise ValueError, "arr.ndim miss much."
        return tensor(arr, idx=self.idx, ud=self.ud)

    def same_trans(self, obj):
        seqlst = []
        oeqlst = []
        for i in xrange(len(self.idx)):
            for j in xrange(len(obj.idx)):
                    if self.idx[i] == obj.idx[j]:
                        seqlst += [i]
                        oeqlst += [j]
        sidx = range(len(self.idx))
        oidx = range(len(obj.idx))
        for x in seqlst: sidx.remove(x) 
        for x in oeqlst: oidx.remove(x) 
        
        self.tlst = sidx + seqlst
        obj.tlst = oidx + oeqlst
        self.transpose(self.tlst)
        obj.transpose(obj.tlst)

    def check_type(self, obj):
        rdic = {}
        try:
            self.transpose(obj.idx)
        except:
            pass
        if type(obj) == int64 or type(obj) == float64 or type(obj) == int or type(obj) == float:
            return 0, rdic
        elif obj.idx == self.idx and self.ud == obj.ud:
            return 1, rdic
        
        seqlst = []
        oeqlst = []
        sodddic = {}
        oodddic = {}
        sudeqlst = []
        oudeqlst = []
        sudoddlst = []
        oudoddlst = []
        sshape = self.arr.shape
        oshape = obj.arr.shape
        for i in xrange(len(self.idx)):
            for j in xrange(len(obj.idx)):
                if self.idx[i] == obj.idx[j]:
                    if sshape[i] != oshape[j]:
                        #print i,j
                        #print sshape, oshape
                        raise ValueError, "Index %s is not same number." %self.idx[i] 
                    seqlst += [i]
                    oeqlst += [j]
                    if self.ud[i] == obj.ud[j]:
                        sudeqlst += [i]
                        oudeqlst += [i]
                    else:
                    #    seqlst += [i]
                    #    oeqlst += [j]
                        sudoddlst += [i]
                        oudoddlst += [j]
                    #else:
                    #    #print soddlst
                    #    soddlst += [i]
                    #    ooddlst += [j]
                    
        #print "seqlst"
        #print self.idx
        #print obj.idx
        #print seqlst
        if len(seqlst) != 0:
            
                
            #print self.idx
            #print obj.idx
            sidx = range(len(self.idx))
            oidx = range(len(obj.idx))
            for x in seqlst: sidx.remove(x) 
            for x in oeqlst: oidx.remove(x) 
            
            slst = sidx + seqlst
            olst = oidx + oeqlst
            #input(seqlst)
            self.transpose(slst)
            obj.transpose(olst)
            #print len(seqlst) == len(self.idx) or len(oeqlst) == len(obj.idx)
            if len(sudeqlst) == len(self.idx): 
                rdic["shape"] = list(obj.arr.shape) 
                rdic["idx"] = obj.idx
                rdic["ud"] = obj.ud
                return 2, rdic

            elif len(oudeqlst) == len(obj.idx):
                rdic["shape"] = list(self.arr.shape) 
                rdic["idx"] = self.idx 
                rdic["ud"] = self.ud
                return 3, rdic
            
            else:
                stmp = self
                # Broadcast size of self. Shape is self > obj
                for n in range(len(oidx)): 
                    stmp = stmp.rup(obj.arr.shape[n], obj.idx[n])
                for i,c in enumerate(reversed(obj.idx)):
                    stmp.transpose([c, -1-i])
                #print stmp.idx
                #for n in sidx:
                #    otmp = otmp.rup(self.arr.shape[n], self.idx[n])
                #for n in sudoddlst:
                #    stmp = stmp.rup(obj.arr.shape[n], obj.idx[n])
                #for n in oudoddlst:
                #    otmp = otmp.cud(self.idx[n])
                
                rdic["shape"] = stmp.arr.shape
                rdic["tmp"] = stmp.arr
                rdic["idx"] = stmp.idx
                rdic["ud"] = stmp.ud
                #rdic["shape"] = list(self.arr.shape)[:-len(seqlst)] + list(obj.arr.shape)[:-len(oeqlst)] + list(self.arr.shape)[-len(seqlst):]
                #print self.idx
                #print obj.idx
                #rdic["tmp"] = outer(self.arr,  ones((obj.arr.shape)[:-len(oeqlst)])).reshape(rdic["shape"])
                ##input(rdic["tmp"].shape)
                #rdic["idx"] = "".join(list(self.idx)[:-len(seqlst)] + list(obj.idx)[:-len(oeqlst)] + list(self.idx)[-len(seqlst):])
                #input(rdic["idx"])
                #rdic["ud"] = "".join(list(self.ud)[:-len(seqlst)] + list(obj.ud)[:-len(oeqlst)] + list(self.ud)[-len(seqlst):])
                if len(oudoddlst) == 0:
                    return 4, rdic
                else:
                    rdic["tmp"] = stmp
                    return 5, rdic
        else:
                rdic["shape"] = list(self.arr.shape) + list(obj.arr.shape)
                rdic["tmp"] = outer(self.arr, ones(obj.arr.shape)).reshape(rdic["shape"])
                rdic["idx"] = "".join(self.idx + obj.idx)
                rdic["ud"] = "".join(self.ud + obj.ud)
                return 6, rdic
        
    def __rdiv__(self, obj):
        tmp = tensor(self)
        tmp.arr = 1./tmp.arr
        return obj * tmp

    def __div__(self, obj):
        tmp = tensor(obj)
        tmp.arr = 1./tmp.arr
        return self * tmp

    def __neg__(self):
        self.arr *= -1
        return self

    def __lshift__(self, obj):
        n,rdic = self.check_type(obj)
        #print n
        if n == 0:
            shape = list(self.arr.shape)[:-1] + [1]
            o = ones(shape) * obj
            arr = append(self.arr, o, axis=-1)
        elif n == 1:
            arr = append(self.arr, obj.arr, axis=-1)
        elif n == 2:
            o = (self * 0 + 1) * obj
            arr = append(obj.arr, o.arr, axis=-1)
            return tensor(arr, idx=obj.idx, ud=obj.ud)
        elif n == 3:
            o = (self * 0 + 1) * obj
            arr = append(self.arr, o.arr, axis=-1)
            return tensor(arr, idx=self.idx, ud=self.ud)
        else:
            raise ValueError, "arr.ndim miss much."
        return tensor(arr, idx=self.idx, ud=self.ud)
      
    

    def __rshift__(self, obj):
        n,rdic = self.check_type(obj)
        if n == 0:
            shape = list(self.arr.shape)[:-1] + [1]
            o = ones(shape) * obj
            arr = append(o, self.arr, axis=-1)
        elif n == 1:
            arr = append(obj.arr, self.arr, axis=-1)
        elif n == 2:
            o = (obj * 0 + 1) * self
            arr = append(self.arr, o.arr, axis=-1)
            return tensor(arr, idx=obj.idx, ud=obj.ud)
        elif n == 3:
            o = (obj * 0 + 1) * self
            arr = append(self.arr, o.arr, axis=-1)
            return tensor(arr, idx=self.idx, ud=self.ud)
        else:
            raise ValueError, "arr.ndim miss much."
        return tensor(arr, idx=self.idx, ud=self.ud)
    
    def roll(self, lst):
        if self.arr.ndim == 1: return 0
        tlst = range(self.arr.ndim)
        lst = [len(self.idx) + x if x < 0 else x for x in lst]
        self.arr = self.arr.transpose(roll(tlst, lst[1] - lst[0]))

        self.idx = roll_str(self.idx, lst[1] - lst[0])
        self.ud = roll_str(self.ud, lst[1] - lst[0])

    def transpose(self, lst=None, opt=False):
        if self.arr.ndim == 1: return 0
        if type(lst) == str: lst = self.index(lst)
        if type(lst[0]) == str: lst[0] = self.index(lst[0])

        lst = [self.arr.ndim + x if x <0 else x for x in lst]
        if self.arr.ndim != len(lst) and len(lst) == 2:
            d = lst[1] - lst[0]
            m = zeros(self.arr.ndim)
            m[lst[0]] += d
            m[lst[1]] += -d
            lst = (arange(self.arr.ndim) + m).tolist()
        elif self.arr.ndim == len(lst) and len(lst) == 2:
            if opt == True: 
                lst = [1,0]
            

        if lst is None: lst = self.tlst
        
        try:
            self.arr = self.arr.transpose(lst)
        except:
            #print lst
            #print "repeated transform"
            return
        self.idx = "".join(array(list(self.idx))[lst].tolist())
        self.ud = "".join(array(list(self.ud))[lst].tolist())

    def __rmul__(self, obj):
        return self * obj

    def __mul__(self, obj):
        n,rdic = self.check_type(obj)
        #print "n is " + str(n)
        if n == 0:
            arr = self.arr * obj
            return tensor(arr, idx=self.idx, ud=self.ud)
        elif n == 1:
            arr = self.arr *  obj.arr
            return tensor(arr, idx=self.idx, ud=self.ud)
        elif n == 2:
            arr = self.arr *  obj.arr
            return tensor(arr, idx=obj.idx, ud=obj.ud)
        elif n == 3:
            arr = self.arr *  obj.arr
            return tensor(arr, idx=self.idx, ud=self.ud)
        elif n == 4:
            arr = rdic["tmp"] * obj.arr
            return tensor(arr, idx=rdic["idx"], ud=rdic["ud"])
    
        elif n == 5 or n == 7:   
            for i in xrange(len(self.idx)):
                for j in xrange(len(obj.idx)):
                    if self.idx[i] == obj.idx[j]:
                        if self.ud[i] != obj.ud[j]:
                            if obj.arr.ndim == 1:
                                self.roll([i, -2])
                                arr = dot (obj.arr, self.arr)
                                idx = self.idx[:-2] + self.idx[-1:] + obj.idx[:-1] 
                                ud = self.ud[:-2] + self.ud[-1:] + obj.ud[:-1] 
                                self.roll([-2, i])
                                ret = tensor(arr, idx=idx, ud=ud)
                            else:
                                stmp  = rdic["tmp"]
                                tmp = stmp.cud(self.idx[i]) * obj
                                ret = tmp.sum(self.idx[i])
                            if not isinstance(ret, tensor):
                                return ret
                            lst = ret.check_odd_ud()
                            while lst:
                                if lst is not None:
                                
                                    mask = eye(ret.arr.shape[lst[0]])
                                    o = ones(ret.arr.shape[lst[0]])
                                    idxlst = range(len(ret.idx))
                                    for x in lst: idxlst.remove(x) 
                                    tlst = idxlst + lst
                                    arr= ret.arr.transpose(tlst)
                                    
                                    arr *= mask
                                    arr = dot(dot(arr, o), o)
                                    idx = "".join(array(list(idx))[tlst][:-2])
                                    ud = "".join(array(list(ud))[tlst][:-2])
                                    if len(idx) == 0:
                                        return arr
                                ret = tensor(arr, idx=idx, ud=ud)
                                lst = ret.check_odd_ud()

                            lst = ret.check_same_ud()
                            while lst:
                                if lst is not None:
                                
                                    mask = eye(ret.arr.shape[lst[0]])
                                    o = ones(ret.arr.shape[lst[0]])
                                    idxlst = range(len(ret.idx))
                                    for x in lst:  idxlst.remove(x) 
                                    tlst = idxlst + lst
                                    arr=ret.arr.transpose(tlst)
                                    arr *= mask
                                    arr = dot(arr, o)
                                    idx = "".join(array(list(idx))[tlst][:-1])
                                    ud = "".join(array(list(ud))[tlst][:-1])
                                    if len(idx) == 0:
                                        return arr
                                ret = tensor(arr, idx=idx, ud=ud)
                                lst = ret.check_same_ud()
                            return ret

        else:
            shape = list(self.arr.shape) + list(obj.arr.shape)
            arr = outer(self.arr, obj.arr).reshape(shape)
            idx = self.idx + obj.idx
            ud = self.ud + obj.ud
            return tensor(arr, idx=idx, ud=ud, name="tmp")

    def check_odd_ud(self,):
        for i in xrange(len(self.idx)):
            for j in xrange(len(self.idx)):
                if self.idx[i] == self.idx[j] and self.ud[i] != self.ud[j]:
                    return [i, j]
        return None
                        
    def check_same_ud(self):
        for i in xrange(len(self.idx)):
            for j in xrange(len(self.idx)):
                if i != j and self.idx[i] == self.idx[j] and self.ud[i] == self.ud[j]:
                    return [i, j]
        return None

                    
    def len(self, idx, ret=False):
        obj = self
        for c in idx:
            if c in obj.idx:
                N = obj.arr.shape[obj.idx.find(c)]
                return N
        raise ValueError, "Index was not found."

    def gud(self, idx):
        obj = self
        for c in idx:
            if c in obj.idx:
                N = obj.ud[obj.idx.find(c)]
                return N
        raise ValueError, "Index was not found."

    def index(self, idx):
        """
            Change up or down 
        """
        lst = []
        for c in idx:
            #print c
            #print self.idx
            N = self.idx.index(c)
            lst += [N]
        if len(lst) == 1: lst = lst[0]
        return lst
            

    def cud(self, idx, ret=False):
        """
            Change up or down 
        """
        obj = self
        t = {"u": "d", "d": "u"}
        for c in idx:
            if c in obj.idx:
                N = obj.idx.find(c)
                ud = list(self.ud)
                ud[N] = t[self.ud[N]]
                return tensor(self.arr, self.idx, "".join(ud))
        raise ValueError, "Index was not found."
    
    def cidx(self, pre, idx):
        """
            Change up or down 
        """
        obj = self
        t = {"u": "d", "d": "u"}
        if pre in obj.idx:
            N = obj.idx.find(pre)
            
            ilst = list(self.idx)
            ilst[N] = idx
            return tensor(self.arr, "".join(ilst), self.ud)
        raise ValueError, "Index was not found."


    def set_tensor(self, obj):
        a = array([])
        if isinstance(obj, tensor): 
            self.idx = obj.idx
            self.ud = obj.ud
            self.arr = array(obj.arr)
            self.name = obj.name

        elif type(obj) == list or type(obj) == type(a):
            tmp = tensor(obj)
            self.set_tensor(tmp)
               
    def __call__(self,):
        return self.view()

    def __getitem__(self, i):
        if isinstance(i, int): i = tuple([i])
        if isinstance(i, slice): i = (i,)
        d = len(self.arr.shape) - len(i)
        if d != 0:
            lst = list(i)
            for x in range(d):
                lst += [slice(None, None, None)] 
            i = tuple(lst)
        
        lst = []
        for n in i:
            if type(n) == slice:
                lst += [True]
            else:
                lst += [False]

        tof = array(lst)
        idx = self.idx
        ud = self.ud
        if not all(tof):
            idx = "".join(array(list(self.idx))[array(lst)])
            ud =  "".join(array(list(self.ud))[array(lst)])

        
        a = array([])
        val = self.arr[i]
        if type(a) == type(val):
            ret = tensor(val, idx, ud)
        else:
            ret = val
            
        return ret



class tensor_eye(tensor):
    def __init__(self,N, **kwargs):
        tensor.__init__(self, eye(N), **kwargs)

class tensor_ps(tensor):
    def __init__(self,N, **kwargs):
        tensor.__init__(self, permutation_symbol_array(N), name="ep", **kwargs)


def t_sin(obj):
    return tensor(sin(obj.arr), obj.idx, obj.ud)
def t_cos(obj):
    return tensor(cos(obj.arr), obj.idx, obj.ud)
def t_exp(obj):
    return tensor(exp(obj.arr), obj.idx, obj.ud)
def t_sqrt(obj):
    return tensor(sqrt(obj.arr), obj.idx, obj.ud)

