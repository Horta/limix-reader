from .cbed import bed_ffi

from numpy import nan
from numpy import asarray

def item(filepath, s, m, shape):
    fp = _filepath_pointer(filepath)
    v = bed_ffi.lib.bed_item(fp, shape[0], shape[1], s, m)
    return nan if v == 3 else float(v)

def intidx(filepath, samples, markers, shape, G):
    fp = _filepath_pointer(filepath)

    strides = asarray(G.strides, int)
    strides = _pointer(strides, 'long')

    n, p = len(samples), len(markers)

    G = _pointer(G, 'double')
    samples = _pointer(samples, 'long')
    markers = _pointer(markers, 'long')

    bed_ffi.lib.bed_intidx(fp, shape[0], shape[1], n, samples,
                           p, markers, G, strides)


def _filepath_pointer(filepath):
    return bed_ffi.ffi.new("char[]", filepath)

def _pointer(x, type_):
    return bed_ffi.ffi.cast("%s*" % type_, x.ctypes.data)
