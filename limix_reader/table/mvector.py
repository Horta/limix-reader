from numpy import union1d
from numpy import intersect1d
from numpy import any

class MVector(object):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

    @property
    def index_values(self):
        return union1d(self._lhs.index_values, self._rhs.index_values)

#     def __len__(self):
#         return len(self._values)
#
#     def __getitem__(self, args):
#         if npy2py_type(type(args)) in [int, bytes, float]:
#             return npy2py_cast(self._map[args])
#         idx = atleast_1d(args)
#         return asarray([self._map[i] for i in idx])
#
#     def items(self):
#         return VectorView(self, self._map)
#
    def __repr__(self):
        return repr(self.__array__())

    def __str__(self):
        return bytes(self.__array__())

    def __array__(self):
        idx = intersect1d(self._lhs.index_values, self._rhs.index_values)
        vals_lhs = self._lhs[idx]
        vals_rhs = self._rhs[idx]
        if any(vals_lhs != vals_rhs):
            raise ValueError("Values differ among vectors.")
        return vals_lhs
#
#     def __array__(self):
#         return self._values
#
#     @property
#     def dtype(self):
#         return npy2py_type(self._values.dtype)
#
#     def __compare__(self, that, opname):
#         if isinstance(that, Vector):
#             labels_lhs = self._labels
#             labels_rhs = that._labels
#             labels = intersect1d(labels_lhs, labels_rhs)
#
#             vals_lhs = _npy_map(labels, self._map)
#             vals_rhs = _npy_map(labels, that._map)
#
#             return self._labels[getattr(vals_lhs, opname)(vals_rhs)]
#
#         return self._labels[getattr(self._values, opname)(that)]
#
# define_binary_operators(Vector, '__compare__')
