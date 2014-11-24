template<typename T>
void ndarr<T>::at_rec(vector<int> tmp_shape){
    vector<T> pre_v;

    if (tmp_shape.size() == 1){
            int end = cnt + tmp_shape[0];
            
            for(int i=cnt; i<end; i++){ 
                tmp_vec.push_back(v[i]);
            }
            cnt = end;
            
    }
    else{
        vector<int> tmp_shape2 = slice(shape, 1, tmp_shape.size());
        for (int i = 0; i < tmp_shape[0]; i++) at_rec(tmp_shape2);
    }
}
    
template<typename T>
ndarr<T> ndarr<T>::at(int n){
    tmp_vec.clear();
    vector<int> ret_shape;
    if (shape.size() == 1) {
        tmp_vec.push_back(v[n]);
        ret_shape.push_back(1);
    }
    else{
        cnt = n;
        ret_shape = slice(shape, 1, shape.size());
        for (auto a:ret_shape) cnt *= a;
        at_rec(shape);
    }
    ndarr<T> ret_t(tmp_vec, ret_shape);
    ret_t.view();
    return ret_t;
}
