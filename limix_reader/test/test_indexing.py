from os.path import dirname
from os.path import join
from os.path import realpath

from numpy import nan
from numpy import asarray
from numpy.testing import assert_equal
from numpy.testing import assert_raises
from numpy.testing import assert_array_equal

import limix_reader as limr

def test_ids():

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
    mtable1 = limr.reader.csv(join(root, '2d_array_bytes.csv'), row_header=True,
                              col_header=True)

    mtable2 = limr.reader.csv(join(root, '2d_array_bytes_2.csv'), row_header=True,
                              col_header=True)

    mtable = mtable1.merge(mtable2)
    assert_array_equal(mtable['status'], ['paused', 'paused', 'running',
                                          'paused', 'running', 'running'])
    assert_array_equal(mtable['temperature'], [ 10.,  -3., -13.,  33.])

def test_zebra():
    root = dirname(realpath(__file__))
    root = join(root, 'data')

    (bed_sample_tbl, bed_marker_tbl, bed_G) = limr.reader.bed(join(root,
                                                                   'zebra',
                                                                   'all'))

    (ped_sample_tbl, ped_marker_tbl, ped_G) = limr.reader.ped(join(root,
                                                                   'zebra',
                                                                   'all'))

    assert_array_equal(bed_sample_tbl, ped_sample_tbl)
    assert_equal(bed_sample_tbl.index_name, ped_sample_tbl.index_name)
    assert_array_equal(bed_sample_tbl.index_values,
                       ped_sample_tbl.index_values)

    assert_array_equal(bed_sample_tbl.columns, ped_sample_tbl.columns)

    bedG = asarray(bed_G)
    pedG = asarray(ped_G)
    import ipdb; ipdb.set_trace()
    bed_G.unphased_equal(ped_G)
    # assert_equal(bed_G, ped_G)
