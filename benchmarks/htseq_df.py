'''
Experiment where we use pysam to read a bam file and print out the
number of reads in the file.
'''
import resource
import time
import os

import argparse
import pandas as pd

from rich import print

import HTSeq

def parse_bam(bam_file: str) -> list:
    '''
    This function will parse a BAM file and return a list of the reads using HTSeq.
    '''

    data = []

    with HTSeq.BAM_Reader(bam_file) as bam_reader:
        for alignment in bam_reader:
            if '_x' in alignment.read.name:
                count = int(alignment.read.name.split('_x')[-1])
            else:
                count = 1
            data.append({
                'read_name': alignment.read.name,
                'read_length': len(alignment.read),
                'reference_name': alignment.iv.chrom if alignment.iv is not None else "",
                'reference_start': alignment.iv.start if alignment.iv is not None else -1,
                'reference_end': alignment.iv.end if alignment.iv is not None else -1,
                'sequence': alignment.read.seq,
                'sequence_qualities': alignment.read.qual,
                'tags': alignment.optional_fields,
                'count': count,
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