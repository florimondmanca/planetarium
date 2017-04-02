import numpy as np
from .settings import STATE_DTYPE
from scipy.spatial.distance import pdist, squareform

N_BODIES = 10


def newemptystate(n):
    """
    Parameters
    ----------
    n : int
        number of bodies

    Returns
    -------
    state : ndarray
        state[0] contains n positions
        state[1] contains n velocities
        state[2] contains n accelarations
    """
    state = np.zeros((n,), dtype=STATE_DTYPE)
    return state


def newstate(pos, vel, acc, mass):
    state = newemptystate(len(pos))
    state['pos'] = pos
    state['vel'] = vel
    state['acc'] = acc
    state['mass'] = mass
    return state


def gravity(state):
    g = 39
    p = state['pos']
    # serparation matrix
    # sep[i] contains pj - pi for all other particles j
    sep = p[np.newaxis, :] - p[:, np.newaxis]
    d3 = squareform(pdist(p))**3
    np.fill_diagonal(d3, 1)  # not to divide by zero
    mjr3 = np.einsum('ijk, ij->ik', sep, state['mass'] / d3)
    grav_acc = -g * mjr3
    return grav_acc


def update(state, dt):
    nbodies = len(state)
    # compute gravity at t
    at = state['acc']
    at += gravity(state)
    # integrate
    # step 1 : compute new positions
    xt, vt = state['pos'], state['vel']
    xtpdt = xt + vt * dt + .5 * at * dt**2
    # step 2 : create temporary new state with new position
    # then compute new accelarations
    # and compute new velocities
    statetpdt = newstate(xtpdt, vt, np.zeros((nbodies, 2)), state['mass'])
    atpdt = gravity(statetpdt)
    vtpdt = vt + (at + atpdt) / 2 * dt
    # final new state
    state = newstate(xtpdt, vtpdt, atpdt, state['mass'])
    return state


def generatesim(first_state, steps):
    dt = .01
    state = first_state
    for _ in range(steps):
        state = update(state, dt)
        yield state


if __name__ == '__main__':
    n = 10
    first = newemptystate(n)
    first['pos'] = np.random.random((n, 2))
    first['mass'] = np.random.random(n)
    for s in generatesim(first, 20):
        for p in range(1):
            print('Particle {}:'.format(p), s[p]['pos'])
