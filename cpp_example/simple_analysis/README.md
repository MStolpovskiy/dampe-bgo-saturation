A simple analysis example using the DmpBgoSatApi to retrieve the BGO energy.

The example shows how to get the reconstructed BGO energy for the saturated events
using the hypothesis that the arriving particle is proton, helium or carbon
(Getting the hypothesis of any other particle is the same -- just specify the particle charge)
But it might not work for electrons / gammas!

* Don't forget to run the

source setup.sh

from the level above

* Compile with

source compile.sh

* Run with 

./example `head -1 test_skim.txt`

* Don't forget to fix the paths to the python installation both in setup.sh and compile.sh