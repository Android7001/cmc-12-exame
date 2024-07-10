from cm import CM
from foot import FeetPoses

import numpy as np
import math
import matplotlib.pyplot as plt

Vx = 0
Vy = 1
Vphi = 0
steps = 4

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

    for i in range(steps):

        phi = cm.get_delta_Phicm(Vphi, phi[-1])
        x = cm.get_delta_Xcm(Vx, 0)

        if((Vy >= 0 and balanco_esquerda == True) or (Vy < 0 and balanco_esquerda == False)):
            y = cm.get_delta_Ycm(Vy, 0, abrindo=True)
            balanco_esquerda = not balanco_esquerda
        elif((Vy >= 0 and balanco_esquerda == False) or (Vy < 0 and balanco_esquerda == True)):
            y = cm.get_delta_Ycm(Vy, 0, abrindo=False)
            balanco_esquerda = not balanco_esquerda

        delta_x = x*math.cos(phi[-1]) - y*math.sin(phi[-1])
        delta_y = x*math.sin(phi[-1]) + y*math.cos(phi[-1])

        xcm = np.concatenate((xcm, delta_x + xcm[-1]))
        ycm = np.concatenate((ycm, delta_y + ycm[-1]))

        if (i < steps):
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


