from os.path import dirname
from os.path import join
from os.path import realpath

from numpy import nan
from numpy.testing import assert_equal
from numpy.testing import assert_raises

import limix_reader as limr

def test_numeric_ids():

    root = dirname(realpath(__file__))
    root = join(root, 'data')

    table1 = limr.reader.csv(join(root, '2d_array.csv'))
    table1.index_name = "sample_ids"

    table2 = limr.reader.csv(join(root, '2d_array_bigger.csv'))
    table2.index_name = "sample_ids"

    G1 = limr.reader.csv(join(root, 'genotype.csv'), genotype=True,
                         na_values='?')
    G2 = limr.reader.csv(join(root, 'genotype_bigger.csv'), genotype=True,
                         na_values='?')
    G3 = limr.reader.csv(join(root, 'genotype_bigger2.csv'), genotype=True,
                         na_values='?')

    G12 = G1.merge(G2)
    G123 = G12.merge(G3)

    assert_equal(G123.item(0, 0), 0)
    assert_equal(G123.item(0, 1), 1)
    assert_equal(G123.item(0, 5), 0)
    assert_equal(G123.item(0, 6), 1)
    assert_equal(G123.item(0, 7), 0)
    assert_equal(G123.item(1, 2), nan)

    with assert_raises(ValueError):
        G123.item(2, 3)

    G = G123[[0, 1], [0, 2, 3, 4, 5]]
    assert_equal(G.item(0, 0), 0)

    assert_equal(G.item(1, 5), 1)
    with assert_raises(IndexError):
        G.item(0, 1)

    sample_ids = table1['column_name_0'] >= table1['column_name_1']
    print(sample_ids)

    mtable1 = limr.reader.csv(join(root, '2d_array_bytes.csv'), row_header=True,
                              col_header=True)
    print(mtable1)
    print(mtable1['color'] == 'red')
    print(mtable1['temperature'] > 0)

    mtable2 = limr.reader.csv(join(root, '2d_array_bytes_2.csv'), row_header=True,
                              col_header=True)

    print(mtable2)
# def test_string_ids():
#
#     root = dirname(realpath(__file__))
#     root = join(root, 'data')
#
#     table1 = limr.reader.csv(join(root, '2d_array.csv'))
#     table1.index_name = "sample_ids"
#
#     table2 = limr.reader.csv(join(root, '2d_array_bigger.csv'))
#     table2.index_name = "sample_ids"
#
#     G1 = limr.reader.csv(join(root, 'genotype.csv'), genotype=True,
#                          na_values='?')
#     G2 = limr.reader.csv(join(root, 'genotype_bigger.csv'), genotype=True,
#                          na_values='?')
#     G3 = limr.reader.csv(join(root, 'genotype_bigger2.csv'), genotype=True,
#                          na_values='?')
#
#     G12 = G1.merge(G2)
#     G123 = G12.merge(G3)
#
#     assert_equal(G123.item(0, 0), 0)
#     assert_equal(G123.item(0, 1), 1)
#     assert_equal(G123.item(0, 5), 0)
#     assert_equal(G123.item(0, 6), 1)
#     assert_equal(G123.item(0, 7), 0)
#     assert_equal(G123.item(1, 2), nan)
#
#     with assert_raises(ValueError):
#         G123.item(2, 3)
#
#     G = G123[[0, 1], [0, 2, 3, 4, 5]]
#     assert_equal(G.item(0, 0), 0)
#
#     assert_equal(G.item(1, 5), 1)
#     with assert_raises(IndexError):
#         G.item(0, 1)
