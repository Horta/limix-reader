from numpy import union1d

class MTable(object):
    def __init__(self, lhs, rhs):
        self._lhs = lhs
        self._rhs = rhs

        if lhs.index_name != rhs.index_name:
            raise ValueError("Index names differ.")

    @property
    def index_name(self):
        return self._lhs.index_name

    @index_name.setter
    def index_name(self, v):
        self._lhs.index_name = v
        self._rhs.index_name = v

    @property
    def index_values(self):
        return union1d(self._lhs.index_values, self._rhs.index_values)

    @property
    def columns(self):
        return union1d(self._lhs.columns, self._rhs.columns)

    def __getitem__(self, colname):
        try:
            c0 = self._lhs.__getitem__(colname)
        except KeyError:
            return self._rhs.__getitem__(colname)

        try:
            c1 = self._rhs.__getitem__(colname)
        except KeyError:
            return c0

        return c0.merge(c1)
        # return Column(colname, self.index_values, self._df[colname].values)
    #
    # def loc(self, index_values):
    #     index_values = make_sure_list(index_values)
    #     return TableView(self, index_values)
    #
    # @property
    # def shape(self):
    #     return self._df.shape
    #
    # @property
    # def ndim(self):
    #     return 2
    #
    # @property
    # def dtypes(self):
    #     return self._df.dtypes
    #
    # def __array__(self, index_values=None):
    #     if index_values is None:
    #         return self._df.__array__()
    #     return self._df.loc[index_values].__array__()
    #
    # def __repr__(self):
    #     return repr(self._df)
    #
    # def __str__(self):
    #     return bytes(self._df)
