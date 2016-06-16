from os.path import dirname
from os.path import join
from os.path import realpath

from numpy import array
from numpy import asarray
from numpy import vstack
from numpy.testing import assert_array_equal

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

    sample_ids1 = table1["column_name_0"] > 0
    sample_ids2 = table2["column_name_0"] != table1["column_name_2"]

    print("-----------------------")

    print(G1.sample_ids, G1.marker_ids)
    print(G2.sample_ids, G2.marker_ids)
    print(sample_ids1)

    # g = G1[sample_ids1, [0, 1, 2, 3]]
    # g.__array__()

    #
    # assert_array_equal(asarray(table["column_name_0"]), R[:,0])
    # assert_array_equal(asarray(table["column_name_1"]), R[:,1])
    # assert_array_equal(asarray(table["column_name_2"]), R[:,2])
    # assert_array_equal(asarray(table["column_name_3"]), R[:,3])
    # assert_array_equal(asarray(table["column_name_4"]), R[:,4])
    #
    # sample_ids = table["column_name_0"] == 0
    # assert_array_equal(table["column_name_0"][sample_ids], [0, 0])
    #
    # sample_ids = table["column_name_0"] != 0
    # assert_array_equal(table["column_name_0"][sample_ids], [1, 2])
    #
    # sample_ids = table["column_name_0"] >= 0
    # assert_array_equal(table["column_name_0"][sample_ids], [0, 0, 1, 2])
    #
    # sample_ids = table["column_name_0"]  > 0
    # assert_array_equal(table["column_name_0"][sample_ids], [1, 2])
    #
    # sample_ids = table["column_name_0"] == table["column_name_4"]
    # assert_array_equal(sample_ids, [0, 1, 2])
    #
    # sample_ids = table["column_name_0"] >= table["column_name_1"]
    # assert_array_equal(sample_ids, [2, 3])
    # assert_array_equal(table["column_name_0"][sample_ids], [1, 2])
    #
    # sample_ids = table["column_name_0"] > table["column_name_1"]
    # assert_array_equal(sample_ids, [2])
    # assert_array_equal(table["column_name_0"][sample_ids], [1])
    #
    # assert_array_equal(table.loc([0, 3]), vstack([R[0,:], R[3,:]]))
