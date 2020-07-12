'''
Created on 19 jun. 2020

@author: Frits de Nijs
'''
import sys

# Number of runs and test points
N_run = 10
N_point = 500000

# Take number of points from command line.
if (len(sys.argv) == 2):
	N_point = int(sys.argv[1])

# Inform user.
print(f"Initializing dataset of {N_point}")

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

# Generate the dataset[run][xy][data]
dataset = np.random.randn(N_run, 2, N_point)

print("Benchmarking...\n")

## Test the vanilla for loop.
for i in range(1, N_run):

    # Collect the elements of the dataset.
    lst_x = dataset[i][0]
    lst_y = dataset[i][1]
    lst_result = []
    
    # First, plain vanilla for-loop
    t1=time.time()
    for i in range(N_point):
        lst_result.append(myfunc(lst_x[i], lst_y[i]))
    t2=time.time()

    # Compute reporting quantities.
    time_us = 1000000*(t2-t1)
    checksum = sum(lst_result)
    head = ("%5.2f" % x for x in lst_result[:5])

    print("%-12s%9.2fus, checksum %f, head [%s, ...]" % ("Vanilla", time_us, checksum, ','.join(head)))

## Separate
print()

## Test the list zip
for i in range(1, N_run):

    # Collect the elements of the dataset.
    lst_x = dataset[i][0]
    lst_y = dataset[i][1]
    
    # Vectorized
    t1=time.time()
    lst_result = vectfunc(lst_x,lst_y)
    t2=time.time()

    # Compute reporting quantities.
    time_us = 1000000*(t2-t1)
    checksum = np.sum(lst_result)
    head = ("%5.2f" % x for x in lst_result[:5])

    print("%-12s%9.2fus, checksum %f, head [%s, ...]" % ("Numpy vec", time_us, checksum, ','.join(head)))

## Separate
print()

## Test the native function wrapping in C.
for i in range(1, N_run):

    # Collect the elements of the dataset.
    lst_x = dataset[i][0]
    lst_y = dataset[i][1]
    
    # Vectorized
    t1=time.time()
    plain_x = list(lst_x)
    plain_y = list(lst_y)
    lst_result = my.native_classify(plain_x, plain_y)
    t2=time.time()

    # Compute reporting quantities.
    time_us = 1000000*(t2-t1)
    checksum = sum(lst_result)
    head = ("%5.2f" % x for x in lst_result[:5])

    print("%-12s%9.2fus, checksum %f, head [%s, ...]" % ("Wrapping c", time_us, checksum, ','.join(head)))

## Separate
print()

## Test the numba vectorized function
for i in range(1, N_run):

    # Collect the elements of the dataset.
    lst_x = dataset[i][0]
    lst_y = dataset[i][1]
    
    # Vectorized
    t1=time.time()
    lst_result = numbafunc(lst_x,lst_y)
    t2=time.time()

    # Compute reporting quantities.
    time_us = 1000000*(t2-t1)
    checksum = np.sum(lst_result)
    head = ("%5.2f" % x for x in lst_result[:5])

    print("%-12s%9.2fus, checksum %f, head [%s, ...]" % ("Numba vec", time_us, checksum, ','.join(head)))
