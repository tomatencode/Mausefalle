from math import *
import numpy as np
import matplotlib.pyplot as plt
import scipy

u = 10 #[-] Übersetzung des getriebes
rr = 1 #[m] radius des antriebsreifen
rh = 1 #[m] länge des hebels

v = 0 #[m/s] startgeschwindigkeit des autos
m = 0.1 #[kg] masse des autos
x = 0 #[m] startposition des autos

def Fr(v):
    """
    Reibungswidersandkraft des Autos in ahängigkeit zur geschwindigkeit in [N]
    """
    return (v/20) #Schätzwert

def Ff(phi):
    """
    Federkraft in abhängigkeit zum Winkel in [N]
    """

    if phi < 180:
        return 0.2
    else:
        return 0

def find_phi(x,rr,u):
    """
    findet den winkel der mausefalle in abhängigkeit zur zurückgelegten strecke in [°]
    """
    umfang = 2*pi*rr
    phi = x/(umfang*u)*360
    return phi

def find_Fa(rr,rh,u,phi):
    """
    findet den impuls des autos in [N]
    """
    Ma = rh*Ff(phi)
    Me = u*Ma
    Fa = Me/rr
    return Fa

def f(t, y):
    [p,x] = y
    v = p/m
    
    return [ find_Fa(rr,rh,u,find_phi(x,rr,u)) - Fr(v), v]

sulution = scipy.integrate.solve_ivp(f, [0, 10], [0,0], dense_output=True)

t = np.linspace(0, 10, 300)

plt.plot(t, sulution.sol(t)[1].T)


plt.xlabel('t')

plt.legend(['t', 'p'], shadow=True)

plt.title('test')

plt.show()