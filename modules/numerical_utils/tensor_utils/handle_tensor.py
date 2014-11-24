import tensor as t
from numpy import *
from modules.numerical_utils.multidimensional_util.handle_graph import handle_graph



class handle_tensor(handle_graph):

    def append(self, obj, idx):
        ## \brief Append a tensor to other tensor.
        self.same_trans(obj)    
        self.transpose([idx,0])
        obj.transpose([idx,0])
        if self.idx != obj.idx:
            raise ValueError, "Index is not much."
        ret = t.tensor(append(self.arr, obj.arr, axis=0), self.idx, self.ud)
        
        return ret

    def rup(self, N, idx, ud="d"):
        o = t.tensor(ones(N), idx=idx, ud=ud)
        return o * self 

    def sum(self, idx):
        obj = t.tensor(self)
        for c in idx:
            obj.transpose([c,0])
            obj.arr = obj.arr.sum(axis=0)
            a = array([])
            if type(obj.arr) != type(a):
                return obj.arr
            obj.idx = obj.idx[1:]
            obj.ud = obj.ud[1:]
        #for c in idx:
        #    if c in obj.idx:
        #        N = obj.arr.shape[obj.idx.find(c)]
        #        ud = obj.ud[obj.idx.find(c)]
        #        o = t.tensor(ones(N), idx=c, ud={"u":"d", "d": "u"}[ud])
        #        
        #        obj = obj * o
        #        check = True
        return obj

    def rfft(self, idx):
        self.transpose([self.index(idx), -1])
        return t.tensor(fft.rfft(self.arr), self.idx, self.ud)

    def mov_grad(self, obj, wid, dx, idx, fs):
        x = obj
        y = self
        xy = x * y
        L = abs(int(float(wid)/float(dx))) 
        h = t.tensor(ones(L), idx, self.gud(idx))

        conv_x = x.convolve(h, idx)
        a = (L * xy.convolve(h, idx) - conv_x * y.convolve(h, idx)) / (L * (x**2).convolve(h, idx) - conv_x ** 2)
        return a


    def convolve(self, h, idx):
        obj = t.tensor(self)
        if isinstance(h, t.tensor): h = h.arr
        N = obj.len(idx)
        obj.transpose([obj.index(idx), 0])
        z = zeros(obj.arr.shape) 
        obj.arr = append(obj.arr, z, axis=0)
        obj.transpose([obj.index(idx), -1],opt=True)
        X = fft.rfft(obj.arr)
        H = fft.rfft(append(h, zeros(2*N - h.size)))
        return t.tensor(fft.irfft(X*H)[0:N], obj.idx, obj.ud)
 
    def mov_ave(self, wid, dx, idx, fs):
        f =  fft.rfftfreq(self.len(idx), float(fs))
        L = int(float(wid) / float(dx))
        H = ((sin(pi *  f * L / fs) / sin(pi * f / fs)) * exp(-1j * pi * f * (L-1) / fs)) / L
        H[0] = 1.
        X = self.rfft(idx).arr * H
        return t.tensor(fft.irfft(X), self.idx, self.ud)


    def view_1data(self, *args, **kwargs):

        if len(args):
            abcs = args[0]
            lgtd = args[1]

        if "abcs" in kwargs: abcs = kwargs["abcs"]
        if "lgtd" in kwargs: lgtd = kwargs["lgtd"]

        self.grace.view_1data([self.t[abcs].arr, self.t[lgtd].arr], **kwargs)

        
        
        

    def view(self, abcs=0, lgtd=1):
        rank = self.a.rank
        if rank == 1:
            self.view2d()
        if rank == 2:
            self.view3d()


