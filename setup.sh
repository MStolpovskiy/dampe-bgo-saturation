#!/bin/bash

source /cvmfs/dampe.cern.ch/centos7/etc/setup_conda_python2.7_tensorflow2.1.sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
export DAMPEBGOAPI=$DIR
