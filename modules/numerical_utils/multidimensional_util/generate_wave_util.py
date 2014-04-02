from modules.numerical_utils.multidimensional_util.handle_3d import handle_3d
from modules.numerical_utils.speana_util import *

import numpy as np

def step_gw(amp=1., period=100, num=100, offset=0, wnum=1):
    """Generate step function

    """
    x = np.arange(0, period*wnum, num)
    #x = np.arange(0, period*wnum, wnum*num)
    y = np.array([])
    y = np.append(y, zeros(x.size/(2*wnum)))
    y = np.append(y, ones(x.size/(2*wnum))) * amp * 1. + offset
    y = np.tile(y, wnum)
    return x, y
        
def discrete_sin_gw(amp=1., period=100, phase=0, dnum=1000, num=100, offset=0, wnum=1):
    """Generate step function

    """
    x = np.linspace(phase, period*wnum+phase, wnum*dnum)
    y = np.zeros(wnum*dnum)
    y[::dnum/num] = np.sin(x[0::dnum/num] / period * 2* pi) + offset

    y = np.tile(y, wnum)
    return x, y

def func_gw(func="y=x", st=0, en=10, num=100, wnum=1):
    """Generate step function

    """
    x = np.linspace(st, en, num)
    exec "y = " + func 

    x = np.linspace(st, wnum*en, wnum*num)
    y = np.tile(y, wnum)
    return x, y

def sinc_gw(amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
    """Generate step function

    """
    x = np.linspace(phase, period*wnum+phase, wnum*num)
    y = np.sinc(x[0:num] / period * 2 * pi) + offset

    y = np.tile(y, wnum)
    return x, y

def harmonic_gw(hnum=2, weight=1, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
    import itertools as it
    """Generate step function

    """
    x = np.linspace(phase, period*wnum+phase, wnum*num)
    y = zeros(num)
    try:
        weight.__iter__
        wit = it.cycle(weight)
    except:
        wit = it.cycle([weight])
        #wit = it.cycle([weight] if type(weight) != list else weight)
    hnumlst = arange(hnum) + 1
    for i in hnumlst:
        y += wit.next() * np.sin(i * x[0:num] / period * 2 * pi) + offset


    y = np.tile(y, wnum)
    return x, y
    
def sin_freq_gw(hnum=2, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
    import itertools as it
    """Generate step function

    """
    x = np.linspace(phase, period*wnum+phase, wnum*num)
    y = zeros(num)
    y = np.sin(hnum * x[0:num] / period * 2 * pi) + offset
    y = np.tile(y, wnum)
    return x, y

def sin_gw(amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
    """Generate step function

    """
    x = np.linspace(phase, period*wnum+phase, wnum*num)
    y = np.sin(x[0:num] / period * 2 * pi) + offset

    y = np.tile(y, wnum)
    return x, y

def cos_gw(amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
    """generate step function

    """
    x = np.linspace(phase, period*wnum+phase, wnum*num)
    y = np.cos(x[0:num] / period * 2 * pi) + offset
    y = np.tile(y, wnum)
    return x, y

def delta_gw(amp=1., period=100, num=100, offset=0, wnum=1):
    """Generate step function

    """
    y = np.array([])
    y = np.append(y, zeros(num/2))
    y = np.append(y, 1) * amp * 1. + offset
    y = np.append(y, zeros(num/2))
    y = np.tile(y, wnum)
    x = np.linspace(0, period*wnum, wnum*y.size)
    return x, y

def flat_gw(amp=1., period=100, num=100, offset=0, wnum=1):
    """Generate step function

    """
    y = np.ones(num) * amp * 1. + offset
    y = np.tile(y, wnum)
    x = np.linspace(0, period*wnum, wnum*y.size)
    return x, y

def step_series_gw(snum=1, amp=1., period=100, phase=0, num=1, offset=0, wnum=1):
    """generate step function

    """
    x = np.arange(phase, period*wnum+phase, num, dtype=double)
    x_num = x.size/wnum
    y = ones(x_num)/2.
    n = -1
    for i in range(snum):
        n += 2 
        y += 2./pi * (sin(n*x[0:x_num]/period * 2 * pi) / n)
    y = y * amp + offset
    y = np.tile(y, wnum)
    return x, y

def triangle_series_gw(snum=1, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
    """generate step function

    """
    x = np.linspace(phase, period*wnum+phase, wnum*num)
    y = pi * ones(num)/2.
    n = -1
    for i in range(snum):
        n += 2 
        y += -4./pi * (cos(n*x[0:num]/period * 2 * pi) / n**2)
    y = y * amp + offset
    y = np.tile(y, wnum)
    return x, y

def ramp_series_gw(snum=1, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
    """generate step function

    """
    x = np.linspace(phase, period*wnum+phase, wnum*num)
    y = zeros(num)
    n = 0
    inv = -1
    for i in xrange(snum):
        n += 1 
        inv *= -1
        y += 2 * (inv * sin(n*x[0:num]/period * 2 * pi) / n)
    y = y * amp + offset
    y = np.tile(y, wnum)
    return x, y

class generate_wave(handle_3d):
    def __init__(self):
        handle_3d.__init__(self)

    def step(self, amp=1., period=100, num=100, offset=0, wnum=1):
        x, y = step_gw(amp, period, num, offset, wnum)
        self.dinput([x, y, None])

    def sinc(self, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
        x, y = sinc_gw(amp, period, phase, num, offset, wnum)
        self.dinput([x, y, None])

    def discrete_sin(self, amp=1., period=100, phase=0, dnum=1000, num=100, offset=0, wnum=1):
        x, y = discrete_sin_gw(amp, period, phase, dnum, num, offset, wnum)
        self.dinput([x, y, None])

    def harmonic(self, hnum=2, weight=1, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
        x, y = harmonic_gw(hnum, weight, amp, period, phase, num, offset, wnum)
        self.dinput([x, y, None])

    def sin_freq(self, hnum=2, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
        x, y = sin_freq_gw(hnum, amp, period, phase, num, offset, wnum)
        self.dinput([x, y, None])

    def sin(self, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
        x, y = sin_gw(amp, period, phase, num, offset, wnum)
        self.dinput([x, y, None])

    def cos(self, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
        x, y = cos_gw(amp, period, phase, num, offset, wnum)
        self.dinput([x, y, None])

    def delta(self, amp=1., period=100, num=100, offset=0, wnum=1):
        x, y = delta_gw(amp, period, num, offset, wnum)
        self.dinput([x, y, None])

    def flat(self, amp=1., period=100, num=100, offset=0, wnum=1):
        x, y = flat_gw(amp, period, num, offset, wnum)
        self.dinput([x, y, None])

    def step_series(self, snum=1, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
        x, y = step_series_gw(snum, amp, period, phase, num, offset, wnum)
        self.dinput([x, y, None])

    def triangle_series(self, snum=1, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
        x, y = triangle_series_gw(snum, amp, period, phase, num, offset, wnum)
        self.dinput([x, y, None])

    def ramp_series(self, snum=1, amp=1., period=100, phase=0, num=100, offset=0, wnum=1):
        x, y = ramp_series_gw(snum, amp, period, phase, num, offset, wnum)
        self.dinput([x, y, None])

    def func(self, func="x", st=0, en=10, num=100, wnum=1):
        x, y = func_gw(func, st, en, num, wnum)
        self.dinput([x, y, None])
