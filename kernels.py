"""
Experimenting with kernels that ramp up starting immediately
but have different shapes when the LBC values are different.
"""

import matplotlib.pyplot as plt
import numpy as np
from soften import soften

DELAY_POWER = 0.4


## IDEA: One kernel that takes into account all recent supports/changes.
## When a block happens with no LBC change, just evaluate the kernel at a different
## time point. When an LBC change occurs, recompute the kernel.

class Kernel:
    """
    Sèrsic Kernels
    """
    def __init__(self, t0, old_lbc, new_lbc):
        self.t0, self.old_lbc, self.new_lbc = t0, old_lbc, new_lbc

        # Five Sèrsic parametrs
        self.A = soften(new_lbc) - soften(old_lbc)
        self.t_peak = new_lbc**DELAY_POWER
        self.rc = 0.0
        if new_lbc < 100.0:
#            log10_L = np.log10(200.0)
            self.n = 0.5
        else:
#            log10_L = np.log10(200.0) - np.log10(new_lbc/100.0)
            self.n = 0.5 + np.log10(new_lbc/100.0)
        print(self.n)
        self.L = 200.0 #10.0**log10_L

    def evaluate(self, t):
        lag = t - self.t0
#        if np.abs(lag) >= 5.0*self.L:
#            return 0.0
#        else:
        rsq = (t - self.t_peak)**2 + self.rc**2
        return self.A*np.exp(-(rsq/self.L**2)**(0.5/self.n))


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


