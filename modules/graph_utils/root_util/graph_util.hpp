#include<iostream>
#include<vector>
#include<TProfile.h>
#include<TApplication.h>

using namespace std;

class graph2d:public TProfile{

public:
    //int binum;
    //double_t, xmin, xmax,

    graph2d(): TProfile(){}
    graph2d(const char* name, const char* title, Int_t nbinsx,  Double_t xmin, Double_t xmax)
        :TProfile(name, title, nbinsx, xmin, xmax)
    {}

   // graph2d(const graph2d& obj){
   //     //xmin = obj.xmin;
   //     //xmax = obj.xmax;
   // }
   // ~graph2d(){}
    
};



//int main(){
//    TApplication app("app", 0,0,0,0);
//
//    //vector<test> a;
//    //test b;
//    //a.push_back(b);
//    //a[0].i = "asdf";
//    //a.push_back(b);
//    //a[1].i = "asdf";
//    //cout << a[0].i << a[1].i << endl;
//    graph2d a;
//    a.Fill(1.,2.);
//    a.Draw();
//    app.Run();
//    cout << "aaa" << endl;
//    
//    return 0;
//}
