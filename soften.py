import math

def soften(lbc):
    """
    Nonlinear softening function.
    """
    return lbc**0.25 #math.log10(lbc + 1.0)

#    if lbc < 100.0:
#        return 0.01*lbc**1.0
#    elif lbc < 1000.0:
#        return 0.1*lbc**0.5
#    elif lbc < 10000.0:
#        return lbc**0.25


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    x = 10.0**np.linspace(-3.0, 6.0, 100001)
    y = np.array([soften(_x) for _x in x])
    plt.semilogx(x, x**0.25, label="Fourth Root")
    plt.semilogx(x, y, label="This")
    plt.legend()
    plt.show()

