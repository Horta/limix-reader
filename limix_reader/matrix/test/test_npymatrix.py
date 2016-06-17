from os.path import dirname
from os.path import join
from os.path import realpath

from numpy import atleast_2d
from numpy import asarray
from numpy.testing import assert_array_equal

from pandas import read_csv

from ..npymatrix import NPyMatrix

def test_npymatrix():
    root = dirname(realpath(__file__))
    root = join(root, 'data')

    G1 = asarray(read_csv(join(root, 'genotype.csv'), header=None,
                          index_col=None, dtype=float, na_values='?'))

    G1 = NPyMatrix(G1)

    G2 = read_csv(join(root, 'genotype_named.csv'), header=0, index_col=0,
                  na_values='?')
    G2 = NPyMatrix(asarray(G2), G2.index.values, G2.columns)

    assert_array_equal(G2['sample4'], atleast_2d([1,0,1,0,1,1,1,0]))
    assert_array_equal(G2['sample4', 'marker3'], atleast_2d([1]))
    assert_array_equal(G2[['sample4', 'sample1'], 'marker3'],
                       atleast_2d([1,1]).T)
    assert_array_equal(G2[['sample4', 'sample1'], ['marker3', 'marker5']],
                       asarray([[1, 1], [1, 0]]))
    assert_array_equal(G2['sample4', ['marker3', 'marker5']], [[1, 1]])
