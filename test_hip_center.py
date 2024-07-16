import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

from cm import CM
from foot import FootPose

# Definindo os parâmetros da caminhada do robô
Vx = 1
Vy = 0
Vphi = 0
steps = 5
T = 1

# Simulação do caminhar do robô
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

# Função para definir as posições das articulações do robô
def humanoid_joint_positions(step, pe_esq_x, pe_esq_y, pe_esq_z, pe_dir_x, pe_dir_y, pe_dir_z):
    hip_x = (pe_esq_x[step] + pe_dir_x[step]) / 2
    hip_y = (pe_esq_y[step] + pe_dir_y[step]) / 2
    hip_height = 1.0

    hip_center = np.array([hip_x, hip_y, hip_height])
    left_foot_center = np.array([pe_esq_x[step], pe_esq_y[step], pe_esq_z[step]])
    right_foot_center = np.array([pe_dir_x[step], pe_dir_y[step], pe_dir_z[step]])
    
    return hip_center, left_foot_center, right_foot_center

# Função para atualizar a animação
def update(step):
    ax.clear()
    
    hip_center, left_foot_center, right_foot_center = humanoid_joint_positions(step, pe_esq_x, pe_esq_y, pe_esq_z, pe_dir_x, pe_dir_y, pe_dir_z)
    
    # Plotar os pontos relevantes
    ax.scatter(hip_center[0], hip_center[1], hip_center[2], color='purple', label='Hip Center')
    ax.scatter(left_foot_center[0], left_foot_center[1], left_foot_center[2], color='blue', label='Pé Esquerdo')
    ax.scatter(right_foot_center[0], right_foot_center[1], right_foot_center[2], color='red', label='Pé Direito')
    
    # Configurar os eixos
    ax.set_xlim([-0.5, 2])
    ax.set_ylim([-1, 1])
    ax.set_zlim([0, 2])
    ax.set_xlabel('Eixo X')
    ax.set_ylabel('Eixo Y')
    ax.set_zlabel('Eixo Z')
    ax.set_title('Simulação da Caminhada do Robô Humanoide')
    ax.legend()

# Simulação do caminhar do robô
tempo, pe_esq_x, pe_esq_y, pe_esq_z, pe_dir_x, pe_dir_y, pe_dir_z = WalkinRobot()

# Criar figura e eixos 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Criar animação
ani = FuncAnimation(fig, update, frames=len(tempo), interval=50)

# Mostrar animação
plt.show()