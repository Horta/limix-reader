#ifndef BED_H
#define BED_H

int
bed_item(char* filepath, int nrows, int ncols, int row, int col);

void
bed_fancyidx(char* filepath, int nrows, int ncols,
         int rn, long* rows, int cn, long* cols, long* matrix);

void
bed_slice(char* filepath, int nrows, int ncols,
           int r_start, int r_stop, int r_step,
           int c_start, int c_stop, int c_step,
           long* matrix);

void
bed_entirely(char* filepath, int nrows, int ncols, long* matrix);

void
bed_row_slice(char* filepath, int nrows, int ncols, int row,
          int c_start, int c_stop, int c_step,
          long* matrix);

void
bed_column_slice(char* filepath, int nrows, int ncols, int col,
             int r_start, int r_stop, int r_step,
             long* matrix);

int bed_snp_major(char* filepath);

#endif
