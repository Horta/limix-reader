#ifndef IMPL_H
#define IMPL_H

#include "stdio.h"

typedef struct
{
    long r;
    long c;
} ItemIdx;

typedef struct
{
    long s;
} ByteIdx;

typedef struct
{
    long s;
} BitIdx;

inline void _convert_idx_itby(long* shape, ItemIdx* idx, ByteIdx* bydx)
{
    const long offset = 3;
    bydx->s = offset + ((shape[1] + 3)/ 4) * idx->r + idx->c / 4;
}

inline void _convert_idx_itbi(long* shape, ItemIdx* idx, BitIdx* bidx)
{
    bidx->s = (idx->c % 4) * 2;
}

inline char _get_snp(char v, BitIdx* bidx)
{
    char f = (v >> bidx->s) & 3;
    char bit1 =  f & 1;
    char bit2 =  (f >> 1) & 1;
    char x = (bit1 ^ bit2);
    x = (x << 0) | (x << 1);
    char b = f ^ x;
    return b ^ (b >> 1);
}

inline char read_item(FILE* fp, long* shape, ItemIdx* idx)
{
    ByteIdx bydx;
    _convert_idx_itby(shape, idx, &bydx);

    BitIdx bidx;
    _convert_idx_itbi(shape, idx, &bidx);

    fseek(fp, bydx.s, SEEK_SET);

    return _get_snp(fgetc(fp), &bidx);
}

void read_intidx(FILE* fp, long* shape,
                 long rn, long* rows, long cn, long* cols,
                 double* matrix, long* strides, long same_axis);

inline long _snp_major(FILE* fp)
{
    fseek(fp, 2, SEEK_SET);
    return fgetc(fp);
}

#endif
