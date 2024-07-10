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

    x = []
    y = []
    phi = [0]
    xfeet = [0]
    yfeet = [0]
    phifeet = [0]
    xcm = [0]
    ycm = [0]
    for _ in range(1):
        phi = cm.get_delta_Phicm(Vphi, phi[-1])
        x = cm.get_delta_Xcm(Vx, 0)
        y = cm.get_delta_Ycm(Vy, 0)
        delta_x = x*math.cos(phi[-1]) - y*math.sin(phi[-1])
        delta_y = x*math.sin(phi[-1]) + y*math.cos(phi[-1])

        for i in range(len(delta_x)):
            xcm.append(delta_x[i] + xcm[-1])
        for i in range(len(delta_y)):
            ycm.append(delta_y[i] + ycm[-1])

    return xcm, ycm, phi

xcm, ycm, phicm = WalkinRobot()
plt.plot(xcm, ycm, label='y(x)')
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.title('Trajetória do Centro de Massa (y em função de x)')
plt.legend()
plt.grid(True)
plt.show()


