#interpolação f(psi)em x, y, psi

#interpolação g(psi) em z

import math

t_b = t_e = t = T = 1

psi = t/T
psi_b = t_b/T
psi_e = t_e/T

if psi <= psi_b:
    f = 0
elif psi > psi_b and psi <= psi_e:
    f = 0.5*(1 - math.cos(math.pi * (psi - psi_b) / (psi_e - psi_b)))
else:
    f = 1


if psi <= psi_b or psi > psi_e:
    g = 0
else:   
    g = 0.5 * (1 - math.cos(2 * math.pi * (psi - psi_b) / (psi_e - psi_b)))

