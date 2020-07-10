#include <math.h>
#include "loop.h"

double classify(double x, double y) {
	if (x > 0.5*y && y < 0.3)
		return sin(x - y);
	else if (x < 0.5*y)
		return 0;
	else if (x > 0.2*y)
		return (2*sin(x+2*y));
	else
		return (sin(y+x));
}

void classifyAll(long n, double* in) {
	for (long i = 0; i < n; i++) {
		in[i] = classify(in[i<<1], in[(i<<1)+1]);
	}
}
