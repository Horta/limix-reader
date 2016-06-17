from numpy import asarray
from numpy import intersect1d
from numpy import union1d
from numpy.ma import masked_invalid

from ..util import define_binary_operators
from ..util import isscalar
from ..util import ndict
from ..util import list_transpose

from tabulate import tabulate

class Vector(object):
    def __init__(self, indices, values):
        self._indices = asarray(indices)
        self._values = asarray(values)

        n = len(values)
        self._map = ndict([(indices[i], values[i]) for i in range(n)])

    def merge(self, that):
        uidx = union1d(self._indices, that._indices)
        iidx = intersect1d(self._indices, that._indices)

        vals_lhs = self._map[iidx]
        vals_rhs = that._map[iidx]
        if any(vals_lhs != vals_rhs):
            raise ValueError("Values differ between the merging vectors.")

        def onehas(key, l, r):
            return l[key] if key in l else r[key]

        return Vector(uidx, [onehas(i, self, that) for i in uidx])

    @property
    def index_values(self):
        return self._indices

    def __len__(self):
        return len(self._values)

    def __contains__(self, idx):
        return idx in self._map

    def __getitem__(self, idx):
        if isscalar(idx):
            return self._map[idx]
        return Vector(idx, [self._map[i] for i in idx])

    def items(self):
        return VectorItems(self)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        l = [list(self._indices), list(self._values)]
        return tabulate(list_transpose(l), tablefmt="plain")

    def __array__(self):
        return self._values

    @property
    def dtype(self):
        return self._values.dtype

    def __compare__(self, that, opname):
        if isinstance(that, Vector):
            idx_lhs = self._indices
            idx_rhs = that._indices
            indices = intersect1d(idx_lhs, idx_rhs)

            vals_lhs = masked_invalid(self._map[indices])
            vals_rhs = masked_invalid(that._map[indices])

            return indices[getattr(vals_lhs, opname)(vals_rhs)]

        return self._indices[getattr(self._values, opname)(that)]

define_binary_operators(Vector, '__compare__')

class VectorItems(object):
    def __init__(self, ref):
        self._ref = ref

    def __len__(self):
        return len(self._ref)

    def __iter__(self):
        return len(self._ref)
