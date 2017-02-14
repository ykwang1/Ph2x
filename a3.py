#! usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import pdb 


#Returns the next iteration given the previous one  
def Explicit(x, v, h):
    return x + h*v, v - h*x

def Implicit(x, v, h):
    return 1/(h**2 + 1) * (x + h*v), 1/(h**2 + 1) * (v - h*x)

def Symplectic(x, v, h):
    return  x + h*v,  1/(h**2 + 1) * (v - h*x)

def find(times, h):     #Analytic solutions
    x = np.cos(times)
    v = -np.sin(times)
    return x, v

def find_trunc(h, method, n):
    v = np.zeros(int(n/h))
    x = np.ones(int(n/h))
    for i in range(1, int(n / h)):
        x[i], v[i] = method(x[i-1], v[i-1], h)
    t= np.linspace(0, n, int(n/h))
    x_true, v_true = find(t, h)
    return np.max(np.abs(x_true - x)), np.max(np.abs(v_true - v))

def plot_method(tf, t0, h, method, cycles):
    plt.figure()
    t = np.arange(t0, tf, h)
    v = np.zeros(len(t))
    x = np.ones(len(t))
    for i in range(1, len(t)):      #using "method" method to find x, v
        x[i], v[i] = method(x[i-1], v[i-1], h)
        if i%100 == 0:
            print "iteration ", i
    x_ax = np.linspace(0, cycles, len(t))
    plt.subplot(311)
    plt.title('Solution by '+ method.__name__ + ' Euler Method')
    plt.plot(x_ax, x, label="x")
    plt.plot(x_ax, v, label="v")
    plt.xlabel('Number of cycles')
    plt.ylabel('Position/Velocity')
    plt.legend()
    plt.subplot(312)
    plt.title('Error')
    x_true, v_true = find(t, h)
    plt.plot(x_ax, x-x_true)
    plt.plot(x_ax, v-v_true)
    plt.xlabel('Number of cycles')
    plt.ylabel('Error')
    plt.subplot(313)
    plt.title('Evolution of Energy')
    plt.plot(x_ax, x**2 + v**2)
    plt.xlabel('Number of cycles')
    plt.ylabel(r'$x^2 + v^2$')
    plt.show()

def plot_phase(tf, t0, h, method, cycles):
    plt.figure()
    t = np.arange(t0, tf, h)
    v = np.zeros(len(t))
    x = np.ones(len(t))
    for i in range(1, len(t)):
        x[i], v[i] = method(x[i-1], v[i-1], h)
    plt.plot(x, v)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Phase space trajectory of system using '+ method.__name__ + ' Euler Method')
    plt.scatter(1, 0, label='start')
    pdb.set_trace()
    cyc_idx = np.linspace(0, len(t)-1, cycles).astype(int)
    plt.scatter(x[cyc_idx], v[cyc_idx], label='point after each cycle')
    plt.axis('equal')
    plt.legend()
    plt.show()

cycles = 10
tf =cycles * 2*np.pi 
t0 = 0
h = .05

#Part 1
plot_method(tf, t0, h, Implicit, cycles)
plot_method(tf, t0, h, Explicit, cycles)


h0 = .125
h_list = h0 * 2.**np.arange(0., -8., -.25)
imp, exp = np.ones((2, len(h_list)))
n = 20

#Find and plot truncation errors
plt.figure()
for i, h in enumerate(h_list):
    pass
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
plt.show()

#Part 2

plot_phase(tf, t0, .01, Implicit, cycles)
plot_phase(tf, t0, .01, Explicit, cycles)
plot_phase(tf, t0, .1, Symplectic, cycles)

plot_method(tf, t0, h, Symplectic, cycles)

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
plt.plot(t[-.1*len(t):]/(2*np.pi), x[-.1*len(t):], label='Symplectic Euler method')
plt.plot(t[-.1*len(t):]/(2*np.pi), np.cos(t)[-.1*len(t):], label = 'True solution')
plt.legend()
plt.xlabel('Cycles')
plt.ylabel('x')
plt.title('Phase lag between true and integrated solutions after 100 cycles')
plt.show()
