#ifndef INTERFACE_H
#define INTERFACE_H

long bed_item(char* filepath, long nsamples, long nmarkers, long sample, long marker);

void bed_intidx(char* filepath, long nsamples, long nmarkers,
                long sn, long* samples, long mn, long* markers, double* matrix,
                long* strides);

#endif
