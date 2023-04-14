'''
Experiment where we use pysam to read a bam file and print out the
number of reads in the file.
'''
import resource
import time
import os

import pandas as pd
import pysam
import argparse

def parse_bam(bam_file: str) -> pd.DataFrame:
    '''
    This function will parse a BAM file and return a DataFrame of the reads.
    '''
    data = []

    # Open the BAM file
    with pysam.AlignmentFile(bam_file, 'rb') as bam_file:
        for read in bam_file:
            data.append({
                'read_name': read.query_name,
                'read_length': read.query_length,
                'reference_name': read.reference_name,
                'reference_start': read.reference_start,
                'reference_end': read.reference_end,
                'sequence': read.query_sequence,
                'sequence_qualities': read.query_qualities,
                'tags': read.tags,
            })

    return pd.DataFrame(data)

def main(args):
    '''
    Main function for the script. This function will execute all experiments found in the
    experiments directory and output the results to a file.
    '''
    start_time = time.time()

    read_dict = parse_bam(args.bam_file)

    end_time = time.time()

    print("CPU usage:", resource.getrusage(resource.RUSAGE_SELF).ru_utime)
    print("Memory usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print("Execution time:", end_time - start_time)

    with open('results.csv', 'a') as f:
        f.write('experiment_name,input_bam,num_reads,max_mem,max_cpu,time\n')
        f.write(f"{os.path.basename(__file__).strip('.py')},{args.bam_file},{len(read_dict)},"
                f"{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},"
                f"{resource.getrusage(resource.RUSAGE_SELF).ru_utime},"
                f"{end_time - start_time}\n")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bam_file', type=str, default='data/NA12878.bam',
                        help='The BAM file to read')
    args = parser.parse_args()
    main(args)