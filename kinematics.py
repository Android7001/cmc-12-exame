import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math


# Defina os parâmetros do vetor de tempo
tempo_inicial = 0  # início do intervalo de tempo
tempo_final = 1    # final do intervalo de tempo
intervalo = 0.01   # intervalo de tempo em segundos (10^-2 segundos)

# Crie o vetor de tempo usando numpy
vetor_tempo = np.arange(tempo_inicial, tempo_final + intervalo, intervalo)

# Definindo os parâmetros da caminhada do robô
Vx = 1            # Velocidade no eixo x
Vy = 0            # Velocidade no eixo y (não utilizada no cálculo atual)
Vphi = 0          # Velocidade angular (não utilizada no cálculo atual)
h = 0.5           # Altura do centro de massa
g = 9.81          # Aceleração da gravidade
T = 1             # Período do passo
tb = 0.4          # Tempo inicial de suporte duplo
te = 0.6          # Tempo final de suporte duplo
x0 = Vx * T / 2   # Posição inicial
xf = 3 * Vx * T / 2  # Posição final
px0 = Vx * T / 2
pxs = Vx * T
pxf = 3 * Vx * T / 2
md1x = (pxs - px0) / tb
md2x = (pxf - pxs) / (T - te)

# Calculando p(t)
px = np.zeros(len(vetor_tempo))
for i in range(len(vetor_tempo)):
    if vetor_tempo[i] <= tb:
        px[i] = px0 + md1x * vetor_tempo[i]
    elif tb < vetor_tempo[i] <= te:
        px[i] = pxs
    else:
        px[i] = pxs + md2x * (vetor_tempo[i] - te)

# Calculando lambda
lamb = math.sqrt(g / h)

# Calculando K0 e Kf
K0 = md1x / lamb * math.sinh(-lamb * tb)
Kf = md2x / lamb * math.sinh(lamb * (T - te))

# Calculando As e Bs
As = (Kf - K0 * math.exp(-lamb * T)) / (math.exp(lamb * T) - math.exp(-lamb * T))
Bs = (K0 * math.exp(lamb * T) - Kf) / (math.exp(lamb * T) - math.exp(-lamb * T))

# Calculando x(t)
x = np.zeros(len(vetor_tempo))
for i in range(len(vetor_tempo)):
    t = vetor_tempo[i]
    if t <= tb:
        x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md1x / lamb) * math.sinh(lamb * (t - tb))
    elif tb < t <= te:
        x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t)
    else:
        x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md2x / lamb) * math.sinh(lamb * (t - te))

# Plotando x(t) ao longo do tempo
plt.figure(figsize=(10, 6))
plt.plot(vetor_tempo, x, label='Posição do Centro de Massa (x)', color='b')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição (m)')
plt.title('Posição do Centro de Massa ao Longo do Tempo')
plt.legend()
plt.grid(True)
plt.show()



# Parâmetros do robô
upper_leg_length = 0.5
lower_leg_length = 0.4
extra_leg_length = 0.1
foot_length = 0.3
hip_width = 0.2
angles = [np.pi / 8, np.pi / 8, np.pi / 8, np.pi / 8, np.pi / 8]

# Função para definir as posições das articulações do robô
def humanoid_joint_positions(hip_x, step, upper_leg_length, lower_leg_length, extra_leg_length, foot_length, hip_width, angles):
    hip_height = 1.0

    left_knee_angle = angles[0] * np.sin(step / 10)
    right_knee_angle = angles[1] * np.sin(step / 10)
    left_ankle_angle = angles[2] * np.sin(step / 10)
    right_ankle_angle = angles[3] * np.sin(step / 10)
    left_foot_angle = angles[4] * np.sin(step / 10)
    right_foot_angle = angles[4] * np.sin(step / 10)

    hip_center = np.array([hip_x, 0, hip_height])
    left_hip = np.array([hip_x, hip_width / 2, hip_height])
    right_hip = np.array([hip_x, -hip_width / 2, hip_height])
    
    left_knee = left_hip + np.array([0, 0, -upper_leg_length])
    right_knee = right_hip + np.array([0, 0, -upper_leg_length])
    
    left_ankle = left_knee + np.array([0, 0, -lower_leg_length])
    right_ankle = right_knee + np.array([0, 0, -lower_leg_length])
    
    left_foot_center = left_ankle + np.array([0, 0, -extra_leg_length])
    right_foot_center = right_ankle + np.array([0, 0, -extra_leg_length])
    
    left_toe = left_foot_center + np.array([foot_length / 2 * np.cos(left_foot_angle), foot_length / 2 * np.sin(left_foot_angle), 0])
    left_heel = left_foot_center + np.array([-foot_length / 2 * np.cos(left_foot_angle), -foot_length / 2 * np.sin(left_foot_angle), 0])
    
    right_toe = right_foot_center + np.array([foot_length / 2 * np.cos(right_foot_angle), foot_length / 2 * np.sin(right_foot_angle), 0])
    right_heel = right_foot_center + np.array([-foot_length / 2 * np.cos(right_foot_angle), -foot_length / 2 * np.sin(right_foot_angle), 0])
    
    return hip_center, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle, left_foot_center, right_foot_center, left_toe, left_heel, right_toe, right_heel

# Função para atualizar a animação
def update(step):
    ax.clear()
    
    hip_center, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle, left_foot_center, right_foot_center, left_toe, left_heel, right_toe, right_heel = humanoid_joint_positions(x[step], step, upper_leg_length, lower_leg_length, extra_leg_length, foot_length, hip_width, angles)
    
    # Plotar o corpo do robô
    ax.plot([hip_center[0], left_hip[0]], [hip_center[1], left_hip[1]], [hip_center[2], left_hip[2]], 'bo-')
    ax.plot([hip_center[0], right_hip[0]], [hip_center[1], right_hip[1]], [hip_center[2], right_hip[2]], 'bo-')
    
    # Plotar as pernas
    ax.plot([left_hip[0], left_knee[0]], [left_hip[1], left_knee[1]], [left_hip[2], left_knee[2]], 'bo-')
    ax.plot([right_hip[0], right_knee[0]], [right_hip[1], right_knee[1]], [right_hip[2], right_knee[2]], 'bo-')
    
    ax.plot([left_knee[0], left_ankle[0]], [left_knee[1], left_ankle[1]], [left_knee[2], left_ankle[2]], 'bo-')
    ax.plot([right_knee[0], right_ankle[0]], [right_knee[1], right_ankle[1]], [right_knee[2], right_ankle[2]], 'bo-')
    
    ax.plot([left_ankle[0], left_foot_center[0]], [left_ankle[1], left_foot_center[1]], [left_ankle[2], left_foot_center[2]], 'bo-')
    ax.plot([right_ankle[0], right_foot_center[0]], [right_ankle[1], right_foot_center[1]], [right_ankle[2], right_foot_center[2]], 'bo-')
    
    # Plotar os pés como chapas com articulação central
    ax.plot([left_heel[0], left_foot_center[0]], [left_heel[1], left_foot_center[1]], [left_heel[2], left_foot_center[2]], 'bo-')
    ax.plot([left_foot_center[0], left_toe[0]], [left_foot_center[1], left_toe[1]], [left_foot_center[2], left_toe[2]], 'bo-')
    
    ax.plot([right_heel[0], right_foot_center[0]], [right_heel[1], right_foot_center[1]], [right_heel[2], right_foot_center[2]], 'bo-')
    ax.plot([right_foot_center[0], right_toe[0]], [right_foot_center[1], right_toe[1]], [right_foot_center[2], right_toe[2]], 'bo-')
    
    # Configurar os eixos
    ax.set_xlim([-0.5, 2])
    ax.set_ylim([-1, 1])
    ax.set_zlim([0, 2])
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_title('Humanoid Robot Step Simulation')

# Criar figura e eixos 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Criar animação
ani = FuncAnimation(fig, update, frames=len(vetor_tempo), interval=50)

# Mostrar animação
plt.show()
