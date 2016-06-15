from os.path import dirname
from os.path import join
from os.path import realpath

from numpy import array
# from numpy import asarray
from numpy import nan
from numpy.testing import assert_equal
from numpy.testing import assert_array_equal
# from numpy.testing import assert_string_equal

def test_read():
    from ..bed import reader

    root = dirname(realpath(__file__))
    root = join(root, 'data')

    (stable, mtable, G) = reader(join(root, 'plink', 'test'))
    R = array([[ 0.,  2.,  2.],
               [  2.,  nan,   1.],
               [ nan,   1.,   1.],
               [  2.,   2.,  nan],
               [  2.,   2.,  nan],
               [ 2.,  2.,  0.]])

    assert_equal(G.item('1_1', '1_snp1'), R[0,0])
    assert_equal(G.item('1_1', '1_snp2'), R[0,1])
    assert_equal(G.item('1_1', '1_snp3'), R[0,2])

    assert_equal(G.item('1_2', '1_snp1'), R[1,0])
    assert_equal(G.item('1_2', '1_snp2'), R[1,1])
    assert_equal(G.item('1_2', '1_snp3'), R[1,2])

    assert_equal(G.item('1_3', '1_snp1'), R[2,0])
    assert_equal(G.item('1_3', '1_snp2'), R[2,1])
    assert_equal(G.item('1_3', '1_snp3'), R[2,2])

    assert_equal(G.item('2_1', '1_snp1'), R[3,0])
    assert_equal(G.item('2_1', '1_snp2'), R[3,1])
    assert_equal(G.item('2_1', '1_snp3'), R[3,2])

    assert_equal(G.item('2_2', '1_snp1'), R[4,0])
    assert_equal(G.item('2_2', '1_snp2'), R[4,1])
    assert_equal(G.item('2_2', '1_snp3'), R[4,2])

    assert_equal(G.item('2_3', '1_snp1'), R[5,0])
    assert_equal(G.item('2_3', '1_snp2'), R[5,1])
    assert_equal(G.item('2_3', '1_snp3'), R[5,2])

    assert_array_equal(G.shape, (6, 3))

    assert_array_equal(G['1_1', '1_snp1'], R[0,0])
    assert_array_equal(G['1_1', '1_snp2'], R[0,1])
    assert_array_equal(G['1_1', '1_snp3'], R[0,2])

    assert_array_equal(G['1_2', '1_snp1'], R[1,0])
    assert_array_equal(G['1_2', '1_snp2'], R[1,1])
    assert_array_equal(G['1_2', '1_snp3'], R[1,2])

    assert_array_equal(G['1_3', '1_snp1'], R[2,0])
    assert_array_equal(G['1_3', '1_snp2'], R[2,1])
    assert_array_equal(G['1_3', '1_snp3'], R[2,2])

    assert_array_equal(G['2_1', '1_snp1'], R[3,0])
    assert_array_equal(G['2_1', '1_snp2'], R[3,1])
    assert_array_equal(G['2_1', '1_snp3'], R[3,2])

    assert_array_equal(G['2_2', '1_snp1'], R[4,0])
    assert_array_equal(G['2_2', '1_snp2'], R[4,1])
    assert_array_equal(G['2_2', '1_snp3'], R[4,2])

    assert_array_equal(G['2_3', '1_snp1'], R[5,0])
    assert_array_equal(G['2_3', '1_snp2'], R[5,1])
    assert_array_equal(G['2_3', '1_snp3'], R[5,2])

    # g = G['1_1', ['1_snp1', '1_snp2', '1_snp3']]
    # print(g)
    # assert_array_equal(G[0,:], array([ 0.,  2.,  2.]))
#     assert_array_equal(G[1,:], array([  2.,  nan,   1.]))
#     assert_array_equal(G[2,:], array([ nan,   1.,   1.]))
#     assert_array_equal(G[3,:], array([  2.,   2.,  nan]))
#     assert_array_equal(G[4,:], array([  2.,   2.,  nan]))
#     assert_array_equal(G[5,:], array([ 2.,  2.,  0.]))
#
#     assert_array_equal(G[:,0], array([  0.,   2.,  nan,   2.,   2.,   2.]))
#     assert_array_equal(G[:,1], array([  2.,  nan,   1.,   2.,   2.,   2.]))
#     assert_array_equal(G[:,2], array([  2.,   1.,   1.,  nan,  nan,   0.]))
#
#     assert_string_equal(stable['family_id']['1_1'], '1')
#     assert_string_equal(stable['family_id']['2_1'], '2')
#     assert_string_equal(stable['family_id']['1_2'], '1')
#
#     assert_string_equal(stable['individual_id']['1_2'], '2')
#     assert_string_equal(stable['individual_id']['2_1'], '1')
#
#     assert_equal(mtable['base_pair_position']['1_snp1'], 1.0)
#     assert_equal(mtable['base_pair_position']['1_snp2'], 2.0)
#     assert_equal(mtable['base_pair_position']['1_snp3'], 3.0)
#
#     R = array([[ 0.,  2.,  2.],
#                [  2.,  nan,   1.],
#                [ nan,   1.,   1.],
#                [  2.,   2.,  nan],
#                [  2.,   2.,  nan],
#                [ 2.,  2.,  0.]])
#     assert_array_equal(asarray(G), R)
