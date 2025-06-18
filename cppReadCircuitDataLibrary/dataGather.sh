#!/bin/bash
# source mlir with sudo
# make sure have sudo privilege, so sub  script can run sudo without asking for password
sudo -v
ulimit -s unlimited
ulimit -v unlimited
echo "Stack size: $(ulimit -s)"
echo "Virtual memory: $(ulimit -v)"
# Check H Clock
if ! xrt-smi examine --advanced -r clocks | grep -q "H Clock *: *1800 MHz"; then
    echo "Error: H Clock is not 1800 MHz!"
    exit 1
fi
# get current directory
current_dir=$(pwd)
NPUproject_dir=$current_dir/../NPUproject
twoCTCacheVersion_dir=$NPUproject_dir/twoCTPerCircuit
twoCTCacheVersion_bitstream=$twoCTCacheVersion_dir/build/xclbins/mv.xclbin 
twoCTCacheVersion_runtimeSequence=$twoCTCacheVersion_dir/build/insts/mv.txt

twoNoCTCacheVersion_dir=$NPUproject_dir/twoCTPerCircuitNoCache
twoNoCTCacheVersion_bitstream=$twoNoCTCacheVersion_dir/build/xclbins/mv.xclbin 
twoNoCTCacheVersion_runtimeSequence=$twoNoCTCacheVersion_dir/build/insts/mv.txt
# First, do the 2CT with Cache version
make clean
make hdf5_reader -j8

rm  -f result_cachex100.csv
rm -f result_cachex100_low_nice.csv
rm  -f result_nocachex100.csv
rm -f result_nocachex100_low_nice.csv
rm -f discard.csv

two_CT_cache_run_data_gather() {
    local MedataFileName="$1"
    ./config_two_CT_no_bank_conflict_only.sh ../$MedataFileName
    make -C "$twoCTCacheVersion_dir" clean
    make -C "$twoCTCacheVersion_dir" run

    bash  $twoCTCacheVersion_dir/run_multiple.sh  20  $twoCTCacheVersion_dir/$MedataFileName \
        $twoCTCacheVersion_bitstream $twoCTCacheVersion_runtimeSequence  $current_dir/discard.csv 
    bash  $twoCTCacheVersion_dir/run_multiple.sh  50  $twoCTCacheVersion_dir/$MedataFileName \
        $twoCTCacheVersion_bitstream $twoCTCacheVersion_runtimeSequence   $current_dir/result_cachex100.csv # launch data gather for this version

    # warmpup first 
    bash  $twoCTCacheVersion_dir/run_multiple.sh  20  $twoCTCacheVersion_dir/$MedataFileName \
        $twoCTCacheVersion_bitstream $twoCTCacheVersion_runtimeSequence  $current_dir/discard.csv 1
    bash  $twoCTCacheVersion_dir/run_multiple.sh  50  $twoCTCacheVersion_dir/$MedataFileName \
        $twoCTCacheVersion_bitstream $twoCTCacheVersion_runtimeSequence  $current_dir/result_cachex100_low_nice.csv  1
}


two_CT_no_cache_run_data_gather() {
    local MedataFileName="$1"
    ./config_two_CT_no_cache.sh ../$MedataFileName
    make -C "$twoNoCTCacheVersion_dir" clean
    make -C "$twoNoCTCacheVersion_dir" run

    bash  $twoNoCTCacheVersion_dir/run_multiple.sh  20  $twoNoCTCacheVersion_dir/$MedataFileName \
        $twoNoCTCacheVersion_bitstream $twoNoCTCacheVersion_runtimeSequence  $current_dir/discard.csv 
    bash  $twoNoCTCacheVersion_dir/run_multiple.sh  50  $twoNoCTCacheVersion_dir/$MedataFileName \
        $twoNoCTCacheVersion_bitstream $twoNoCTCacheVersion_runtimeSequence   $current_dir/result_nocachex100.csv # launch data gather for this version

    # warmpup first 
    bash  $twoNoCTCacheVersion_dir/run_multiple.sh  20  $twoNoCTCacheVersion_dir/$MedataFileName \
        $twoNoCTCacheVersion_bitstream $twoNoCTCacheVersion_runtimeSequence  $current_dir/discard.csv 1
    bash  $twoNoCTCacheVersion_dir/run_multiple.sh  50  $twoNoCTCacheVersion_dir/$MedataFileName \
        $twoNoCTCacheVersion_bitstream $twoNoCTCacheVersion_runtimeSequence  $current_dir/result_nocachex100_low_nice.csv  1
}


MedataFileName=Metadata_half_bridge_llc_0.004.h5
two_CT_cache_run_data_gather "$MedataFileName"

MedataFileName=Metadata_half_bridge_llc_0.04.h5
two_CT_cache_run_data_gather "$MedataFileName"


MedataFileName=Metadata_half_bridge_llc_0.4.h5
two_CT_cache_run_data_gather "$MedataFileName"


#MedataFileName=Metadata_half_bridge_llc_2.h5
#two_CT_cache_run_data_gather "$MedataFileName"



MedataFileName=Metadata_half_bridge_llc_0.004.h5
two_CT_no_cache_run_data_gather "$MedataFileName"

MedataFileName=Metadata_half_bridge_llc_0.04.h5
two_CT_no_cache_run_data_gather "$MedataFileName"

MedataFileName=Metadata_half_bridge_llc_0.4.h5
two_CT_no_cache_run_data_gather "$MedataFileName"

# MedataFileName=Metadata_half_bridge_llc_2.h5
# two_CT_no_cache_run_data_gather "$MedataFileName"
