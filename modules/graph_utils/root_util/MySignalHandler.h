// MySignalHandler.h
#include<iostream>
#include "TSysEvtHandler.h"
#include "TSystem.h"


class MySignalHandler : public TSignalHandler{
public:
    MySignalHandler(ESignals sig) : TSignalHandler(sig){}
    Bool_t Notify();
};

Bool_t MySignalHandler::Notify()
{
    std::cout << "Catch signal" << (UInt_t)GetSignal() << std::endl;

    gSystem->ExitLoop();

    return kTRUE;
}
