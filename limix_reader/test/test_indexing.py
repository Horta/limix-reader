from os.path import dirname
from os.path import join
from os.path import realpath

from numpy import nan
from numpy.testing import assert_equal
from numpy.testing import assert_raises

import limix_reader as limr

def test_read():

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

    # sample_ids1 = table1["column_name_0"] > 0
    # sample_ids2 = table2["column_name_0"] != table1["column_name_2"]

    print("-----------------------")

    # print(G1.sample_ids, G1.marker_ids)
    # print(G2.sample_ids, G2.marker_ids)
    # print(sample_ids1)

    G12 = G1.merge(G2)
    G123 = G12.merge(G3)
    # print(G12.sample_ids)
    # print(G12.marker_ids)

    assert_equal(G123.item(0, 0), 0)
    assert_equal(G123.item(0, 1), 1)
    assert_equal(G123.item(0, 5), 0)
    assert_equal(G123.item(0, 6), 1)
    assert_equal(G123.item(0, 7), 0)
    assert_equal(G123.item(1, 2), nan)

    with assert_raises(ValueError):
        G123.item(2, 3)
