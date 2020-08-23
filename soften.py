import math

def soften(lbc):
    """
    Nonlinear softening function.
    """
    if lbc < 1E2:
        return (lbc/1E2)           # Maxes out at 1
    elif lbc < 1E3:
        return (lbc/1E2)**0.5      # Maxes out at 10^(1/2)
    elif lbc < 1E4:
        return 3.1622776601683795*(lbc/1E3)**0.33333333  # Maxes out at 10^(5/6)
    elif lbc < 1E5:
        return 6.812920690579613*(lbc/1E4)**0.25   # Maxes out at 10^(13/12)
    elif lbc < 1E6:
        return 12.115276586285882*(lbc/1E5)**0.2   # Maxes out at 10^(77/60)
    else:
        return 19.20141938638802*(lbc/1E6)**0.16666667


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    x = 10.0**np.linspace(-3.0, 6.0, 100001)
    y = np.array([soften(_x) for _x in x])
    plt.semilogx(x, x**0.25, label="Fourth Root")
    plt.semilogx(x, y, label="This")
    plt.legend()
    plt.show()

