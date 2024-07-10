import numpy as np
import math
import matplotlib.pyplot as plt

class FootPose:
    def __init__(self, T=1, t_b=0.4, t_e=0.6, t_inicio=0, t_fim=1, passo=0.01):
        self.t_inicio = t_inicio
        self.t_fim = t_fim
        self.passo = passo
        self.T = T 

        self.t_b = t_b
        self.t_e = t_e
        self.phi_b = t_b / T
        self.phi_e = t_e / T

        self.vetor_tempo = np.arange(t_inicio, t_fim, passo)

    def v(self, phi):
        if phi < self.phi_b or phi >= self.phi_e:
            return 0
        else:
            return 0.5 * (1 - math.cos(2 * math.pi * (phi - self.phi_b) / (self.phi_e - self.phi_b)))

    def v_ponto(self, phi):
        if phi < self.phi_b or phi >= self.phi_e:
            return 0
        else: 
            return 0.5 * (math.sin(2 * math.pi * (phi - self.phi_b) / (self.phi_e - self.phi_b)))

    def get_z(self):
        z_a = []
        z_cm = 0
        z_step = 0.5
        for tempo in self.vetor_tempo:
            phi = tempo % self.T  
            z_a.append(z_cm + z_step * self.v(phi))
        return z_a

    def get_foot_position(self, v, initial_position):
        Vx, Vy, Vpsi = v
        xi, yi, psi0 = initial_position
        x_a = []
        y_a = []
        psi_a = []

        for tempo in self.vetor_tempo:
            phi = tempo % self.T
            if phi < self.phi_b:
                x_a.append(xi)
                y_a.append(yi)
                psi_a.append(psi0)
            elif self.phi_b <= phi < self.phi_e:
                x_a.append(xi + 2 * Vx * (phi - self.phi_b))
                y_a.append(yi + 2 * Vy * (phi - self.phi_b))
                psi_a.append(psi0 + 2 * Vpsi * (phi - self.phi_b))
            else:
                x_a.append(xi + 2 * Vx * (self.phi_e - self.phi_b))
                y_a.append(yi + 2 * Vy * (self.phi_e - self.phi_b))
                psi_a.append(psi0 + 2 * Vpsi * (self.phi_e - self.phi_b))

        return x_a, y_a, self.get_z(), psi_a

# Exemplo de uso
foot_pose = FootPose()
v = [1.0, 0.5, 0.1]  # Velocidades [v_x, v_y, v_psi]
initial_position = [0.0, 0.0, 0.0]  # Posição inicial [x, y, psi]
x_positions, y_positions, z_positions, psi_positions = foot_pose.get_foot_position(v, initial_position)

# Plotando as posições
plt.figure(figsize=(12, 8))

# Plot para a posição X
plt.subplot(2, 2, 1)
plt.plot(foot_pose.vetor_tempo, x_positions)
plt.title('Posição X do Pé')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição X (m)')

# Plot para a posição Y
plt.subplot(2, 2, 2)
plt.plot(foot_pose.vetor_tempo, y_positions)
plt.title('Posição Y do Pé')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição Y (m)')

# Plot para a posição Z
plt.subplot(2, 2, 3)
plt.plot(foot_pose.vetor_tempo, z_positions)
plt.title('Posição Z do Pé')
plt.xlabel('Tempo (s)')
plt.ylabel('Posição Z (m)')

# Plot para a posição Psi
plt.subplot(2, 2, 4)
plt.plot(foot_pose.vetor_tempo, psi_positions)
plt.title('Posição Psi do Pé')
plt.xlabel('Tempo (s)')
plt.ylabel('Ângulo Psi (rad)')

plt.tight_layout()
plt.show()

