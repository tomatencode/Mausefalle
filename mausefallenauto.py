from math import *

u = 1 #Übersetzung des getriebes
rr = 1 #radius des antriebsreifen
rh = 1 #länge des hebels

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

def find_phi(x,rr):
    phi = x/(2*pi*rr)
    return phi

def Fa(rr,rh,u,phi):
    Ma = rh*Ff(phi)
    Me = u*Ma
    Fa = Me/rr
    return Fa

print(find_phi(3.1,0.5))