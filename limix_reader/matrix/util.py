def normalize_getitem_args(args):
    if len(args) != 2:
        raise IndexError
    return _normalize_getitem_args(args[0]), _normalize_getitem_args(args[1])

def _normalize_getitem_args(arg):
    if isinstance(arg, list):
        return arg

    if isinstance(arg, tuple):
        return list(arg)

    return list([arg])
