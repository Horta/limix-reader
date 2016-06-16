from .view import MatrixInterface

from numpy import union1d
from numpy import isnan
from numpy import nan

class MMatrix(MatrixInterface):
    def __init__(self, lhs, rhs):
        super(MMatrix, self).__init__()
        self._lhs = lhs
        self._rhs = rhs
        self._sample_map = dict()
        self._marker_map = dict()

        for sid in lhs.sample_ids:
            if sid not in self._sample_map:
                self._sample_map[sid] = []
            self._sample_map[sid].append(0)

        for mid in lhs.marker_ids:
            if mid not in self._marker_map:
                self._marker_map[mid] = []
            self._marker_map[mid].append(0)

        for sid in rhs.sample_ids:
            if sid not in self._sample_map:
                self._sample_map[sid] = []
            self._sample_map[sid].append(0)

        for mid in rhs.marker_ids:
            if mid not in self._marker_map:
                self._marker_map[mid] = []
            self._marker_map[mid].append(0)

    def item(self, sample_id, marker_id):
        try:
            v0 = self._lhs.item(sample_id, marker_id)
        except IndexError:
            v0 = None

        try:
            v1 = self._rhs.item(sample_id, marker_id)
        except IndexError:
            v1 = None

        if v0 is None and v1 is None:
            raise IndexError

        if v0 is None:
            return v1 if not isnan(v1) else nan
        if v1 is None:
            return v0 if not isnan(v0) else nan

        if isnan(v0) and isnan(v1):
            return nan

        if isnan(v0):
            return v1

        if isnan(v1):
            return v0

        if v0 != v1:
            msg = ("There are conflicting genotype values from" +
                   " different sources.")
            raise ValueError(msg)

        return v0

    def __getitem__(self, args):
        raise NotImplementedError

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

    def __array__(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def sample_ids(self):
        return union1d(self._lhs.sample_ids, self._rhs.sample_ids)

    @property
    def marker_ids(self):
        return union1d(self._lhs.marker_ids, self._rhs.marker_ids)
