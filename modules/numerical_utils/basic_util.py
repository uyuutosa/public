from numpy import *

def chg(x, y):
    if type(x) == int: x = float(x)
    if type(y) == int: x = float(y)
    return (x/y - 1) * 100 

def trapezoid(x,y):
    dx = x[1] - x[0]
    return sum(dx * (y[1:] + y[:-1]) / 2)

def ascale(arr, margin=0.1):
    #autoscale
    r = 1. / arr.ptp()
    retmin = (r * arr.min() - margin) / r
    retmax = (r * arr.max() + margin) / r
    return retmin, retmax
