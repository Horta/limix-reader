from .interface import MatrixInterface

class MatrixView(MatrixInterface):
    def __init__(self, ref, sample_ids, marker_ids):
        super(MatrixView, self).__init__()
        self._ref = ref
        self._sample_ids = sample_ids
        self._marker_ids = marker_ids
        self._sample_set = set(list(sample_ids))
        self._marker_set = set(list(marker_ids))

    def item(self, sample_id, marker_id):
        if sample_id in self._sample_set and marker_id in self._marker_set:
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

        return self._ref.__array__(*args, **kwargs)

    @property
    def sample_ids(self):
        return self._sample_ids([])

    @property
    def marker_ids(self):
        return self._marker_ids([])
