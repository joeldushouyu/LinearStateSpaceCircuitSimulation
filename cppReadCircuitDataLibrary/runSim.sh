#!/bin/bash

# make
#  ./simulation_main ../Metadata.h5 2>stder.log 1>stdout.log
# python plot_data.py




# Usage: ./runSimulation.sh ../Metadata.h5

if [ $# -lt 1 ]; then
  echo "Usage: $0 <path_to_Metadata.h5>"
  exit 1
fi

HDF5_FILE=$1

make
./simulation_main "$HDF5_FILE" 2>stder.log 1>stdout.log

python plot_data.py "$HDF5_FILE"
