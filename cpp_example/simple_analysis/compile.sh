g++ -std=c++11 -Wall *.cpp -o example \
 -I${PEVSPACE_CONDA_PATH}/include/python2.7 \
 -L${PEVSPACE_CONDA_PATH}/lib -lpython2.7 -lssl -lPyROOT \
 -I${DAMPEBGOAPI}/api/include \
 -L${DAMPEBGOAPI}/api/lib -lDampeBgoApi \
 -I${DMPSWSYS}/include \
 -L${DMPSWSYS}/lib -lDmpEvent -lDmpKernel -lDmpService -lDmpTool \
 `root-config --cflags --libs`

