#ifndef _NDARR_
#define _NDARR_
#include<iostream>
#include<iomanip>
#include<vector>
#include<string>
#include<numeric>
#include<cmath>
#include<cstdarg>
using namespace std;

template<typename T>
class ndarr{
public:
    vector<int> shape;
    vector<T> v;
    //included ndarr_constructor.cpp----------------------
    ndarr(initializer_list<int> list);
    ndarr(vector<T> &vec, vector<int> &tmp_shape);
    ndarr(const ndarr<T> &obj);
    //included ndarr_ref.cpp------------------------------
    ndarr<T> at(int n);
    //included ndarr_view.cpp-----------------------------
    void view();
    //included ndarr_operators.cpp------------------------
    ndarr<T> operator [](int n);
    ndarr<T> operator +(ndarr<T> obj);
    ndarr<T> operator -(ndarr<T> obj);
    ndarr<T> operator *(ndarr<T> obj);
    ndarr<T> operator /(ndarr<T> obj);
    ndarr<T> operator +(T val);
    ndarr<T> operator -(T val);
    ndarr<T> operator *(T val);
    ndarr<T> operator /(T val);
    //included ndarr_broadcast.cpp------------------------
    vector<int> check_shape(ndarr &obj);
    void broadcast(ndarr &obj);
    //included ndarr_transpose.cpp------------------------
    ndarr<T> transpose(vector<int> &t_lst);
    ndarr<T> transpose(int num, ...);
    //included ndarr_gen.cpp------------------------------
    void zeros();
    void range();
    //included ndarr_math.cpp-----------------------------
    ndarr<T> dot(ndarr<T> &obj);
    void dot_rec(ndarr<T> &obj, vector<int> arr);
    ndarr<T> diad(ndarr<T> &obj);
    void diad_rec(ndarr<T> &obj, vector<int> arr);
    ndarr<T> cross(ndarr<T> &obj);
    T min();
    T max();
    T sum();
    T mean();
private:
    vector<T> tmp_vec;
    int cnt;
    int ndim;
    vector<T> tmp_v;
    int tmp;
    int size=1;
    string idxz;
    //included ndarr_ref.cpp------------------------------
    void at_rec(vector<int> tmp_shape);
    //included ndarr_view.cpp-----------------------------
    void view_rec(vector<int> arr, int w);
    //included ndarr_broadcast.cpp------------------------
    void broadcast_rec(int shape_n);
    //included ndarr_transpose.cpp------------------------
    void transpose_rec(int tmp2, vector<int> &mult_arr, vector<int> &arr);
};

#include "utils.cpp"
#include "ndarr_constructor.cpp"
#include "ndarr_ref.cpp"
#include "ndarr_view.cpp"
#include "ndarr_broadcast.cpp"
#include "ndarr_transpose.cpp"
#include "ndarr_operators.cpp"
#include "ndarr_gen.cpp"
#include "ndarr_math.cpp"


#endif
