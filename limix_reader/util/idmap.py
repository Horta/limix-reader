from numpy import asarray

from .ndict import ndict

class IdMap(object):
    def __init__(self, keys, values):
        self._keys = asarray(keys)
        self._values = asarray(values)
        self._map =  ndict(zip(keys, values))

    def __getitem__(self, key):
        return self._map[key]

    def __contains__(self, key):
        return key in self._map

    def keys(self):
        return self._keys

    def values(self):
        return self._values

    def __len__(self):
        return len(self._map)
