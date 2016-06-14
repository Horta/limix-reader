from .bed_ffi import ffi
from .bed_ffi.lib import bed_item
from .bed_ffi.lib import bed_fancyidx
from .bed_ffi.lib import bed_slice
from .bed_ffi.lib import bed_entirely
from .bed_ffi.lib import bed_row_slice
from .bed_ffi.lib import bed_column_slice
from .bed_ffi.lib import bed_snp_major

from numpy import empty
from numpy import nan

def item(filepath, r, c, shape):
    if _snp_major(filepath):
        r, c = c, r
        shape = (shape[1], shape[0])

    fp = ffi.new("char[]", filepath)
    v = bed_read_item(fp, shape[0], shape[1], r, c)

    return nan if v == 3 else float(v)

def fancyidx(filepath, shape, rows, cols, G):
    fp = _filepath_pointer(filepath)
    G = _matrix_pointer(G)
    bed_fancyidx(fp, shape[0], shape[1], len(rows), rows, len(cols), cols, G)

def slice(filepath, shape, c_start, c_stop, c_step,
          r_start, r_stop, r_step, G):

    if _snp_major(filepath):
        shape = (shape[1], shape[0])
        _slice(filepath, shape, r_start, r_stop, r_step,
               c_start, c_stop, c_step, G)
    else:
        _slice(filepath, shape, c_start, c_stop, c_step,
               r_start, r_stop, r_step, G)

def row_slice(filepath, r, start, stop, step, shape):
    major = _bed_major(filepath)

    if major == 'm':
        shape = (shape[1], shape[0])
        G = _read_col_slice(filepath, r, start, stop, step, shape)
    elif major == 's':
        G = _read_row_slice(filepath, r, start, stop, step, shape)

    return _normalize(G)

def column_slice(filepath, c, start, stop, step, shape):
    major = _bed_major(filepath)

    if major == 'm':
        shape = (shape[1], shape[0])
        G = _read_row_slice(filepath, c, start, stop, step, shape)
    elif major == 's':
        G = _read_col_slice(filepath, c, start, stop, step, shape)

    return _normalize(G)

def read(filepath, shape):
    major = _bed_major(filepath)
    if major == 'm':
        shape = (shape[1], shape[0])
        G = _read(filepath, shape)
        G = G.T
    elif major == 's':
        G = _read(filepath, shape)

    return _normalize(G)

def _read_slice(filepath, rslice, cslice, shape):
    fp = bed_ffi.ffi.new("char[]", filepath)
    nrows = (rslice.stop - rslice.start) // rslice.step
    ncols = (cslice.stop - cslice.start) // cslice.step
    G = empty((nrows, ncols), dtype=int)
    pointer = bed_ffi.ffi.cast("long*", G.ctypes.data)

    bed_ffi.lib.bed_read_slice(fp, shape[0], shape[1], c,
                                   start, stop, step, pointer)

    return G

def _snp_major(filepath):
    fp = bed_ffi.ffi.new("char[]", filepath)
    return bed_ffi.lib.snp_major(fp)

def _normalize(G):
    G = G.astype(float)
    G[G == 3] = nan
    return G

def _filepath_pointer(filepath):
    return bed_ffi.ffi.new("char[]", filepath)

def _matrix_pointer(G):
    return bed_ffi.ffi.cast("long*", G.ctypes.data)

def _read_row_slice(filepath, r, start, stop, step, shape):
    fp = _filepath_pointer(filepath)
    G = empty((stop - start)//step, dtype=int)
    pointer = _matrix_pointer(G)

    bed_ffi.lib.bed_row_slice(fp, shape[0], shape[1], r,
                              start, stop, step, pointer)

    return G

def _read_col_slice(filepath, c, start, stop, step, shape):
    fp = _filepath_pointer(filepath)
    G = empty((stop - start)//step, dtype=int)
    pointer = _matrix_pointer(G)

    bed_ffi.lib.bed_column_slice(fp, shape[0], shape[1], c,
                                 start, stop, step, pointer)

    return G

def _entirely(filepath, shape):
    fp = _filepath_pointer(filepath)
    G = empty(shape, dtype=int)
    pointer = _matrix_pointer(G)
    bed_entirely(fp, shape[0], shape[1], pointer)
    return G

def _slice(filepath, shape, c_start, c_stop, c_step,
           r_start, r_stop, r_step, G):
    fp = _filepath_pointer(filepath)
    pointer = _matrix_pointer(G)

    bed_slice(fp, shape[0], shape[1],
              r_start, r_stop, r_step,
              c_start, c_stop, c_step,
              pointer)
