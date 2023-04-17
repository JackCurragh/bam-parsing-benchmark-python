import argparse
import time
import resource
from cython_samtools_python_parser import parse_bam
import os
from rich import print

def main(args):
    start_time = time.time()
    read_df = parse_bam(args.bam_file)
    end_time = time.time()

    print("CPU usage:", resource.getrusage(resource.RUSAGE_SELF).ru_utime)
    print("Memory usage:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    print("Execution time:", end_time - start_time)
    with open('results.csv', 'a') as f:
        if args.header:
            f.write('experiment_name,input_bam,num_reads,max_mem,max_cpu,time\n')
        f.write(f"{os.path.basename(__file__).strip('.py')},{args.bam_file},{len(read_df)},"
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