from os.path import join
from os.path import dirname
from os.path import realpath

from distutils.sysconfig import get_python_inc

import numpy

from cffi import FFI

root = dirname(realpath(__file__))

ffi = FFI()

include_dirs = [root, get_python_inc(), numpy.get_include()]
src_files = [join(root, 'interface.c'), join(root, 'impl.c')]

ffi.set_source('limix_reader.reader.plink.cbed.bed_ffi',"""
#include "interface.h"
#include "impl.h"
#include <Python.h>
#include "numpy/npy_math.h"
""",
    include_dirs=include_dirs,
    sources=src_files,
    libraries=[])

ffi.cdef("""
int bed_item(char* filepath, int nsamples, int nmarkers, int sample, int marker);

void bed_intidx(char* filepath, int nsamples, int nmarkers,
                int sn, long* samples, int mn, long* markers, double* matrix,
                int* strides);
""")


if __name__ == '__main__':
    ffi.compile(verbose=True)
