from os.path import dirname
from os.path import join
from os.path import realpath

from numpy import atleast_2d
from numpy import asarray
from numpy import isnan
from numpy.testing import assert_equal
from numpy.testing import assert_array_equal
from numpy.testing import assert_raises

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

    G3 = read_csv(join(root, 'genotype_named2.csv'), header=0, index_col=0,
                  na_values='?')
    G3 = NPyMatrix(asarray(G3), G3.index.values, G3.columns)

    G23 = G2.merge(G3)
    assert_equal(G23.item("sample1", "marker1"), 0)
    assert_equal(isnan(G23.item("sample6", "marker4")), True)
    assert_equal(isnan(G23.item("sample5", "marker7")), True)
    assert_equal(G23.item("sample5", "marker8"), 1)

    with assert_raises(ValueError):
        G23.item("sample4", "marker3")

    g = G23[["sample1", "sample3"], ["marker2", "marker8"]]
    assert_equal(g.item("sample1", "marker2"), 1)
    assert_equal(g.item("sample1", "marker8"), 0)
    assert_equal(isnan(g.item("sample3", "marker2")), True)
    assert_equal(g.item("sample3", "marker8"), 0)

def test_missing_completion():
    root = dirname(realpath(__file__))
    root = join(root, 'data')

    G1 = read_csv(join(root, 'genotype_2x2_lhs.csv'), header=0, index_col=0,
                  na_values='?')
    G2 = read_csv(join(root, 'genotype_2x2_rhs.csv'), header=0, index_col=0,
                  na_values='?')

    G1 = NPyMatrix(G1)
    G2 = NPyMatrix(G2)

    G12 = G1.merge(G2)
    assert_equal(G12, asarray([[2, 2], [2, 2]]))
