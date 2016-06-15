from os.path import dirname
from os.path import join
from os.path import realpath

from numpy import array
from numpy import asarray
from numpy.testing import assert_array_equal

def test_read():
    from ..csv import reader

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
