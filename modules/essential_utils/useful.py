#_*_ coding:utf-8 _*_
from numpy import *
from pylab import *
import os 


def find_dec_place(val):
    """Find decimal place.
    
    Arguments
        val -- float value.
    """
    val = str(val)
    try:
        p = val.index(".")
        return len(val) - (p + 1)
    except:
        return 0



def np_None():
    return array([None])[0]






