from numpy import intersect1d
from numpy import union1d
from numpy import isnan
from numpy import full
from numpy import nan

from .interface import MatrixInterface

def _check_alleles_conherence(lhs, rhs):
    imids = intersect1d(lhs.marker_ids, rhs.marker_ids)

    lhs_iaA = [lhs.alleleA(m) for m in imids]
    lhs_iaB = [lhs.alleleB(m) for m in imids]

    rhs_iaA = [rhs.alleleA(m) for m in imids]
    rhs_iaB = [rhs.alleleB(m) for m in imids]

    lhs_set = [set(t) for t in zip(lhs_iaA, lhs_iaB)]
    rhs_set = [set(t) for t in zip(rhs_iaA, rhs_iaB)]

    matches = [len(t[0].intersection(t[1])) for t in zip(lhs_set, rhs_set)]

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

        # imids = intersect1d(lhs.marker_ids, rhs.marker_ids)
        # self._imarker_ids = imids
        #
        # mapA = lhs.allelesA[lhs._marker_map[imids]]
        # mapB = lhs.allelesB[lhs._marker_map[imids]]
        #
        # self._iallelesA_map = ndict(zip(imids, mapA))
        # self._iallelesB_map = ndict(zip(imids, mapB))
        #
        # n = len(self._sample_ids)
        # p = len(self._marker_ids)
        #
        # self._sample_map = ndict(zip(self._sample_ids, arange(n, dtype=int)))
        # self._marker_map = ndict(zip(self._marker_ids, arange(p, dtype=int)))

    def _item(self, sample_id, marker_id):
        alleleB = self.alleleB(marker_id)

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

    def _copy_from_ref(self, sample_ids, marker_ids, ref, G):
        sample_ids = intersect1d(ref.sample_ids, sample_ids)
        marker_ids = intersect1d(ref.marker_ids, marker_ids)
        sidx = self._sample_map[sample_ids]
        midx = self._marker_map[marker_ids]
        ref._copy_to(sample_ids, marker_ids, sidx, midx, G)

    def _array(self, sample_idx, marker_idx):
        n = len(sample_idx)
        p = len(marker_idx)
        G = full((n, p), nan)

        sample_ids = self.sample_ids[sample_idx]
        marker_ids = self.marker_ids[marker_idx]

        self._copy_from_ref(sample_ids, marker_ids, self._lhs, G)
        self._copy_from_ref(sample_ids, marker_ids, self._rhs, G)

        return G
