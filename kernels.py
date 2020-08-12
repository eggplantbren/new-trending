"""
Experimenting with kernels that ramp up starting immediately
but have different shapes when the LBC values are different.
"""

import math
import matplotlib.pyplot as plt

DECAY_TIME = 500

class Kernel:

    def __init__(self, t0, lbc):
        self.t0, self.lbc = t0, lbc

    def evaluate(self, ts):

        # Peak time and amplitude
        delay = min([1E3, self.lbc**0.4])
        t_peak = self.t0 + delay
        t_final = t_peak + DECAY_TIME
        y_peak = self.lbc**0.25
        if self.lbc <= 100.0:
            power = 1.0
        else:
            power = 1.0 + math.log10(self.lbc/100.0)

        # Create the kernel
        frac = []
        for t in ts:
            if t < self.t0:
                frac.append(0.0)
            elif t < t_peak:
                frac.append(1.0 - (t_peak - t)/delay)
            elif t >= t_peak and t < t_final:
                frac.append(1.0 - (t - t_peak)/DECAY_TIME)
            else:
                frac.append(0.0)

        # Multiply in amplitude, also do the power
        ys = []
        for f in frac:
            ys.append(f**power * y_peak)

        return ys


ts = range(1000)
plt.plot(ts, Kernel(0.0, 100.0).evaluate(ts))
plt.plot(ts, Kernel(0.0, 10000.0).evaluate(ts))
plt.plot(ts, Kernel(0.0, 1000000.0).evaluate(ts))
plt.show()

