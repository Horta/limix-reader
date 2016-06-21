from .interface import MatrixInterface

class MatrixView(MatrixInterface):
    def __init__(self, ref, sample_ids, marker_ids):
        alA = [ref.alleleA(m) for m in marker_ids]
        alB = [ref.alleleB(m) for m in marker_ids]
        shape = (len(sample_ids), len(marker_ids))

        super(MatrixView, self).__init__(sample_ids, marker_ids,
                                         alA, alB, shape)
        self._ref = ref

    def _item(self, sample_id, marker_id):
        return self._ref.item(sample_id, marker_id)

    @property
    def shape(self):
        return (len(self._sample_ids), len(self._marker_ids))

    @property
    def ndim(self):
        return 2

    @property
    def dtype(self):
        return self._ref.dtype

    def _array(self, sample_idx, marker_idx):
        return self._ref._array(sample_idx, marker_idx)
