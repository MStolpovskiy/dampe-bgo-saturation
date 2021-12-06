#!/bin/bash

working_dir=`pwd`

cd /atlas/users/andrii/conda_test/pevspace-ml-tracking-0-0-4_p01/api/script
source ./setup_gridvm10.sh

dampe_init trunk
export LD_LIBRARY_PATH=$DMPSWSYS/lib:${LD_LIBRARY_PATH}

source ~/DAMPE/GenDa/bin/thisgenda.sh

cd $working_dir

export DAMPEBGOAPI=/atlas/users/stolpovs/DAMPE/dampe-bgo-saturation/
