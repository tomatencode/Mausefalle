from math import *
import numpy as np
import matplotlib.pyplot as plt
import scipy

ü = 1 #[-] Übersetzung des getriebes
rr = 0.1 #[m] radius des antriebsreifen
rh = 0.1 #[m] länge des hebels
m = 0.1 #[kg] masse des autos

max_lenght = 30 #[s] maximum simulation length

def Fr(v):
    """
    Reibungswidersandkraft des Autos in ahängigkeit zur geschwindigkeit in [N] (Benutzerdefinirt)
    """
    return v / 20 # Wiederstand in [N] (Schätzwert)



def Ff(phi):
    """
    Federkraft in abhängigkeit zu den umdrehungen in [N] (Benutzerdefinirt)
    """

    # wenn die mausefalle noch nicht zu ist (phi < 0.5) gibt die falle eine konstante kraft zurück.
    # sonst hat die falle zugeschnappt und ist nicht mehr mit der achse verbunden.

    # phi[-] = anzahl der bisherigen umdrehungen

    if phi < 0.5:
        return 2 # Kraft der Feder in [N] (Schätzwert)
    else:
        return 0 # Kraft der Feder in [N]

def find_phi(x,rr,ü):
    """
    findet die anzahl der umdrehungen der mausefalle in abhängigkeit zur zurückgelegten strecke in [-],
    """

    # teilt die zurückgelekte stricke durch die bisherigen umdrehungen mal das übersetzungsverhältnis.

    # x[m] = zurückgelegte strecke
    # ü[-] = überstetzungsverhältnis von Mausefalle zu Achse
    # ur[m] = umfang des rades 
    # rr[m] = radius des rades
    # phi[-] = anzahl der bisherigen umdrehungen

    ur = 2 * pi * rr # ur[m] = 2pi[-] * rr[m]
    phi = x / ( ur * ü ) # phi[-] = x[m] / (ur[m] * u[-])

    return phi

def find_Fa(rr,rh,ü,phi):
    """
    findet die Kraft des Rades in [N]
    """

    # findet das Drehmoment der Mausefalle Ma
    # benutzt das übersetztungsverhältnis um Ma in das Drehmoment der Achse Me zu überrsetzten.
    # wandelt das drehmoment der Achse in Die kraft des Rades Fa um.

    # Fa[N] = Kraft des Rades
    # Ma[Nm] = Drehmoment der Mausefalle
    # Me[Nm] = Drehmoment der Achse
    # rh[M] = länge des hebels der Mausefalle
    # rr[M] = Radius des Rades
    # ü[-] = überstetzungsverhältnis von Mausefalle zu Achse

    Ma = rh * Ff(phi) # Ma[Nm] = rh[m] * Ff(phi[-])[N]
    Me = ü * Ma # Me[Nm] = ü[-] * Ma[Nm]
    Fa = Me / rr # Fa[N] = Me[Nm] / rr[m]

    return Fa # [Nm]


def find_simulation_lenght(max_lenght,sulution,rr,ü,v_min):
    """
    findet passende simulationslänge in [s]
    """

    # testet für jede sekunde ob das auto langsamer als v_min (v < v_min) ist und ob die Mausefalle zu (phi < 0.5) ist.

    # max_lenght[s] = maximale simulationslänge
    # v_min[m/s] = Geschwindigkeit ab der die simulation abgebrochen wird
    # x[m] = zurückgelegte strecke
    # v[m/s] = aktuelle geschwindigkeit
    # phi[-] = anzahl der bisherigen umdrehungen

    for s in range(0,max_lenght):
        x = sulution.sol(s)[1]
        v = sulution.sol(s)[0]
        phi = find_phi(x,rr,ü)
        if phi > 0.5 and v < v_min:
            return s
    
    return max_lenght


def f(t, y):
    """
    Differenzialgleichung die von scipy gelöst wird
    """

    # v[m/s] = aktuelle geschwindigkeit
    # x[m] = zurückgelegte strecke
    # t[s] = zeit

    [v,x] = y 
    
    return [ (find_Fa(rr,rh,ü,find_phi(x,rr,ü)) - Fr(v))/m, v]

# löst Differenzialgleichung
sulution = scipy.integrate.solve_ivp(f, [0, max_lenght], [0,0], dense_output=True)

s = find_simulation_lenght(max_lenght,sulution,rr,ü,0.1)

t = np.linspace(0, s, 300)

plt.plot(t, sulution.sol(t)[0].T)
plt.plot(t, sulution.sol(t)[1].T)

plt.xlabel('t')
plt.legend(['speed', 'position'], shadow=True)
plt.title('test')

plt.show()