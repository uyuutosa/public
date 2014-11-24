
template<typename T>
void ndarr<T>::view_rec(vector<int> arr, int w){
    int n = arr[0];
    if (arr.size() == 1){
        cout << "[";
        int end = cnt + arr[0];
        for(int i=cnt; i<end; i++){
            cout << scientific << setprecision(2) 
            << v[i] << " ";
        }
        cnt = end;
        cout << "]";
    }
    else{
        vector<int> arr2 = slice(arr, 1, arr.size());
        cout << "[";
        w++;
        view_rec(arr2, w);
        if (n != 1) cout << endl;
        for (int i = 1; i < n; i++){ 
            cout << setw(w);
            view_rec(arr2, w);
            if (i != n-1) cout << endl;
        }
        cout << "]";
    }

}

template<typename T>
void ndarr<T>::view(){
   cnt = 0;
   view_rec(shape, 1);
   cout << endl << endl;
}
