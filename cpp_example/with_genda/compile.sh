g++ -std=c++11 -Wall *.cpp -o example \
 -I${DAMPEBGOAPI}/api/include \
 -L${DAMPEBGOAPI}/api/lib -lDampeBgoApi \
 -I/cvmfs/dampe.cern.ch/centos7/opt/conda_python2.7_tensorflow/include/python2.7 \
 -L/cvmfs/dampe.cern.ch/centos7/opt/conda_python2.7_tensorflow/lib -lpython2.7 -lssl -lPyROOT \
 -I${DMPSWSYS}/include \
 -L${DMPSWSYS}/lib -lDmpEvent -lDmpKernel -lDmpService -lDmpTool \
 -I${GENDA}/include \
 -L${GENDA}/lib -lGenDa \
 `root-config --cflags --libs`

