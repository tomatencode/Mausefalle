from math import *

u = 1 #[-] Übersetzung des getriebes
rr = 1 #[m] radius des antriebsreifen
rh = 1 #[m] länge des hebels

def Fr(v):
    """
    Reibungswidersandkraft des Autos in ahängigkeit zur geschwindigkeit in [N]
    """
    return v/5 #Schätzwert

def Ff(phi):
    """
    Federkraft in abhängigkeit zum Winkel in [N]
    """
    return 2.5 #Schätzwert

def find_phi(x,rr,u):
    """
    findet den winkel der mausefalle in abhängigkeit zur zurückgelegten strecke in [°]
    """
    umfang = 2*pi*rr
    phi = x/(umfang*u)*360
    return phi

def Fa(rr,rh,u,phi):
    """
    findet den impuls des autos in [N]
    """
    Ma = rh*Ff(phi)
    Me = u*Ma
    Fa = Me/rr
    return Fa


print(find_phi(3.1,0.5,u))