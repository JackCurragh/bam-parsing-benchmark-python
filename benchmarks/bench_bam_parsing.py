'''
Run benchmarks on the BAM parsing implementations.

this script is to be run by richbench (richbech bencharks/) from the root of the repository.

'''

from pysam_dict import parse_bam as parse_bam_dict
from pysam_df import parse_bam as parse_bam_df
from pysam_numpy import parse_bam as parse_bam_numpy
from htseq_dict import parse_bam as parse_bam_htseq_dict
from htseq_df import parse_bam as parse_bam_htseq_df
from htseq_numpy import parse_bam as parse_bam_htseq_numpy
from samtools_sam_pure_python import parse_bam as parse_bam_samtools_sam_pure_python
from samtools_sam_pure_python_df import parse_bam as parse_bam_samtools_sam_pure_python_df
from cython_samtools_python_parser import parse_bam as parse_bam_samtools_sam_pure_python_df_w_duplicate_handling_cython

bam_file = "bam_files/subsampled_1_percent.bam"

def benchmark_pysam_dict():
    result = parse_bam_dict(bam_file)

def benchmark_pysam_df():
    result = parse_bam_df(bam_file)

def benchmark_pysam_numpy():
    result = parse_bam_numpy(bam_file)

def benchmark_htseq_dict():
    result = parse_bam_htseq_dict(bam_file)

def benchmark_htseq_df():
    result = parse_bam_htseq_df(bam_file)

def benchmark_htseq_numpy():
    result = parse_bam_htseq_numpy(bam_file)

def benchmark_samtools_sam_pure_python():
    result = parse_bam_samtools_sam_pure_python(bam_file)

def benchmark_samtools_sam_pure_python_df():
    result = parse_bam_samtools_sam_pure_python_df(bam_file)

def benchmark_samtools_sam_pure_python_df_w_duplicate_handling_cython():
    result = parse_bam_samtools_sam_pure_python_df_w_duplicate_handling_cython(bam_file)

# ... (Repeat the same for the other implementations)

__benchmarks__ = [

    ## Pysam Comparisons
    # (benchmark_pysam_dict, benchmark_pysam_df, "Pysam: Dictionary vs DataFrame"),
    # (benchmark_pysam_dict, benchmark_pysam_numpy, "Pysam: Dictionary vs Numpy"),
    # (benchmark_pysam_df, benchmark_pysam_numpy, "Pysam: DataFrame vs Numpy"),

    # HTSeq Comparisons
    # (benchmark_htseq_dict, benchmark_htseq_df, "HTSeq Dictionary vs DataFrame"),
    # (benchmark_htseq_dict, benchmark_htseq_numpy, "HTSeq Dictionary vs Numpy"),
    # (benchmark_htseq_df, benchmark_htseq_numpy, "HTSeq DataFrame vs Numpy"),

    # Pysam vs HTSeq
    # (benchmark_pysam_dict, benchmark_htseq_dict, "Dictionary: Pysam vs HTSeq"),
    # (benchmark_pysam_df, benchmark_htseq_df, "DataFrame: Pysam vs HTSeq"),
    # (benchmark_pysam_numpy, benchmark_htseq_numpy, "Numpy: Pysam vs HTSeq"),

    # Samtools vs Pysam
    # (benchmark_pysam_dict, benchmark_samtools_sam_pure_python, "Dictionary: Pysam vs Samtools"),
    # (benchmark_pysam_df, benchmark_samtools_sam_pure_python, "DataFrame: Pysam vs Samtools"),
    # (benchmark_pysam_numpy, benchmark_samtools_sam_pure_python, "Numpy: Pysam vs Samtools"),

    # Samtools vs HTSeq
    # (benchmark_htseq_dict, benchmark_samtools_sam_pure_python, "Dictionary: HTSeq vs Samtools"),
    # (benchmark_htseq_df, benchmark_samtools_sam_pure_python, "DataFrame: HTSeq vs Samtools"),
    # (benchmark_htseq_numpy, benchmark_samtools_sam_pure_python, "Numpy: HTSeq vs Samtools"),

    # Samtools Comparisons
    (benchmark_samtools_sam_pure_python, benchmark_samtools_sam_pure_python_df, "Samtools: Dict vs DataFrame"),
    (benchmark_samtools_sam_pure_python, benchmark_samtools_sam_pure_python_df_w_duplicate_handling_cython, "Samtools: Dict vs DataFrame w/ Cython"),
    (benchmark_samtools_sam_pure_python, benchmark_samtools_sam_pure_python_df, "Dictionary: Samtools pure vs Samtools pysam"),







]
