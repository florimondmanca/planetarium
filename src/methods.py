"""
Integration methods
"""

import numpy as np
import matplotlib.pyplot as plt


def euler(at, vt, xt, dt):
    vtpdt = vt + at * dt
    xtpdt = xt + vt * dt
    return vtpdt, xtpdt


def test_euler():
    # test with a spring force F = -kx
    x0 = 0
    v0 = 1
    k = 100
    dt = .01
    t = np.arange(0, 5, dt)
    x = [x0]
    v = [v0]
    for tt in t[1:]:
        at = -k * x[-1]
        vt, xt = euler(at, v[-1], x[-1], dt)
        x.append(xt)
        v.append(vt)
    assert len(t) == len(x), "{}, {}".format(len(t), len(x))
    plt.figure()
    plt.title(r'Euler integration on a spring with $x_0$={}, $v_0$={}'
              .format(x0, v0))
    plt.plot(t, x)
    plt.show()


if __name__ == '__main__':
    test_euler()
