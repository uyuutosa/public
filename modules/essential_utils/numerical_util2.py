from numpy import *

def permutation_symbol_array(n):
    lst = [":%s" %n for x in xrange(n)]
    lst2 = [":" for x in xrange(n+1)]
    lst2[-1] = "::-1"
    line = "ret =  mgrid[" + ",".join(lst) + "].transpose()[" + ",".join(lst2) + "]"
    exec line
    return apply_along_axis(permutation_symbol, n, ret)

def permutation_symbol(arr):
    try:
        ret = permutation_num(arr)
        return 1 if ret%2 == 0 else -1
    except ValueError:
        return 0

def permutation_num(arr, idxarr=None):
    arr = array(arr)
    if idxarr is None: idxarr = arange(arr.size)
    c = arr - idxarr
    if arr.size != unique(arr).size:
    #if c.sum() != 0 or arr.size != unique(arr).size:
        raise ValueError, "array is not invalid."
    plus = c[where(c > 0)]
    minus = c[where(c < 0)] * -1
