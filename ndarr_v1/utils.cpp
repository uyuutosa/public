#include "ndarr.hpp"

template<typename T>
vector<T> slice(vector<T> v, int st, int en){
    vector<T> ret_v;
    for (int i=st; i<en; i++) ret_v.push_back(v[i]);
    return ret_v;
}

template<typename T, T Func(T)>
ndarr<T> ufunc(ndarr<T> obj){
    vector<T> ret_v;
    for (auto a:obj.v) ret_v.push_back(Func(a));
    ndarr<T> ret(ret_v, obj.shape);
    return ret;
}


