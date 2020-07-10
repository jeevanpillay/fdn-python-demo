#ifndef _fdn_loop_h
#define _fdn_loop_h

/**
 * Classify all given points. In-place function, modifies in.
 *
 * Preconditions:
 *	- length of array in is 2n,
 *  - contents of array in are [x1, y1, x2, y2, x3, y3, ..., x2n, y2n]
 *
 * Postconditions:
 *  - contents of array in are [c1, c2, c3, c4, c5, ..., cn, xn+1, yn+1, ... x2n, y2n]
 */
void classifyAll(long n, double* in);

#endif
