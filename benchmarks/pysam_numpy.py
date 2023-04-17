'''
Experiment where we use pysam to read a bam file and print out the
number of reads in the file.
'''
import resource
import time
import os

import pysam
import argparse
from rich import print


import numpy as np

def parse_bam(bam_file: str) -> np.ndarray:
    '''
    This function will parse a BAM file and return a NumPy structured array of the reads.
    '''

    dtype = [
        ('read_name', 'U50'),
        ('read_length', np.uint32),
        ('reference_name', 'U50'),
        ('reference_start', np.int32),
        ('reference_end', np.int32),
        ('sequence', 'U50'),
        ('sequence_qualities', 'O'),
        ('tags', 'O'),
        ('count', np.uint32)
    ]

    data = []

    # Open the BAM file
    with pysam.AlignmentFile(bam_file, 'rb') as bam_file:
        for read in bam_file:
            if '_x' in read.query_name:
                count = int(read.query_name.split('_x')[-1])
            else:
                count = 1
            data.append((
                read.query_name,
                read.query_length if read.query_length is not None else 0,
                read.reference_name if read.reference_name is not None else "",
                read.reference_start if read.reference_start is not None else -1,
                read.reference_end if read.reference_end is not None else -1,
                read.query_sequence if read.query_sequence is not None else "",
                read.query_qualities if read.query_qualities is not None else [],
                read.tags if read.tags is not None else [],
                count
            ))

    return np.array(data, dtype=dtype)

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
        if args.header:
            f.write('experiment_name,input_bam,num_reads,max_mem,max_cpu,time\n')
        f.write(f"{os.path.basename(__file__).strip('.py')},{args.bam_file},{len(read_dict)},"
                f"{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},"
                f"{resource.getrusage(resource.RUSAGE_SELF).ru_utime},"
                f"{end_time - start_time}\n")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bam_file', type=str, default='data/NA12878.bam',
                        help='The BAM file to read')
    parser.add_argument('--header', action='store_true', default=False, help='Print the header')
    args = parser.parse_args()
    main(args)