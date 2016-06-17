from .vector import Vector

class Column(Vector):
    def __init__(self, name, labels, values):
        super(Column, self).__init__(labels, values)
        if name is None:
            raise ValueError("A column must have a name.")
        self.name = name

    def __repr__(self):
        return "Column(" + bytes(self._values) + ")"

    def __str__(self):
        return "Column(" + bytes(self._values) + ")"

    def merge(self, that):
        pass
        # return MColumn(self, that)

# class MColumn(MVector):
#     def __init__(self, lhs, rhs):
#         super(MColumn, self).__init__(lhs, rhs)
#         self._lhs = lhs
#         self._rhs = rhs
#         if lhs.name != rhs.name:
#             raise ValueError("Merging columns have different index names.")
#
#     @property
#     def name(self):
#         return self._lhs.name
#
#     def __repr__(self):
#         return "Column(" + bytes(self.__array__()) + ")"
#
#     def __str__(self):
#         return "Column(" + bytes(self.__array__()) + ")"
