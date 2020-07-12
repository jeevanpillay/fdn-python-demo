import numpy as np
from numba import float64
from numba.experimental import jitclass

"""
  First-order thermal model, approximating the temperature of a system, such as
  a house, a thermal zone, or a refrigerator by a single state variable (the
  indoor temperature).
  
  Model due Mortensen and Haggerty, "A stochastic computer model for heating and
  cooling loads", IEEE Transactions on Power Systems (3:3), 1988

  :by Frits de Nijs
"""
class FirstOrderModel(object):

    """
    Constructor; computes thermal parameters P, C, and R (R is always 1) on the basis
    of four quantities of interest, namely:
    
    :param secondsToHeat: the time it takes for the indoor temperature to increase
        from (goal - range) to (goal + range) if the outdoor temperature is 0C.
    :param secondsToCool: the time it takes for the indoor temperature to decrease
        from (goal + range) to (goal - range) if the outdoor temperature is 0C.
    :param goal: the ideal temperature of the object under control (default 20C).
    :param flex: the size of the 'deadband' range, where comfort is equal to the
        goal comfort. (default 1C wide).
    
    """
    def __init__(self, secondsToHeat, secondsToCool, goal = np.float64(20), flex = np.float64(0.5)):

        # Explicitly cast variables
        secondsToHeat = np.int32(secondsToHeat)
        secondsToCool = np.int32(secondsToCool)
        goal = np.float64(goal)
        flex = np.float64(flex)

        # Check preconditions, strictly positive durations.
        assert secondsToHeat > 0 and secondsToCool > 0

        # Store the goal temperature and comfortable range.
        self.goal = goal
        self.deadband = flex

        # Compute alpha component.
        lower = goal - self.deadband
        upper = goal + self.deadband
        alpha = self.__computeAlpha(lower, upper, secondsToCool)
        
        # Compute thermal constants.
        self.C = self.__computeCapacitance(alpha)
        self.P = self.__computePower(lower, upper, alpha, secondsToHeat)

    def __computeAlpha(self, lower, upper, time):
        return np.power(lower / upper, 1 / time)

    def __computeCapacitance(self, alpha):
        return np.float64(-1 / 3600) / np.log(alpha)
    
    def __computePower(self, lower, upper, alpha, time):
        return (lower * np.power(alpha, time) - upper) / (np.power(alpha, time) - 1)

    def nextTemperature(self, tempIn, tempOut, deltaSecs, power):
 
        alpha = np.exp((-deltaSecs / np.int32(3600)) / self.C)
    
        return alpha * tempIn + (1 - alpha) * (tempOut + power * self.P)

    def comfortScore(self, tempIn):
    
        # Distance from the goal temperature?
        distance = np.abs(tempIn - self.goal)
    
        # Apply comfort deadband.
        error = np.fmax(distance - self.deadband, np.float64(0))
    
        # Squared error penalty term.
        return -np.square(error)

"""
JIT compiled version of the same class.
"""
spec = [
    ('goal',     float64),          # Goal temperature
    ('deadband', float64),          # Deadband width
    ('C',        float64),          # Capacitance
    ('P',        float64),          # Power
]

@jitclass(spec)
class FirstOrderModelJIT(FirstOrderModel):
    pass
