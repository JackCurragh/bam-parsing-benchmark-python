
for file in benchmarks/*.py; do
    if [ $file == "benchmarks/bench_bam_parsing.py" ]; then
        continue
    fi
    echo "Running ${file}"
    python $file --bam_file bam_files/subsampled_1_percent.bam
    python $file --bam_file bam_files/subsampled_5_percent.bam
    python $file --bam_file bam_files/subsampled_10_percent.bam
    echo
done

#!/bin/bash

# function run_benchmark() {
#     file="$1"
#     bam_file="$2"
#     if [ "$file" == "benchmarks/bench_bam_parsing.py" ]; then
#         return
#     fi
#     echo "Running ${file} with ${bam_file}"
#     python "$file" --bam_file "$bam_file"
#     echo
# }

# export -f run_benchmark

# find benchmarks -type f -name "*.py" | parallel -j "$(nproc)" run_benchmark "{}" bam_files/subsampled_1_percent.bam
# find benchmarks -type f -name "*.py" | parallel -j "$(nproc)" run_benchmark "{}" bam_files/subsampled_5_percent.bam
# find benchmarks -type f -name "*.py" | parallel -j "$(nproc)" run_benchmark "{}" bam_files/subsampled_10_percent.bam
