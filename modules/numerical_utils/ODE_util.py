from multidimensional_util.handle_3d import handle_3d
from tensor_utils.tensor import * 
from numpy import *

# euler method
def euler(t, g, y0, h):
    f = tensor(g(t), "j", "d")
    o = tensor(ones(N), "j", "u")
    T = tensor(tri(N), "ij", "dd")

    y = y0 + f * h * T * o

    t = append(t, t[-1]+h)
    y.arr = append(array([y0]),y.arr)
    return handle_3d(t, y.arr)

#RK2
def RK2(t, g, y0, h):
    def k(x):
        a = (g(x) + g(x+h)) / 2.  
        return a
    f = tensor(k(t), "j", "d")

    o = tensor(ones(N), "j", "u")
    T = tensor(tri(N), "ij", "dd")

    y = y0 + f * h * T * o

    t = append(t, t[-1]+h)
    y.arr = append(array([y0]),y.arr)
    return handle_3d(t, y.arr)

#RK4
def RK4(t, g, y0, h):
    def k(x, y):
        k1 = g(x, y)
        k2 = g(x+0.5*h, y+0.5*k1)
        k3 = g(x+0.5*h, y+0.5*k2)
        k4 = g(x+h, y+0.5*k3)
        a = (k1 + 2*k2 + 2*k3 + k4)/6.  
        return a

    f = tensor(k(t), "j", "d")
    o = tensor(ones(N), "j", "u")

    y = y0 + f.convolve(o, idx="j") * h

    t = append(t, t[-1]+h)
    y.arr = append(array([y0]),y.arr)
    return handle_3d(t, y.arr)

def RK4_tensor(x, g, y0, h, sidx="i", didx="z", **kwarg):
    def k(x, y0, **kwarg):
        k1 = g(x, y0, **kwarg)
        k2 = g(x+0.5*h, y0+0.5*k1, **kwarg)
        k3 = g(x+0.5*h, y0+0.5*k2, **kwarg)
        k4 = g(x+h, y0+0.5*k3, **kwarg)
        a = (k1 + 2*k2 + 2*k3 + k4)/6.  
        return a
    f = k(x, y0, **kwarg) * h
    N = f.len(sidx)
    o = tensor(ones(N), didx, "u")
    y = f.convolve(o, idx=sidx)  
    #y = y0 + f.convolve(o, idx=sidx)  
    #x = x << x[-1] + h
    #y = y0.append(y, sidx)
    return x, y
    
def RK4_tensor_poor(x, g, y0, h, sidx="i", didx="z", **kwarg):

    x.transpose([sidx, 0])
    prey = y0
    xlst = []
    ylst = []
    for i in xrange(x.len(sidx)):
        tmpx = x[i]
        tmpy = prey
        
        k1 = g(tmpx, tmpy, **kwarg)
        k2 = g(tmpx+0.5*h, tmpy+0.5*h*k1, **kwarg)
        k3 = g(tmpx+0.5*h, tmpy+0.5*h*k2, **kwarg)
        k4 = g(tmpx+h, tmpy+h*k3, **kwarg)
        f = (k1 + 2*k2 + 2*k3 + k4)/6.  

        tmpy = prey + f * h
        xlst += [tmpx]
        ylst += [tmpy]
        prey = tmpy
    return tensor(xlst, sidx, x.ud[0]), tensor(ylst, sidx, x.ud[0])

def RK5(t, g, y0, h):
    def k(x):
        a = (23*g(x) +125*g(x+h/3.) - 81*g(x+2*h/3) + 125*g(x+4.*h/5.)) / 192.  
        return a
    f = tensor(k(t), "j", "d")
    o = tensor(ones(N), "j", "u")
    T = tensor(tri(N), "ij", "dd")

    y = y0 + f * h * T * o

    t = append(t,t[-1]+h)
    y.arr = append(array([y0]),y.arr)
    return handle_3d(t, y.arr)
                                                    
