
template<typename T>
void ndarr<T>::zeros(){
    show(shape);
    for (int i = 0; size > i; i++)
        v[i] = 0;
}

template<typename T>
void ndarr<T>::range(){
    for (int i = 0; size > i; i++)
        v[i] = i;
}

    


template<typename T>
ndarr<T> permutation_symbol(int n){
    int plus;
    int minus;
    int quo;
    int mod;
    vector<int> ret_shape;
    vector<T> ret_v(pow(n,n));
    vector<int> comp_v;
    bool unique;
    for(int i=0; i<pow(n,n); i++){
        plus = 0;
        minus = 0;
        quo = i;
        comp_v.clear();
        unique = true;

        for (int j=n-1; j>=0; j--){
            mod  = quo % n;
            quo /= n;
            for (auto a:comp_v)
                if(a == mod) unique = false;
            comp_v.push_back(mod);
            if (mod - j == 0) continue;
            (mod - j) < 0 ? minus++ : plus++;
        }
        if (!unique) ret_v[i] = 0;
        else if (minus > plus) ret_v[i] = minus % 2 ? -1 : 1;
        else  ret_v[i] = plus % 2  ? -1 : 1;
    }
    for (int i = 0; i<n; i++) ret_shape.push_back(n);
    ndarr<T> ret_arr(ret_v, ret_shape);
    return ret_arr;
}
