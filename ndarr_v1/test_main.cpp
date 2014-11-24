#include "ndarr.hpp"

using namespace std;

int main(){
    /*
    ndarr<T> is a thing so-called "N dimensional array".
    This is able to have any dimension.
    "N dimensional array" is maily provided high-level language
    such as Fortran, Python, MATLAB and so on but C++ is not seemed 
    to be provided.
    C++ is a program which has both high speed performance and high readability. 
    There are realization with genelic programing due to
    the template metaprograming.
    Using these technic abundantly,
    ndarr<T> will be more fastly and usuful. 
    
    
    Fllow test program is overview of andarr<T>.
    */
//    
    //setting dimension.
    ndarr<double> a{2}; 
    ndarr<double> b{3,2}; 
    ndarr<double> c{4,3,2};
    ndarr<double> d{5,4,3,2};
    ndarr<double> e{6,5,4,3,2};
    ndarr<double> f{7,6,5,4,3,2};
    ndarr<double> g{8,7,6,5,4,3,2};

    //for example, input the number from 0 to {array size -1}.
    a.range(); 
    b.range();
    c.range();
    d.range();
    e.range();
    f.range();
    g.range();

    
    cout << "1. array is able to be viewed with following format" << endl;
    cout << "a =" << endl;
    a.view();
    cout << "b =" << endl;
    b.view();
    
    cout << "2. Binary operation is supported." << endl;
    cout << "a + 2 - a * a / 4 =" << endl;
    (a+2.-a*a/4.).view();
    cout << endl;

    cout << "3. So-called 'broadcast' tecnhnic is supported." << endl;
    cout << "a + b = [0 1] + [[0 1], [2 3], [4 5]] =" << endl; 
    (a+b).view();

    cout << "a + b + c + d + e + f + g" << endl 
    << " = {is also able to be calculeted but too big to output.}" << endl; 
    cout << endl;

    cout << "4. Product of dot, cross and diad is suported." << endl;
    cout << "The dot product of a and b is " << endl;
    a.dot(b).view();
    cout << "The cross product of a and b is " << endl;
    a.cross(b).view();
    cout << "The diadic product of a and b is " << endl;
    a.diad(b).view();
    cout << endl;
    
    cout << "5. Universal function is roughly supported." << endl;
    cout << "sin(b) = "  << endl;
    ufunc<double, sin>(b).view();
    cout << "fabs(b) = "  << endl;
    ufunc<double, fabs>(b).view();
    cout << endl;

    cout << "6. Transpose is supported." << endl;
    cout << "b's dimension transpose [0,1] to [1,0] as fllows." << endl;
    b.transpose(1,0).view();
    cout << "c's dimension transpose [0,1,2] to [0,2,1] as fllows." << endl;
    c.transpose(0,2,1).view();
    cout << "c's dimension transpose [0,1,2] to [2,1,0] as fllows." << endl;
    c.transpose(2,1,0).view();
    cout << endl;
    
    cout << "7. Other utility menber function is provided a little." << endl;
    cout << "min(b) =  "<< b.min() << endl;
    cout << "sum(b) =  "<< b.max() << endl;
    cout << "sum(b) =  "<< b.sum() << endl;
    cout << "mean(b) =  "<< b.mean() << endl;
}
