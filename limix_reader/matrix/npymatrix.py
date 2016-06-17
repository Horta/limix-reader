from numpy import atleast_2d
from numpy import arange
from numpy import asarray

from .interface import MatrixInterface
from .view import MatrixView
from ..util import isscalar
from ..util import ndict

def _get_ids(ids, size):
    if ids is None:
        return arange(size, dtype=int)
    else:
        if isscalar(ids):
            return asarray([ids])
        else:
            return asarray(ids)

class NPyMatrix(MatrixInterface):
    def __init__(self, arr, sample_ids=None, marker_ids=None):
        super(NPyMatrix, self).__init__()
        self._arr = atleast_2d(arr)

        self._sample_ids = _get_ids(sample_ids, self._arr.shape[0])
        self._marker_ids = _get_ids(marker_ids, self._arr.shape[1])

        n = len(self._sample_ids)
        p = len(self._marker_ids)

        self._sample_map = ndict(zip(self._sample_ids, arange(n, dtype=int)))
        self._marker_map = ndict(zip(self._marker_ids, arange(p, dtype=int)))

    def item(self, sample_id, marker_id):
        if sample_id in self._sample_map and marker_id in self._marker_map:
            return self._arr.item(self._sample_map[sample_id],
                                  self._marker_map[marker_id])
        raise IndexError

    def __getitem__(self, args):
        if isscalar(args):
            args = (args,)

        if len(args) == 1:
            args = (args[0], self._marker_ids)

        args_ = []
        for i in range(2):
            if isscalar(args[i]):
                args_.append([args[i]])
            else:
                args_.append(args[i])

        args = tuple(args_)

        return MatrixView(self, args[0], args[1])

    @property
    def shape(self):
        return self._arr.shape

    @property
    def dtype(self):
        return self._arr.dtype

    def __repr__(self):
        return self._arr.__repr__()

    def __str__(self):
        return self._arr.__str__()

    def __array__(self, *args, **kwargs):
        kwargs = dict(kwargs)

        if 'sample_ids' not in kwargs:
            kwargs['sample_ids'] = self._sample_ids
            kwargs['marker_ids'] = self._marker_ids

        sample_idx = self._sample_map[kwargs['sample_ids']]
        marker_idx = self._marker_map[kwargs['marker_ids']]

        return atleast_2d(self._arr[sample_idx,:][:,marker_idx])

    @property
    def sample_ids(self):
        return self._sample_ids

    @property
    def marker_ids(self):
        return self._marker_ids
