from numpy import intersect1d

from pandas import DataFrame

from .column import Column
from ..util import isscalar

class Table(object):
    def __init__(self, df=None):
        super(Table, self).__init__()
        self._df = DataFrame() if df is None else df

    def add(self, c):
        for (i, v) in iter(c.items()):
            self._df.set_value(i, c.name, v)

    @property
    def index_name(self):
        return self._df.index.name

    @index_name.setter
    def index_name(self, v):
        self._df.index.name = v

    @property
    def index_values(self):
        return self._df.index.values

    @index_values.setter
    def index_values(self, values):
        name = self._df.index.name
        self._df.index = values
        self._df.index.name = name

    @property
    def columns(self):
        return self._df.columns.values

    def __getitem__(self, colname):
        if isscalar(colname):
            return Column(colname, self.index_values, self._df[colname].values)
        return Table(self._df[colname])

    def __setitem__(self, colname, value):
        raise NotImplementedError

    def loc(self, index_values):
        pass
        # index_values = make_sure_list(index_values)
        # return TableView(self, index_values)

    @property
    def shape(self):
        return self._df.shape

    @property
    def ndim(self):
        return 2

    @property
    def dtypes(self):
        return self._df.dtypes

    def __array__(self):
        return self._df.__array__()

    def __repr__(self):
        return repr(self._df)

    def __str__(self):
        return bytes(self._df)

    def merge(self, that):
        indcol = "__indicator_column__"
        df = self._df.merge(that._df, how='outer', left_index=True,
                            right_index=True, indicator=indcol)
        cols = intersect1d(self._df.columns, that._df.columns)
        for c in cols:
            cl = c + '_x'
            cr = c + '_y'
            for i in df.index:
                if df[indcol][i] == 'right_only':
                    df.loc[i, cl] = df.loc[i, cr]

        for c in cols:
            del df[c + '_y']
        df.rename(columns={(c+'_x'):c for c in cols}, inplace=True)
        del df[indcol]

        return Table(df)
