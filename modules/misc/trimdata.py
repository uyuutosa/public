#_*_coding:utf-8_*_
from numpy import *
from useful import alignment
from calc import pfit

def prmconv(paralst, tmplst):
    """
    'prmconv' convert a value as decline in 'paralst' 
    to new value baced on the config data as decline in 'tmplst'.

    Example:

    >>> print prmconv([2,3,3.5,7],[[1,2,3,4,5,6,7],[3,4,5,6,7,8,9]])
    [4.0, 5.0, 5.5, 9.0]

    """
    from numpy import array, where, ndarray
    origlst, convlst = array(tmplst,dtype=float)
    retlst = []
    for para in array(paralst,dtype=float):
        try:
            nummin = where(origlst <= para)[0][-1]
            nummax = where(origlst >= para)[0][0]
            orig_paramin = origlst[nummin]
            orig_paramax = origlst[nummax]
            orig_delta = orig_paramax - orig_paramin
            if orig_delta != 0:
                ratio = (para - orig_paramin) / orig_delta
                conv_paramin = convlst[nummin]
                conv_paramax = convlst[nummax]
                conv_delta = conv_paramax - conv_paramin
                ret = conv_delta * ratio + conv_paramin
            else:
                ret = convlst[nummin]
            retlst += [ret]
        except IndexError:
            retlst += [para]
             

    return retlst


def tieup(lst, d): 
    """
    'tieup' ties up a list or numpy.array.
    In paticular, 'tieup' recieves a 'lst' as a list or array,
    numerical data in 'lst' separate every 'd',
    separated data is averaged severally.
    A retern data is this averged array. 

    Example:

    >>> print tieup([0, 5 ,6 ,11 ,23 ,32 ,33 ,34], 10)
    [  5.5  11.   23.   33. ]


    """
    tmp = array(lst)
    ret = array([])
    cntr = tmp[0]
    while True:
        if tmp[-1] < cntr:
            return ret[::-1]
            break
        ret = append(mean(tmp[where(((cntr + d) <= tmp) == (cntr >= tmp))[0]]), ret)
        cntr += d

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

def fit_diff(xlst, ylst, time, slicelst=None, M=1, sen=(20, 40, 500), check=None):
    """
    'fit_diff' provides diffarential data between a dataset ('xlst' and 'ylst')
    and fitting dataset (on itself).

    Fitting is conducted using dataset but the range of dataset specifies by 'slicelst'.
    'slicelst' is assigned as forrows,

    slicelst = [[x_min1,x_max1], [x_min2, x_max2], [x_min3,x_max3], ...]

    The fitting sensitivity is setted on 'sen' param. 'sen' contains 
    
    (min value, max value, data number)
    
    Fitting dataset is made in the range of 'min value' and 'max value'.
    'data number' assigns the number of the data point.


    Example:
    
    >>> print fit_diff(array([0,1,2,3,4,5,6,7]), array([5,5,5,2,2,5,5,5]), 3, [[1,2],[5,6]], M=1, sen=(0,10,500))
    3.0
    
    """
    import pylab as p
    import numpy as n
    
    xlst = xlst.tolist()
    ylst = ylst.tolist()

    dt = xlst[1] - xlst[0]
    tmpxlst = []
    tmpylst = []
    a=[]
    for s in slicelst:
        smin = (s[0] - xlst[0]) / dt
        smax = (s[1] - xlst[0]) / dt
        tmpxlst += xlst[int(smin):int(smax)]
        tmpylst += ylst[int(smin):int(smax)]
        
    
    fxlst,fylst = pfit(n.array(tmpxlst), n.array(tmpylst), M=M, sen=sen)

    a=alignment([[xlst,ylst],[fxlst,fylst]])
    diff = pullout(time, a[0], a[2]) - pullout(time, a[0], a[1])

    if check:
        p.plot(a[0],a[1])          
        p.plot(a[0],a[2])          

    return diff     


if __name__ == "__main__":
    import doctest
    doctest.testmod()
