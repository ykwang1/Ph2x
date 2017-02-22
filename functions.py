import matplotlib.pyplot as plt
import numpy as np
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

def plot_method(tf, t0, h, method, cycles, name):
    plt.figure()
    t = np.arange(t0, tf, h)
    v = np.zeros(len(t))
    x = np.ones(len(t))
    for i in range(1, len(t)):      #using "method" method to find x, v
        x[i], v[i] = method(x[i-1], v[i-1], h)
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
    plt.savefig(name)

def plot_phase(tf, t0, h, method, cycles, name):
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
    cyc_idx = np.linspace(0, len(t)-1, cycles).astype(int)
    plt.scatter(x[cyc_idx], v[cyc_idx], label='point after each cycle')
    plt.axis('equal')
    plt.legend()
    plt.savefig(name)

