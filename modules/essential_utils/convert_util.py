from numpy import *
from obj_util import *

def val2index(refarr, vallst):
    retlst = []
    for val in vallst:
        retlst += [mywhere(array(array(refarr, dtype=float), dtype=str) == str(float(val)))[0][0]]
    return retlst

def rm_naninf(abarr, lgarr):
#    abarr = abarr[mywhere(lgarr == lgarr)[0]]
#    lgarr = lgarr[mywhere(lgarr == lgarr)[0]]
#    abarr = abarr[mywhere(lgarr != inf)[0]]
#    lgarr = lgarr[mywhere(lgarr != inf)[0]]
#    abarr = abarr[mywhere(lgarr != -inf)[0]]
#    lgarr = lgarr[mywhere(lgarr != -inf)[0]]
    blarr = (lgarr!=inf) == (lgarr==lgarr)
#    input(blarr)
#    input(abarr
    return abarr[blarr], lgarr[blarr]

def num_dcml(val):
    val = str(val)
    try:
        val.index(".")
        if "0" == val[-1]:
            val = val[:-1]
    except:
        val += "."
    return len(val) - val.index(".") - 1

def sig_fig(val, num):
    """
        significant figure
    """
    posinega = -1 if val < 0 else 1
    val = abs(val)
    if (int == type(num) and num != 0):
        pass
    else:
        raise ValueError , "Number of significant figures must be integer and not zero. %s is invalid value." %num
    return posinega * round(val, - (int(log10(val) - (1 if val < 1 else 0))) + num - 1)

def prmconv(paralst, cnvlst, comments="#", delim=","):
    """
    'prmconv' convert a value as decline in 'paralst' 
    to new value baced on the config data as decline in 'cnvlst'.
    if a text file path name which has string type substitute 'cnvlst',
    convert data contained the file is read.
    """
    from numpy import array, where, ndarray
    #if (type(paralst) != list and type(paralst) != ndarray) == False:
    #    paralst = [paralst]
    if type(cnvlst) == str:
        cnv1, cnv2 = loaddat(cnvlst, comments, delim)
        cnvlst = [cnv1, cnv2]

    origlst, convlst = array(cnvlst,dtype=float)
    retlst = []
    for para in array(paralst,dtype=float):
        try:
            nummin = mywhere(origlst <= para)[0][-1]
            nummax = mywhere(origlst >= para)[0][0]
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
