#include "tensor.hpp"

using namespace std;

int main(){
    /*
    ndarr<T> is a thing so-called "N dimensional array".
    This is able to have any dimension.
    "N dimensional array" is maily provided high-level language
    such as Fortran, Python, Ruby and so on but C++ is not seemed 
    to be provided.
    C++ is a program which has both high speed performance and high readability. 
    There are realization with genelic programing due to
    the template metaprograming.
    Using these technic abundantly,
    ndarr<T> will be more fastly and usuful. 
    
    
    Fllow test program is overview of andarr<T>.
    */
    
    //setting dimension.
    ndarr<double> a{2}; 
    ndarr<double> b{3,2}; 
    ndarr<double> d{5,5}; 

    //for example, input the number from 0 to {array size -1}.
    a.range(); 
    b.range();
    d.range();

   // d.view();
    vector<int> c(4);
    c[0] = 3;
    c[1] = 1;
    c[2] = 2;
    c[3] = 0;
   // (d.transpose(c)).view();
    
    vector<int> e(2);
    e[0] = 1;
    e[1] = 0;
    //e[3] = 0;
    //e[4] = 3;
    d.view();
    (d.transpose(e)).view();

    
}
