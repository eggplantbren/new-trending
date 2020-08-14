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
        self.delay = int(self.new_lbc**0.4)
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

    def __str__(self):
        d = dict(t0=self.t0, t1=self.t_peak, t2=self.t_final,
                 A=self.y_peak, delta=self.delay, ell=DECAY_TIME)
        return d.__str__()


class Claim:
    def __init__(self):
        self.heights = []
        self.lbc = []
        self.kernels = []

    def update(self, height, lbc):
        assert len(self.heights) == 0 or height > self.heights[-1]

        old_lbc = 0.0
        if len(self.lbc) > 0:
            old_lbc = self.lbc[-1]

        # Add the next kernel
        self.heights.append(height)
        self.lbc.append(lbc)
        self.kernels.append(Kernel(height, old_lbc, lbc))

    def sum_kernels(self, height):
        return sum([k.evaluate(height) for k in self.kernels])

# Simulate trending scores
claims = dict(minnow=Claim(), dolphin=Claim(), moderate_whale=Claim(),
              huge_whale=Claim(), huge_whale_botted=Claim())
trending = dict()
for name in claims:
    trending[name] = []

heights = range(1000)
for height in heights:

    # All claims start at 0.1 LBC
    if height == 0:
        for name in claims:
            claims[name].update(height, 0.1)

    # Minnow and botted whale are continually boosted
    if height > 0:
        claims["minnow"].update(height, claims["minnow"].lbc[-1] + 1.0)
        claims["huge_whale_botted"].update(height, claims["huge_whale_botted"].lbc[-1] + 1E6/400)

    # Others are boosted once at block 1
    if height == 1:
        for name in claims:
            if name == "dolphin":
                claims[name].update(height, claims[name].lbc[-1] + 10000.0)
            if name == "moderate_whale":
                claims[name].update(height, claims[name].lbc[-1] + 100000.0)
            if name == "huge_whale":
                claims[name].update(height, claims[name].lbc[-1] + 1000000.0)

    # Remove all supports at a certain block
    if height == 400:
        for name in claims:
            claims[name].lbc[-1] = claims[name].lbc[0]
            claims[name].kernels = claims[name].kernels[0:1]

    for name in claims:
        trending[name].append([height, claims[name].sum_kernels(height)])


for name in claims:
    trend = np.array(trending[name])
    plt.plot(trend[:,0], trend[:,1], "-", label=name)
plt.ylim(bottom=0.0)
plt.xlim([heights[0]-1, heights[-1]+1])
plt.legend()
plt.show()


