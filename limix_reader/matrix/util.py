from numpy import full
from numpy import arange
from numpy import asarray

from ..util import isscalar

def normalize_getitem_args(args, marker_ids):
    if isscalar(args):
        args = (args,)

    if len(args) == 1:
        args = (args[0], marker_ids)

    args_ = []
    for i in range(2):
        if isscalar(args[i]):
            args_.append([args[i]])
        else:
            args_.append(args[i])

    return tuple(args_)

def get_ids(ids, size):
    if ids is None:
        return arange(size, dtype=int)
    else:
        if isscalar(ids):
            return asarray([ids])
        else:
            return asarray(ids)

def get_alleles(alleles, size, default_char_name):
    if alleles is None:
        return full(size, default_char_name, dtype='|S1')
    else:
        if isscalar(alleles):
            return asarray([alleles])
        else:
            return asarray(alleles)
