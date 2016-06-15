
def define_binary_operators(cls, method_name):
    _opnames = ['__eq__', '__ne__', '__ge__', '__gt__',  '__le__', '__lt__']
    for opn in _opnames:
        def _create(opn_):
            def func(self, that):
                return getattr(self, method_name)(that, opn_)
            func.__name__ = opn_
            return func
        setattr(cls, opn, _create(opn))
