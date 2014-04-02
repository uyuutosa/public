#define BOOST_PYTHON_STATIC_LIB
//#define BOOST_TEST_DYN_LINK
#include <boost/python.hpp>
#include <sstream>
#include <string>
#include <math.h>
//#include <pyublas/numpy.hpp>
#include <iostream>
#include <iomanip>
#include"TColor.h"
#include"TApplication.h"
#include"TH1.h"
#include"TProfile.h"
#include"TProfile2D.h"
#include"TGraph.h"
#include"TGraph2d.h"
#include"TCanvas.h"
#include"graph_util.hpp"
#include "MysignalHandler.h"
#include "TSystem.h"
#include "TStyle.h"
#include "TBox.h"
#include "TFrame.h"
#include "TEllipse.h"
#include "root_prop_util.hpp"

using namespace std;

int add(int lhs, int rhs)
{
        return lhs + rhs;
}

enum  status_tag{TP, TP2D, TG, TG2D};
class Tobj_container{
private:
    Int_t cnt_gnum;
    Double_t* bin_calc(boost::python::tuple tpl);
    Int_t gcnt(){return cnt_gnum++;}
public:
    TProfile    *tp;    
    TProfile2D  *tp2d;    
    TGraph      *tg; 
    TGraph2D    *tg2d; 
    void *obj;
    status_tag tag;
    void set_obj(TProfile* obj){tag = TP; tp = obj;}
    void set_obj(TProfile2D* obj){tag = TP2D; tp2d = obj;}
    void set_obj(TGraph* obj){tag = TG; tg = obj;}
    void set_obj(TGraph2D* obj){tag = TG2D; tg2d = obj;}
    void set_xname(char* name);
    void set_yname(char* name);
    void set_zname(char* name);
    void set_xlim(Double_t xmin, Double_t xmax);
    void set_ylim(Double_t ymin, Double_t ymax);
    void set_zlim(Double_t zmin, Double_t zmax);
    void set_xyzdata(boost::python::tuple xtpl, boost::python::tuple ytpl, boost::python::tuple ztpl, boost::python::tuple bin_xtpl, boost::python::tuple bin_ytpl);
    void Draw(const char *opt);
    Int_t i;
    Tobj_container(Int_t i){
        cnt_gnum = i;
    }
};

Double_t* Tobj_container::bin_calc(boost::python::tuple tpl){
    Double_t d, x1, x2;
    Int_t arrsize=boost::python::len(tpl)+1;
    Double_t *ret_lst = new Double_t[arrsize]; 
    for (i=0; i<arrsize-2; i++){
        x1 = boost::python::extract<double>(tpl[i]);
        x2 = boost::python::extract<double>(tpl[i+1]);
        d = (x2 - x1) / 2;
        if (i == 0) ret_lst[i] = x1 - d;
        ret_lst[i+1] = x1 + d;
    }
    ret_lst[i+1] = boost::python::extract<double>(tpl[i])+d;
    return ret_lst;
}

void Tobj_container::set_xname(char* name){
        switch (tag){
            case TP:
                break;
            case TP2D: 
                cout << name << endl;
                tp2d->GetXaxis()->SetTitle(name);
                tp2d->GetXaxis()->CenterTitle();
                break;
            case TG:
                break;
            case TG2D: 
                break;
        }

}


void Tobj_container::set_yname(char* name){
        switch (tag){
            case TP:
                break;
            case TP2D: 
                tp2d->GetYaxis()->SetTitle(name);
                tp2d->GetYaxis()->CenterTitle();
                break;
            case TG:
                break;
            case TG2D: 
                break;
        }
}

void Tobj_container::set_zname(char* name){
        switch (tag){
            case TP:
                break;
            case TP2D: 
                tp2d->GetZaxis()->SetTitle(name);
                tp2d->GetZaxis()->CenterTitle();
                break;
            case TG:
                break;
            case TG2D: 
                break;
        }
}

void Tobj_container::set_xlim(Double_t xmin, Double_t xmax){
    switch (tag){
        case TP:
            break;
        case TP2D: 
            if (xmin != xmax){
                cout << xmin << xmax << endl;
                tp2d->GetXaxis()->SetRangeUser(xmin, xmax);
            }
            break;
        case TG:
            break;
        case TG2D: 
            break;
    }
}

void Tobj_container::set_ylim(Double_t ymin, Double_t ymax){
    switch (tag){
        case TP:
            break;
        case TP2D: 
            if (ymin != ymax){
                tp2d->GetYaxis()->SetRangeUser(ymin, ymax);
            }
            break;
        case TG:
            break;
        case TG2D: 
            break;
    }
}

void Tobj_container::set_zlim(Double_t zmin, Double_t zmax){
    switch (tag){
        case TP:
            break;
        case TP2D: 
            if (zmin != zmax){
                tp2d->GetZaxis()->SetRangeUser(zmin, zmax);
                cout << zmin << ", " << zmax << endl;
            }
            break;
        case TG:
            break;
        case TG2D: 
            break;
    }
}
void Tobj_container::set_xyzdata(boost::python::tuple xtpl, boost::python::tuple ytpl, boost::python::tuple ztpl, boost::python::tuple bin_xtpl, boost::python::tuple bin_ytpl){
    Int_t xnbin = boost::python::len(bin_xtpl);
    Int_t ynbin = boost::python::len(bin_ytpl);
    stringstream ss;
    ss << "g";
    ss << Tobj_container::gcnt();
    set_obj(new TProfile2D(ss.str().c_str(), "", xnbin, Tobj_container::bin_calc(bin_xtpl), ynbin, Tobj_container::bin_calc(bin_ytpl), ""));
    for (int i = 0; i < boost::python::len(xtpl); ++i){
        tp2d->Fill(boost::python::extract<Double_t>(xtpl[i]), boost::python::extract<Double_t>(ytpl[i]), boost::python::extract<Double_t>(ztpl[i]));
    }
}


void Tobj_container::Draw(const char *opt){
    switch (tag){
        case TP:
            break;
        case TP2D: 
            tp2d->Draw(opt);
            break;
        case TG:
            break;
        case TG2D: 
            break;
    }
}

//----------------------------------------------------------------------------------------------------
class root_util: public input_prop{
    private:
        Int_t i, pad_size;
        Int_t cnt_gnum;
        Int_t gcnt(){return cnt_gnum++;}
        vector<string> split(string line, string delim);
    public:
        TCanvas *c1;
        vector<TCanvas*> clst;
        void root_init();
        void set_xlim(Double_t xmin, Double_t xmax, int gnum=0);
        void set_ylim(Double_t ymin, Double_t ymax, int gnum=0);
        void set_zlim(Double_t zmin, Double_t zmax, int gnum=0);
        void set_xname(char *name, int gnum=0);
        void set_yname(char *name, int gnum=0);
        void set_zname(char *name, int gnum=0);
        void set_xydata(boost::python::tuple xtpl, boost::python::tuple ytpl,
                                                        int gnum=0, int snum=0);
        void set_xyzdata(boost::python::tuple xtpl, boost::python::tuple ytpl, boost::python::tuple ztpl, boost::python::tuple bin_xtpl, boost::python::tuple bin_ytpl,
                                                        int gnum=0, int snum=0);
        void dump_fig(char *figpath);
        void single_layout(string opt="");
        void layout1_logz(string opt="");
        void layout2(string opt="");
        void dual_layout(string opt="");
        void sextuple_layout(string opt="");
        void sextuple_layout2(string opt="");
        void palette_rainbow();
        void mypalette1();
        void mypalette2();
        void mypalette3();
        void mypalette4();
        void palette_red2blue();
        void view_graph();
        void set_prop();
        void set_box(Double_t xmin, Double_t xmax, Double_t ymin, Double_t ymax, 
                              Int_t lstyle, Double_t lwidth, Double_t lcolor,  Double_t fcolor, 
                              Int_t fptn, Char_t *loctype, Int_t gnum, Int_t xonly, Int_t yonly,
                              boost::python::tuple gtpl);
                              //Double_t gxmin, Double_t gxmax, Double_t gymin, Double_t gymax);
        bool gnum_check(int gnum);
        Double_t *bin_calc(boost::python::tuple tpl);

        TApplication *app;
        vector<Tobj_container*> objlst;

        root_util(){
            app = new TApplication("app" ,0,0,0,0);
            cnt_gnum=0;
            gSystem->AddSignalHandler( new MySignalHandler(kSigInterrupt));
            gSystem->AddSignalHandler( new MySignalHandler(kSigTermination));
            root_init();
        }
};



bool root_util::gnum_check(int gnum){
    stringstream ss;
    if (objlst.size() >  gnum)
        return true;
    else
        for (i = objlst.size(); i<=gnum; i++){
            ss << root_util::gcnt();
            objlst.push_back(new Tobj_container(i));
            //objlst.push_back(new TProfile(ss.str().c_str(),"aaa",100,0,100));
        }
}


void root_util::root_init(){
        //objlst.clear();
        //if (root_util::gnum_chack(gnum))
  
}

void root_util::set_xlim(Double_t xmin, Double_t xmax, int gnum){
   root_util::gnum_check(gnum);
   objlst[gnum]->set_xlim(xmin, xmax);
}

void root_util::set_ylim(Double_t ymin, Double_t ymax, int gnum){
   root_util::gnum_check(gnum);
   objlst[gnum]->set_ylim(ymin, ymax);
}

void root_util::set_zlim(Double_t zmin, Double_t zmax, int gnum){
   root_util::gnum_check(gnum);
   objlst[gnum]->set_zlim(zmin, zmax);
}

void root_util::set_prop(){
    for (i=0; i<objlst.size(); i++){
        root_util::gnum_check(i);
//        objlst[i]->get_obj()->GetXaxis()->SetRangeUser(glst[i].xlim[0], glst[i].xlim[1]);
//        objlst[i]->get_obj()->GetYaxis()->SetRangeUser(glst[i].ylim[0], glst[i].ylim[1]);
//        objlst[i]->get_obj()->GetZaxis()->SetRangeUser(glst[i].zlim[0], glst[i].zlim[1]);
//        objlst[i]->get_obj()->GetXaxis()->SetTitle(glst[i].xname);
//        objlst[i]->get_obj()->GetXaxis()->CenterTitle();
//        objlst[i]->get_obj()->GetYaxis()->SetTitle(glst[i].yname);
//        objlst[i]->get_obj()->GetYaxis()->CenterTitle();
//        objlst[i]->get_obj()->GetZaxis()->SetTitle(glst[i].zname);
//        objlst[i]->get_obj()->GetZaxis()->CenterTitle();
    }
}

void root_util::set_xydata(boost::python::tuple xtpl, boost::python::tuple ytpl,
                                                        int gnum, int snum){
    root_util::gnum_check(gnum);
    //xlen[gnum] = boost::python::len(xtpl);
    //ylen[gnum] = boost::python::len(ytpl);
    //zlen[gnum] = boost::python::len(ztpl);
//    for (int i = 0; i < boost::python::len(xtpl); ++i){
//        objlst[gnum]->Fill(boost::python::extract<Double_t>(xtpl[i]), boost::python::extract<Double_t>(ytpl[i]));
//    }
}

void root_util::set_xyzdata(boost::python::tuple xtpl, boost::python::tuple ytpl, boost::python::tuple ztpl, boost::python::tuple bin_xtpl, boost::python::tuple bin_ytpl,
                                                        int gnum, int snum){
    root_util::gnum_check(gnum);
    objlst[gnum]->set_xyzdata(xtpl, ytpl, ztpl, bin_xtpl, bin_ytpl);
}

void root_util::set_xname(char *name, int gnum){
    objlst[gnum]->set_xname(name);
}

void root_util::set_yname(char *name, int gnum){
    objlst[gnum]->set_yname(name);
}

void root_util::set_zname(char *name, int gnum){
    objlst[gnum]->set_zname(name);
}

void root_util::mypalette1(){
    static const Int_t kN = 99;
    static Int_t colors[kN];
    static Bool_t initialized = kFALSE;
    
    Double_t r[] = {  0,   0,   0,   0,   0,   0, 0.5,   1,   1,   1, 0.5};
    Double_t g[] = {  0,   0, 0.5,   1,   1,   1,   1,   1, 0.5,   0,   0};
    Double_t b[] = {0.5,   1,   1,   1, 0.5,   0,   0,   0,   0,   0,   0};
    Double_t stop[] = {0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0};
    
    if(!initialized){
        Int_t index = TColor::CreateGradientColorTable(11, stop, r, g, b, kN);
    for (int i = 0; i < kN; i++) {
        colors[i] = index + i;
    } // i
    initialized = kTRUE;
    } else {
    gStyle->SetPalette(kN, colors);
    } 
    gStyle -> SetNumberContours(kN);
}

void root_util::mypalette2(){
    static const Int_t kN = 99;
    static Int_t colors[kN];
    static Bool_t initialized = kFALSE;
    
    Double_t r[] = {0.5,   1,   1,   1,   1,   1};
    Double_t g[] = {0. ,   0, 0.5,   1,   1,   1};
    Double_t b[] = {0. ,   0,   0,   0, 0.5,   1};
    Double_t stop[] = {0, 0.2, 0.4, 0.6, 0.8, 1};
    
    if(!initialized){
        Int_t index = TColor::CreateGradientColorTable(6, stop, r, g, b, kN);
    for (int i = 0; i < kN; i++) {
        colors[i] = index + i;
    } // i
    initialized = kTRUE;
    } else {
    gStyle->SetPalette(kN, colors);
    } 
    gStyle -> SetNumberContours(kN);
}

void root_util::mypalette3(){
    static const Int_t kN = 99;
    static Int_t colors[kN];
    static Bool_t initialized = kFALSE;
    
    Double_t r[] = {1,  0,   0,   0,   0,   0,   0, 0.5,   1,   1,   1, 0.5};
    Double_t g[] = {1,  0,   0, 0.5,   1,   1,   1,   1,   1, 0.5,   0,   0};
    Double_t b[] = {1,0.5,   1,   1,   1, 0.5,   0,   0,   0,   0,   0,   0};
    Double_t stop[] = {0, 0.0909090, 0.18181818, 0.27272727, 0.36363636,
                       0.45454545, 0.54545454, 0.63636363, 0.72727272,
                       0.81818181, 0.90909090, 1};
    
    if(!initialized){
        Int_t index = TColor::CreateGradientColorTable(12, stop, r, g, b, kN);
    for (int i = 0; i < kN; i++) {
        colors[i] = index + i;
    } // i
    initialized = kTRUE;
    } else {
    gStyle->SetPalette(kN, colors);
    } 
    gStyle -> SetNumberContours(kN);
}

void root_util::mypalette4(){
    static const Int_t kN = 99;
    static Int_t colors[kN];
    static Bool_t initialized = kFALSE;
    
    Double_t r[] = {1,  0,   0,   0,   0,   0,   0, 0.5,   1, 0.5};
    Double_t g[] = {1,  0,   0, 0.5,   1,   1,   1,   1,   0,   0};
    Double_t b[] = {1,0.5,   1,   1,   1, 0.5,   0,   0,   0,   0};
   // Double_t stop[] = {0, 0.0909090, 0.18181818, 0.27272727, 0.36363636,
   //                    0.45454545, 0.54545454, 0.63636363, 0.72727272,
   //                   0.81818181, 0.90909090, 1};
    Double_t stop[] = {0, 0.11111, 0.22222, 0.33333, 0.44444, 0.55555, 0.66666, 0.77777, 0.88888, 1.0};
    
    if(!initialized){
        Int_t index = TColor::CreateGradientColorTable(10, stop, r, g, b, kN);
    for (int i = 0; i < kN; i++) {
        colors[i] = index + i;
    } // i
    initialized = kTRUE;
    } else {
    gStyle->SetPalette(kN, colors);
    } 
    gStyle -> SetNumberContours(kN);
}

void root_util::palette_red2blue(){
    static const Int_t kN = 99;
    static Int_t colors[kN];
    static Bool_t initialized = kFALSE;
    //Double_t r[] = {  0,   0,   0,   0,   0,   1,   1,   1,    1,   1, 0.5};
    //Double_t g[] = {  0,   0,   0, 0.5, 0.6,   1,   1, 0.6, 0.5,   0,   0};
    Double_t r[] = {  0,   0, 0.5, 0.6,   1,   1,   1,   1,    1,   1, 0.5};
    Double_t g[] = {  0,   0,   0,   0,   0,   1,   1, 0.6, 0.5,   0,   0};
    Double_t b[] = {0.5,   1,   1,   1,   1,   1,   0,    0,    0,   0,   0};
    Double_t stop[] = {0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0};
    
    if(!initialized){
        Int_t index = TColor::CreateGradientColorTable(11, stop, r, g, b, kN);
    for (int i = 0; i < kN; i++) {
        colors[i] = index + i;
    } // i
    initialized = kTRUE;
    } else {
    gStyle->SetPalette(kN, colors);
    } 
    gStyle -> SetNumberContours(kN);
}

void root_util::palette_rainbow(){
    gStyle->SetPalette(1);
}

//Single, dual, triple, quadruple, quintuple, sextuple, septuple, octuple, nonuple, decuple, undecuple, duodecuple...

vector<string> root_util::split(string line, string delim){
    Int_t delim_size = delim.size();
    Int_t line_size = line.size();
    Int_t i, pre=0, cnt=0;
    vector<string> retlst;
    for (i=0; i<line_size; i++){
        if (line[i] == delim[cnt]) cnt++;
        cout << cnt << endl;
        if (cnt == delim_size){
            cout<< line.substr(pre, i-delim_size+1)<< endl;
            retlst.push_back(line.substr(pre, i-delim_size+1));
            cnt = 0;
            pre = i + 1;
        }
    }
    if (retlst.size() == 0) retlst.push_back(line);
    else retlst.push_back(line.substr(pre, line.size()));
    return retlst;
}

void root_util::single_layout(string opt){
    pad_size = 1;
    gStyle->SetFrameFillStyle(4000);
    gStyle->SetNdivisions(10, "XYZ");
    gStyle->SetFrameLineWidth(2);
    gStyle->SetLabelOffset(0.018,"X");
    gStyle->SetLabelOffset(0.018,"Y");
    gStyle->SetLabelOffset(0.018,"Z");
    gStyle->SetLabelSize(0.08,"x");
    gStyle->SetLabelSize(0.08,"y");
    gStyle->SetLabelSize(0.08,"z");
    gStyle->SetTitleOffset(1, "X");
    gStyle->SetTitleOffset(0.8, "Y");
    gStyle->SetTitleOffset(0.8, "Z");
    gStyle->SetTitleSize(0.08, "X");
    gStyle->SetTitleSize(0.08, "Y");
    gStyle->SetTitleSize(0.08, "Z");
    gStyle->SetTickLength(0.04, "X");
    gStyle->SetTickLength(0.02, "Y");
    gStyle->SetTickLength(0.02, "Z");
    gStyle->SetLineWidth(2);
    gStyle->SetHistFillStyle(1001);
    gStyle->SetPadTopMargin(0.15);
    gStyle->SetPadRightMargin(0.23);
    gStyle->SetPadLeftMargin(0.19);
    gStyle->SetPadBottomMargin(0.2);
    gStyle->SetOptStat(0);
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    stringstream ss;
    vector<string> optlst = root_util::split(opt, ",");
    TPad *pad;


    clst.clear();
    Int_t cnum = 0, i, j;
    for (i=0; i<objlst.size(); i++){
        ss.str("");
        ss << "c";
        ss << cnum;
        clst.push_back(new TCanvas(ss.str().c_str(), ss.str().c_str(),0,0, 1131, 800));
        for (j=0; j<optlst.size(); j++){
            ss.str("");
            ss << "pad" << j;
            pad = new TPad(ss.str().c_str(), ss.str().c_str(), 0, 0, 1, 1);
            if (j != 0)pad->SetFillStyle(4000);
            pad->Draw();
            pad->cd();
            cout << optlst[j] << endl;
            objlst[i]->Draw(optlst[j].c_str());
            clst[i]->UseCurrentStyle();
            clst[i]->cd();
        }
 //       clst[i]->Modified()
//        clst[i]->Update();
        cnum ++;
    }
}

void root_util::layout1_logz(string opt){
    pad_size = 1;
    gStyle->SetFrameFillStyle(4000);
    gStyle->SetNdivisions(10, "XYZ");
    gStyle->SetFrameLineWidth(2);
    gStyle->SetLabelOffset(0.018,"X");
    gStyle->SetLabelOffset(0.018,"Y");
    gStyle->SetLabelOffset(0.018,"Z");
    gStyle->SetLabelSize(0.08,"x");
    gStyle->SetLabelSize(0.08,"y");
    gStyle->SetLabelSize(0.08,"z");
    gStyle->SetTitleOffset(1, "X");
    gStyle->SetTitleOffset(0.8, "Y");
    gStyle->SetTitleOffset(0.8, "Z");
    gStyle->SetTitleSize(0.08, "X");
    gStyle->SetTitleSize(0.08, "Y");
    gStyle->SetTitleSize(0.08, "Z");
    gStyle->SetTickLength(0.04, "X");
    gStyle->SetTickLength(0.02, "Y");
    gStyle->SetTickLength(0.02, "Z");
    gStyle->SetLineWidth(2);
    gStyle->SetHistFillStyle(1001);
    gStyle->SetPadTopMargin(0.15);
    gStyle->SetPadRightMargin(0.23);
    gStyle->SetPadLeftMargin(0.19);
    gStyle->SetPadBottomMargin(0.2);
    gStyle->SetOptStat(0);
    gStyle->SetOptLogz();
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    stringstream ss;
    vector<string> optlst = root_util::split(opt, ",");
    TPad *pad;


    clst.clear();
    Int_t cnum = 0, i, j;
    for (i=0; i<objlst.size(); i++){
        ss.str("");
        ss << "c";
        ss << cnum;
        clst.push_back(new TCanvas(ss.str().c_str(), ss.str().c_str(),0,0, 1131, 800));
        for (j=0; j<optlst.size(); j++){
            ss.str("");
            ss << "pad" << j;
            pad = new TPad(ss.str().c_str(), ss.str().c_str(), 0, 0, 1, 1);
            if (j != 0)pad->SetFillStyle(4000);
            pad->SetLogz(); 
            pad->Draw();
            pad->cd();
            cout << optlst[j] << endl;
            objlst[i]->Draw(optlst[j].c_str());
            clst[i]->UseCurrentStyle();
            clst[i]->cd();
        }
 //       clst[i]->Modified()
//        clst[i]->Update();
        cnum ++;
    }
}
void root_util::layout2(string opt){
    pad_size = 2;
    gStyle->SetNdivisions(10, "XYZ");
    gStyle->SetFrameLineWidth(2);
    gStyle->SetLabelOffset(0.022,"X");
    gStyle->SetLabelOffset(0.018,"Y");
    gStyle->SetLabelOffset(0.024,"Z");
    gStyle->SetLabelSize(0.08,"x");
    gStyle->SetLabelSize(0.08,"y");
    gStyle->SetLabelSize(0.08,"z");
    gStyle->SetTitleOffset(1, "X");
    gStyle->SetTitleOffset(0.8, "Y");
    gStyle->SetTitleOffset(0.8, "Z");
    gStyle->SetTitleSize(0.08, "X");
    gStyle->SetTitleSize(0.08, "Y");
    gStyle->SetTitleSize(0.08, "Z");
    gStyle->SetTickLength(0.04, "X");
    gStyle->SetTickLength(0.02, "Y");
    gStyle->SetTickLength(0.02, "Z");
    gStyle->SetLineWidth(2);
    gStyle->SetHistFillStyle(1001);
    gStyle->SetPadTopMargin(0.1);
    gStyle->SetPadRightMargin(0.24);
    gStyle->SetPadLeftMargin(0.18);
    gStyle->SetPadBottomMargin(0.2);
    gStyle->SetOptStat(0);
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    stringstream ss;
    clst.clear();
    Int_t cnum = 0, i, j=1;
    ss << cnum;
    ss << "c";
    clst.push_back(new TCanvas(ss.str().c_str(), ss.str().c_str(),0,0, 800, 1131));
    clst[cnum]->Divide(1,2);
    for (i=0; i<objlst.size(); i++){
        if (j == pad_size + 1) {
            cnum ++;
            ss.str("");
            ss << "c";
            ss << cnum;
            clst.push_back(new TCanvas(ss.str().c_str(), ss.str().c_str(),0,0, 800, 1131));
            j = 1;
            clst[cnum]->Divide(1,2);
        }
        clst[cnum]->cd(j);
        objlst[i]->Draw(opt.c_str());
        clst[cnum]->UseCurrentStyle();
        j ++;
    }
}
void root_util::dual_layout(string opt){
    pad_size = 2;
    gStyle->SetNdivisions(10, "XYZ");
    gStyle->SetFrameLineWidth(2);
    gStyle->SetLabelOffset(0.022,"X");
    gStyle->SetLabelOffset(0.018,"Y");
    gStyle->SetLabelOffset(0.024,"Z");
    gStyle->SetLabelSize(0.08,"x");
    gStyle->SetLabelSize(0.08,"y");
    gStyle->SetLabelSize(0.08,"z");
    gStyle->SetTitleOffset(1, "X");
    gStyle->SetTitleOffset(0.8, "Y");
    gStyle->SetTitleOffset(0.8, "Z");
    gStyle->SetTitleSize(0.08, "X");
    gStyle->SetTitleSize(0.08, "Y");
    gStyle->SetTitleSize(0.08, "Z");
    gStyle->SetTickLength(0.04, "X");
    gStyle->SetTickLength(0.02, "Y");
    gStyle->SetTickLength(0.02, "Z");
    gStyle->SetLineWidth(2);
    gStyle->SetHistFillStyle(1001);
    gStyle->SetPadTopMargin(0.1);
    gStyle->SetPadRightMargin(0.24);
    gStyle->SetPadLeftMargin(0.18);
    gStyle->SetPadBottomMargin(0.2);
    gStyle->SetOptStat(0);
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    stringstream ss;
    clst.clear();
    Int_t cnum = 0, i, j=1;
    ss << cnum;
    ss << "c";
    clst.push_back(new TCanvas(ss.str().c_str(), ss.str().c_str(),0,0, 800, 1131));
    clst[cnum]->Divide(1,2);
    for (i=0; i<objlst.size(); i++){
        if (j == pad_size + 1) {
            cnum ++;
            ss.str("");
            ss << "c";
            ss << cnum;
            clst.push_back(new TCanvas(ss.str().c_str(), ss.str().c_str(),0,0, 800, 1131));
            j = 1;
            clst[cnum]->Divide(1,2);
        }
        clst[cnum]->cd(j);
        objlst[i]->Draw(opt.c_str());
        clst[cnum]->UseCurrentStyle();
        j ++;
    }
}

void root_util::sextuple_layout(string opt){
    pad_size = 6;
    gStyle->SetNdivisions(10, "XYZ");
    gStyle->SetFrameLineWidth(2);
    gStyle->SetLabelOffset(0.018,"X");
    gStyle->SetLabelOffset(0.018,"Y");
    gStyle->SetLabelOffset(0.018,"Z");
    gStyle->SetLabelSize(0.08,"x");
    gStyle->SetLabelSize(0.08,"y");
    gStyle->SetLabelSize(0.08,"z");
    gStyle->SetTitleOffset(1, "X");
    gStyle->SetTitleOffset(0.8, "Y");
    gStyle->SetTitleOffset(0.7, "Z");
    gStyle->SetTitleSize(0.08, "X");
    gStyle->SetTitleSize(0.08, "Y");
    gStyle->SetTitleSize(0.08, "Z");
    gStyle->SetTickLength(0.04, "X");
    gStyle->SetTickLength(0.02, "Y");
    gStyle->SetTickLength(0.02, "Z");
    gStyle->SetLineWidth(2);
    gStyle->SetHistFillStyle(1001);
    gStyle->SetPadTopMargin(0.1);
    gStyle->SetPadRightMargin(0.16);
    gStyle->SetPadLeftMargin(0.12);
    gStyle->SetPadBottomMargin(0.2);
    gStyle->SetOptStat(0);
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    stringstream ss;
    clst.clear();
    Int_t cnum = 0, i, j=1;
    ss << cnum;
    ss << "c";
    clst.push_back(new TCanvas(ss.str().c_str(), ss.str().c_str(),0,0, 1131, 800));
    clst[cnum]->Divide(3,2);
    for (i=0; i<objlst.size(); i++){
        if (j == pad_size + 1) {
            cnum ++;
            ss.str("");
            ss << "c";
            ss << cnum;
            clst.push_back(new TCanvas(ss.str().c_str(), ss.str().c_str(),0,0, 1131, 800));
            j = 1;
            clst[cnum]->Divide(3,2);
        }
        clst[cnum]->cd(j);
        objlst[i]->Draw(opt.c_str());
        clst[cnum]->UseCurrentStyle();
        j ++;
    }
}

void root_util::sextuple_layout2(string opt){
    pad_size = 6;
    gStyle->SetNdivisions(10, "XYZ");
    gStyle->SetFrameLineWidth(2);
    gStyle->SetLabelOffset(0.018,"X");
    gStyle->SetLabelOffset(0.018,"Y");
    gStyle->SetLabelOffset(0.018,"Z");
    gStyle->SetLabelSize(0.08,"x");
    gStyle->SetLabelSize(0.08,"y");
    gStyle->SetLabelSize(0.08,"z");
    gStyle->SetTitleOffset(1, "X");
    gStyle->SetTitleOffset(0.8, "Y");
    gStyle->SetTitleOffset(0.7, "Z");
    gStyle->SetTitleSize(0.08, "X");
    gStyle->SetTitleSize(0.08, "Y");
    gStyle->SetTitleSize(0.08, "Z");
    gStyle->SetTickLength(0.04, "X");
    gStyle->SetTickLength(0.02, "Y");
    gStyle->SetTickLength(0.02, "Z");
    gStyle->SetLineWidth(2);
    gStyle->SetHistFillStyle(1001);
    gStyle->SetPadTopMargin(0.1);
    gStyle->SetPadRightMargin(0.16);
    gStyle->SetPadLeftMargin(0.12);
    gStyle->SetPadBottomMargin(0.2);
    gStyle->SetOptStat(0);
    gStyle->SetPadTickX(1);
    gStyle->SetPadTickY(1);
    stringstream ss;
    clst.clear();
    Int_t cnum = 0, i, j=1;
    ss << cnum;
    ss << "c";
    clst.push_back(new TCanvas(ss.str().c_str(), ss.str().c_str(),0,0, 1131, 800));
    clst[cnum]->Divide(2,3);
    for (i=0; i<objlst.size(); i++){
        if (j == pad_size + 1) {
            cnum ++;
            ss.str("");
            ss << "c";
            ss << cnum;
            clst.push_back(new TCanvas(ss.str().c_str(), ss.str().c_str(),0,0, 1131, 800));
            j = 1;
            clst[cnum]->Divide(2,3);
        }
        clst[cnum]->cd(j);
        objlst[i]->Draw(opt.c_str());
        clst[cnum]->UseCurrentStyle();
        j ++;
    }
}

void root_util::view_graph(){
    app->Run();
}

void root_util::dump_fig(char *fig_path){
    for (i=0; i<clst.size(); i++){
        clst[i]->SaveAs(fig_path);
    }
}


void root_util::set_box(Double_t xmin, Double_t xmax, Double_t ymin, Double_t ymax, 
                              Int_t lstyle, Double_t lwidth, Double_t lcolor,  Double_t fcolor, 
                              Int_t fptn, Char_t *loctype, Int_t gnum, Int_t xonly, Int_t yonly,
                              boost::python::tuple gtpl){


    Double_t gxmin = boost::python::extract<double>(gtpl[0]);
    Double_t gxmax = boost::python::extract<double>(gtpl[1]);
    Double_t gymin = boost::python::extract<double>(gtpl[2]);
    Double_t gymax = boost::python::extract<double>(gtpl[3]);
    //cout << pad_size <<endl;
    Int_t clen = clst.size();
    //cout << clen<<endl;
    Int_t cnum = gnum / pad_size;
    //cout << cnum << fcolor<<endl;
    Int_t pad_num = gnum % pad_size + 1;
    //cout << pad_num<<endl;
    //cout << xmin <<endl;
    //cout << xmax <<endl;
    //cout << ymin <<endl;
    //cout << ymax <<endl;
    clst[cnum]->cd(pad_num);
    if (strcmp(loctype, "world") == 0){
        Double_t lm = clst[cnum]->GetLeftMargin();
        Double_t rm = clst[cnum]->GetRightMargin();
        Double_t tm = clst[cnum]->GetTopMargin();
        Double_t bm = clst[cnum]->GetBottomMargin();
        xmin = lm + (1 - (lm + rm))/(gxmax - gxmin) * (xmin - gxmin);
        xmax = lm + (1 - (lm + rm))/(gxmax - gxmin) * (xmax - gxmin);
        ymin = bm + (1 - (bm + tm))/(gymax - gymin) * (ymin - gymin);
        ymax = bm + (1 - (bm + tm))/(gymax - gymin) * (ymax - gymin);
//        cout<<objlst[gnum]->tp2d->GetYaxis()->GetFirst()<<endl;
//        cout<<objlst[gnum]->tp2d->GetYaxis()->GetBinLowEdge(objlst[gnum]->tp2d->GetYaxis()->GetLast())<<endl;
//        cout<<rm<<endl;
//        cout<<tm<<endl;
//        cout<<bm<<endl;
//        cout<<xmin<<endl;
//        cout<<xmax<<endl;
//        cout<<ymin<<endl;
//        cout<<ymax<<endl;
    }
    if (strcmp(loctype, "view") == 0){cout << "view" << endl;}

    TPad *b;
    b = new TPad("box","box", xmin, ymin, xmax, ymax);
    //b->SetFillColor(lcolor);
    //b->SetFillStyle(lstyle);
    //b = new TPad("box","box", xmin, ymin, xmax, ymax);
    b->SetFillColor(fcolor);
    b->SetFillStyle(fptn);
    b->SetFrameLineColor(lcolor);
    b->SetFrameLineStyle(lstyle);
    b->SetFrameLineWidth(lwidth);
    //b->SetMargin(lwidth, lwidth, lwidth, lwidth);
    b->Draw();
}

//struct root_util_pickle_suite:boost::python::pickle_suite
//{
//    static 
//    boost::python:::tuple
//    getinitargs(const root_util& r)
//    {
//        using namespace boost::python;
//        return make_tuple(r.set_xname())
//    }
//
//
//    static
//    boost::python::tuple
//    getstate(const world& r)
//    {
//        using namespace boost::python;
//        return make_tuple(r.get_secret_number());
//    }
//
//    static 
//    void
//    setstate(root_util& r, boost::python::tuple state)
//    {
//        using namespace boost::python;
//        if (len(state) != 1)
//        {
//            PyErr_SetObject(PyExc_ValueError,
//                ("expected 1-item tuple in call to __setstate__; got %s" % state).ptr());
//        throw_error_already_set();
//        }
//
//    long number = extract<long>(state[0]);
//    if (number != 42)
//        w.set_secret_number(number);
//    }
//};

BOOST_PYTHON_MODULE(root_util)
{
  //import_array();
  //numeric::array::set_module_and_type("numpy", "ndarray");
        using namespace boost::python;
//            def("add", &add);
        class_<input_prop>("input_prop");
        class_<root_util, bases<input_prop> >("root_util")
//            .def("set_xlim", &root_util::set_xlim)
            .enable_pickling()
            .def("root_init", &root_util::root_init)
            .def("set_xname", &root_util::set_xname)
            .def("set_yname", &root_util::set_yname)
            .def("set_zname", &root_util::set_zname)
            .def("set_xlim", &root_util::set_xlim)
            .def("set_ylim", &root_util::set_ylim)
            .def("set_zlim", &root_util::set_zlim)
            .def("set_xydata", &root_util::set_xydata)
            .def("set_xyzdata", &root_util::set_xyzdata)
            .def("dump_fig", &root_util::dump_fig)
            .def("single_layout", &root_util::single_layout)
            .def("layout1_logz", &root_util::layout1_logz)
            .def("dual_layout", &root_util::dual_layout)
            .def("layout2", &root_util::layout2)
            .def("sextuple_layout", &root_util::sextuple_layout)
            .def("sextuple_layout2", &root_util::sextuple_layout2)
            .def("mypalette1", &root_util::mypalette1)
            .def("mypalette2", &root_util::mypalette2)
            .def("mypalette3", &root_util::mypalette3)
            .def("mypalette4", &root_util::mypalette4)
            .def("palette_red2blue", &root_util::palette_red2blue)
            .def("palette_rainbow", &root_util::palette_rainbow)
            .def("view_graph",    &root_util::view_graph)
            .def("input_xname",   &root_util::input_xname)
            .def("input_yname",   &root_util::input_yname)
            .def("input_zname",   &root_util::input_zname)
            .def("input_xlim",    &root_util::input_xlim)
            .def("input_ylim",    &root_util::input_ylim)
            .def("input_zlim",    &root_util::input_zlim)
            .def("input_palette", &root_util::input_palette)
            .def("show_prop", &root_util::show_prop)
            .def("set_prop", &root_util::set_prop)
            .def("set_box", &root_util::set_box)
//            .def_pickle(root_util_pickle_suite())
            ;
}

//int main(){
//    a aaa;
//    aaa.b();
//    return 0;
//}
