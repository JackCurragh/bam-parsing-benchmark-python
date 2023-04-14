'''
Experiment where we use pysam to read a bam file and print out the
number of reads in the file.
'''
import resource
import time
import os

import argparse

import HTSeq
from rich import inspect

def parse_bam(bam_file: str) -> list:
    '''
    This function will parse a BAM file and return a list of the reads using HTSeq.
    '''

    read_dict = {}

    with HTSeq.BAM_Reader(bam_file) as bam_reader:
        for alignment in bam_reader:
            read_dict[alignment.read.name] = {
                'read_name': alignment.read.name,
                'read_length': len(alignment.read),
                'reference_name': alignment.iv.chrom if alignment.iv is not None else "",
                'reference_start': alignment.iv.start if alignment.iv is not None else -1,
                'reference_end': alignment.iv.end if alignment.iv is not None else -1,
                'sequence': alignment.read.seq,
                'sequence_qualities': alignment.read.qual,
                'tags': alignment.optional_fields
            }

    return read_dict

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
    parser.add_argument('--bam-file', type=str, default='data/NA12878.bam',
                        help='The BAM file to read')
    args = parser.parse_args()
    main(args)