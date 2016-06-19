from tabulate import tabulate

class MatrixInterface(object):
    def __init__(self):
        pass

    def item(self, sample_id, marker_id, alleleB=None):
        raise NotImplementedError

    def __getitem__(self, args):
        raise NotImplementedError

    @property
    def shape(self):
        raise NotImplementedError

    @property
    def ndim(self):
        return 2

    @property
    def dtype(self):
        raise NotImplementedError

    def __repr__(self):
        return self.__repr__()

    def __str__(self):
        p = self.shape[1]
        header = ['', 'marker_id: alleleA/alleleB'] + [''] * (p-1)
        alA = self.allelesA
        alB = self.allelesB
        mid = self.marker_ids
        subhdr = ['sample_id']
        subhdr += [bytes(mid[i])+': '+bytes(alA[i])+'/'+bytes(alB[i])
                   for i in range(p)]
        tbl = [header] + [subhdr]
        sid = self.sample_ids
        arr = self.__array__()
        tbl += [[sid[i]] + r for (i, r) in enumerate(arr.tolist())]
        return bytes(tabulate(tbl, tablefmt='plain'))

    def __array__(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def sample_ids(self):
        raise NotImplementedError

    @property
    def allelesA(self):
        raise NotImplementedError

    @property
    def allelesB(self):
        raise NotImplementedError

    @property
    def marker_ids(self):
        raise NotImplementedError

    def merge(self, that):
        raise NotImplementedError
