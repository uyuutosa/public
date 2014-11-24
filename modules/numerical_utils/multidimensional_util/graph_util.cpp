#define BOOST_PYTHON_STATIC_LIB
#include <boost/python.hpp>
#include <sstream>
#include <string>
#include <math.h>
#include <iostream>
#include <iomanip>
#include <boost/numeric/ublas/matrix.hpp>         
#include <boost/numeric/ublas/triangular.hpp>     
#include <boost/numeric/ublas/symmetric.hpp>      
#include <boost/numeric/ublas/hermitian.hpp>      
#include <boost/numeric/ublas/matrix_sparse.hpp>  
#include <boost/numeric/ublas/vector.hpp>         
#include <boost/numeric/ublas/vector_sparse.hpp>  
#include "root_util.cpp"


class handle_graph{
private:
    int  i;
    int size;
public:
    root_util root;
};
