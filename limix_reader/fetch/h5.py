import h5py

from numpy import asarray

def fetch(filename, itempath):
    with h5py.File(filename, 'r') as f:
        return asarray(f[itempath])
