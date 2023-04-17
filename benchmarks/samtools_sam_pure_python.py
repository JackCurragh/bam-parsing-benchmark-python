


'''
Experiment where we use pysam to read a bam file and print out the
number of reads in the file.
'''
import resource
import time
import os

import argparse
import pandas as pd
import subprocess

from rich import print

import HTSeq

def parse_bam(bam_file: str) -> list:
    '''
    This function will convert a BAM file to SAM format, read the output in chunks,
    and then parse the SAM data using pure Python.
    '''

    # Convert the BAM file to SAM format and read the output in chunks
    cmd = f'samtools view {bam_file}'
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, text=True)

    read_list = []
    for line in iter(process.stdout.readline, ''):
        fields = line.strip().split('\t')

        if line.startswith('@'):
            continue
        if '_x' in fields[0]:
            count = int(fields[0].split('_x')[-1])
        else:
            count = 1
        read_list.append({
            'read_name': fields[0],
            'read_length': len(fields[9]),
            'reference_name': fields[2],
            'reference_start': int(fields[3]) - 1,
            'sequence': fields[9],
            'sequence_qualities': fields[10],
            'tags': fields[11:]
        })

    process.communicate()
    return read_list


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
    output_name = args.bam_file.split('/')[-1].split('.')[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bam_file', type=str, default='data/NA12878.bam',
                        help='The BAM file to read')
    parser.add_argument('--header', action='store_true', default=False, help='Print the header')
    args = parser.parse_args()
    main(args)