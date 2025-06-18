#!/bin/bash

script_dir=$(dirname "$(readlink -f "$0")")
if [ $# -lt 5 ]; then
    echo "Usage: $0 <number_of_runs> <MetadataFile> <bitstream> <runtimeSequnece> <result_csv_path> [high_priority=1]"
    exit 1
fi

X=$1
MetadataFile=$2
Bitstream=$3
RuntimeSequence=$4
RESULT_CSV=$5
HIGH_PRIORITY=${6:-0}

for ((i=1; i<=X; i++))
do
    echo "Run $i of $X"
    if [ "$HIGH_PRIORITY" -eq 1 ]; then
        echo "Running with high priority (nice -20)..."
        sudo nice -20 $script_dir/run.exe "$MetadataFile" "$Bitstream" "$RuntimeSequence" "$RESULT_CSV"
    else
        $script_dir/run.exe "$MetadataFile" "$Bitstream" "$RuntimeSequence" "$RESULT_CSV"
    fi
    if [ $i -lt $X ]; then
        echo "Waiting 1 seconds before next run..."
        sleep 1
    fi
done