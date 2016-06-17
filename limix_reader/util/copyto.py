from numpy import isnan

def copyto_nans(from_sidx, from_midx, F, to_sidx, to_midx, T):
    for i in range(len(from_sidx)):
        for j in range(len(from_midx)):
            tos, tom = to_sidx[i], to_midx[j]
            froms, fromm = from_sidx[i], from_midx[j]
            if isnan(T[tos, tom]):
                T[tos, tom] = F[froms, fromm]
            else:
                if (not isnan(F[froms, fromm]) and
                        T[tos, tom] != F[froms, fromm]):
                    raise ValueError("Matrices values are contradicting.")
