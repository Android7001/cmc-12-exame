import math
import numpy as np

t_inicio = 0
t_fim = 1
passo = 0.01
T = 1  
vetor_tempo = np.arange(t_inicio, t_fim, passo)

#a: tamanho da coxa; b: tamanho da canela
a = 1
b = 1

x_l_t2h = 0.2
y_l_t2h = 0.2
z_l_t2h = 0.2

x_l_a2f = 0.05
y_l_a2f = 0.1
z_l_a2f = 0.05

vetor_theta_hp = []
vetor_theta_k = []
vetor_theta_ap = []
vetor_theta_hr = []
vetor_theta_fr = []

for t in vetor_tempo:
    w_l = np.array([[x_l],[y_l],[z_l],[psi_l]])

    w_l_t2h = w_l - np.array([[x_l_t2h],[y_l_t2h],[z_l_t2h], [0]])

    x_l_h2f = w_l_t2h[0, 0]
    y_l_h2f = w_l_t2h[1, 0]


    rotacao = np.array([[math.cos(psi_l), math.sin(psi_l)],
                            [-math.sin(psi_l), math.cos(psi_l)]])

    [[x1_l_h2f],[y1_l_h2f]] = rotacao * [[x_l_h2f],[y_l_h2f]]

    x2_l_h2f = x1_l_h2f - x_l_a2f
    y2_l_h2f = y1_l_h2f - y_l_a2f
    z2_l_h2f = z_l - z_l_a2f

    c = math.sqrt(x2_l_h2f**2 + y2_l_h2f**2 + z2_l_h2f**2)
    h = math.sqrt(y2_l_h2f**2 + z2_l_h2f**2)

    alpha = math.acos((b**2 + c**2 - a**2)/(2*b*c))
    beta = math.acos((a**2 + c**2 - b**2)/(2*a*c))
    gama = math.acos((a**2 + b**2 - c**2)/(2*a*b))

    theta_hp = -(math.atan2(x2_l_h2f, h) + beta)
    theta_k = math.pi - gama
    theta_ap = alpha - math.atan2(h, x2_l_h2f)

    theta_hr = math.atan2(x2_l_h2f, z2_l_h2f)
    theta_fr = -theta_hr

    vetor_theta_hp.append(theta_hp)
    vetor_theta_k.append(theta_k)
    vetor_theta_ap.append(theta_ap)
    vetor_theta_hr.append(theta_hr)
    vetor_theta_fr.append(theta_fr)