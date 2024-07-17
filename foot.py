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
            if phi <= self.phi_b:
                x_a.append(xi)
                y_a.append(yi)
                psi_a.append(psi0)
            elif self.phi_b < phi <= self.phi_e:
                x_a.append(xi + Vx * self.T * (1 - math.cos(math.pi * (phi - self.phi_b) / (self.phi_e - self.phi_b)))) # Funcao de interpolacao utilizada, mesma do angulo do CM
                y_a.append(yi + 2.5 * Vy * self.T * (1 - math.cos(math.pi * (phi - self.phi_b) / (self.phi_e - self.phi_b))))
                psi_a.append(psi0 + 2.5 * Vpsi * self.T * (1 - math.cos(math.pi * (phi - self.phi_b) / (self.phi_e - self.phi_b))))
            else:
                x_a.append(xi + 2 * Vx * self.T)
                y_a.append(yi + 2 * Vy * self.T)
                psi_a.append(psi0 + 2 * Vpsi * self.T)

        return x_a, y_a, self.get_z(), psi_a



