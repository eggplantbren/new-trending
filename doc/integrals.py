import matplotlib.pyplot as plt
import numpy as np
#from sympy import *

## Kernel parameters
#t0, A, delta, ell, alpha = symbols("t0 A delta ell alpha")

## Derived kernel parameters
#t1 = t0 + delta
#t2 = t1 + ell

## Kernel function
#t = symbols("t")
#K = Piecewise((0, t < t0),
#              (A*((t - t0)/delta)**alpha, t < t1),
#              (A*((t2 - t)/ell)**alpha, t < t2),
#              (0, True))


## Assumptions
#from sympy.assumptions.assume import global_assumptions
#global_assumptions.clear()

## Entropy
#facts = Q.positive(A), Q.positive(delta), Q.positive(ell), Q.positive(alpha)
#with assuming(*facts):
#    H = integrate(K, (t, t0, t2))
#    print(H)

#ts = np.linspace(0.0, 1000.0, 10001)
#ys = np.empty(len(ts))
#for i in range(len(ts)):
#    e = K.evalf(subs=dict(t=ts[i], t0=20.0, A=5.0, delta=100.0, ell=500.0,
#                                   alpha=2.0))
#    ys[i] = e
#    print(ts[i], ys[i])
#plt.plot(ts, ys)
#plt.show()

import numpy as np
import matplotlib.pyplot as plt

def evaluate(ts, kernel):
    t0, A, delta, ell, alpha = kernel
    t1 = t0 + delta
    ys = np.zeros(len(ts))
    rise = (ts >= t0) & (ts < t1)
    fall = (ts >= t1)
    ys[rise] = A*np.exp(2.0*(ts[rise] - t1)/delta)
    ys[fall] = A*np.exp((t1 - ts[fall])/ell)
    return ys

kernel = [40.0, 3.2, 30.0, 500.0, 2.5]
t0, A, delta, ell, alpha = kernel

ts = np.linspace(0, 1000.0, 100001)
ys = evaluate(ts, kernel)
#print(np.trapz(ys, x=ts), A*(delta + ell)/alpha)

plt.plot(ts, ys)
plt.show()


