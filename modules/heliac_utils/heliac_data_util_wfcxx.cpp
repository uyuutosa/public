#include"myheader.h"
#include <boost/python/numeric.hpp>
#include <boost/numeric/ublas/vector.hpp>

extern "C" {
    struct mod_get_hel_data_mp_xydata {
        double xarr[20000];
        double yarr[20000];
    };
    int mod_get_hel_data_mp_get_hel_data_(int *shot, int *ch, struct mod_get_hel_data_mp_xydata *xys);
}

typedef struct mod_get_hel_data_mp_xydata xydata;

boost::python::numeric::array tmp(int shot, int  ch){
    vector<double> tmpxvec;
    vector<double> tmpyvec;
    boost::python::list tmpylst;
    xydata xys;
    int i, num;
    num=mod_get_hel_data_mp_get_hel_data_(&shot,&ch, &xys);
    //boost::numeric::ublas::vector<double> tmpxvec(num);
    //boost::numeric::ublas::vector<double> tmpyvec(num);

    for(i=0;i< num; i++){
        tmpxvec.push_back(xys.xarr[i]);
        tmpyvec.push_back(xys.yarr[i]);
        //tmpxvec[i] = xys.xarr[i];
        //tmpyvec[i] = xys.yarr[i];
    }
    boost::python::numeric::array bbb(boost::python::make_tuple(tmpyvec.begin(),tmpyvec.end()));
    return bbb;
}

boost::python::tuple get_heliac_data(int shot, int  ch){
//void get_heliac_data(int shot, int  ch){
    boost::python::list tmpxlst;
    boost::python::list tmpylst;
    xydata xys;
    int i, num;

    num = mod_get_hel_data_mp_get_hel_data_(&shot,&ch, &xys);
    
    for(i=0; i<num-10; i++){
        cout << xys.xarr[i]<<endl;
        tmpxlst.append(xys.xarr[i]);
        tmpylst.append(xys.yarr[i]);
    }
    //return boost::python::make_tuple(tmpxlst, tmpylst);
    //boost::python::numeric::array ret(boost::python::make_tuple(tmpxlst, tmpylst));
    //return ret;
}

boost::python::tuple multiget(boost::python::list shotlst, boost::python::list  chlst){
   // boost::python::numeric::array tmparr;
    boost::python::tuple tmptpl;
    boost::python::list tmpxlst;
    boost::python::list tmpylst;
    int i, j;

    for(i=0; i<boost::python::len(shotlst); i++){
        for(j=0; j<boost::python::len(chlst); j++){
            tmptpl = get_heliac_data(boost::python::extract<int>(shotlst[i]),boost::python::extract<int>(chlst[j]));
            tmpxlst.append(tmptpl[0]);
            tmpylst.append(tmptpl[1]);
        }

    }
    return boost::python::make_tuple(tmpxlst, tmpylst);
    //boost::python::numeric::array ret(boost::python::make_tuple(tmpxlst, tmpylst));
    //return ret;
}

BOOST_PYTHON_MODULE(heliac_data_util_wfcxx)
{
        using namespace boost::python;
        Py_Initialize();
        numeric::array::set_module_and_type("numpy", "ndarray");
//            def("gdat", &get_heliac_data);
//            def("hello", &hello_);
//        class_<heliac_data_util>("heliac_data_util")
//              .def_readwrite("xlst", &heliac_data_util::xlst)
//              .def_readwrite("ylst", &heliac_data_util::ylst)
//              .def_readwrite("xlsts", &heliac_data_util::xlsts)
//              .def_readwrite("ylsts", &heliac_data_util::ylsts)
              def("tmp", &tmp);
              def("gdat", &get_heliac_data);
//              def("gdats", &multiget);
}
