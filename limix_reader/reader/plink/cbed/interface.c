#include "interface.h"
#include "impl.h"

long bed_item(char* filepath, long nsamples, long nmarkers, long sample, long marker)
{
    FILE* fp = fopen(filepath, "rb");
    long shape[2];
    ItemIdx idx;

    if (_snp_major(fp))
    {
        shape[0] = nmarkers;
        shape[1] = nsamples;
        idx.r = marker;
        idx.c = sample;
    } else {
        shape[1] = nmarkers;
        shape[0] = nsamples;
        idx.c = marker;
        idx.r = sample;
    }

    long item = read_item(fp, shape, &idx);
    fclose(fp);

    return item;
}

void bed_intidx(char* filepath, long nsamples, long nmarkers,
                long sn, long* samples, long mn, long* markers, double* matrix,
                long* strides)
{
    FILE* fp = fopen(filepath, "rb");
    long shape[2];

    long smajor = _snp_major(fp);
    if (smajor)
    {
        shape[0] = nmarkers;
        shape[1] = nsamples;
    } else {
        shape[1] = nmarkers;
        shape[0] = nsamples;
    }

    read_intidx(fp, shape, sn, samples, mn, markers, matrix, strides, smajor ^ 0x01);
    fclose(fp);
}
