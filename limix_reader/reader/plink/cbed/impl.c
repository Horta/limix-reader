#include "impl.h"
#include <Python.h>
#include "numpy/npy_math.h"

inline double _long2double(char item)
{
    if (item == 3)
        return NPY_NAN;
    return item;
}

inline void _inv_strides(int* strides)
{
    int tmp = strides[0];
    strides[0] = strides[1];
    strides[1] = tmp;
}

void _read_intidx(FILE* fp, int* shape,
                  int rn, long* rows, int cn, long* cols,
                  double* matrix, int* strides)
{
    int r, c;
    ItemIdx idx;
    int index;
    for (r = 0; r < rn; r++)
    {
        for (c = 0; c < cn; c++)
        {
            idx.r = rows[r];
            idx.c = cols[c];
            index = r * (strides[0]/sizeof(long))
                  + c * (strides[1]/sizeof(long));
            matrix[index] = _long2double(read_item(fp, shape, &idx));
        }
    }
}

void read_intidx(FILE* fp, int* shape,
                  int rn, long* rows, int cn, long* cols,
                  double* matrix, int* strides, int same_axis)
{
    int _strides[2] = {strides[0], strides[1]};

    if (same_axis)
        _read_intidx(fp, shape, rn, rows, cn, cols,
                               matrix, _strides);
    else
    {
        _inv_strides(_strides);
        _read_intidx(fp, shape, cn, cols, rn, rows,
                               matrix, _strides);
    }
}
