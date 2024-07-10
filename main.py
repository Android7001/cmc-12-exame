from cm import CM
from foot import FeetPoses
from angle import Angles
import numpy as np
import math
import matplotlib.pyplot as plt

Vx = 1
Vy = 0
Vphi = math.pi/3

def WalkinRobot():
    cm = CM()
    feet_poses = FeetPoses()

    x = [0]
    y = [0]
    phi = [0]
    xfeet = [0]
    yfeet = [0]
    phifeet = [0]
    xcm = [0]
    ycm = [0]
    for _ in range(180):
        x = np.concatenate((x, cm.get_Xcm(Vx, xcm[-1])))
        y = np.concatenate((y, cm.get_Ycm(Vy, ycm[-1])))
        phicm = np.concatenate((phi, cm.get_Phicm(Vphi, phicm[-1])))



    for i in range(180):
        xcm[i] = x[i]*math.cos(phi[i]) - y[i]*math.sin(phi[i])
        ycm[i] = x[i]*math.sin(phi[i]) + y[i]*math.cos(phi[i])

    return xcm, ycm, phi

xcm, ycm, phicm = WalkinRobot()
plt.plot(xcm, ycm, label='y(x)')
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.title('Trajetória do Centro de Massa (y em função de x)')
plt.legend()
plt.grid(True)
plt.show()


