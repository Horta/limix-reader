#include "impl.h"
#include <Python.h>
#include "numpy/npy_math.h"

inline double _long2double(char item)
{
    if (item == 3)
        return NPY_NAN;
    return item;
}

inline void _inv_strides(long* strides)
{
    long tmp = strides[0];
    strides[0] = strides[1];
    strides[1] = tmp;
}

void _read_intidx(FILE* fp, long* shape,
                  long rn, long* rows, long cn, long* cols,
                  double* matrix, long* strides)
{
    long r, c;
    ItemIdx idx;
    long index;
    for (r = 0; r < rn; r++)
    {
        for (c = 0; c < cn; c++)
        {
            idx.r = rows[r];
            idx.c = cols[c];
            index = r * (strides[0]/sizeof(double))
                  + c * (strides[1]/sizeof(double));
            matrix[index] = _long2double(read_item(fp, shape, &idx));
        }
    }
}

void read_intidx(FILE* fp, long* shape,
                  long rn, long* rows, long cn, long* cols,
                  double* matrix, long* strides, long same_axis)
{
    long _strides[2] = {strides[0], strides[1]};

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
