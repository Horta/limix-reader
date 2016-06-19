from numpy import asarray
from .scalar import isscalar

class ndict(dict):
    def __getitem__(self, key):
        if isscalar(key):
            return super(ndict, self).__getitem__(key)
        return asarray([self[k] for k in key], dtype=int)
