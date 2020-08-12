"""
Experimenting with kernels that ramp up starting immediately
but have different shapes when the LBC values are different.
"""

import matplotlib.pyplot as plt
import numpy as np

class Kernel:

    def __init__(self, t0, lbc):
        self.t0, self.lbc = t0, lbc

    def evaluate(self, ts):
        ys = np.zeros(ts.shape)
        return ys


ts = np.arange(1000)
plt.plot(ts, Kernel(0.0, 100.0).evaluate(ts))
plt.plot(ts, Kernel(0.0, 10000.0).evaluate(ts))
plt.plot(ts, Kernel(0.0, 1000000.0).evaluate(ts))
plt.show()

