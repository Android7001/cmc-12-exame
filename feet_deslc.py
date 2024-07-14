from cm import CM
from foot import FootPose
import numpy as np
import math
import matplotlib.pyplot as plt

Vx = 0.1
Vy = 0.2
Vphi = 0
steps = 5
T = 1

def WalkinRobot():
    cm = CM(T=T)
    pe_esq = FootPose(T=T)
    pe_dir = FootPose(T=T)
    
    balanco_esquerda = True if Vy >= 0 else False  # Determina se o movimento começa com o pé esquerdo ou direito

    tempo = []
    phi = []

    pe_esq_pos = [0.0, 0.1, 0.0]  # Posição inicial do pé esquerdo
    pe_dir_pos = [0.0, -0.1, 0.0]  # Posição inicial do pé direito

    pe_esq_x, pe_esq_y, pe_esq_z, pe_esq_psi = [], [], [], []
    pe_dir_x, pe_dir_y, pe_dir_z, pe_dir_psi = [], [], [], []

    for i in range(steps):
        new_phi = cm.get_delta_Phicm(Vphi, phi[-1] if phi else 0)
        phi.extend(new_phi if not phi else new_phi[1:])  # Ignora o primeiro valor se já estiver adicionado

        if (Vy >= 0 and balanco_esquerda) or (Vy < 0 and not balanco_esquerda):
            # Está abrindo, então o primeiro passo é com o pé esquerdo
            pe_esq_x_temp, pe_esq_y_temp, pe_esq_z_temp, pe_esq_psi_temp = pe_esq.get_foot_position([Vx, Vy, Vphi], pe_esq_pos)
            pe_esq_pos = [pe_esq_x_temp[-1], pe_esq_y_temp[-1], pe_esq_psi_temp[-1]]
            pe_esq_x.extend(pe_esq_x_temp)
            pe_esq_y.extend(pe_esq_y_temp)
            pe_esq_z.extend(pe_esq_z_temp)
            pe_esq_psi.extend(pe_esq_psi_temp)
            # Manter a posição do pé direito
            pe_dir_x.extend([pe_dir_pos[0]] * len(pe_esq_x_temp))
            pe_dir_y.extend([pe_dir_pos[1]] * len(pe_esq_x_temp))
            pe_dir_z.extend([0] * len(pe_esq_x_temp))
            balanco_esquerda = not balanco_esquerda
        else:
            # Está fechando, então o primeiro passo é com o pé direito
            pe_dir_x_temp, pe_dir_y_temp, pe_dir_z_temp, pe_dir_psi_temp = pe_dir.get_foot_position([Vx, Vy, Vphi], pe_dir_pos)
            pe_dir_pos = [pe_dir_x_temp[-1], pe_dir_y_temp[-1], pe_dir_psi_temp[-1]]
            pe_dir_x.extend(pe_dir_x_temp)
            pe_dir_y.extend(pe_dir_y_temp)
            pe_dir_z.extend(pe_dir_z_temp)
            pe_dir_psi.extend(pe_dir_psi_temp)
            # Manter a posição do pé esquerdo
            pe_esq_x.extend([pe_esq_pos[0]] * len(pe_dir_x_temp))
            pe_esq_y.extend([pe_esq_pos[1]] * len(pe_dir_x_temp))
            pe_esq_z.extend([0] * len(pe_dir_x_temp))
            balanco_esquerda = not balanco_esquerda

        # Atualiza o vetor tempo para refletir corretamente os 5 segundos de caminhada
        tempo.extend(np.arange(i * T, (i + 1) * T, cm.tempo[1] - cm.tempo[0]))

    return np.array(tempo), np.array(pe_esq_x), np.array(pe_esq_y), np.array(pe_esq_z), np.array(pe_dir_x), np.array(pe_dir_y), np.array(pe_dir_z)

tempo, pe_esq_x, pe_esq_y, pe_esq_z, pe_dir_x, pe_dir_y, pe_dir_z = WalkinRobot()

# Criar subplots para os pés esquerdo e direito
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# Plotando as posições do pé esquerdo
ax1.plot(tempo[:len(pe_esq_x)], pe_esq_x, label='x_esq')
ax1.plot(tempo[:len(pe_esq_y)], pe_esq_y, label='y_esq')
ax1.plot(tempo[:len(pe_esq_z)], pe_esq_z, label='z_esq')
ax1.set_xlabel('Tempo (s)')
ax1.set_ylabel('Posição (cm)')
ax1.set_title('Posições do Pé Esquerdo')
ax1.legend()
ax1.grid(True)

# Plotando as posições do pé direito
ax2.plot(tempo[:len(pe_dir_x)], pe_dir_x, label='x_dir')
ax2.plot(tempo[:len(pe_dir_y)], pe_dir_y, label='y_dir')
ax2.plot(tempo[:len(pe_dir_z)], pe_dir_z, label='z_dir')
ax2.set_xlabel('Tempo (s)')
ax2.set_ylabel('Posição (cm)')
ax2.set_title('Posições do Pé Direito')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
