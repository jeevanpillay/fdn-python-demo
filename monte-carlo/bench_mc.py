'''
Created on 29 jun. 2020

@author: Frits de Nijs
'''

import time
import numpy as np
from numba import njit

import thermalmodel

## Fixed constants.
DELTA = np.int32(5 * 60)
HORIZON = np.int32((24 * 60 * 60) / DELTA)
T_OUT = np.float64(0)

def monte_carlo(tcl, tStart, schedule):
    tIn = tStart
    reward = tcl.comfortScore(tIn)
    for t in range(0, HORIZON):
        tIn = tcl.nextTemperature(tIn, T_OUT, DELTA, schedule[t])
        reward += tcl.comfortScore(tIn)
    return reward

@njit
def monte_carlo_njit(tcl, tStart, schedule):
    tIn = tStart
    reward = tcl.comfortScore(tIn)
    for t in range(0, HORIZON):
        tIn = tcl.nextTemperature(tIn, T_OUT, DELTA, schedule[t])
        reward += tcl.comfortScore(tIn)
    return reward

## Problem scale.
seed = 743298347
numSimulations = 10000

# Datastructure storing the methods to compare
toHeat = np.int32(20*60)
toCool = np.int32(35*60)
methods = [("JIT all", monte_carlo_njit, thermalmodel.FirstOrderModelJIT(toHeat, toCool)),
           ("JIT class", monte_carlo,    thermalmodel.FirstOrderModelJIT(toHeat, toCool)),
           ("Python OO", monte_carlo,    thermalmodel.FirstOrderModel(toHeat, toCool))]

for method in methods:

    ## Create random number generator.
    rng = np.random.RandomState(seed)
    
    checksum = np.float64(0);
    runtime = 0;
    fulltime = time.time()
    for i in range(0, numSimulations):
    
        # Create activation schedule (50% yes, 50% no) and initial temperature Uniform in (18, 20).
        schedule = rng.randint(0, 2, HORIZON)
        tStart = np.float64(18 + 2 * rng.random())

        f = method[1]
        tcl = method[2]
        runtime = runtime - time.time()
        checksum += f(tcl, tStart, schedule)
        runtime = runtime + time.time()
    
    fulltime = time.time() - fulltime
    
    pertime = runtime / numSimulations
    print("%-12s: per-run %.10fs, total %8.5fs. (checksum %f)" % (method[0], pertime, fulltime, checksum))
