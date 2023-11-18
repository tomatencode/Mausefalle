from math import *

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
    return v/5 #Schätzwert

def Ff(phi):
    """
    Federkraft in abhängigkeit zum Winkel in [N]
    """
    if phi < 180:
        return 2.5 #Schätzwert
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

def update(x,v,m,rr,rh,u,dt):
    phi = find_phi(x,rr,u)
    Fa = find_Fa(rr,rh,u,phi)
    dI_dt = Fa-Fr(v)
    v = dI_dt/m
    x += v*dt
    return x, v

while find_phi(x,rr,u) < 180 or v < 0.1:
    x_new,v_new = update(x,v,m,rr,rh,u,1/120)
    x = x_new
    v = v_new

print(x)