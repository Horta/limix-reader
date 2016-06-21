from numpy import intersect1d
from numpy import union1d
from numpy import arange
from numpy import isnan
from numpy import full
from numpy import nan

from .interface import MatrixInterface
from ..util import ndict

def _check_alleles_conherence(lhs, rhs):
    imids = intersect1d(lhs.marker_ids, rhs.marker_ids)

    lhs_iaA = lhs.allelesA[lhs._marker_map[imids]]
    lhs_iaB = lhs.allelesB[lhs._marker_map[imids]]

    rhs_iaA = rhs.allelesA[rhs._marker_map[imids]]
    rhs_iaB = rhs.allelesB[rhs._marker_map[imids]]

    lhs_set = [set([lhs_iaA[i], lhs_iaB[i]])
                  for i in range(len(imids))]

    rhs_set = [set([rhs_iaA[i], rhs_iaB[i]])
                  for i in range(len(imids))]

    matches = [len(lhs_set[i].intersection(rhs_set[i]))
                   for i in range(len(imids))]

    if sum(matches) != 2 * len(matches):
        msg = "There are conflicting allele names between the merging"
        msg += " genotypes."
        raise ValueError(msg)

class MMatrix(MatrixInterface):
    def __init__(self, lhs, rhs):
        _check_alleles_conherence(lhs, rhs)

        sample_ids = union1d(lhs.sample_ids, rhs.sample_ids)
        marker_ids = union1d(lhs.marker_ids, rhs.marker_ids)

        shape = (len(sample_ids), len(marker_ids))

        alA = []
        alB = []
        for m in marker_ids:
            alA.append(lhs.alleleA(m) if lhs.hasmarker(m) else rhs.alleleA(m))
            alB.append(lhs.alleleB(m) if lhs.hasmarker(m) else rhs.alleleB(m))

        super(MMatrix, self).__init__(sample_ids, marker_ids,
                                      alA, alB, shape)
        self._lhs = lhs
        self._rhs = rhs

        imids = intersect1d(lhs.marker_ids, rhs.marker_ids)
        self._imarker_ids = imids

        mapA = lhs.allelesA[lhs._marker_map[imids]]
        mapB = lhs.allelesB[lhs._marker_map[imids]]

        self._iallelesA_map = ndict(zip(imids, mapA))
        self._iallelesB_map = ndict(zip(imids, mapB))

        n = len(self._sample_ids)
        p = len(self._marker_ids)

        self._sample_map = ndict(zip(self._sample_ids, arange(n, dtype=int)))
        self._marker_map = ndict(zip(self._marker_ids, arange(p, dtype=int)))

    def _item(self, sample_id, marker_id):

        alleleB = self.alleleB(marker_id)
        # if alleleB is None and marker_id in self._iallelesB_map:
            # alleleB = self._iallelesB_map[marker_id]

        try:
            v0 = self._lhs.item(sample_id, marker_id, alleleB)
        except IndexError:
            v0 = nan

        try:
            v1 = self._rhs.item(sample_id, marker_id, alleleB)
        except IndexError:
            v1 = nan

        if not isnan(v0) and not isnan(v1):
            if v0 != v1:
                msg = ("There are conflicting genotype values from" +
                       " different sources.")
                raise ValueError(msg)

        return v0 if isnan(v1) else v1

    @property
    def shape(self):
        return (len(self.sample_ids), len(self.marker_ids))

    @property
    def ndim(self):
        return 2

    @property
    def dtype(self):
        raise NotImplementedError

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
