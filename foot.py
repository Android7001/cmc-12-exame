import math
import numpy as np
import matplotlib.pyplot as plt 

class FeetPoses:
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
        zponto_a = []
        z_cm = 0
        z_step = 1
        for tempo in self.vetor_tempo:
            phi = tempo % self.T  
            z_a.append(z_cm + z_step * self.v(phi))
            zponto_a.append(z_step * self.v_ponto(phi))
        return z_a, zponto_a
    
    def get_x_foot(self, Vx, xi):
        x_a = []
        for tempo in self.vetor_tempo:
            phi = tempo % self.T
            if phi < self.phi_b:
                x_a.append(xi)
            elif self.phi_b <= phi < self.phi_e:
                x_a.append(xi + 2* Vx * (phi- self.phi_b))
            else:
                x_a.append(xi + 2* Vx * (self.phi_e - self.phi_b))
        return x_a

    def get_y_foot(self, Vy, yi, abrindo = True):
        y_a = []
        for tempo in self.vetor_tempo:
            phi = tempo % self.T
            if abrindo:
                if phi < self.phi_b:
                    y_a.append(yi)
                elif self.phi_b <= phi < self.phi_e:
                    y_a.append(yi + 2* Vy * (phi- self.phi_b))
                else:
                    y_a.append(yi + 2* Vy * (self.phi_e - self.phi_b))
            else:
                if phi < self.phi_b:
                    y_a.append(yi)
                elif self.phi_b <= phi < self.phi_e:
                    y_a.append(yi - 2* Vy * (phi- self.phi_b))
                else:
                    y_a.append(yi - 2* Vy * (self.phi_e - self.phi_b))
        return y_a

    def get_psi_foot(self, Vpsi, psi0, abrindo = True):
        psi_a = []
        for tempo in self.vetor_tempo:
            phi = tempo % self.T
            if abrindo:
                if phi < self.phi_b:
                    psi_a.append(psi0)
                elif self.phi_b <= phi < self.phi_e:
                    psi_a.append(psi0 + 2* Vpsi * (phi- self.phi_b))
                else:
                    psi_a.append(psi0 + 2* Vpsi * (self.phi_e - self.phi_b))
            else:
                if phi < self.phi_b:
                    psi_a.append(psi0)
                elif self.phi_b <= phi < self.phi_e:
                    psi_a.append(psi0 - 2* Vpsi * (phi- self.phi_b))
                else:
                    psi_a.append(psi0 - 2* Vpsi * (self.phi_e - self.phi_b))
        return psi_a
    
# Parâmetros
# T = 1
# t_b = 0.4
# t_e = 0.6
# t_inicio = 0
# t_fim = 1
# passo = 0.01
#
# # Instancia a classe e obtém os valores de z
feet_poses = FeetPoses()
y_a = feet_poses.get_x_foot(1,0)#

# Plotagem
plt.plot(feet_poses.vetor_tempo, y_a, label='y_a')
#plt.plot(feet_poses.vetor_tempo, zponto_a, label='zPonto_a')
plt.xlabel('Tempo (s)')
plt.ylabel('y')
plt.legend()
plt.show()


