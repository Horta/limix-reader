from ..util import list_transpose
from .vector import Vector

from tabulate import tabulate

class Column(Vector):
    def __init__(self, name, indices, values):
        super(Column, self).__init__(indices, values)
        if name is None:
            raise ValueError("A column must have a name.")
        self.name = name

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        l = [['']+list(self._indices), [self.name]+list(self._values)]
        return tabulate(list_transpose(l), tablefmt="plain")

    def merge(self, that):
        if self.name != that.name:
            raise ValueError("Names differ between the merging columns.")
        v = super(Column, self).merge(that)
        return Column(self.name, v._indices, v._values)
