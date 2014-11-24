enum objects {THIS, OBJ};
template<typename T>
vector<int> ndarr<T>::check_shape(ndarr &obj){
    enum objects which_is_small = shape.size() < obj.shape.size() ? THIS : OBJ;
    vector<int> small_shape;
    vector<int> large_shape;
    switch(which_is_small){
        case THIS:
            small_shape = shape;
            large_shape = obj.shape;
            //vector<int> ret_shape(shape);
            break;
        case OBJ:
            small_shape = obj.shape;
            large_shape = shape;
            break;
    }

    cnt = 0;
    for (int i=1; i<=small_shape.size(); i++){
        if( shape[shape.size()-i] != obj.shape[obj.shape.size()-i]) throw "shape mismatch.";
        large_shape.pop_back();
        
    }

    return large_shape;
}

template<typename T>
void ndarr<T>::broadcast_rec(int shape_n){
    vector<T> tmp_v(v);
    shape.insert(shape.begin(), shape_n);
    for (int i=0; i<shape_n-1; i++)
        v.insert(v.end(), tmp_v.begin(), tmp_v.end());
}

template<typename T>
void ndarr<T>::broadcast(ndarr &obj){
   try{
       vector<int> conca_shape(check_shape(obj));
        enum objects which_is_small = shape.size() < obj.shape.size() ? THIS : OBJ;
        switch(which_is_small){
            case THIS:
                for (auto a:conca_shape) broadcast_rec(a);
                break;
            case OBJ:
                for (auto a:conca_shape) obj.broadcast_rec(a);
                break;
        }

   } catch(const char*  mismatch){
       cerr << mismatch << endl;
       exit(1);
   }
}
