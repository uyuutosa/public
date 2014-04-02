from numpy import *
def dft(arr):
    k = arange(arr.size)
    n = arange(arr.size)
    return array(map(lambda x: (arr * exp(- x * n * 1j * 2 * pi / arr.size)).sum(), k))
    
def idft(arr):
    k = arange(arr.size)
    n = arange(arr.size)
    return array(map(lambda x: (arr.conj() * exp(- x * n * 1j * 2 * pi / arr.size)).sum().conjugate() / arr.size, k))
    
def bit_rev(n, conca=False):
    if n == 2:
        tmp =  array([0,1])
    elif n == 1:
        tmp =  array([0])
    elif n <= 0:
        raise ValueError
    else:
        pw = int(log(n)/log(2))
        minpw = pw - 2
        tmp = array([0, 2, 1, 3]) * 2 ** minpw
        retlst = []
        cnt = minpw - 1
        #cnt = minpw 
        #add_arr = repeat(arange(2**cnt) , 2 ** (cnt + 1))
        #tmp = tile(tmp, cnt+1)
        #tmp = tmp + add_arr
        while cnt >= 0:
            tmp = append(tmp, tmp + 2 ** cnt)
            cnt -= 1
        
    if conca:
        add_arr = repeat(arange(conca/tmp.size) * tmp.size, tmp.size)
        tmp = tile(tmp, conca/tmp.size) + add_arr
    return tmp

def butterfly(a, b, w):
    wb = (w * b)
    ret_a = a + wb
    ret_b = a - wb
    return ret_a, ret_b


def myfft_slow(arr):
    arr = array(arr, dtype=complex)
    anum = arr.size
    pnum = int(log(anum) / log(2))
    revarr = bit_rev(anum)
    arr = arr[revarr]
    for n in xrange(1, pnum + 1):
        tmp_warr = exp(-1.j * 2.  * pi / (2.**(n))) ** arange(2**(n-1))
        tmp_warr = tmp_warr[bit_rev(2.**(n - 1))]
        warr = array([])
        while True:
            if warr.size == anum / 2: 
                break
            for tmp_w in tmp_warr:
                warr = append(warr, tmp_w)
        revarr = bit_rev(2**n, anum)
        arr = arr[revarr]
        arr = append([butterfly(x, y, z) for x,y,z in zip(arr[range(0,anum,2)], arr[range(1,anum,2)], warr)],[])[revarr]
    return arr   

def myfft2(arr):
    arr = array(arr, dtype=complex)
    anum = arr.size
    pnum = int(log(anum) / log(2))
    revarr = bit_rev(anum)
    arr = arr[revarr]
    w = exp(-1j * 2 * pi / anum) ** arange(anum/2)
    for s in xrange(1, pnum + 1):
        k1 = 2 ** s
        k2 = k1 / 2
        Nk1 = anum/k1
        for m in xrange(k2):
            kn = (m) * Nk1 
            for q in xrange(m,anum, k1):
                r = q + k2
                Xtmp =  w[kn] * arr[r]
                arr[r] = arr[q] - Xtmp
                arr[q ] = arr[q] + Xtmp
    return arr

def zero_pad(arr, pnum):
    add_num = 2 ** pnum - arr.size
    return append(arr, zeros(add_num))
    
def myfft(arr, pnum=False):
    if pnum == False:
        pnum = log(arr.size)/log(2)
        if pnum - int(pnum) == 0:
            pnum = int(pnum)
        else:
            pnum = int(pnum + 1)
            arr = zero_pad(arr, pnum)
    else:
        arr = zero_pad(arr, pnum)
    arr = array(arr, dtype=complex)
    anum = arr.size
    revarr = bit_rev(anum)
    arr = arr[revarr]
    for n in xrange(1, pnum + 1):
        tmp_warr = exp(-1.j * 2.  * pi / (2.**(n))) ** arange(2**(n-1))
        tmp_warr = tmp_warr[bit_rev(2.**(n - 1))]
        warr = tile(tmp_warr, anum / (2**(n)))
        revarr = bit_rev(2**n, anum)
        arr = arr[revarr]
        a = arr[range(0,anum,2)]
        wb = arr[range(1,anum,2)] * warr
        ret_a = a + wb
        ret_b = a - wb
        arr = append(array([ret_a, ret_b]).transpose(),[])[revarr]
    return arr   
 
def myifft(arr):
    pnum = log(arr.size)/log(2)
    if pnum - int(pnum) == 0:
        pnum = int(pnum)
    else:
        pnum = int(pnum + 1)
        arr = zero_pad(arr, pnum)
    arr = array(arr, dtype=complex).conj()
    anum = arr.size
    revarr = bit_rev(anum)
    arr = arr[revarr]
    for n in xrange(1, pnum + 1):
        tmp_warr = exp(-1.j * 2.  * pi / (2.**(n))) ** arange(2**(n-1))
        tmp_warr = tmp_warr[bit_rev(2.**(n - 1))]
        warr = tile(tmp_warr, anum / (2**(n)))
        revarr = bit_rev(2**n, anum)
        arr = arr[revarr]
        a = arr[range(0,anum,2)]
        wb = arr[range(1,anum,2)] * warr
        ret_a = a + wb
        ret_b = a - wb
        arr = append(array([ret_a, ret_b]).transpose(),[])[revarr]
    return arr.conj() / arr.size

def wig_spec(arr, n=None, pnum=False):
    if n == None:
        n = arr.size
    a = arr[0:n/2][-1::-1]
    b = arr[n/2-1:][0:a.size]

    arr = 2 * a * b.conj()
    return fft.fft(arr)
    #return myfft(arr, pnum)

def myfftfreq(n, tstep=1):
    return arange(n) / (n * float(tstep))


