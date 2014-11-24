
template<typename T>
T ndarr<T>::max(){
    T max(v[0]);
    for (int i = 1; v.size() > i; i++){
        if (max < v[i]) max = v[i];
    }
    return max;
}

template<typename T>
T ndarr<T>::min(){
    T min(v[0]);
    for (int i = 1; v.size() > i; i++){
        if (min > v[i]) min = v[i];
    }
    return min;
}

template<typename T>
T ndarr<T>::sum(){
    T sum(0);
    for (int i = 0; v.size() > i; i++){
        sum += v[i];
    }
    return sum;
}

template<typename T>
T ndarr<T>::mean(){
    return sum() / v.size();
}

template<typename T>
void ndarr<T>::dot_rec(ndarr<T> &obj, vector<int> arr){
    int n = arr[0];
    if (arr.size() == 1){
        T ret_val(0);
        for(int j=0; j<obj.v.size(); j+=n){

            ret_val = 0;
            for(int i=0; i<n; i++){
               ret_val += v[i+cnt] * obj.v[i+j];
            }
            tmp_v.push_back(ret_val);
        }
        cnt += n;
    } else{
        vector<int> arr2 = slice(arr, 1, arr.size());
        for (int i = 0; i < n; i++){ 
            dot_rec(obj, arr2);
        }
    }
}

template<typename T>
ndarr<T> ndarr<T>::dot(ndarr<T> &obj){
   cnt = 0;
   tmp_v.clear();
   dot_rec(obj, shape);

   vector<int> conca_shape(shape);
   vector<int> obj_shape(obj.shape);
   conca_shape.pop_back();
   obj_shape.pop_back();
   conca_shape.insert(conca_shape.end(), obj_shape.begin(), obj_shape.end());
   ndarr<T> ret_arr(tmp_v, conca_shape);
   tmp_v.clear();
   return ret_arr;
}

template<typename T>
ndarr<T> ndarr<T>::diad(ndarr<T> &obj){
    tmp_v.clear();
    for(int j=0; j < v.size(); j++){
        for(int i=0; i< obj.v.size(); i++){
                tmp_v.push_back(v[i] * obj.v[j]);}
        }
    vector<int> conca_shape(shape);
    conca_shape.insert(conca_shape.end(), obj.shape.begin(), obj.shape.end());
    ndarr<T> ret_arr(tmp_v, conca_shape);
    tmp_v.clear();
    return ret_arr;
}


template<typename T>
ndarr<T> ndarr<T>::cross(ndarr<T> &obj){
    ndarr<T> arr(permutation_symbol<T>(shape[shape.size()-1]));
    ndarr<T> dot1(obj.dot(arr));
    ndarr<T> dot2(dot(dot1));
    ndarr<T> ret_arr(dot2);
    return ret_arr;
}
