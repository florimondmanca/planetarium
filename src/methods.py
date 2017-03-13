"""
Integration methods
-------------------
An integration method is a function f defined as follows:
f: (body, dt) --> (new_vel, new_pos)
"""

import numpy as np
import matplotlib.pyplot as plt


def euler_raw(at, vt, xt, dt):
    vtpdt = vt + at * dt
    xtpdt = xt + vt * dt
    return vtpdt, xtpdt


def body_euler(body, dt):
    at = body.forces * body.inv_mass
    xt = body.pos
    vt = body.vel
    return euler_raw(at, vt, xt, dt)


def euler(system, dt):
    system.integrate(dt, body_method=body_euler)


def body_verlet_pos(body, dt):
    xt = body.pos
    vt = body.vel
    at = body.forces * body.inv_mass
    return vt, xt + vt * dt + 1 / 2 * at * dt**2


def body_verlet_vel(body, dt):
    vt = body.vel
    at = body.prev_forces * body.inv_mass
    atpdt = body.forces * body.inv_mass
    return vt + (at + atpdt) / 2 * dt, body.pos


def verlet(system, dt):
    system.integrate(dt, body_method=body_verlet_pos)
    system.new_state()
    system.integrate(dt, body_method=body_verlet_vel)


def spring_test(method=euler_raw):
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
    spring_test(method=euler_raw)
