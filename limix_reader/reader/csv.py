from __future__ import absolute_import

from pandas import read_csv

from numpy import asarray

from ..table import Table
from ..table import Column
from ..matrix import NPyMatrix

def reader(filepath, dtype=float, row_header=False, col_header=False,
           genotype=False, na_values=None):

    if genotype:
        return _reader_matrix(filepath, dtype, row_header, col_header,
                              na_values)
    else:
        return _reader_table(filepath, dtype, row_header, col_header, na_values)

def _reader_table(filepath, dtype, row_header, col_header, na_values):
    header = 0 if col_header else None
    index_col = 0 if row_header else None

    data = read_csv(filepath, header=header, index_col=index_col,
                    na_values=na_values)
    data = data.astype(dtype)

    table = Table()
    for (i, cn) in enumerate(data):
        if not col_header or data[cn].name is None:
            data[cn].name = 'column_name_%d' % i
        c = Column(data[cn].name, data.index.values, data[cn].values)
        table.add(c)

    if data.index.name is None:
        table.index_name = 'index_name'
    else:
        table.index_name = data.index.name

    return table

def _reader_matrix(filepath, dtype, row_header, col_header, na_values):
    header = 0 if col_header else None
    index_col = 0 if row_header else None

    data = read_csv(filepath, header=header, index_col=index_col,
                    na_values=na_values)
    data = data.astype(dtype)
    return NPyMatrix(asarray(data))
