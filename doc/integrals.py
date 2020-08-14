import numpy as np
import matplotlib.pyplot as plt

def evaluate(ts, kernel):
    t0, A, delta, ell, alpha = kernel
    t1 = t0 + delta
    t2 = t1 + ell
    ys = np.zeros(len(ts))
    rise = (ts >= t0) & (ts < t1)
    fall = (ts >= t1) & (ts < t2)
    ys[rise] = A*((ts[rise] - t0)/delta)**alpha
    ys[fall] = A*((t2 - ts[fall])/ell)**alpha
    return ys

kernel = [40.0, 3.2, 30.0, 500.0, 2.0]
t0, A, delta, ell, alpha = kernel

ts = np.linspace(0, 1000.0, 100001)
ys = evaluate(ts, kernel)

plt.plot(ts, ys)
plt.show()

