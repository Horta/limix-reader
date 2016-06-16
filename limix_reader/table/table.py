from collections import Iterable

from numpy import where

from pandas import DataFrame

from .column import Column
from ..util import npy2py_type
from ..util import make_sure_list
from .interface import TableInterface

class Table(TableInterface):
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
        self._df.index = values

    @property
    def columns(self):
        return self._df.columns.values

    def set_index_value(self, old_val, new_val):
        otype = npy2py_type(type(old_val))
        ntype = npy2py_type(type(new_val))

        index_name = self._df.index.name
        values = self._df.index.values
        i = where(values == old_val)[0][0]

        if otype != ntype:
            values = values.astype(ntype)

        values[i] = new_val

        self._df.index = values

        self._df.index.name = index_name

    def __getitem__(self, args):
        if isinstance(args, bytes):
            return Column(args, self.index_values, self._df[args].values)
        if isinstance(args, Iterable):
            return TableView(column_names=args)
        return Column(args, self.index_values, self._df[args].values)

    def loc(self, index_values):
        index_values = make_sure_list(index_values)
        return TableView(self, index_values)

    @property
    def shape(self):
        return self._df.shape

    @property
    def ndim(self):
        return 2

    @property
    def dtypes(self):
        return self._df.dtypes

    def __array__(self, *args, **kwargs):
        kwargs = dict(kwargs)
        if 'index_values' not in kwargs:
            return self._df.__array__()
        return self._df.loc[kwargs['index_values']].__array__()

    def __repr__(self):
        return repr(self._df)

    def __str__(self):
        return bytes(self._df)

class TableView(object):
    def __init__(self, ref, index_values=None, column_names=None):
        self._ref = ref
        self._index_values = index_values
        self._column_values = column_names

    @property
    def index_name(self):
        return self._ref.index_name

    @index_name.setter
    def index_name(self, v):
        self._ref.index_name = v

    @property
    def index_values(self):
        if self._index_values is None:
            return self._ref.index_values
        return self._index_values

    @index_values.setter
    def index_values(self, values):
        self._ref.index_values = values

    @property
    def columns(self):
        return self._ref.columns

    def __getitem__(self, colname, index_values=None):
        if index_values is None:
            index_values = self._index_values
        return self._ref.__getitem__(colname, index_values)

    def loc(self, index_values):
        pass

    @property
    def shape(self):
        return self._df.shape

    @property
    def ndim(self):
        return 2

    @property
    def dtypes(self):
        return self._df.dtypes

    def __array__(self, *args, **kwargs):
        kwargs = dict(kwargs)
        if 'index_values' not in kwargs:
            kwargs['index_values'] = self._index_values
        return self._ref.__array__(*args, **kwargs)

    def __repr__(self):
        return repr(self.__array__())

    def __str__(self):
        return bytes(self.__array__())
