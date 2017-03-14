"""
Integration methods
-------------------
An integration method is a function f defined as follows:
f: (body, dt) --> (new_vel, new_pos)
"""

import numpy as np
import matplotlib.pyplot as plt


class IntegrationMethod:

    def system_method(system, dt):
        raise NotImplementedError


class Euler(IntegrationMethod):

    def raw_method(at, vt, xt, dt):
        return vt + at * dt, xt + vt * dt

    def body_method(body, dt):
        at = body.forces * body.inv_mass
        xt = body.pos
        vt = body.vel
        return vt + at * dt, xt + vt * dt

    def system_method(system, dt):
        system.integrate(dt, Euler.body_method)


class Verlet(IntegrationMethod):

    def body_method_pos(body, dt):
        xt = body.pos
        vt = body.vel
        at = body.forces * body.inv_mass
        return vt, xt + vt * dt + 1 / 2 * at * dt**2

    def body_method_vel(body, dt):
        vt = body.vel
        at = body.prev_forces * body.inv_mass
        atpdt = body.forces * body.inv_mass
        return vt + (at + atpdt) / 2 * dt, body.pos

    def system_method(system, dt):
        system.integrate(dt, Verlet.body_method_pos)
        system.new_state()
        system.apply_gravity()
        system.integrate(dt, Verlet.body_method_vel)


def get(method_str):
    methods = {
        'euler': Euler,
        'verlet': Verlet,
    }
    if method_str.lower() in methods:
        return methods[method_str]
    else:
        raise ValueError('Unknown integration method: ' + method_str)


def spring_test_euler():
    # test with a spring: F = -kx
    # parameters
    x0, v0 = 0, 1
    k = 10
    m = .1
    w = np.sqrt(k / m)
    dt = .01
    t = np.arange(0, 10, dt)
    # compute exact solution
    x_exact = v0 / w * np.sin(w * t)
    # compute numerical solution
    x, v = [x0], [v0]
    for tt in t[1:]:
        at = -k / m * x[-1]
        vtpdt, xtpdt = v[-1] + at * dt, x[-1] + v[-1] * dt
        x.append(xtpdt)
        v.append(vtpdt)
    assert len(t) == len(x), "{}t != {}x".format(len(t), len(x))
    # plot
    plt.figure()
    plt.title(r'Mobile on spring: $k={}$, $m={}$, $x_0$={}, $v_0$={}'
              .format(k, m, x0, v0))
    plt.plot(t, x)
    plt.plot(t, x_exact)
    plt.legend([
        'Euler integration',
        'exact solution'])
    plt.show()


def spring_test_verlet():
    # test with a spring: F = -kx
    # parameters
    x0, v0 = 0, 1
    k = 10
    m = .1
    w = np.sqrt(k / m)
    dt = .01
    t = np.arange(0, 10, dt)
    # compute exact solution
    x_exact = v0 / w * np.sin(w * t)
    # compute numerical solution
    x, v = [x0], [v0]
    for tt in t[1:]:
        xt = x[-1]
        vt = v[-1]
        at = -k / m * x[-1]
        xtpdt = xt + vt * dt + 1 / 2 * at * dt**2
        x.append(xtpdt)
        atpdt = -k / m * x[-1]
        vtpdt = vt + (at + atpdt) / 2 * dt
        v.append(vtpdt)
    assert len(t) == len(x), "{}t != {}x".format(len(t), len(x))
    # plot
    plt.figure()
    plt.title(r'Mobile on spring: $k={}$, $m={}$, $x_0$={}, $v_0$={}'
              .format(k, m, x0, v0))
    plt.plot(t, x)
    plt.plot(t, x_exact)
    plt.legend([
        'Verlet integration',
        'exact solution'])
    plt.show()


if __name__ == '__main__':
    spring_test_euler()
