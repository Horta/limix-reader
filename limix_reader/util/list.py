from numpy import ndarray

def make_sure_list(v):
    if isinstance(v, list):
        return v

    if isinstance(v, tuple):
        return list(v)

    if isinstance(v, ndarray):
        return list(v)

    return list([v])

def list_transpose(l):
    return map(list, zip(*l))
