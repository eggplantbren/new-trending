"""
Experimenting with kernels that ramp up starting immediately
but have different shapes when the LBC values are different.
"""

import math
import matplotlib.pyplot as plt
import numpy as np

DECAY_TIME = 500
DELAY_POWER = 0.4
SOFTEN_POWER = 0.25

class Kernel:

    def __init__(self, t0, old_lbc, new_lbc):
        self.t0, self.old_lbc, self.new_lbc = t0, old_lbc, new_lbc

        # Derived parameters
        self.delay = self.new_lbc**0.4
        self.t_peak = self.t0 + self.delay
        self.t_final = self.t_peak + DECAY_TIME
        self.y_peak = new_lbc**SOFTEN_POWER - old_lbc**SOFTEN_POWER
        if self.new_lbc <= 10.0:
            self.power = 1.0
        else:
            self.power = 1.0 + math.log2(self.new_lbc/10.0)


    def evaluate(self, t):

        f = 0.0
        if t >= self.t0 and t < self.t_peak:
            f = 1.0 - (self.t_peak - t)/self.delay
        if t >= self.t_peak and t < self.t_final:
            f = 1.0 - (t - self.t_peak)/DECAY_TIME

        # Protect against rounding errors making it negative
        if f < 0.0:
            f = 0.0

        # Multiply in amplitude, also do the power
        return self.y_peak*f**self.power


class Claim:
    def __init__(self):
        self.heights = []
        self.lbc = []
        self.kernels = []
        self.trending = []

    def update(self, height, lbc):
        assert len(self.heights) == 0 or height > self.heights[-1]
        old_lbc = 0.0
        if len(self.lbc) > 0:
            old_lbc = self.lbc[-1]

        self.heights.append(height)
        self.lbc.append(lbc)
        self.kernels.append(Kernel(height, old_lbc, lbc))

        if len(self.trending) == 0:
            self.trending.append([height, self.sum_kernels(height)])
        else:
            # Calculate trending scores up to present height
            for h in range(self.trending[-1][0]+1, height+1):
                self.trending.append([h, self.sum_kernels(h)])

    def finalise(self, height):
        # Extend trending scores out to the given height
        for h in range(self.trending[-1][0]+1, height+1):
            self.trending.append([h, self.sum_kernels(h)])

    def sum_kernels(self, height):
        return sum([k.evaluate(height) for k in self.kernels])

# Simulate trending scores
claims = dict(minnow=Claim(), dolphin=Claim(), whale=Claim())

heights = range(1000)
for height in heights:
    if height == 0:
        claims["minnow"].update(0, 1E-1)
        claims["dolphin"].update(0, 1E+4)
        claims["whale"].update(0, 3E+5)
    else:
        claims["minnow"].update(height, claims["minnow"].lbc[-1] + 1.0)
for name in claims:
    claims[name].finalise(heights[-1])

for name in claims:
    claim = claims[name]
    trending = np.array(claim.trending)
    plt.plot(trending[:,0], trending[:,1], label=name)
plt.legend()
plt.xlabel("Height")
plt.ylabel("Trending Score")
plt.show()

