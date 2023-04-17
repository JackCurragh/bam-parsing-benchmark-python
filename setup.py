from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("benchmarks/cython_samtools_python_parser.pyx", compiler_directives={'language_level': "3"}),
)