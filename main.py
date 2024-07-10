from cm import CM
from foot import FeetPoses
from angle import Angles
import numpy as np
import math
import matplotlib.pyplot as plt

Vx = 1
Vy = 1
Vphi = math.pi

def WalkinRobot():
    cm = CM()
    feet_poses = FeetPoses()

    xcm = [0]
    ycm = [0]
    phicm = [0]
    xfeet = [0]
    yfeet = [0]
    phifeet = [0]
    for _ in range(5):
        xcm = np.concatenate((xcm, cm.get_Xcm(Vx, xcm[-1])))
        ycm = np.concatenate((ycm, cm.get_Ycm(Vy, ycm[-1])))
        phicm = np.concatenate((phicm, cm.get_Phicm(Vphi, phicm[-1])))

    return xcm, ycm, phicm

xcm, ycm, phicm = WalkinRobot()
plt.plot(xcm, ycm, label='y(x)')
plt.xlabel('x (cm)')
plt.ylabel('y (cm)')
plt.title('Trajetória do Centro de Massa (y em função de x)')
plt.legend()
plt.grid(True)
plt.show()


