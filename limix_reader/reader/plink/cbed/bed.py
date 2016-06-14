from os.path import join
from os.path import dirname
from os.path import realpath

from cffi import FFI

root = dirname(realpath(__file__))

ffi = FFI()

include_dirs = [root]
src_files = [join(root, 'bed.c')]

ffi.set_source('lim.reader.cplink.bed_ffi',
        '#include "bed.h"',
        include_dirs=include_dirs,
        sources=src_files,
        libraries=[])

ffi.cdef("""
int bed_item(char* filepath, int nrows, int ncols, int row, int col);

void
bed_slice(char* filepath, int nrows, int ncols,
               int r_start, int r_stop, int r_step,
               int c_start, int c_stop, int c_step,
               long* matrix);

void
bed_row_slice(char* filepath, int nrows, int ncols, int row,
                   int c_start, int c_stop, int c_step,
                   long* matrix);

void
bed_column_slice(char* filepath, int nrows, int ncols, int col,
                  int r_start, int r_stop, int r_step,
                  long* matrix);

void
bed_entirely(char* filepath, int nrows, int ncols, long* matrix);

int
bed_snp_major(char* filepath);

void
bed_fancyidx(char* filepath, int nrows, int ncols,
             int rn, long* rows, int cn, long* cols, long* matrix);
""")


if __name__ == '__main__':
    ffi.compile(verbose=True)
