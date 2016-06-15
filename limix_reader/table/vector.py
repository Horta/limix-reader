from collections import MutableMapping
from collections import OrderedDict as odict

from numpy import asarray
from numpy import vectorize
from numpy import atleast_1d

from ..util import npy2py_cast
from ..util import npy2py_type

# def __npy_map(v, d):
#     return d[v]
#
# _npy_map = vectorize(__npy_map)

class Vector(object):
    def __init__(self, labels, values):
        labels = asarray(labels).astype(npy2py_type(type(labels[0])))
        self._labels = labels

        values = asarray(values).astype(npy2py_type(type(values[0])))
        self._values = values

        n = len(values)
        self._map = odict([(labels[i], values[i]) for i in range(n)])

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
        return repr(self._values)

    def __str__(self):
        return bytes(self._values)

    def __array__(self):
        return self._values

    @property
    def dtype(self):
        return npy2py_type(self._values.dtype)

    def __eq__(self, that):
        if isinstance(that, Vector):
            raise NotImplementedError
        return self._labels[self._values == that]

    def __ne__(self, that):
        if isinstance(that, Vector):
            raise NotImplementedError
        return self._labels[self._values != that]

    def __ge__(self, that):
        if isinstance(that, Vector):
            raise NotImplementedError
        return self._labels[self._values >= that]

    def __gt__(self, that):
        if isinstance(that, Vector):
            raise NotImplementedError
        return self._labels[self._values > that]

class VectorView(MutableMapping):
    def __init__(self, _ref, map_):
        self._ref, self._map = _ref, map_

    def __getitem__(self, key):
        if key in self._map.keys():
            return self._map[key]
        else:
            raise KeyError(key)

    def __len__(self):
        return len(self._map)

    def __iter__(self):
        for (key, val) in iter(self._map.items()):
            yield key, val

    def __setitem__(self, key, value):
        if key in self._map:
            self._map[key] = value
        else:
            raise KeyError(key)

    def __delitem__(self, key):
        self._map.remove(key)
