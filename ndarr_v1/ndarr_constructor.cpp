template<typename T>
ndarr<T>::ndarr(initializer_list<int> list){
    for (auto a:list) shape.push_back(a);
    for (auto a:shape) size *= a;
    v.resize(size);
    ndim = shape.size();
}

template<typename T>
ndarr<T>::ndarr(vector<T> &vec, vector<int> &tmp_shape){
    shape = tmp_shape;
    v = vec;
    ndim = shape.size();
}

template<typename T>
ndarr<T>::ndarr(const ndarr<T> &obj){
    shape = obj.shape;
    v = obj.v;
}
