#!/bin/bash

if [ $# -lt 1 ]; then
  echo "Usage: $0 <path_to_Metadata.h5>"
  exit 1
fi

HDF5_FILE=$1

make hdf5_reader
./hdf5_reader "$HDF5_FILE" > hdf5_reader_output.txt

python generate_config.py ./config.json \
  --final_json final_config.json \
  --header circuitConfig.hpp \
  --override TRUE \
  --CTNumber 1
