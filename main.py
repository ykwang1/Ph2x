#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pdb

from functions import *

cycles = 10
tf =cycles * 2*np.pi
t0 = 0
h = .05

#Part 1
plot_method(tf, t0, h, Implicit, cycles, 'impl.png')
plot_method(tf, t0, h, Explicit, cycles, 'expl.png')


h0 = .125
h_list = h0 * 2.**np.arange(0., -8., -.25)
imp, exp = np.ones((2, len(h_list)))
n = 20

#Find and plot truncation errors
plt.figure()
for i, h in enumerate(h_list):
    imp[i] = find_trunc(h, Implicit, n)[0]
    exp[i] = find_trunc(h, Explicit, n)[0]
plt.semilogx(h_list, imp, basex=2, label='Implicit')
plt.semilogx(h_list, exp, basex=2, label='Explicit')
plt.semilogx(h_list, h_list, basex=2, label='h')
plt.scatter(h_list, imp)
plt.scatter(h_list, exp)
plt.gca().invert_xaxis()
plt.legend()
plt.xlabel('h')
plt.ylabel('Max Error over 4 cycles')
plt.title('h v. Truncation Error')
plt.savefig('t_err.png')

#Part 2

plot_phase(tf, t0, .01, Implicit, cycles, 'ph_i.png')
plot_phase(tf, t0, .01, Explicit, cycles, 'ph_e.png')
plot_phase(tf, t0, .1, Symplectic, cycles, 'ph_s.png')

plot_method(tf, t0, h, Symplectic, cycles, 'sympl.png')

#Plot phase lag after ~100 cycles
h = .1
cycles = 110
tf =cycles * 2*np.pi
plt.figure()
t = np.arange(t0, tf, h)
v = np.zeros(len(t))
x = np.ones(len(t))
for i in range(1, len(t)):
    x[i], v[i] = Symplectic(x[i-1], v[i-1], h)
plt.plot(t[int(-.1*len(t)):]/(2*np.pi), x[int(-.1*len(t)):], label='Symplectic Euler method')
plt.plot(t[int(-.1*len(t)):]/(2*np.pi), np.cos(t)[int(-.1*len(t)):], label = 'True solution')
plt.legend()
plt.xlabel('Cycles')
plt.ylabel('x')
plt.title('Phase lag between true and integrated solutions after 100 cycles')
plt.savefig('lag.png')
