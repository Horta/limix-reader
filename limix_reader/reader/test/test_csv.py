from os.path import dirname
from os.path import join
from os.path import realpath

from numpy import array
from numpy import asarray
# from numpy import vstack
from numpy.testing import assert_array_equal
from numpy.testing import assert_equal

from ..csv import reader

def test_read():
    root = dirname(realpath(__file__))
    root = join(root, 'data')

    table = reader(join(root, '2d_array.csv'))

    R = [[ 0.,  1.,  2.,  1.,  0.],
         [ 0.,  1.,  2.,  1.,  0.],
         [ 1.,  0.,  1.,  1.,  1.],
         [ 2.,  2.,  0.,  1.,  0.]]

    R = array(R)
    assert_array_equal(asarray(table), array(R))

    assert_array_equal(asarray(table["column_name_0"]), R[:,0])
    assert_array_equal(asarray(table["column_name_1"]), R[:,1])
    assert_array_equal(asarray(table["column_name_2"]), R[:,2])
    assert_array_equal(asarray(table["column_name_3"]), R[:,3])
    assert_array_equal(asarray(table["column_name_4"]), R[:,4])

    sample_ids = table["column_name_0"] == 0
    assert_array_equal(table["column_name_0"][sample_ids], [0, 0])

    sample_ids = table["column_name_0"] != 0
    assert_array_equal(table["column_name_0"][sample_ids], [1, 2])

    sample_ids = table["column_name_0"] >= 0
    assert_array_equal(table["column_name_0"][sample_ids], [0, 0, 1, 2])

    sample_ids = table["column_name_0"]  > 0
    assert_array_equal(table["column_name_0"][sample_ids], [1, 2])

    sample_ids = table["column_name_0"] == table["column_name_4"]
    assert_array_equal(sample_ids, [0, 1, 2])

    sample_ids = table["column_name_0"] >= table["column_name_1"]
    assert_array_equal(sample_ids, [2, 3])
    assert_array_equal(table["column_name_0"][sample_ids], [1, 2])

    sample_ids = table["column_name_0"] > table["column_name_1"]
    assert_array_equal(sample_ids, [2])
    assert_array_equal(table["column_name_0"][sample_ids], [1])

    # assert_array_equal(table.loc([0, 3]), vstack([R[0,:], R[3,:]]))

def test_alleles():
    root = dirname(realpath(__file__))
    root = join(root, 'data')

    tbl1 = reader(join(root, '2d_array.csv'), genotype=True)

    tbl2 = reader(join(root, '2d_array_inv_alleles.csv'), genotype=True)

    alA = tbl2.allelesA
    alB = tbl2.allelesB

    tbl2.allelesA = alB
    tbl2.allelesB = alA

    tabl12 = tbl1.merge(tbl2)
    assert_equal(tabl12.item(0,0), 0)
    assert_equal(tabl12.item(4,0), 1)
    assert_equal(tabl12.item(4,4), 0)
