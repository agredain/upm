%module jsupm_adxl335
%include "../upm.i"
%include "cpointer.i"

%pointer_functions(int, intPointer);
%pointer_functions(float, floatPointer);

%{
    #include "adxl335.hpp"
%}

%include "adxl335.hpp"
