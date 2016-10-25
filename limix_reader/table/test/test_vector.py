from limix_reader.table.vector import Vector

from numpy import asarray
from numpy.testing import assert_array_equal
from numpy.testing import assert_equal
from numpy.testing import assert_raises
from numpy.testing import assert_almost_equal

def test_creation():
    indices = ['sample01', 'sample02', 'sample03']
    values = [34.3, 2.3, 103.4]
    v1 = Vector(indices, values)

    assert_array_equal(v1['sample03'], [103.4])
    assert_array_equal(v1['sample01', 'sample03'], [34.3, 103.4])
    assert_array_equal(v1[asarray(['sample01', 'sample03'])], [34.3, 103.4])

    v2 = Vector(indices, values)
    assert_array_equal(v1 == v2, ['sample01', 'sample02', 'sample03'])

    v3 = Vector(['sample02', 'sample03', 'sample04'], [2.3, 3.4, 34.3])

    assert_array_equal(v1 == v3, ['sample02'])

    v12 = v1.merge(v2)
    assert_array_equal(v12 == v1, ['sample01', 'sample02', 'sample03'])

    with assert_raises(ValueError):
        v1.merge(v3)

    items = iter(v12.items())

    (i, v) = next(items)
    assert_equal(i, 'sample01')
    assert_almost_equal(v, 34.299999999999997)

    (i, v) = next(items)
    assert_equal(i, 'sample02')
    assert_almost_equal(v, 2.2999999999999998)

    (i, v) = next(items)
    assert_equal(i, 'sample03')
    assert_almost_equal(v, 103.40000000000001)
