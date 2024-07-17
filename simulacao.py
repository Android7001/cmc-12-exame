import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from cm import CM
from foot import Foot

# Definindo os parâmetros da caminhada do robô
Vx = 1
Vy = 0
Vphi = 0
steps = 4
T = 1

# Função para simulação do caminhar do robô
def WalkinRobot():
    cm = CM(T=T)
    pe_esq = Foot(T=T)
    pe_dir = Foot(T=T)

    balanco_esquerda = True if Vy >= 0 else False 

    tempo = np.zeros(1)
    phi = np.zeros(1) 
    pe_esq_x = np.zeros(1)
    pe_esq_y = np.zeros(1)
    pe_esq_z = np.zeros(1)
    pe_esq_psi = np.zeros(1)
    pe_dir_x = np.zeros(1)
    pe_dir_y = np.zeros(1)
    pe_dir_z = np.zeros(1)
    pe_dir_psi = np.zeros(1)
    xcm = np.zeros(1)
    ycm = np.zeros(1)

    pe_esq_pos_inicial = [- Vx*T/2, 0.1, 0.0]  # Posição inicial do pé esquerdo [xi, yi, psi0]
    pe_dir_pos_inicial = [ Vx*T/2, -0.1, 0.0]  # Posição inicial do pé direito [xi, yi, psi0]

    for i in range(steps):
        new_phi = cm.get_delta_Phicm(Vphi, phi[-1] if phi.any() else 0)
        phi = np.concatenate((phi, new_phi if not phi.any() else new_phi[1:])) 

        # Calcular o deslocamento do CM
        x_delta = cm.get_delta_Xcm(Vx, 0)
        y_delta = cm.get_delta_Ycm(Vy, 0, abrindo=balanco_esquerda)

        delta_x = x_delta * math.cos(phi[-1]) - y_delta * math.sin(phi[-1])
        delta_y = x_delta * math.sin(phi[-1]) + y_delta * math.cos(phi[-1])

        xcm = np.concatenate((xcm, delta_x + xcm[-1]))
        ycm = np.concatenate((ycm, delta_y + ycm[-1]))

        if (Vy >= 0 and balanco_esquerda) or (Vy < 0 and not balanco_esquerda):
            # Está abrindo, então o passo é com o pé esquerdo
            pe_esq_x_temp, pe_esq_y_temp, pe_esq_z_temp, pe_esq_psi_temp = pe_esq.get_foot_position([Vx, Vy, Vphi], pe_esq_pos_inicial)
            pe_esq_pos_inicial = [pe_esq_x_temp[-1], pe_esq_y_temp[-1], pe_esq_psi_temp[-1]]  # atualização da posição inicial do pé esquerdo

            pe_esq_delta_x = pe_esq_x_temp * np.cos(pe_esq_psi_temp) - pe_esq_y_temp * np.sin(pe_esq_psi_temp)
            pe_esq_delta_y = pe_esq_x_temp * np.sin(pe_esq_psi_temp) + pe_esq_y_temp * np.cos(pe_esq_psi_temp)

            pe_esq_x = np.concatenate((pe_esq_x, pe_esq_delta_x))
            pe_esq_y = np.concatenate((pe_esq_y, pe_esq_delta_y))
            pe_esq_z = np.concatenate((pe_esq_z, pe_esq_z_temp))
            pe_esq_psi = np.concatenate((pe_esq_psi, pe_esq_psi_temp))

            pe_dir_x = np.concatenate((pe_dir_x, np.full(len(pe_esq_x_temp), pe_dir_pos_inicial[0])))
            pe_dir_y = np.concatenate((pe_dir_y, np.full(len(pe_esq_x_temp), pe_dir_pos_inicial[1])))
            pe_dir_z = np.concatenate((pe_dir_z, np.zeros(len(pe_esq_x_temp))))
            pe_dir_psi = np.concatenate((pe_dir_psi, np.full(len(pe_esq_x_temp), pe_dir_pos_inicial[2])))

            balanco_esquerda = not balanco_esquerda
        else:
            # Está fechando, então o passo é com o pé direito
            pe_dir_x_temp, pe_dir_y_temp, pe_dir_z_temp, pe_dir_psi_temp = pe_dir.get_foot_position([Vx, Vy, Vphi], pe_dir_pos_inicial)
            pe_dir_pos_inicial = [pe_dir_x_temp[-1], pe_dir_y_temp[-1], pe_dir_psi_temp[-1]]  # Atualização da posição inicial do pé direito 

            pe_dir_delta_x = pe_dir_x_temp * np.cos(pe_dir_psi_temp) - pe_dir_y_temp * np.sin(pe_dir_psi_temp)
            pe_dir_delta_y = pe_dir_x_temp * np.sin(pe_dir_psi_temp) + pe_dir_y_temp * np.cos(pe_dir_psi_temp)

            pe_dir_x = np.concatenate((pe_dir_x, pe_dir_delta_x))
            pe_dir_y = np.concatenate((pe_dir_y, pe_dir_delta_y))
            pe_dir_z = np.concatenate((pe_dir_z, pe_dir_z_temp))
            pe_dir_psi = np.concatenate((pe_dir_psi, pe_dir_psi_temp))

            pe_esq_x = np.concatenate((pe_esq_x, np.full(len(pe_dir_x_temp), pe_esq_pos_inicial[0])))
            pe_esq_y = np.concatenate((pe_esq_y, np.full(len(pe_dir_x_temp), pe_esq_pos_inicial[1])))
            pe_esq_z = np.concatenate((pe_esq_z, np.zeros(len(pe_dir_x_temp))))
            pe_esq_psi = np.concatenate((pe_esq_psi, np.full(len(pe_dir_x_temp), pe_esq_pos_inicial[2])))

            balanco_esquerda = not balanco_esquerda

        tempo = np.concatenate((tempo, tempo[-1] + np.linspace(0, T, len(new_phi))))

    return tempo, xcm, ycm, pe_esq_x, pe_esq_y, pe_esq_z, pe_dir_x, pe_dir_y, pe_dir_z

# Função para atualizar a animação
def update(step):
    ax.clear()

    # Plotar o Centro de Massa (CM)
    ax.scatter(xcm[step], ycm[step], 1, c='r', marker='o', label='CM')

    # Plotar os pés
    ax.scatter(pe_esq_x[step], pe_esq_y[step], pe_esq_z[step], c='b', marker='o', label='Pé Esquerdo')
    ax.scatter(pe_dir_x[step], pe_dir_y[step], pe_dir_z[step], c='g', marker='o', label='Pé Direito')

    # Configurar os eixos
    ax.set_xlim([-2, 6])
    ax.set_ylim([-1, 1])
    ax.set_zlim([0, 1])
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('Humanoid Robot Step Simulation')
    ax.legend()

# Simulação do caminhar do robô
tempo, xcm, ycm, pe_esq_x, pe_esq_y, pe_esq_z, pe_dir_x, pe_dir_y, pe_dir_z = WalkinRobot()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ani = FuncAnimation(fig, update, frames=len(tempo), interval=50)
plt.show()
