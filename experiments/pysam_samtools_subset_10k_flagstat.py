'''
Experiment where we use pysam to read a bam file and print out the
number of reads in the file.
'''
import resource
import time
import os

import pysam
import argparse

def flagstat_bam(bam_path: str) -> dict:
    '''
    Run samtools flagstat on the bam file at the provided path and return a dictionary

    Inputs:
        bam_path: Path to the bam file

    Outputs:
        flagstat_dict: Dictionary containing the flagstat information
    
    '''
    flagstat_dict = {}
    with pysam.AlignmentFile(bam_path, "rb") as bamfile:
        flagstat_dict['total_reads'] = bamfile.mapped + bamfile.unmapped
        flagstat_dict['mapped_reads'] = bamfile.mapped
        flagstat_dict['unmapped_reads'] = bamfile.unmapped
        flagstat_dict['duplicates'] = bamfile.mapped + bamfile.unmapped
    return flagstat_dict


def parse_bam(bam_file: str) -> dict:
    '''
    This function will parse a BAM file and return a dictionary of the reads.
    '''
    flagstat = flagstat_bam(bam_file)
    fraction = 10000/flagstat['total_reads']

    pysam.view("-s", f"123.{str(fraction).split('.')[1]}", "-bo",  f"{bam_file}.subsampled.bam", f"{bam_file}")
    pysam.index(f"{bam_file}.subsampled.bam")

    read_dict = {}
    # Open the BAM file
    bam_file = pysam.AlignmentFile(f"{bam_file}.subsampled.bam", 'rb')

    for read in bam_file:
        if read.query_name not in read_dict:
            read_dict[read.query_name] = {
                        'read_name': read.query_name,
                        'read_length': read.query_length,
                        'reference_name': read.reference_name,
                        'reference_start': read.reference_start,
                        'reference_end': read.reference_end,
                        'sequence': read.query_sequence,
                        'sequence_qualities': read.query_qualities,
                        'tags': read.tags,
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
        f.write('experiment_name,input_bam,num_reads,max_mem,max_cpu,time')
        f.write(f"{os.path.basename(__file__).strip('.py')},{args.bam_file},{len(read_dict)},"
                f"{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},"
                f"{resource.getrusage(resource.RUSAGE_SELF).ru_utime},"
                f"{end_time - start_time}")
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bam_file', type=str, default='data/NA12878.bam',
                        help='The BAM file to read')
    args = parser.parse_args()
    main(args)