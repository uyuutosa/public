import heliac_f2py as a
from numpy import *

def get_xy(shot, ch):
    a.dataret.get_xy(shot, ch)
    ret =  array(a.dataret.xy)
    a.dataret.deallo_xy()
    return ret

def get_multixy(shots, chs, itvl=0.01, wid=0.1, raw=0):
    a.dataret.get_multixy(shots, chs, itvl, wid, raw)
    ret =  array(a.dataret.multixy)
    a.dataret.deallo_xy()
    return ret
 
def get_dset(dlsts):
    inlst = []
    instr = []

    l_max = max(map(lambda y: max(map(lambda x: len(x), y)), dlsts))

    for dlst in dlsts:
        for dstr in dlst:
            d = l_max - len(dstr)
            if d != 0:
                dstr = add_blnk(dstr, d)
            instr += [array(list(dstr))]
        inlst += [instr]
        instr = []
    a.dataret.get_dset(inlst)

def add_blnk(line, n):
    for b in range(n):
        line += " "
    return line

#for test in range(100):
#get_xy(80000,"pc")
#print "done"
#a=get_multixy([80000,80001,80002],"rf")
#print a
#print get_multixy([80000,80000],["pp","cb"])

