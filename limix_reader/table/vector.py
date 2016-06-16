from collections import MutableMapping
from collections import OrderedDict as odict

from numpy import asarray
from numpy import vectorize
from numpy import atleast_1d
from numpy import intersect1d
from numpy.ma import masked_invalid

from ..util import npy2py_cast
from ..util import npy2py_type
from ..util import define_binary_operators

def __npy_map(v, d):
    return d[v]

_npy_map = vectorize(__npy_map)

class Vector(object):
    def __init__(self, labels, values):
        labels = asarray(labels).astype(npy2py_type(type(labels[0])))
        self._labels = labels

        values = asarray(values).astype(npy2py_type(type(values[0])))
        self._values = values

        n = len(values)
        self._map = odict([(labels[i], values[i]) for i in range(n)])

    def merge(self, that):
        from .mvector import MVector
        return MVector(self, that)

    @property
    def index_values(self):
        return self._labels

    def __len__(self):
        return len(self._values)

    def __getitem__(self, args):
        if npy2py_type(type(args)) in [int, bytes, float]:
            return npy2py_cast(self._map[args])
        idx = atleast_1d(args)
        return asarray([self._map[i] for i in idx])

    def items(self):
        return VectorView(self, self._map)

    def __repr__(self):
        return repr(self.__array__())

    def __str__(self):
        return bytes(self.__array__())

    def __array__(self):
        return self._values

    @property
    def dtype(self):
        return npy2py_type(self._values.dtype)

    def __compare__(self, that, opname):
        if isinstance(that, Vector):
            labels_lhs = self._labels
            labels_rhs = that._labels
            labels = intersect1d(labels_lhs, labels_rhs)

            vals_lhs = masked_invalid(_npy_map(labels, self._map))
            vals_rhs = masked_invalid(_npy_map(labels, that._map))

            return self._labels[getattr(vals_lhs, opname)(vals_rhs)]

        return self._labels[getattr(self._values, opname)(that)]

define_binary_operators(Vector, '__compare__')
