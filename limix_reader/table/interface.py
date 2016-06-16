class TableInterface(object):
    def __init__(self):
        pass

    @property
    def index_name(self):
        raise NotImplementedError

    @index_name.setter
    def index_name(self, v):
        raise NotImplementedError

    @property
    def columns(self):
        raise NotImplementedError

    def __getitem__(self, colname):
        raise NotImplementedError

    def loc(self, index_values):
        raise NotImplementedError

    @property
    def shape(self):
        raise NotImplementedError

    @property
    def ndim(self):
        return 2

    @property
    def dtypes(self):
        raise NotImplementedError

    def __array__(self, *args, **kwargs):
        raise NotImplementedError

    def __repr__(self):
        return repr(self.__array__())

    def __str__(self):
        return bytes(self.__array__())

    def merge(self, that):
        from .mtable import MTable
        return MTable(self, that)
