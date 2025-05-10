

make hdf5_reader
./hdf5_reader  ../Metadata.h5  > hdf5_reader_output.txt

python generate_config.py ./config.json --final_json final_config.json --header circuitConfig.hpp --override TRUE