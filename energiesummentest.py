from math import *
from mausefallenauto import find_Fa

def find_E(M,w):
    """
    berechnet die Energie[J] mit Drhemoment[Nm] und umdrehungen[-].
    """

    # errechnet die Energie[J] indem es das Drehmoment[Nm] mit dem winkelbereich[rad].

    # M[Nm] = Drehmoment
    # w[rad] = anzahl der umdrehungen in Radien
    # E[J] = Energie

    e = M * w # e[J] = M[Nm] * w[rad]

    return e #[J]

print(find_E(2,pi))