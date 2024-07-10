from cm import CM
from foot import FeetPoses
import numpy as np
import math
import matplotlib.pyplot as plt

Vx = 1
Vy = 0
Vphi = math.pi/3

def WalkinRobot():
    cm = CM()
    #feet_poses = FeetPoses()
    delta_tempo = cm.tempo

    tempo = [0]
    phi = [0]
    xfeet = [0]
    yfeet = [0]
    phifeet = [0]
    xcm = [0]
    ycm = [0]
    for i in range(1): # 2 = number of steps
        phi = cm.get_delta_Phicm(Vphi, phi[-1])
        x = cm.get_delta_Xcm(Vx, 0)
        y = cm.get_delta_Ycm(Vy, 0)
        delta_x = x*math.cos(phi[-1]) - y*math.sin(phi[-1])
        delta_y = x*math.sin(phi[-1]) + y*math.cos(phi[-1])

        xcm = np.concatenate((xcm, delta_x + xcm[-1]))
        ycm = np.concatenate((ycm, delta_y + ycm[-1]))
        tempo = np.concatenate((tempo, (i + 1) * delta_tempo + tempo[-1]))

    return xcm, ycm, phi, tempo

xcm, ycm, phicm, tempo = WalkinRobot()
plt.plot(tempo, xcm, label='y(x)')
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.title('Trajetória do Centro de Massa (y em função de x)')
plt.legend()
plt.grid(True)
plt.show()


