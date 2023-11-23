import matplotlib.pyplot as plt
import numpy as np
from main import solve_ivp, find_simulation_length,find_phi,Fr,rr,u,max_sim_length,m,friction


sulution = solve_ivp(max_sim_length,friction) # lösung der differenzialgleichung [-]      # papa: sulution -> solution

s = find_simulation_length(max_sim_length,sulution,rr,u,0.1) # passende länge der simulation [s]    # lenght -> length, bitte Rechtschreibprüfung "Code Spell Checker" verwenden, dann kriegst Du Rechtschreibfehler angezeigt

t = np.linspace(0, s, 300) # vektor von 300 zeitpunkten von 0 bis s [s]

plt.plot(t, sulution.sol(t)[0].T,label='Speed[m/s]',color="green")   # papa: sehr schöner plot :-)
plt.plot(t, sulution.sol(t)[1].T,label='position[m]',color=(1,0.55,0))
plt.plot(t, find_phi(sulution.sol(t)[1],rr,u).T,label='Winkel Mausefalle[rad]',color=(0.58,0,0.82))
if friction == True:
    plt.plot(t, (Fr(sulution.sol(t)[0])/m).T,label='Reibung[m/s²]',color="red")

plt.xlabel('t')
plt.legend()
plt.title('Auto')

plt.show()