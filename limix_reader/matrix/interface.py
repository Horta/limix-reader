from tabulate import tabulate

from numpy import isnan
from numpy import arange

from .util import get_ids
from .util import get_alleles
from ..util import isscalar
from ..util import ndict
from ..util import copyto_nans

class MatrixInterface(object):
    def __init__(self, sample_ids, marker_ids, allelesA, allelesB, shape):

        self._allelesA_map = None
        self._allelesB_map = None

        self._sample_ids = get_ids(sample_ids, shape[0])
        self._marker_ids = get_ids(marker_ids, shape[1])

        self._sample_map = ndict(zip(self.sample_ids,
                                     arange(shape[0], dtype=int)))

        self._marker_map = ndict(zip(self.marker_ids,
                                     arange(shape[1], dtype=int)))

        p = len(self._marker_ids)

        self._allelesA = get_alleles(allelesA, p, 'A')
        self._allelesB = get_alleles(allelesB, p, 'B')

        self._update_alleles_map()

    def _item(self, sample_id, marker_id):
        raise NotImplementedError

    def item(self, sample_id, marker_id, alleleB=None):
        if alleleB is None and marker_id in self._allelesB_map:
            alleleB = self._allelesB_map[marker_id]

        if sample_id in self._sample_map and marker_id in self._marker_map:
            v = self._item(self._sample_map[sample_id],
                           self._marker_map[marker_id])

            if isnan(v):
                return v

            eq = int(alleleB == self._allelesB_map[marker_id])
            return eq * v + (1-eq) * (2 - v)

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

        from .view import MatrixView
        return MatrixView(self, args[0], args[1])

    @property
    def shape(self):
        raise NotImplementedError

    @property
    def ndim(self):
        return 2

    @property
    def dtype(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__repr__()

    def __str__(self):
        p = self.shape[1]
        header = ['', 'marker_id: alleleA/alleleB'] + [''] * (p-1)
        alA = self.allelesA
        alB = self.allelesB
        mid = self.marker_ids
        subhdr = ['sample_id']
        subhdr += [bytes(mid[i])+': '+bytes(alA[i])+'/'+bytes(alB[i])
                   for i in range(p)]
        tbl = [header] + [subhdr]
        sid = self.sample_ids
        arr = self.__array__()
        tbl += [[sid[i]] + r for (i, r) in enumerate(arr.tolist())]
        return bytes(tabulate(tbl, tablefmt='plain'))

    def __array__(self, *_, **kwargs):
        kwargs = dict(kwargs)

        if 'sample_ids' not in kwargs:
            kwargs['sample_ids'] = self._sample_ids
            kwargs['marker_ids'] = self._marker_ids

        sample_idx = self._sample_map[kwargs['sample_ids']]
        marker_idx = self._marker_map[kwargs['marker_ids']]

        return self._array(sample_idx, marker_idx)

    def _copy_to(self, sample_ids, marker_ids, to_sidx, to_midx, G):
        from_sidx = self._sample_map[sample_ids]
        from_midx = self._marker_map[marker_ids]
        copyto_nans(from_sidx, from_midx, self._arr, to_sidx, to_midx, G)

    def _update_alleles_map(self):
        self._allelesA_map = ndict(zip(self.marker_ids, self.allelesA))
        self._allelesB_map = ndict(zip(self.marker_ids, self.allelesB))

    @property
    def sample_ids(self):
        return self._sample_ids

    @property
    def marker_ids(self):
        return self._marker_ids

    def merge(self, that):
        from .mmatrix import MMatrix
        return MMatrix(self, that)

    @property
    def allelesA(self):
        return self._allelesA

    @property
    def allelesB(self):
        return self._allelesB

    @allelesA.setter
    def allelesA(self, v):
        self._allelesA = v
        self._update_alleles_map()

    @allelesB.setter
    def allelesB(self, v):
        self._allelesB = v
        self._update_alleles_map()

    def alleleA(self, marker_id):
        return self._allelesA_map[marker_id]

    def alleleB(self, marker_id):
        return self._allelesB_map[marker_id]

    def hasmarker(self, marker_id):
        return marker_id in self._marker_map
