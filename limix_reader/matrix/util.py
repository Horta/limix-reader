from ..util import isscalar

def normalize_getitem_args(args, marker_ids):
    if isscalar(args):
        args = (args,)

    if len(args) == 1:
        args = (args[0], marker_ids)

    args_ = []
    for i in range(2):
        if isscalar(args[i]):
            args_.append([args[i]])
        else:
            args_.append(args[i])

    return tuple(args_)
