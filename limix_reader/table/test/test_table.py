from numpy import nan
from numpy import array
from numpy import asarray

from numpy.testing import assert_array_equal
from numpy.testing import assert_equal
from numpy.testing import assert_raises

from limix_reader.table import Table
from limix_reader.table import Column

def test_adding_columns():
    t = Table()

    labels =['sample01', 'sample02', 'sample03']
    values = [34.3, 2.3, 103.4]
    c = Column('height', labels, values)
    t.add(c)

    labels =['sample02', 'sample03']
    values = ['doce', 'cogumelo']
    c = Column('comida', labels, values)
    t.add(c)

    t.index_name = 'sample_id'

    a = array([[34.3, nan], [2.3, 'doce'],
               [103.4, 'cogumelo']], dtype=bytes)
    assert_array_equal(asarray(t).astype(bytes), a)

def test_column_indexing():

    t = Table()

    labels =['sample01', 'sample02', 'sample03']
    values = [34.3, 2.3, 103.4]
    c = Column('height', labels, values)
    t.add(c)

    labels =['sample02', 'sample03']
    values = ['doce', 'cogumelo']
    c = Column('comida', labels, values)
    t.add(c)

    t.index_name = 'sample_id'

    c = t['comida']

    assert_equal(c['sample03'], array(['cogumelo']))
    with assert_raises(KeyError):
        print(c['sample05'])

def test_change_index():
    t = Table()

    labels =['sample01', 'sample02', 'sample03']
    values = [34.3, 2.3, 103.4]
    c = Column('height', labels, values)
    t.add(c)

    labels =['sample02', 'sample03']
    values = ['doce', 'cogumelo']
    c = Column('comida', labels, values)
    t.add(c)
    t.index_name = 'sample_id'
    t.index_values = [1, 2, 3]
    t.index_name = 'hola'

# def test_merge_tables():
#     t1 = Table()
#
#     labels =['sample01', 'sample02', 'sample03']
#     values = [34.3, 2.3, 103.4]
#     c = Column('height', labels, values)
#     t1.add(c)
#
#     labels =['sample02', 'sample03']
#     values = ['doce', 'cogumelo']
#     c = Column('comida', labels, values)
#     t1.add(c)
#     t1.index_name = 'sample_id'
#
#     t2 = Table()
#
#     labels =['sample01', 'sample09', 'sample02', 'sample03']
#     values = [34.3, -23, 2.3, 103.4]
#     c = Column('height', labels, values)
#     t2.add(c)
#
#     t12 = t1.merge(t2)
#
#     assert_equal(t12['height']['sample01'], 34.3)
#     assert_equal(t12['height']['sample02'], 2.3)
#     assert_equal(t12['height']['sample03'], 103.4)
#     assert_equal(t12['height']['sample09'], -23.0)
#
#     assert_equal(bytes(t12['comida']['sample01']), 'nan')
#     assert_equal(t12['comida']['sample02'], 'doce')
#     assert_equal(t12['comida']['sample03'], 'cogumelo')
#     assert_equal(bytes(t12['comida']['sample09']), 'nan')
