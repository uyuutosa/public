# coding: utf-8
import root_util as s
from numpy import *
from random import *

#import pyublas
d=s.root_util()
d.root_init()
#a = [gauss(1,1)for x in range(100)]
#b = [gauss(1,1)for x in range(100)]
#c = [gauss(1,1)for x in range(100)]
a = [0.0000001,0.0000002,2,4,5,6,8,10]
b = [0,1,2,4,5,6,8,10]
c = [0,1,2,4,5,6,8,10]
d.set_xyzdata(tuple(a),tuple(b),tuple(c),tuple(a), tuple(b),0, 0)
#d.simplelayout("colz")
d.set_xname("adg",0)
d.set_yname("adg",0)
#d.set_xlim(0.,20., 0)
#d.set_ylim(0.,20., 0)
d.set_zlim(-0.1,0.1, 0)
d.simplelayout("cont4 cont3")
d.dump_fig("test.pdf")
d.view_graph()
