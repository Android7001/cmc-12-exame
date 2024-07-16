import numpy as np
import math
import matplotlib.pyplot as plt
from cm import CM
from foot import FootPose

# Definindo os parâmetros da caminhada do robô
Vx = 1
Vy = 0
Vphi = 0
steps = 4
T = 1

# Função para simulação do caminhar do robô
def WalkinRobot():
    cm = CM(T=T)
    pe_esq = FootPose(T=T)
    pe_dir = FootPose(T=T)

    balanco_esquerda = True if Vy >= 0 else False  # Determina se o movimento começa com o pé esquerdo ou direito

    tempo = np.zeros(1)
    phi = np.zeros(1)
    pe_esq_x = np.zeros(1)
    pe_esq_y = np.zeros(1)
    pe_esq_z = np.zeros(1)
    pe_dir_x = np.zeros(1)
    pe_dir_y = np.zeros(1)
    pe_dir_z = np.zeros(1)
    xcm = np.zeros(1)
    ycm = np.zeros(1)

    pe_esq_pos = [0.0 - Vx*T, 0.1, 0.0]  # Posição inicial do pé esquerdo
    pe_dir_pos = [0.0 + Vx*T, -0.1, 0.0]  # Posição inicial do pé direito

    for i in range(steps):
        new_phi = cm.get_delta_Phicm(Vphi, phi[-1] if phi.any() else 0)
        phi = np.concatenate(
            (phi, new_phi if not phi.any() else new_phi[1:]))  # Ignora o primeiro valor se já estiver adicionado

        # Calcular o deslocamento do CM
        x_delta = cm.get_delta_Xcm(Vx, 0)
        y_delta = cm.get_delta_Ycm(Vy, 0, abrindo=balanco_esquerda)
        delta_x = x_delta * math.cos(phi[-1]) - y_delta * math.sin(phi[-1])
        delta_y = x_delta * math.sin(phi[-1]) + y_delta * math.cos(phi[-1])

        xcm = np.concatenate((xcm, delta_x + xcm[-1]))
        ycm = np.concatenate((ycm, delta_y + ycm[-1]))

        if (Vy >= 0 and balanco_esquerda) or (Vy < 0 and not balanco_esquerda):
            # Está abrindo, então o primeiro passo é com o pé esquerdo
            pe_esq_x_temp, pe_esq_y_temp, pe_esq_z_temp, _ = pe_esq.get_foot_position([Vx, Vy, Vphi], pe_esq_pos)
            pe_esq_pos = [pe_esq_x_temp[-1], pe_esq_y_temp[-1], pe_esq_z_temp[-1]]
            pe_esq_x = np.concatenate((pe_esq_x, pe_esq_x_temp))
            pe_esq_y = np.concatenate((pe_esq_y, pe_esq_y_temp))
            pe_esq_z = np.concatenate((pe_esq_z, pe_esq_z_temp))
            # Manter a posição do pé direito
            pe_dir_x = np.concatenate((pe_dir_x, np.full(len(pe_esq_x_temp), pe_dir_pos[0])))
            pe_dir_y = np.concatenate((pe_dir_y, np.full(len(pe_esq_x_temp), pe_dir_pos[1])))
            pe_dir_z = np.concatenate((pe_dir_z, np.zeros(len(pe_esq_x_temp))))
            balanco_esquerda = not balanco_esquerda
        else:
            # Está fechando, então o primeiro passo é com o pé direito
            pe_dir_x_temp, pe_dir_y_temp, pe_dir_z_temp, _ = pe_dir.get_foot_position([Vx, Vy, Vphi], pe_dir_pos)
            pe_dir_pos = [pe_dir_x_temp[-1], pe_dir_y_temp[-1], pe_dir_z_temp[-1]]
            pe_dir_x = np.concatenate((pe_dir_x, pe_dir_x_temp))
            pe_dir_y = np.concatenate((pe_dir_y, pe_dir_y_temp))
            pe_dir_z = np.concatenate((pe_dir_z, pe_dir_z_temp))
            # Manter a posição do pé esquerdo
            pe_esq_x = np.concatenate((pe_esq_x, np.full(len(pe_dir_x_temp), pe_esq_pos[0])))
            pe_esq_y = np.concatenate((pe_esq_y, np.full(len(pe_dir_x_temp), pe_esq_pos[1])))
            pe_esq_z = np.concatenate((pe_esq_z, np.zeros(len(pe_dir_x_temp))))
            balanco_esquerda = not balanco_esquerda

        # Atualiza o vetor tempo para refletir corretamente os 5 segundos de caminhada
        tempo = np.concatenate((tempo, tempo[-1] + np.linspace(0, T, len(new_phi))))

    return tempo, xcm, ycm, pe_esq_x, pe_esq_y, pe_esq_z, pe_dir_x, pe_dir_y, pe_dir_z

# Simulação do caminhar do robô
tempo, xcm, ycm, pe_esq_x, pe_esq_y, pe_esq_z, pe_dir_x, pe_dir_y, pe_dir_z = WalkinRobot()

# Plotando as posições dos pés e do centro de massa (CM)
fig, axs = plt.subplots(3, 1, figsize=(12, 12))

# Plotando as posições do centro de massa (CM)
axs[0].plot(tempo, xcm, label='x_cm')
axs[0].plot(tempo, ycm, label='y_cm')
axs[0].set_xlabel('Tempo (s)')
axs[0].set_ylabel('Posição (cm)')
axs[0].set_title('Posições do Centro de Massa (CM)')
axs[0].legend()
axs[0].grid(True)

# Plotando as posições do pé esquerdo
axs[1].plot(tempo, pe_esq_x, label='x_esq')
axs[1].plot(tempo, pe_esq_y, label='y_esq')
axs[1].plot(tempo, pe_esq_z, label='z_esq')
axs[1].set_xlabel('Tempo (s)')
axs[1].set_ylabel('Posição (cm)')
axs[1].set_title('Posições do Pé Esquerdo')
axs[1].legend()
axs[1].grid(True)

# Plotando as posições do pé direito
axs[2].plot(tempo, pe_dir_x, label='x_dir')
axs[2].plot(tempo, pe_dir_y, label='y_dir')
axs[2].plot(tempo, pe_dir_z, label='z_dir')
axs[2].set_xlabel('Tempo (s)')
axs[2].set_ylabel('Posição (cm)')
axs[2].set_title('Posições do Pé Direito')
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()
plt.show()
