# cython: language_level=3
import resource
import time
import os
import argparse
import pandas as pd
import subprocess

from rich import print
import HTSeq

def parse_bam(bam_file):
    cdef str cmd = f'samtools view {bam_file}'
    cdef process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, text=True)

    cdef list read_list = []
    cdef str line
    cdef list fields
    for line in iter(process.stdout.readline, ''):
        if line.startswith('@'):
            continue
        fields = line.strip().split('\t')
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
            'tags': fields[11:],
            'count': count
        })

    process.communicate()
    return pd.DataFrame(read_list)