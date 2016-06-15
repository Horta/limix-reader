#include "interface.h"
#include "impl.h"

int bed_item(char* filepath, int nsamples, int nmarkers, int sample, int marker)
{
    FILE* fp = fopen(filepath, "rb");
    int shape[2];
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

    int item = read_item(fp, shape, &idx);
    fclose(fp);

    return item;
}

void bed_intidx(char* filepath, int nsamples, int nmarkers,
                int sn, long* samples, int mn, long* markers, double* matrix,
                int* strides)
{
    FILE* fp = fopen(filepath, "rb");
    int shape[2];

    int smajor = _snp_major(fp);
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
