from .interface import MatrixInterface

from numpy import asarray
from numpy import arange

from ..util import ndict

class MatrixView(MatrixInterface):
    def __init__(self, ref, sample_ids, marker_ids):
        super(MatrixView, self).__init__()
        self._ref = ref
        self._sample_ids = asarray(sample_ids)
        self._marker_ids = asarray(marker_ids)

        n = len(self._sample_ids)
        p = len(self._marker_ids)

        self._sample_map = ndict(zip(self._sample_ids, arange(n, dtype=int)))
        self._marker_map = ndict(zip(self._marker_ids, arange(p, dtype=int)))

    def item(self, sample_id, marker_id):
        if sample_id in self._sample_map and marker_id in self._marker_map:
            return self._ref.item(sample_id, marker_id)
        raise IndexError

    def __getitem__(self, args):
        raise NotImplementedError

    @property
    def shape(self):
        raise NotImplementedError

    def _shape(self, index_list):
        return self._shape([self._index]+index_list)

    @property
    def ndim(self):
        return 2

    @property
    def dtype(self):
        return self._ref.dtype

    def __repr__(self):
        return repr(self.__array__())

    def __str__(self):
        return bytes(self.__array__())

    def __array__(self, *args, **kwargs):
        kwargs = dict(kwargs)

        if 'sample_ids' not in kwargs:
            kwargs['sample_ids'] = self._sample_ids
            kwargs['marker_ids'] = self._marker_ids

            kwargs['sample_map'] = self._sample_map
            kwargs['marker_map'] = self._marker_map

        return self._ref.__array__(*args, **kwargs)

    @property
    def sample_ids(self):
        return self._sample_ids([])

    @property
    def marker_ids(self):
        return self._marker_ids([])
