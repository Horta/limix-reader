from numpy import atleast_2d

import h5py as h5

from .interface import MatrixInterface

class H5Matrix(MatrixInterface):
    def __init__(self, filepath, itempath, sample_ids=None, marker_ids=None,
                 allelesA=None, allelesB=None):

        self._filepath = filepath
        self._itempath = itempath

        super(H5Matrix, self).__init__(sample_ids, marker_ids,
                                        allelesA, allelesB, self.shape)

    def _item(self, sample_id, marker_id):
        with h5.File(self._filepath, 'r') as f:
            arr = f[self._itempath]
            return arr.item(self._sample_map[sample_id],
                            self._marker_map[marker_id])

    @property
    def shape(self):
        with h5.File(self._filepath, 'r') as f:
            return f[self._itempath].shape

    @property
    def dtype(self):
        with h5.File(self._filepath, 'r') as f:
            return f[self._itempath].dtype

    def _array(self, sample_ids, marker_ids):
        sample_idx = self._sample_map[sample_ids]
        marker_idx = self._marker_map[marker_ids]
        with h5.File(self._filepath, 'r') as f:
            arr = f[self._itempath]
            return atleast_2d(arr[sample_idx,:][:,marker_idx])
