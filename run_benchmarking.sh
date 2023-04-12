
# This script contains the code to execute experiments found in the experiments directory and
# output the results to a file. The results are outputted in a format that can be used by the
# plot_benchmarking.py script to generate plots of the results.

# Results fields are as follows:
#     - experiment_name: The name of the experiment
#     - input_bam: The input BAM file
#     - num_reads: The number of reads in the input BAM file
#     - max_mem: The maximum memory used by the experiment
#     - max_cpu: The maximum CPU used by the experiment
#     - time: The total time taken by the experiment



BAM_FILE=$1

# run all experiments in the experiments directory
for experiment in experiments/*.py; do
    # get the experiment name
    experiment_name=$(basename $experiment .py)

    # run the experiment
    echo "Running experiment $experiment_name"
    python $experiment --bam_file $BAM_FILE

done