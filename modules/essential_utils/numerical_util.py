def trapezoid(x,y):
    dx = x[1] - x[0]
    return sum(dx * (y[1:] + y[:-1]) / 2)



def ascale(arr, margin=0.1):
    #autoscale
    r = 1. / arr.ptp()
    retmin = (r * arr.min() - margin) / r
    retmax = (r * arr.max() + margin) / r
    return retmin, retmax


def dec2bin(val, precision=10):
    """Convert decimal number to binary number.
    """
    n = 1
    vallst = str(val).split(".")
    if len(vallst) == 2:
        ret = "%s." %bin(int(vallst[0]))
        x = float(vallst[1]) / (10 ** int(len(vallst[1])))
        for i in xrange(precision):
            if 2 * x < 1: 
                ret += "0"
                x *= 2
            elif 2 * x > 1: 
                ret += "1"
                x = 2 * x - 1
            else:
                ret += "1"
                break
    else:
        ret =  bin(int(vallst[0]))
        
     
    return ret
        
        
        
def prime(N):
    from numpy import arange, where
    a = arange(2, N+1)
    for i in xrange(2, N+1): a = a[where((a <= i) + (a%i != 0))]
    return a
