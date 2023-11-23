from math import *
from mausefallenauto import solve_ivp,m,max_sim_length

tolleranz = 0.05 # erlaubte abweichung des energie erhaltungs Satzes

def find_Wmf(M,w):
    """
    berechnet die Spannarbeit der Mausefalle in [J]
    """

    # errechnet die Arbeit[J] indem es das Drehmoment[Nm] mit dem winkelbereich[rad].

    # M[Nm] = Drehmoment
    # w[rad] = anzahl der umdrehungen in Radien
    # Wmf[J] = verrichtete Spannarbeit der Feder

    e = M * w # e[J] = M[Nm] * w[rad]

    return e #[J]

def find_Wacc(m,ve,va):
    """
    berechnet die beschleunigungsarbei des autos(ohne reibung) in [J].
    """
    # benutzt die formel W = 1/2mve² - 1/2mva² um die beschleunigungsarbei zu berechnen

    # m[kg] = masse des autos
    # va[m/s] = anfangsgeschwindigkeit des autos
    # ve[m/s] = endgeschwindigkeit des autos
    # Wacc[J] = die verrichtete Beschleunigungsarbeit des autos

    Wacc = (1/2) * m * ve**2 - (1/2) * m * va**2 # Wacc[J] = 1/2m[kg]ve[m/s]² - 1/2m[kg]va[m/s]²

    return Wacc #[J]

sulution = solve_ivp(max_sim_length,False)
ve = sulution.sol(max_sim_length)[0]
va = sulution.sol(0)[0]

Wmf = find_Wmf(2,pi)
Wacc = find_Wacc(m,ve,va)
abweichung = abs(Wmf - Wacc)

print("Emf = "+str(Wmf) + " J und Eacc = " + str(Wacc)+ " J")

if abweichung < tolleranz:
    print("kein bug! abweichung: " + str(abweichung) + " J")
else:
    print("abweichung über tolleranz! abweichung: " + str(abweichung) + " J")