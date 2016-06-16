from .mvector import MVector

class MColumn(MVector):
    def __init__(self, lhs, rhs):
        super(MColumn, self).__init__(lhs, rhs)
        self._lhs = lhs
        self._rhs = rhs
        if lhs.name != rhs.name:
            raise ValueError("Merging columns have different index names.")

    @property
    def name(self):
        return self._lhs.name

    def __repr__(self):
        return "Column(" + bytes(self.__array__()) + ")"

    def __str__(self):
        return "Column(" + bytes(self.__array__()) + ")"
