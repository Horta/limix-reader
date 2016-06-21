import h5py as h5

from numpy import asarray
from numpy import arange
from numpy import atleast_2d

from ..table import Table
from ..table import Column
# from ..util.type import npy2py_type

from ..matrix import H5Matrix

# def _reader_matrix(filepath, itempath):
#     with h5.File(filepath, 'r') as f:
#         arr = asarray(f[itempath])
#         arr = atleast_2d(arr)

def reader(filepath, itempath, genotype=False):

    if genotype:
        return H5Matrix(filepath, itempath)
    # else:
    #     return _reader_table(filepath, row_header, col_header, na_values)

    with h5.File(filepath, 'r') as f:

        # if dtype is None:
            # dtype = npy2py_type(f[itempath].dtype)

        arr = asarray(f[itempath])
        arr = atleast_2d(arr)

    index = arange(arr.shape[0], dtype=int)

    table = Table()
    for i in range(arr.shape[1]):
        column_name = 'column_name_%d' % i
        c = Column(column_name, index, arr[:,i])
        table.add(c)

    table.index_name = 'index_name'
    return table
