#include<stdio.h>
#include<iostream>

//extern "C" void tmp_mp_get_hel_data_(int *shot, int *ch, double **x, double **y);
extern "C" struct tmp_mp_xydata {
    double *xarr, *arr;
            };
extern "C" void tmp_mp_get_hel_data_(int *shot, int *ch, struct tmp_mp_xydata **xys);//, double *x, double *y);
            

void test(int shot,int  ch, struct tmp_mp_xydata *xys){
    tmp_mp_get_hel_data_(shot,ch, &xys);//, &x, &y);
    std::cout<< xys->xarr[100] << std::endl;
}

void main(){
    test();
}
