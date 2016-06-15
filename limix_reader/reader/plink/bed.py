from .cbed import bed_ffi

from numpy import nan

def item(filepath, s, m, shape):
    fp = _filepath_pointer(filepath)
    v = bed_ffi.lib.bed_item(fp, shape[0], shape[1], s, m)
    return nan if v == 3 else float(v)

def intidx(filepath, samples, markers, shape, G):
    fp = _filepath_pointer(filepath)

    strides = bed_ffi.ffi.new("int[2]")
    strides[0] = G.strides[0]
    strides[1] = G.strides[1]

    G = _matrix_pointer(G)
    bed_ffi.lib.bed_intidx(fp, shape[0], shape[1], len(samples), samples,
                           len(markers), markers, G, strides)


def _filepath_pointer(filepath):
    return bed_ffi.ffi.new("char[]", filepath)

def _matrix_pointer(G):
    return bed_ffi.ffi.cast("double*", G.ctypes.data)

def _strides_pointer(strides):
    return bed_ffi.ffi.cast("long*", strides.ctypes.data)
