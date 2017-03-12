"""
Integration methods
"""

import numpy as np
import matplotlib.pyplot as plt


def euler(at, vt, xt, dt):
    vtpdt = vt + at * dt
    xtpdt = xt + vt * dt
    return vtpdt, xtpdt


def verlet(at, vt, xt, dt):
    pass


def spring_test(method=euler):
    # test with a spring: F = -kx
    # parameters
    x0, v0 = 0, 1
    k = 10
    m = .1
    w = np.sqrt(k / m)
    dt = .001
    t = np.arange(0, 5, dt)
    # compute exact solution
    x_exact = v0 / w * np.sin(w * t)
    # compute numerical solution
    x, v = [x0], [v0]
    for tt in t[1:]:
        at = -k / m * x[-1]
        vt, xt = method(at, v[-1], x[-1], dt)
        x.append(xt)
        v.append(vt)
    assert len(t) == len(x), "{}t != {}x".format(len(t), len(x))
    # plot
    plt.figure()
    plt.title(r'Mobile on spring: $k={}$, $m={}$, $x_0$={}, $v_0$={}'
              .format(k, m, x0, v0))
    plt.plot(t, x)
    plt.plot(t, x_exact)
    plt.legend([
        '{} integration'.format(method.__name__.capitalize()),
        'exact solution'])
    plt.show()


if __name__ == '__main__':
    spring_test(method=euler)
