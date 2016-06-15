from pandas import read_csv

from bidict import bidict

from numpy import arange
from numpy import empty

from .plink import read_bed_item
# from .plink.bed import entirely as bed_entirely
from .plink import read_bed_intidx

from .plink import read_map

from ..matrix import MatrixInterface
from ..matrix import normalize_getitem_args
from ..matrix import MatrixView
from ..table import Table

def _read_fam(filepath):
    column_names = ['family_id', 'individual_id', 'paternal_id', 'maternal_id',
                    'sex', 'phenotype']
    column_types = [bytes, bytes, bytes, bytes, bytes, float]


    df = read_csv(filepath, header=None, sep=r'\s+', names=column_names,
                  dtype=dict(zip(column_names, column_types)))
    table = Table(df)

    fid = table['family_id']
    iid = table['individual_id']
    n = table.shape[0]
    table.index_values = [fid[i] + '_' + iid[i] for i in range(n)]
    table.index_name = 'sample_id'

    return table

class BedPath(MatrixInterface):
    def __init__(self, filepath, sample_ids, marker_ids):
        super(BedPath, self).__init__()
        self._filepath = filepath
        self._sample_ids = sample_ids
        self._marker_ids = marker_ids

        n = len(self._sample_ids)
        p = len(self._marker_ids)

        self._sample_map = bidict(zip(self._sample_ids, arange(n, dtype=int)))
        self._marker_map = bidict(zip(self._marker_ids, arange(p, dtype=int)))

    def item(self, sample_id, marker_id):
        r = self._sample_map[sample_id]
        c = self._marker_map[marker_id]
        return read_bed_item(self._filepath, r, c, self.shape)

    def __getitem__(self, args):
        sample_ids, marker_ids = normalize_getitem_args(args)
        return MatrixView(self, sample_ids, marker_ids)

    @property
    def shape(self):
        return (len(self._sample_ids), len(self._marker_ids))

    @property
    def dtype(self):
        return int

    def __repr__(self):
        return repr(self.__array__())

    def __str__(self):
        return bytes(self.__array__())

    def __array__(self, *args, **kwargs):
        kwargs = dict(kwargs)

        if 'sample_ids' not in kwargs:
            kwargs['sample_ids'] = self._sample_ids
            kwargs['marker_ids'] = self._marker_ids

        sample_idx = [self._sample_map[si] for si in kwargs['sample_ids']]
        marker_idx = [self._marker_map[mi] for mi in kwargs['marker_ids']]

        G = empty((len(sample_idx), len(marker_idx)))
        read_bed_intidx(self._filepath, sample_idx, marker_idx, self.shape, G)

        return G

    @property
    def sample_ids(self):
        return self._sample_ids

    @property
    def marker_ids(self):
        return self._marker_ids

def reader(basepath):
    sample_tbl = _read_fam(basepath + '.fam')
    marker_tbl = read_map(basepath + '.map')
    G = BedPath(basepath + '.bed', sample_tbl.index_values,
                marker_tbl.index_values)
    return (sample_tbl, marker_tbl, G)
