from math import *

def find_Emf(Ma,w = 0.5):
    """
    berechnet wie viel Energie in der mausefalle gespeichert ist in [J].
    """

    # errechnet die Energie[J] indem es das Drehmoment[Nm] mit dem winkelbereich[rad] der mausefalle multiplizirt.

    # Ma[Nm] = Drehmoment der mausefalle
    # w[-] = anzahl der umdrehungen der mausefalle
    # w_rad[rad] = anzahl der umdrehungen der mausefalle
    # Emf[J] = Energie der mausefalle 

    w_rad = 2*pi*w
    Emf = Ma * w_rad

    return Emf

print(find_Emf(2))