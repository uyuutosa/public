template<typename T>
void ndarr<T>::transpose_rec(int tmp2, vector<int> &mult_arr, vector<int> &arr){
    int n = arr[0];
    int mult = mult_arr[0];
    if (arr.size() == 1){
        for(int i=0; i<n; i++){
            tmp_v[mult*i+tmp2] = v[i+cnt];
        }
        cnt += n;
      
    }
    else{
        vector<int> arr2 = slice(arr, 1, arr.size());
        vector<int> mult_arr2 = slice(mult_arr, 1, mult_arr.size());
        for (int i = 0; i < n; i++){ 
            transpose_rec(tmp2,mult_arr2, arr2);
            tmp2 += mult;
        }
        tmp = 0;
    }
}


template<typename T>
ndarr<T> ndarr<T>::transpose(vector<int> &t_lst){
    int n(t_lst.size());
    vector<int> t_shape(n); 
    vector<int> t_shape2(n); 
    vector<int> mult_t_shape(n,1); 
    vector<int> mult_shape(n);
    for (int i=0; i<n; i++) t_shape[i] = shape[t_lst[i]];
    for (int i=n-1; i>=0; i--) t_shape2[i] = shape[t_lst[i]];
    int mul(1);
    for (int i=shape.size()-1; i>=0; i--) {
        mult_shape[i] = mul;
        mul *= t_shape[i];
    }
    for (int i=0; i<n; i++) mult_t_shape[i] = mult_shape[t_lst[i]];
    cnt = 0;
    tmp_v.clear();
    tmp_v.resize(v.size());
    tmp =0;
    
    transpose_rec(0, mult_t_shape, shape);
    ndarr<T> ret_arr(tmp_v, t_shape);
    return ret_arr;
}

template<typename T>
ndarr<T> ndarr<T>::transpose(int num, ...){
    va_list args;
    vector<int> t_lst(ndim);

    va_start(args, ndim-1);
    t_lst[0] = num;
    for (int i=1; i<ndim; i++) t_lst[i] = va_arg(args, int);
    ndarr<T> ret_arr(transpose(t_lst));
    va_end(args);
    return ret_arr;
}
