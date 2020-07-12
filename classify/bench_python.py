'''
Created on 19 jun. 2020

@author: Frits de Nijs
'''
import sys

# Number of runs and test points
N_run = 10
N_point = 500000
seed = 3247520923

# Take number of points from command line.
if (len(sys.argv) == 2):
	N_point = int(sys.argv[1])

import numpy as np
from numba import vectorize, float64
from math import sin as sn
import time
import demo as my

# Define a custom function with some if-else loops
def myfunc(x,y):
	if (x>0.5*y and y<0.3):
		return (sn(x-y))
	elif (x<0.5*y):
		return 0
	elif (x>0.2*y):
		return (2*sn(x+2*y))
	else:
		return (sn(y+x))

# Vectorize the function using numpy.
vectfunc = np.vectorize(myfunc, otypes=[np.float], cache=False)

# Vectorize with numba instead.
@vectorize([float64(float64, float64)])
def numbafunc(x, y):
	if (x>0.5*y and y<0.3):
		return (sn(x-y))
	elif (x<0.5*y):
		return 0
	elif (x>0.2*y):
		return (2*sn(x+2*y))
	else:
		return (sn(y+x))

# Functions for the methods to compare:
def vanilla(lst_x, lst_y):
	lst_result = []
	for i in range(N_point):
		lst_result.append(myfunc(lst_x[i], lst_y[i]))
	checksum = sum(lst_result)
	return (lst_result, checksum)

def using_numpy(lst_x, lst_y):
	lst_result = vectfunc(lst_x, lst_y)
	checksum = np.sum(lst_result)
	return (lst_result, checksum)

def compiled(lst_x, lst_y):
	lst_result = my.native_classify(list(lst_x), list(lst_y))
	checksum = sum(lst_result)
	return (lst_result, checksum)

def using_numba(lst_x, lst_y):
	lst_result = numbafunc(lst_x, lst_y)
	checksum = np.sum(lst_result)
	return (lst_result, checksum)

# Datastructure storing the methods to compare
methods = [("Vanilla", vanilla), ("Numpy vec", using_numpy), ("Wrapping c", compiled), ("Numba vec", using_numba)]

# Inform user.
print(f"Initializing dataset of {N_point}")

# Generate the dataset[run][xy][data]
rng = np.random.RandomState(seed)
dataset = rng.randn(N_run, 2, N_point)

# Inform user.
print("Benchmarking...")

## Test each of the methods in turn,
for method in methods:

	## Separate method blocks with a newline
	print()
	
	for i in range(1, N_run):
		
		# Collect the elements of the dataset.
		lst_x = dataset[i][0]
		lst_y = dataset[i][1]
		
		# First, plain vanilla for-loop
		f = method[1]
		t1=time.time()
		answer = f(lst_x, lst_y)
		t2=time.time()

		# Compute reporting quantities.
		time_us = 1000000*(t2-t1)
		head = ("%5.2f" % x for x in answer[0][:5])

		print("%-12s%9.2fus, checksum %f, head [%s, ...]" % (method[0], time_us, answer[1], ','.join(head)))