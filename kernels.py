"""
Experimenting with kernels that ramp up starting immediately
but have different shapes when the LBC values are different.
"""

import matplotlib.pyplot as plt
import numpy as np
from soften import soften

DECAY_TIMESCALE = 500
DELAY_POWER = 0.4

class Kernel:
    """
    Sharpened bi-exponential kernel
    """
    def __init__(self, t0, old_lbc, new_lbc):
        self.t0, self.old_lbc, self.new_lbc = t0, old_lbc, new_lbc

        # Kernel parameters
        self.t_peak = self.t0 + new_lbc**DELAY_POWER

        # Two recipes
        self.A = soften(new_lbc) - soften(old_lbc)

        # Minnow boost
        self.A += 10.0*soften(new_lbc - old_lbc) / ((new_lbc + 100.0) / 100.0)**2

        self.sharpen = 1.0
        if new_lbc >= 100.0:
            self.sharpen = 1.0 + 2*np.log10(new_lbc/100.0)


    def evaluate(self, t):
        lag = t - self.t_peak

        # Biexponential with unit amplitude
        y = np.exp(-np.abs(lag/DECAY_TIMESCALE))
        return y**self.sharpen * self.A

    def print(self):
        print(dict(A=self.A, alpha=self.alpha, beta=self.beta))


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
claims = dict(dolphin=Claim(), moderate_whale=Claim(),
              huge_whale=Claim(), minnow=Claim(), huge_whale_botted=Claim())
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
#    if height == 700:
#        for name in claims:
#            claims[name].lbc[-1] = claims[name].lbc[0]
#            claims[name].kernels = claims[name].kernels[0:1]

    for name in claims:
        trending[name].append([height, claims[name].sum_kernels(height)])

for name in claims:
    trend = np.array(trending[name])
    plt.plot(trend[:,0], trend[:,1], "-", label=name)
plt.ylim(bottom=0.0)
plt.xlim([heights[0]-1, heights[-1]+1])
plt.legend()
plt.show()


