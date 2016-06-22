from numpy import atleast_2d

from .interface import MatrixInterface

class NPyMatrix(MatrixInterface):
    def __init__(self, arr, sample_ids=None, marker_ids=None,
                 allelesA=None, allelesB=None):

        self._arr = atleast_2d(arr)
        super(NPyMatrix, self).__init__(sample_ids, marker_ids,
                                        allelesA, allelesB, self._arr.shape)

    def _item(self, sample_id, marker_id):
        return self._arr.item(self._sample_map[sample_id],
                              self._marker_map[marker_id])

    @property
    def shape(self):
        return self._arr.shape

    @property
    def dtype(self):
        return self._arr.dtype

    def _array(self, sample_ids, marker_ids):
        sample_idx = self._sample_map[sample_ids]
        marker_idx = self._marker_map[marker_ids]
        return atleast_2d(self._arr[sample_idx,:][:,marker_idx])
