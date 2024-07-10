import numpy as np
import math
import matplotlib.pyplot as plt

class CM:
    def __init__(self, h=0.5, L=0.25, g=9.81, T=1, tb=0.4, te=0.6, tempo_inicial=0, tempo_final=1, intervalo=0.01):
        self.h = h  # Altura do centro de massa
        self.L = L  # Largura do robô
        self.g = g  # Aceleração da gravidade
        self.T = T  # Período do passo
        self.tb = tb  # Tempo inicial de suporte duplo
        self.te = te  # Tempo final de suporte duplo
        self.tempo = np.arange(tempo_inicial, tempo_final + intervalo, intervalo)  # Vetor de tempo

    def get_delta_Xcm(self, Vx, xi):
        px0 = 0  # Posicao inicial do ZPM/CM
        pxs = Vx * self.T / 2  # Posicao do pe de suporte em relacao ao CM
        pxf = Vx * self.T  # Posicao final do ZPM/CM
        md1x = (pxs - px0) / self.tb
        md2x = (pxf - pxs) / (self.T - self.te)

        # Calculando px(t) (ZMP)
        px = np.zeros(len(self.tempo))
        for i in range(len(self.tempo)):
            if self.tempo[i] <= self.tb:
                px[i] = px0 + md1x * self.tempo[i]
            elif self.tb < self.tempo[i] <= self.te:
                px[i] = pxs
            else:
                px[i] = pxs + md2x * (self.tempo[i] - self.te)

        # Calculando lambda
        lamb = math.sqrt(self.g / self.h)

        # Calculando K0 e Kf
        K0 = md1x / lamb * math.sinh(-lamb * self.tb)
        Kf = md2x / lamb * math.sinh(lamb * (self.T - self.te))

        # Calculando As e Bs
        As = (Kf - K0 * math.exp(-lamb * self.T)) / (math.exp(lamb * self.T) - math.exp(-lamb * self.T))
        Bs = (K0 * math.exp(lamb * self.T) - Kf) / (math.exp(lamb * self.T) - math.exp(-lamb * self.T))

        # Calculando x(t)
        x = np.zeros(len(self.tempo))
        for i in range(len(self.tempo)):
            t = self.tempo[i]
            if t <= self.tb:
                x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md1x / lamb) * math.sinh(
                    lamb * (t - self.tb)) + xi
            elif self.tb < t <= self.te:
                x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) + xi
            else:
                x[i] = px[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md2x / lamb) * math.sinh(
                    lamb * (t - self.te)) + xi

        return x

    def get_delta_Ycm(self, Vy, yi, abrindo=True):
        if abrindo:
            py0 = 0
            pys = -np.sign(Vy) * self.L / 2
            pyf = np.sign(Vy) * Vy * self.T
        else:
            py0 = 0
            pys = np.sign(Vy) * (self.L / 2 + Vy * self.T)
            pyf = np.sign(Vy) * Vy * self.T

        md1y = (pys - py0) / self.tb
        md2y = (pyf - pys) / (self.T - self.te)

        # Calculando py(t) (ZMP)
        py = np.zeros(len(self.tempo))
        for i in range(len(self.tempo)):
            if self.tempo[i] <= self.tb:
                py[i] = py0 + md1y * self.tempo[i]
            elif self.tb < self.tempo[i] <= self.te:
                py[i] = pys
            else:
                py[i] = pys + md2y * (self.tempo[i] - self.te)

        # Calculando lambda
        lamb = math.sqrt(self.g / self.h)

        # Calculando K0 e Kf
        K0 = md1y / lamb * math.sinh(-lamb * self.tb)
        Kf = md2y / lamb * math.sinh(lamb * (self.T - self.te))

        # Calculando As e Bs
        As = (Kf - K0 * math.exp(-lamb * self.T)) / (math.exp(lamb * self.T) - math.exp(-lamb * self.T))
        Bs = (K0 * math.exp(lamb * self.T) - Kf) / (math.exp(lamb * self.T) - math.exp(-lamb * self.T))

        # Calculando y(t)
        y = np.zeros(len(self.tempo))
        for i in range(len(self.tempo)):
            t = self.tempo[i]
            if t <= self.tb:
                y[i] = py[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md1y / lamb) * math.sinh(
                    lamb * (t - self.tb)) + yi
            elif self.tb < t <= self.te:
                y[i] = py[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) + yi
            else:
                y[i] = py[i] + As * math.exp(lamb * t) + Bs * math.exp(-lamb * t) - (md2y / lamb) * math.sinh(
                    lamb * (t - self.te)) + yi

        return y

    def get_delta_Phicm(self, Vphi, phi0, abrindo=True):
        psi = self.tempo / self.T
        psib = self.tb / self.T
        psie = self.te / self.T
        phif = Vphi * self.T

        phi = np.zeros(len(self.tempo))
        for i in range(len(self.tempo)):
            if psi[i] <= psib:
                phi[i] = phi0
            elif psib < psi[i] <= psie:
                phi[i] = phif / 2 * (1 - math.cos(math.pi * (psi[i] - psib) / (psie - psib))) + phi0
            else:
                phi[i] = phif + phi0

        return phi

# Exemplo de uso da classe
#robo = CM()

# Vx = 1
# xi = 0
# x = robo.get_Xcm(Vx, xi)
#
# Vy = 1
# yi = 0
# y = robo.get_Ycm(Vy, yi)
#
# Vphi = 0.1
# phi0 = 0
# phi = robo.get_Phicm(Vphi, phi0)
#
# # Plotando os resultados
# plt.plot(robo.tempo, x, label='x(t)')
# plt.plot(robo.tempo, y, label='y(t)')
# plt.plot(robo.tempo, phi, label='phi(t)')
# plt.xlabel('Tempo (s)')
# plt.ylabel('Posição/Ângulo')
# plt.legend()
# plt.title('Posição do Centro de Massa e Ângulo durante a Caminhada do Robô')
# plt.show()
