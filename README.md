# dampe-bgo-saturation

BGO saturation correction using convolutional neural networks

Method is explained in details here:
https://arxiv.org/abs/2201.12185

* INSTALLATION:

1. Prerequirements : 
    Python 2.7.18
    tensorflow 2.1.0
    numpy
    root 5.34/36

   If you are using A. Tykhonov's tracking api, you have all dependencies
already installed. Simply use his setup scripts (these scripts are already used inside
the setup scripts of this package).

2. Modify setup.sh according to your installation. It is now written to use Tykhonov's api. Then

source setup.sh

3. Install python dampe_bgo package

cd dampe_bgo
pip install . --user

4. Install python api

cd ../api/python
pip install . --user

5. Compile C++ api

cd .. # to the api directory
make # build the C++ api library

* USAGE:

Run 'source setup.sh' before each use. Don't use root or dampe_init before setup.sh. See usage examples in the corresponding folders
