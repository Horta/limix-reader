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

    assert_array_equal(asarray(table), array(R))
