from cm import CM
from foot import FeetPoses
from enum import Enum
import numpy as np
import math
import matplotlib.pyplot as plt

class SwingLeg(Enum):
    RIGHT = "Right"
    LEFT = "Left"

Vx = 1
Vy = 0
Vphi = math.pi/2

# Inicialização dos vetores de posição (exemplo)
w_l = np.array([0.0, 0.0, 0.0, 0.0])  # Posição do pé esquerdo [x, y, z, psi]
w_r = np.array([0.0, 0.0, 0.0, 0.0])  # Posição do pé direito [x, y, z, psi]

# Inicialização da variável swingLeg
swingLeg = SwingLeg.RIGHT

def next_step(swingLeg, w_l, w_r):
    if swingLeg == SwingLeg.RIGHT:
        # Realiza operação com o vetor w_r (pé direito)
        selected_vector = w_r
        swingLeg = SwingLeg.LEFT
    else:
        # Realiza operação com o vetor w_l (pé esquerdo)
        selected_vector = w_l
        swingLeg = SwingLeg.RIGHT
    
    return swingLeg, selected_vector

def WalkinRobot():
    cm = CM()
    #feet_poses = FeetPoses()
    delta_tempo = cm.tempo

    tempo = np.zeros(1)
    phi = np.zeros(1)
    xfeet = np.zeros(1)
    yfeet = np.zeros(1)
    phifeet = np.zeros(1)
    xcm = np.zeros(1)
    ycm = np.zeros(1)
    for i in range(2): # 2 = number of steps
        phi = cm.get_delta_Phicm(Vphi, phi[-1])
        x = cm.get_delta_Xcm(Vx, 0)
        y = cm.get_delta_Ycm(Vy, 0)
        delta_x = x*math.cos(phi[-1]) - y*math.sin(phi[-1])
        delta_y = x*math.sin(phi[-1]) + y*math.cos(phi[-1])

        xcm = np.concatenate((xcm, delta_x + xcm[-1]))
        ycm = np.concatenate((ycm, delta_y + ycm[-1]))
        if (i < 2):
            tempo = np.concatenate((tempo, delta_tempo + tempo[-1]))

    return xcm, ycm, phi, tempo

xcm, ycm, phicm, tempo = WalkinRobot()
plt.plot(tempo, xcm, label='y(x)')
plt.xlabel('x (cm)')
plt.ylabel('t (s)')
plt.title('Trajetória do Centro de Massa (x em função de )')
plt.legend()
plt.grid(True)
plt.show()


