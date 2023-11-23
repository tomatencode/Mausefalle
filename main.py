from math import *
import scipy

u = 50 #[-] Verhältnis von Drehmoment der Feder zu Drehmoment der Achse
rr = 0.1 #[m] radius des antriebsreifen
m = 0.1 #[kg] masse des autos

friction = True
max_sim_length = 60 #[s] maximum simulation length

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

    if phi < pi:
        return 2 # Kraft der Feder in [Nm] (Schätzwert)
    else:
        return 0 # Kraft der Feder in [Nm]



def find_phi(x,rr,u):
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
    phi = x / ( ur * u ) # phi[-] = x[m] / (ur[m] * u[-])
    phi_rad = 2 * pi * phi # phi_rad[rad] = 2pi[-] * phi[-]

    return phi_rad # [rad]


def find_Fa(rr,ü,phi):
    """
    findet die Kraft des Rades in [N]
    """

    # findet das Drehmoment der Mausefalle Ma.
    # benutzt das übersetztungsverhältnis ü um Ma in das Drehmoment der Achse Me zu überrsetzten.
    # wandelt das drehmoment der Achse in Die kraft des Rades Fa um.

    # Fa[N] = Kraft des Rades
    # Ma[Nm] = Drehmoment der Mausefalle
    # Me[Nm] = Drehmoment der Achse
    # rh[M] = länge des hebels der Mausefalle
    # rr[M] = Radius des Rades
    # ü[-] = überstetzungsverhältnis von Mausefalle zu Achse

    Ma = Ff(phi) # Ma[Nm] = Ff(phi[rad])[Nn]
    Me = Ma / ü # Me[Nm] = Ma / ü[-]
    Fa = Me / rr # Fa[Nm] = Me[Nm] / rr[m]

    return Fa # [N]


def f(t, y):
    """
    Differenzialgleichung die von scipy gelöst wird
    """

    # v[m/s] = aktuelle geschwindigkeit
    # x[m] = zurückgelegte strecke
    # t[s] = zeit

    [v,x] = y 
    
    return [ (find_Fa(rr,u,find_phi(x,rr,u)) - Fr(v))/m, v]

def fnofric(t, y):
    """
    Differenzialgleichung die von scipy gelöst wird ohne reibung
    """

    # v[m/s] = aktuelle geschwindigkeit
    # x[m] = zurückgelegte strecke
    # t[s] = zeit

    [v,x] = y 
    
    return [ find_Fa(rr,u,find_phi(x,rr,u))/m, v]

def solve_ivp(max_sim_length,friction):
    """
    lößt die differenzialgleichung f(t,y) mit scipy
    """

    # max_sim_length[s] = maximale simulationslänge
    if friction == True:
        solution = scipy.integrate.solve_ivp(f, [0, max_sim_length], [0,0], method = "Radau", dense_output=True)
    else:
        solution = scipy.integrate.solve_ivp(fnofric, [0, max_sim_length], [0,0], method = "Radau", dense_output=True)
    return solution


def find_simulation_lenght(max_lenght,sulution,rr,u,v_min):
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
        phi = find_phi(x,rr,u)
        if phi > pi and v < v_min:
            return s
    
    return max_lenght
