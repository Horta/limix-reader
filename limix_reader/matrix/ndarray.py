from numpy import atleast_2d
from numpy import arange

from bidict import bidict

from .interface import MatrixInterface
from ..util import make_sure_list
from .view import MatrixView

class NPyMatrix(MatrixInterface):
    def __init__(self, arr, sample_ids=None, marker_ids=None):
        super(NPyMatrix, self).__init__()
        self._arr = atleast_2d(arr)

        if sample_ids is None:
            self._sample_ids = arange(self._arr.shape[0], dtype=int)
        else:
            self._sample_ids = sample_ids

        if marker_ids is None:
            self._marker_ids = arange(self._arr.shape[1], dtype=int)
        else:
            self._marker_ids = marker_ids

        n = len(self._sample_ids)
        p = len(self._marker_ids)
        self._sample_map = bidict(zip(self._sample_ids, arange(n, dtype=int)))
        self._marker_map = bidict(zip(self._marker_ids, arange(p, dtype=int)))

    def item(self, *args):
        return self._arr.item(*args)

    def __getitem__(self, args):
        sample_ids = make_sure_list(args[0])
        marker_ids = make_sure_list(args[1])
        return MatrixView(self, sample_ids, marker_ids)

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

        sample_idx = [self._sample_map[si] for si in kwargs['sample_ids']]
        marker_idx = [self._marker_map[mi] for mi in kwargs['marker_ids']]
        #
        # G = empty((len(sample_idx), len(marker_idx)))
        # read_bed_intidx(self._filepath, sample_idx, marker_idx, self.shape, G)
        #
        # return G
        return None

    @property
    def sample_ids(self):
        return self._sample_ids

    @property
    def marker_ids(self):
        return self._marker_ids
