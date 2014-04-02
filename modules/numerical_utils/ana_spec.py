from ctypes import *
from numpy import *

#spec = ctypeslib.load_library("ana_spec_wf.so", ".")
spec = ctypeslib.load_library("/Users/yu/Documents/progs/py_prog/modules/numerical_utils/ana_spec_wf.so", ".")




def autocorr(tau, x, y):
    x = array(x, dtype=float)
    y = array(y, dtype=float)
    spec.autocorr_.argtypes = [
            POINTER(c_int64),
            ctypeslib.ndpointer(dtype=float64),
            ctypeslib.ndpointer(dtype=float64),
            POINTER(c_int64),
            ctypeslib.ndpointer(dtype=float64),
            ctypeslib.ndpointer(dtype=float64),
            POINTER(c_int64)]
    spec.autocorr_.restype = c_void_p
    dx = x[1] - x[0]
    if type(tau) == list:
        ret_n = abs(int((tau[1] - tau[0]) / dx))
        st_x = tau[0]
    else:
        ret_n = abs(int(tau / dx))
        st_x = 0 if tau > 0 else tau
    st_n = int(st_x / dx)
    st_n = c_int64(st_n)
    n = c_int64(x.size)
    ret_x = zeros(ret_n, dtype=float)
    ret_y = zeros(ret_n, dtype=float)
    ret_n = c_int64(ret_n)
    spec.autocorr_(byref(st_n), x, y, byref(n), ret_x,ret_y, byref(ret_n))

    return ret_x, ret_y

def crosscorr(tau, x1, y1, y2):
    x1 = array(x1, dtype=float)
    y1 = array(y1, dtype=float)
    y2 = array(y2, dtype=float)
    spec.crosscorr_.argtypes = [
            POINTER(c_int64),
            ctypeslib.ndpointer(dtype=float64),
            ctypeslib.ndpointer(dtype=float64),
            ctypeslib.ndpointer(dtype=float64),
            POINTER(c_int64),
            ctypeslib.ndpointer(dtype=float64),
            ctypeslib.ndpointer(dtype=float64),
            POINTER(c_int64)]
    spec.crosscorr_.restype = c_void_p
    dx = x1[1] - x1[0]
    if type(tau) == list:
        ret_n = abs(int((tau[1] - tau[0]) / dx))
        st_x = tau[0]
    else:
        ret_n = abs(int(tau / dx))
        st_x = 0 if tau > 0 else tau
    st_n = int(st_x / dx)
    st_n = c_int64(st_n)
    n = c_int64(x1.size)
    ret_x = zeros(ret_n, dtype=float)
    ret_y = zeros(ret_n, dtype=float)
    ret_n = c_int64(ret_n)
    spec.crosscorr_(byref(st_n), x1, y1, y2, byref(n), ret_x,ret_y, byref(ret_n))
    return ret_x, ret_y

def crosscorr_func(tau, x1, y1, y2):
    x1 = array(x1, dtype=float64)
    y1 = array(y1, dtype=float64)
    y2 = array(y2, dtype=float64)
    spec.crosscorr_func_.argtypes = [
            POINTER(c_int64),
            ctypeslib.ndpointer(dtype=float64),
            ctypeslib.ndpointer(dtype=float64),
            ctypeslib.ndpointer(dtype=float64),
            POINTER(c_int64),
            ctypeslib.ndpointer(dtype=float64),
            ctypeslib.ndpointer(dtype=float64),
            ctypeslib.ndpointer(dtype=float64),
            POINTER(c_int64),
            POINTER(c_int64)]
    spec.crosscorr_func_.restype = c_void_p
    dx = x1[1] - x1[0]
    if type(tau) == list:
        ret_row_n = abs(int((tau[1] - tau[0]) / dx))
        st_x = tau[0]
    else:
        ret_row_n = abs(int(tau / dx))
        st_x = 0 if tau > 0 else tau

    n = x1.size
    #ret_col_n = n 
    ret_col_n = n - 2 * ret_row_n
    input(ret_col_n)
    input(ret_row_n)
    st_n = int(st_x / dx)
    ret_x = zeros((ret_row_n,ret_col_n), dtype=float64)
    ret_y = zeros((ret_row_n,ret_col_n), dtype=float64)
    #ret_x = zeros((ret_col_n,ret_row_n), dtype=float64)
    #ret_y = zeros((ret_col_n,ret_row_n), dtype=float64)
    ret_lag = zeros((ret_col_n,ret_row_n), dtype=float64)
    
    n = c_int64(n)
    ret_col_n = c_int64(ret_col_n)
    ret_row_n = c_int64(ret_row_n)
    st_n = c_int64(st_n)
    spec.crosscorr_func_(byref(st_n), x1, y1, y2, byref(n), ret_x, ret_y, ret_lag, byref(ret_row_n), byref(ret_col_n))

    ret_lag = tile(array_split(arange(st_x, ret_row_n.value*dx, dx), ret_row_n.value),ret_col_n.value)
    #array(array_split(f,100)).transpose()
    return ret_x, ret_y, ret_lag
#test.crosscorr_.argtypes = [
#            POINTER(c_double),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            POINTER(c_int64),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#                                ]
#test.multi_ccorr_.argtypes = [
#            POINTER(c_double),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            POINTER(c_int64),
#            POINTER(c_int64),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            POINTER(c_int64),
#                                ]
#
#test.run_crosscorr_.argtypes = [
#            POINTER(c_double),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            POINTER(c_int64),
#            POINTER(c_int64),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            POINTER(c_int64),
#                                ]
#
#test.multi_run_ccorr_.argtypes = [
#            POINTER(c_double),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            POINTER(c_int64),
#            POINTER(c_int64),
#            POINTER(c_int64),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            ctypeslib.ndpointer(dtype=float64),
#            POINTER(c_int64),
#                                ]
#test.crosscorr_.restype = c_void_p
#test.multi_ccorr_.restype = c_void_p
#test.run_crosscorr_.restype = c_void_p
#test.multi_run_ccorr_.restype = c_void_p
#
#a = arange(0,500, dtype=float64)
#b = a*2
#tau = byref(c_double(10))
#n = c_int64(a.size)
#ret_n = c_int64(0)
#c=zeros(a.size,dtype=float)
#d=zeros(a.size, dtype=float)
#test.crosscorr_(tau,a,b, b,byref(n), c, d, byref(ret_n))
#
##print c[0:ret_n.value]
##print d[0:ret_n.value]
#
#
##q= arange(500, dtype=float)
##for n in range(30):
##    q= append([q],[q],axis=0)
##r= q *2
##
##n = c_int64(500)
##l = c_int64(len(q))
##from copy import *
##t = deepcopy(q)
##k = deepcopy(r)
##tau = byref(c_double(30))
##input(len(q))
##test.multi_ccorr_(tau,q,r,r,byref(n),byref(l), t, k, byref(ret_n))
##print t[:,0:ret_n.value]
##print k[:,0:ret_n.value]
#
#
#q= arange(500, dtype=float)
#q= tile(q, (6,2))
#r= q *2
#
#n = c_int64(500)
#l = c_int64(len(q))
#from copy import *
#tau = c_double(30)
#input(q[0][1])
#num = c_int64((abs(int(tau.value / (q[0][1] - q[0][0])))))
#t = zeros([n.value,num.value])
#k = zeros([n.value,num.value])
##t = zeros([n.value,num.value])
##k = zeros([n.value,num.value])
#time = zeros([n.value - 2 * num.value, l.value])
#test.multi_run_ccorr_(byref(tau),q,r,r,byref(n), byref(l), byref(num), time, t, k, byref(ret_n))
#print t#[:,0:ret_n.value]
##print k[:,0:ret_n.value]
