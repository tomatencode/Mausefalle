from math import *
import numpy as np
import matplotlib.pyplot as plt
import scipy

u = 1 #[-] Übersetzung des getriebes
rr = 0.1 #[m] radius des antriebsreifen
rh = 0.1 #[m] länge des hebels
m = 0.1 #[kg] masse des autos

max_lenght = 30 #[s] maximum simulation length

def Fr(v):
    """
    Reibungswidersandkraft des Autos in ahängigkeit zur geschwindigkeit in [N]
    """
    return (v/20) #Schätzwert



def Ff(phi):
    """
    Federkraft in abhängigkeit zum Winkel in [N]
    """

    if phi < 0.5:
        return 2.5
    else:
        return 0

def find_phi(x,rr,u):
    """
    findet den winkel der mausefalle in abhängigkeit zur zurückgelegten strecke in [°]
    """
    umfang = 2*pi*rr
    phi = x/(umfang*u)

    return phi

def find_Fa(rr,rh,u,phi):
    """
    findet den impuls des autos in [N]
    """
    Ma = rh*Ff(phi)
    Me = u*Ma
    Fa = Me/rr

    return Fa

def find_simulation_lenght(max_lenght,sulution,rr,u,m):
    for i in range(0,max_lenght):
        x = sulution.sol(i)[1]
        v = sulution.sol(i)[0]
        print(x)
        print(find_phi(x,rr,u))
        if find_phi(x,rr,u) > 0.5 and v/m < 0.1:
            return x
    return max_lenght


def f(t, y):
    [v,x] = y
    
    return [ (find_Fa(rr,rh,u,find_phi(x,rr,u)) - Fr(v))/m, v]

sulution = scipy.integrate.solve_ivp(f, [0, max_lenght], [0,0], dense_output=True)

s = find_simulation_lenght(max_lenght,sulution,rr,u,m)



t = np.linspace(0, s, 300)

plt.plot(t, sulution.sol(t)[0].T)
plt.plot(t, sulution.sol(t)[1].T)

plt.xlabel('t')

plt.legend(['speed', 'position'], shadow=True)

plt.title('test')

plt.show()