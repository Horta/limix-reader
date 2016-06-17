from numpy import intersect1d
from numpy import union1d
from numpy import arange
from numpy import isnan
from numpy import full
from numpy import nan

from .interface import MatrixInterface
from .view import MatrixView
from .util import normalize_getitem_args
from ..util import ndict

class MMatrix(MatrixInterface):
    def __init__(self, lhs, rhs):
        super(MMatrix, self).__init__()
        self._lhs = lhs
        self._rhs = rhs

        self._sample_ids = union1d(lhs.sample_ids, rhs.sample_ids)
        self._marker_ids = union1d(lhs.marker_ids, rhs.marker_ids)

        n = len(self._sample_ids)
        p = len(self._marker_ids)

        self._sample_map = ndict(zip(self._sample_ids, arange(n, dtype=int)))
        self._marker_map = ndict(zip(self._marker_ids, arange(p, dtype=int)))

    def item(self, sample_id, marker_id):
        if (sample_id not in self._sample_map and
                marker_id not in self._marker_map):
            raise IndexError

        try:
            v0 = self._lhs.item(sample_id, marker_id)
        except IndexError:
            v0 = nan

        try:
            v1 = self._rhs.item(sample_id, marker_id)
        except IndexError:
            v1 = nan

        if not isnan(v0) and not isnan(v1):
            if v0 != v1:
                msg = ("There are conflicting genotype values from" +
                       " different sources.")
                raise ValueError(msg)

        return v0 if isnan(v1) else v1

    def __getitem__(self, args):
        args = normalize_getitem_args(args, self._marker_ids)
        return MatrixView(self, args[0], args[1])

    @property
    def shape(self):
        return (len(self.sample_ids), len(self.marker_ids))

    @property
    def ndim(self):
        return 2

    @property
    def dtype(self):
        raise NotImplementedError

    def __repr__(self):
        return repr(self.__array__())

    def __str__(self):
        return bytes(self.__array__())

    @property
    def sample_ids(self):
        return self._sample_ids

    @property
    def marker_ids(self):
        return self._marker_ids

    def __array__(self, *args, **kwargs):
        kwargs = dict(kwargs)

        if 'sample_ids' not in kwargs:
            kwargs['sample_ids'] = self._sample_ids
            kwargs['marker_ids'] = self._marker_ids
            kwargs['sample_map'] = self._sample_map
            kwargs['marker_map'] = self._marker_map

        n = len(kwargs['sample_ids'])
        p = len(kwargs['marker_ids'])

        G = full((n, p), nan)

        s = intersect1d(self._lhs.sample_ids, kwargs['sample_ids'])
        m = intersect1d(self._lhs.marker_ids, kwargs['marker_ids'])

        sidx = kwargs['sample_map'][s]
        midx = kwargs['marker_map'][m]

        self._lhs._copy_to(s, m, sidx, midx, G)

        s = intersect1d(self._rhs.sample_ids, kwargs['sample_ids'])
        m = intersect1d(self._rhs.marker_ids, kwargs['marker_ids'])

        sidx = kwargs['sample_map'][s]
        midx = kwargs['marker_map'][m]

        self._rhs._copy_to(s, m, sidx, midx, G)

        return G
