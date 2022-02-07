g++ -std=c++11 -Wall *.cpp -o example \
 -I/cvmfs/dampe.cern.ch/centos7/opt/conda_python2.7_tensorflow/include/python2.7 \
 -L/cvmfs/dampe.cern.ch/centos7/opt/conda_python2.7_tensorflow/lib -lpython2.7 -lssl -lPyROOT \
 -I${DAMPEBGOAPI}/api/include \
 -L${DAMPEBGOAPI}/api/lib -lDampeBgoApi \
 -I${DMPSWSYS}/include \
 -L${DMPSWSYS}/lib -lDmpEvent -lDmpKernel -lDmpService -lDmpTool \
 `root-config --cflags --libs`

