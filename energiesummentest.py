from math import *
import scipy
from main import solve_ivp, find_Ff_nolim,m,max_sim_length

tolleranz = 0.05 # erlaubte abweichung des energie erhaltungs Satzes

def find_Ff_solve(phi,F):
    """
    differenzialgleichung mit der die kraft der mausefalle berechnet wird
    """

    return [find_Ff_nolim(phi)]

def find_Wmf(phi):
    """
    berechnet die Spannarbeit der Mausefalle in [J]
    """

    # errechnet die Arbeit[J] indem es das Integral der Kraft der Feder [Nm] abhängig zum winkelbereich[rad] löst.

    # phi[rad] = winkel in dem die Feder Arbeit verrichtet in Radien
    # Wmf[J] = verrichtete Spannarbeit der Feder

    Ff_solution = scipy.integrate.solve_ivp(find_Ff_solve, [0, phi], [0],  method = "Radau")
    
    x_size = Ff_solution.y[0].size    
    max_x = Ff_solution.y[0][x_size-1]

    Wmf = max_x

    return Wmf #[J]

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

def test(do_print):
    solution,max_x = solve_ivp(max_sim_length,False)
    ve = solution.sol(max_sim_length)[0]
    va = solution.sol(0)[0]

    Wmf = find_Wmf(pi)
    Wacc = find_Wacc(m,ve,va)
    abweichung = abs(Wmf - Wacc)

    print("Emf = "+str(Wmf) + " J und Eacc = " + str(Wacc)+ " J")

    if do_print:
        if abweichung < tolleranz:
            print("kein bug! abweichung: " + str(abweichung) + " J")
        else:
            print("abweichung über tolleranz! abweichung: " + str(abweichung) + " J")
    return abweichung

#test(True)