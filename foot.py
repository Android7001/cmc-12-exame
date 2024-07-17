import numpy as np
import math
import matplotlib.pyplot as plt

class FootPose:
    def __init__(self, T=1, t_b=0.4, t_e=0.6, tempo_inicial=0, tempo_final=1, intervalo=0.01):
        self.T = T              # Período do Passo
        self.t_b = t_b          # Tempo inicial de suporte simples
        self.t_e = t_e          # Tempo final de suporte simples
        self.phi_b = t_b / T    # Normalização do tempo inicial de suporte simples
        self.phi_e = t_e / T    # Normalização do tempo final de suporte simples
        self.vetor_tempo = np.arange(tempo_inicial, tempo_final, intervalo)

    def v(self, phi):
        if phi < self.phi_b or phi >= self.phi_e:
            return 0
        else:
            return 0.5 * (1 - math.cos(2 * math.pi * (phi - self.phi_b) / (self.phi_e - self.phi_b)))

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
        x_a = np.zeros(len(self.vetor_tempo))
        y_a = np.zeros(len(self.vetor_tempo))
        psi_a = np.zeros(len(self.vetor_tempo))

        for i in range(len(self.vetor_tempo)):
            
            phi = self.vetor_tempo[i] % self.T
            if phi <= self.phi_b:
                x_a[i] = xi
                y_a[i] = yi
                psi_a[i] = psi0
            elif self.phi_b < phi <= self.phi_e:
                x_a[i] = xi + Vx * self.T * (1 - math.cos(math.pi * (phi - self.phi_b) / (self.phi_e - self.phi_b))) # Funcao de interpolacao utilizada, mesma do angulo do CM
                y_a[i] = yi +  Vy * self.T * (1 - math.cos(math.pi * (phi - self.phi_b) / (self.phi_e - self.phi_b)))
                psi_a[i] = psi0 +  Vpsi * self.T * (1 - math.cos(math.pi * (phi - self.phi_b) / (self.phi_e - self.phi_b)))
            else:
                x_a[i] = xi + 2 * Vx * self.T
                y_a[i] = yi + 2 * Vy * self.T
                psi_a[i] = psi0 + 2 * Vpsi * self.T

        return x_a, y_a, self.get_z(), psi_a



