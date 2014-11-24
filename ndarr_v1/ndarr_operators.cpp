
template<typename T>
ndarr<T> ndarr<T>::operator [](int n){
    return at(n);
}

template<typename T>
ndarr<T> ndarr<T>::operator +(ndarr<T> obj){
   broadcast(obj); 
   vector<T> ret_v(v.size());
   for (int i=0; i < v.size(); i++) ret_v[i] = v[i] + obj.v[i];
   ndarr<T> ret_t(ret_v, shape);
   return ret_t;
}

template<typename T>
ndarr<T> ndarr<T>::operator -(ndarr<T> obj){
   broadcast(obj); 
   vector<T> ret_v(v.size());
   for (int i=0; i < v.size(); i++) ret_v[i] = v[i] - obj.v[i];
   ndarr<T> ret_t(ret_v, shape);
   return ret_t;
}

template<typename T>
ndarr<T> ndarr<T>::operator *(ndarr<T> obj){
   broadcast(obj); 
   vector<T> ret_v(v.size());
   for (int i=0; i < v.size(); i++) ret_v[i] = v[i] * obj.v[i];
   ndarr<T> ret_t(ret_v, shape);
   return ret_t;
}

template<typename T>
ndarr<T> ndarr<T>::operator /(ndarr<T> obj){
   broadcast(obj); 
   vector<T> ret_v;
   for (int i=0; i < v.size(); i++) ret_v.push_back(v[i] / obj.v[i]);
   ndarr<T> ret_t(ret_v, shape);
   return ret_t;
}

template<typename T>
ndarr<T> ndarr<T>::operator +(T val){
   vector<T> ret_v;
   for (int i=0; i < v.size(); i++) ret_v.push_back(v[i] + val);
   ndarr<T> ret_t(ret_v, shape);
   return ret_t;
}

template<typename T>
ndarr<T> ndarr<T>::operator -(T val){
   vector<T> ret_v;
   for (int i=0; i < v.size(); i++) ret_v.push_back(v[i] - val);
   ndarr<T> ret_t(ret_v, shape);
   return ret_t;
}

template<typename T>
ndarr<T> ndarr<T>::operator *(T val){
   vector<T> ret_v;
   for (int i=0; i < v.size(); i++) ret_v.push_back(v[i] * val);
   ndarr<T> ret_t(ret_v, shape);
   return ret_t;
}

template<typename T>
ndarr<T> ndarr<T>::operator /(T val){
   vector<T> ret_v;
   for (int i=0; i < v.size(); i++) ret_v.push_back(v[i] / val);
   ndarr<T> ret_t(ret_v, shape);
   return ret_t;
}


//global -------------------


template<typename T>
ndarr<T> operator +(T val, ndarr<T> &obj){
   vector<T> ret_v(obj.v.size());
   for (int i=0; i < obj.v.size(); i++) ret_v[i] = val + obj.v[i];
   ndarr<T> ret_t(ret_v, obj.shape);
   return ret_t;
}

template<typename T>
ndarr<T> operator -(T val, ndarr<T> &obj){
   vector<T> ret_v(obj.v.size());
   for (int i=0; i < obj.v.size(); i++) ret_v[i] = val - obj.v[i];
   ndarr<T> ret_t(ret_v, obj.shape);
   return ret_t;
}

template<typename T>
ndarr<T> operator *(T val, ndarr<T> &obj){
   vector<T> ret_v(obj.v.size());
   for (int i=0; i < obj.v.size(); i++) ret_v[i] = val * obj.v[i];
   ndarr<T> ret_t(ret_v, obj.shape);
   return ret_t;
}

template<typename T>
ndarr<T> operator /(T val, ndarr<T> &obj){
   vector<T> ret_v(obj.v.size());
   for (int i=0; i < obj.v.size(); i++) ret_v[i] = val / obj.v[i];
   ndarr<T> ret_t(ret_v, obj.shape);
   return ret_t;
}
