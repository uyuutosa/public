//#define BOOST_PYTHON_STATIC_LIB
//#define BOOST_TEST_DYN_LINK
//#include <boost/python.hpp>
#include <vector>
#include <sstream>
//#include <pyublas/numpy.hpp>
#include <iostream>

using namespace std;

//-------------------------------------

class set_prop{
public:
    Int_t t;    
};

//-------------------------------------

class graph_prop{
public:
    Char_t *xname, *yname, *zname, *palette;
    Double_t xlim[2], ylim[2], zlim[2];
    vector<set_prop> slst;

    graph_prop(){
        init();
    }

    void init(){
    Int_t g;
    xname = "None";
    yname = "None";
    zname = "None";
    palette = "rainbow";
    xlim[0] = 0;
    xlim[1] = 0;
    ylim[0] = 0;
    ylim[1] = 0;
    zlim[0] = 0;
    zlim[1] = 0;
    }

};

//-------------------------------------


class input_prop{
public:
    vector<graph_prop> glst;
    void input_xname(Char_t *xname, Int_t gnum);
    void input_yname(Char_t *yname, Int_t gnum);
    void input_zname(Char_t *zname, Int_t gnum);
    void input_xlim(Double_t xmin, Double_t xmax, Int_t gnum);
    void input_ylim(Double_t ymin, Double_t ymax, Int_t gnum);
    void input_zlim(Double_t zmin, Double_t zmax, Int_t gnum);
    void input_palette(Char_t *palette, Int_t gnum);
    void glst_check(Int_t gnum);
    void show_prop();
};

void input_prop::show_prop(){
    Int_t i;
    for (i=0; i<glst.size(); i++){
        cout << "--------------------" << endl;
        cout << "       graph " << i << endl;
        cout << "--------------------" << endl;
        cout << left << setw(10) << "xname ";
        cout << left << setw(10) << glst[i].xname << endl;
        cout << left << setw(10) << "yname ";
        cout << left << setw(10) << glst[i].yname << endl;
        cout << left << setw(10) << "zname ";
        cout << left << setw(10) << glst[i].zname << endl;
        cout << left << setw(10) << "xlim";
        cout << left << glst[i].xlim[0] << ", "<< glst[i].xlim[1] << endl;
        cout << left << setw(10) << "ylim";
        cout << left << glst[i].ylim[0] << ", "<< glst[i].ylim[1] << endl;
        cout << left << setw(10) << "zlim";
        cout << left << glst[i].zlim[0] << ", "<< glst[i].zlim[1] << endl;
    }
}

void input_prop::input_xname(Char_t *xname, Int_t gnum){
    glst_check(gnum);
    glst[gnum].xname = xname;
}

void input_prop::input_yname(Char_t *yname, Int_t gnum){
    glst_check(gnum);
    glst[gnum].yname = yname;
}

void input_prop::input_zname(Char_t *zname, Int_t gnum){
    glst_check(gnum);
    glst[gnum].zname = zname;
}

void input_prop::input_xlim(Double_t xmin, Double_t xmax, Int_t gnum){
    glst_check(gnum);
    glst[gnum].xlim[0] = xmin;
    glst[gnum].xlim[1] = xmax;
}

void input_prop::input_ylim(Double_t ymin, Double_t ymax, Int_t gnum){
    glst_check(gnum);
    glst[gnum].ylim[0] = ymin;
    glst[gnum].ylim[1] = ymax;
}

void input_prop::input_zlim(Double_t zmin, Double_t zmax, Int_t gnum){
    glst_check(gnum);
    glst[gnum].zlim[0] = zmin;
    glst[gnum].zlim[1] = zmax;
}

void input_prop::input_palette(Char_t *palette, Int_t gnum){
    glst_check(gnum);
    glst[gnum].palette = palette;
}

void input_prop::glst_check(Int_t gnum){
    cout << glst.size() << endl;
    if (glst.size() <= gnum){
        while (glst.size() <= gnum){
            graph_prop tmp;    
            glst.push_back(tmp);
        }
    }
}

//-------------------------------------

