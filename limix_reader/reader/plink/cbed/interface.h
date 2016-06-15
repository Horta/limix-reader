#ifndef INTERFACE_H
#define INTERFACE_H

int bed_item(char* filepath, int nsamples, int nmarkers, int sample, int marker);

void bed_intidx(char* filepath, int nsamples, int nmarkers,
                int sn, long* samples, int mn, long* markers, double* matrix,
                int* strides);

#endif
