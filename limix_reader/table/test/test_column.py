from ..column import Column

from numpy import asarray
from numpy.testing import assert_array_equal
from numpy.testing import assert_raises

def test_creation():
    indices = ['sample01', 'sample02', 'sample03']
    values = [34.3, 2.3, 103.4]
    v1 = Column('height', indices, values)

    assert_array_equal(v1['sample03'], [103.4])
    assert_array_equal(v1['sample01', 'sample03'], [34.3, 103.4])
    assert_array_equal(v1[asarray(['sample01', 'sample03'])], [34.3, 103.4])

    v2 = Column('height', indices, values)
    assert_array_equal(v1 == v2, ['sample01', 'sample02', 'sample03'])

    v3 = Column('height', ['sample02', 'sample03', 'sample04'], [2.3, 3.4, 34.3])

    assert_array_equal(v1 == v3, ['sample02'])

    v12 = v1.merge(v2)
    assert_array_equal(v12 == v1, ['sample01', 'sample02', 'sample03'])

    with assert_raises(ValueError):
        v1.merge(v3)
