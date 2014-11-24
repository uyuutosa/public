#include<vector>
using namespace std;

template<typename T>
vector<T> slice(vector<T> v, int st, int en);


template<typename T, T Func(T)>
ndarr<T> ufunc(ndarr<T> obj);


