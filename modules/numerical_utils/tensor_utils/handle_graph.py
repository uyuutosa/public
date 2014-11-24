from modules.numerical_utils.handle_graph import handle_graph

class graph(handle_graph):
    grace = grace_util()
    def view(self, idx, abcs=0, lgtd=1):
        self.
    def view_2d(self, layout="1", logx=false, logy=false):
        layout = str(layout)
        layoutdic = {
                     "1"      : self.grace.layout_1,
                     "1_2"      : self.grace.layout_1_2,
                     "2"      : self.grace.layout_2,
                     "3"      : self.grace.layout_3,
                     "4"      : self.grace.layout_4,
                     "5"      : self.grace.layout_5,
                     "6"      : self.grace.layout_6,
                     "7"      : self.grace.layout_7,
                     "8"      : self.grace.layout_8,
                     "8_2"    : self.grace.layout_8_2,
                     "column" : self.grace.layout_column,
                     "column4": self.grace.layout_column_4grid,
                    }
        self.hist.input()
        #self.grace.layout_1()
        if layout == "column":
            layoutdic[layout](gnumlim)
        else:
            layoutdic[layout]()
        self.set_xaxes(1,0) if logx == true else self.set_xaxes(0,0)
        self.set_yaxes(1,0) if logy == true else self.set_yaxes(0,0)
        arrs,errs = self.get_data(reterr=true)
        if type(errs[lgtd]) == type(none):
            self.grace.set_xydata(array(arrs[abcs]), array(arrs[lgtd]))
        else:
            self.grace.set_xydy(array(arrs[abcs]), array(arrs[lgtd]), array(errs[lgtd]))
        if type(self.grace.prop.decolst) != type(none):
            self.grace.set_ornament()
        if self.grace.prop.gdiclst[0]["lim"] is none:
            self.grace.set_autoscale(arrs[abcs], arrs[lgtd],logx=logx, logy=logy)
        else:
            (xmin, xmax, ymin, ymax, gnum) = self.grace.prop.gdiclst[0]["lim"]
        if len(self.grace.prop.gdiclst): self.grace.set_graphitems()

        self.grace.open_grace()
        self.grace.initialize()
        self.dinput(arrs)
        
    
    

