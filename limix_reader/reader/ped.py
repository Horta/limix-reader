from numpy import unique
from numpy import asarray
from numpy import concatenate
from numpy import nan
from numpy import empty

from pandas import read_csv

from .plink import read_map
from ..table import Table
from ..matrix import NPyMatrix

def _read_ped_genotype(M, allelesB):
    nsnps = M.shape[1] // 2
    nsamples = M.shape[0]
    allelesA_ = []
    allelesB_ = []

    G = empty((nsamples, nsnps))
    for i in range(nsnps):
        left  = M[:,i*2 + 0]
        right = M[:,i*2 + 1]

        v = concatenate([left, right])
        u = unique(v)
        a = list(set(u).difference('0'))
        if len(a) == 0 or len(a) > 2:
            raise ValueError

        if allelesB is None:
            if len(a) == 1:
                ref_allele = a[0]
                if 'A' == ref_allele:
                    null_allele = 'B'
                else:
                    null_allele = 'A'
            else:
                n0 = sum(v == a[0])
                n1 = len(v) - n0
                if n0 <= n1:
                    ref_allele = a[0]
                    null_allele = a[1]
                else:
                    ref_allele = a[1]
                    null_allele = a[0]
        else:
            ref_allele = allelesB[i]
            a = list(set(a).difference(ref_allele))
            if len(a) == 1:
                null_allele = a[0]
            else:
                if 'A' == ref_allele:
                    null_allele = 'B'
                else:
                    null_allele = 'A'

        G[:,i]  = left == ref_allele
        G[:,i] += right == ref_allele
        G[left == '0',i] = nan

        allelesA_.append(null_allele)
        allelesB_.append(ref_allele)

    return (G, asarray(allelesA_), asarray(allelesB_))

def _read_ped(filepath, allelesB):
    column_names = ['family_id', 'individual_id', 'paternal_id', 'maternal_id',
                    'sex', 'phenotype']
    column_types = [bytes, bytes, bytes, bytes, bytes, float]

    n = len(column_names)
    df = read_csv(filepath, header=None, sep=r'\s+', names=column_names,
                  usecols=range(n), dtype=dict(zip(column_names, column_types)))

    table = Table(df)
    n = table.shape[0]

    fid = table['family_id']
    iid = table['individual_id']
    table.index_values = [fid[i] + '_' + iid[i] for i in range(n)]
    table.index_name = 'sample_id'

    df = read_csv(filepath, header=None, sep=r'\s+')
    (G, allelesA, allelesB) = _read_ped_genotype(df.as_matrix().astype(bytes)
                                                 [:,6:], allelesB)

    return (table, G, allelesA, allelesB)

def reader(basepath, allelesB=None):
    marker_tbl = read_map(basepath + '.map')
    (sample_tbl, G, allelesA, allelesB) =\
        _read_ped(basepath + '.ped', allelesB)


    G = NPyMatrix(G, sample_ids=sample_tbl.index_values,
                     marker_ids=marker_tbl.index_values,
                     allelesA=allelesA,
                     allelesB=allelesB)

    marker_tbl['alleleA'] = allelesA
    marker_tbl['alleleB'] = allelesB

    return (sample_tbl, marker_tbl, G)
