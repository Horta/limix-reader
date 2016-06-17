from numpy import isnan

def copyto_nans(from_sidx, from_midx, F, to_sidx, to_midx, T):
    for i in range(len(from_sidx)):
        for j in range(len(from_midx)):
            if isnan(T[to_sidx[i], to_midx[j]]):
                T[to_sidx[i], to_midx[j]] = F[from_sidx[i], from_midx[j]]
