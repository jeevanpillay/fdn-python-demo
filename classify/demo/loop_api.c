#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <time.h>
#include <stdio.h>
#include "loop.h"

static PyObject* loop_classify(PyObject* self, PyObject* args) {

	// We expect two lists as input, the x coords and y coords.
	PyObject* xList;
	PyObject* yList;

	// Extract arguments.
	if(!PyArg_ParseTuple(args, "OO", &xList, &yList))
        return NULL;

	// Extract length of lists.
	Py_ssize_t xLen = PyObject_Length(xList);
	Py_ssize_t yLen = PyObject_Length(yList);

	// Check preconditions, both lists equally long.
	if (xLen < 0 || yLen < 0 || xLen != yLen) {
		return NULL;
	}

	// Create two lists, in and out.
	long n = xLen;

	// Create in array, guard against out-of-memory.
	double* in = malloc(2*n*sizeof(double));
	if (!in) {
		return PyErr_NoMemory();
	}

	// Populate in array.
	for (long i = 0; i < n; i++) {
		PyObject* xObj = PySequence_Fast_GET_ITEM(xList, i);
		PyObject* yObj = PySequence_Fast_GET_ITEM(yList, i);
		in[i<<1] = PyFloat_AS_DOUBLE(xObj);
		in[(i<<1)+1] = PyFloat_AS_DOUBLE(yObj);
	}

	// Time the function that does the work.
	clock_t start, end;
    double cpu_time_used;
    start = clock();
	classifyAll(n, in); // Call the function that does the actual work.
    end = clock();
  	cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
	cpu_time_used = cpu_time_used * 1000000.0;   // Unit to Micro

	// Reporting.
    printf("%-12s%9.2fus", "Native-c", cpu_time_used);

	// Populate result array.
	Py_ssize_t zLen = PyLong_AsSsize_t(PyLong_FromLong(n));
	PyObject* zList = PyList_New(zLen);
	double checksum = 0;
	for (long i = 0; i < n; i++) {
		PyList_SET_ITEM(zList, i, PyFloat_FromDouble(in[i]));
		checksum += in[i];
	}

    printf(", checksum %f, head [%5.2f,%5.2f,%5.2f,%5.2f,%5.2f, ...]\r\n", 
			checksum, 
			in[0], in[1], in[2], in[3], in[4]);

	// Clean up (free memory).
	free(in);

    return zList;
}

// Our Module's Function Definition struct
// We require this `NULL` to signal the end of our method
// definition
static PyMethodDef myMethods[] = {
    { "native_classify", loop_classify, METH_VARARGS, "Native C implementation of the vectorized example loop." },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef demo = {
    PyModuleDef_HEAD_INIT,
    "demo",
    "Demo Module",
    -1,
    myMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_demo(void)
{
    return PyModule_Create(&demo);
}
