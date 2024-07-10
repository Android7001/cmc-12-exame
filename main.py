from cm import CM
from foot import FeetPoses
import numpy as np
import math
import matplotlib.pyplot as plt

Vx = 1
Vy = 1
Vphi = math.pi

def WalkinRobot():
    cm = CM()
    # Parâmetros
    T = 1
    t_b = 0.4
    t_e = 0.6
    t_inicio = 0
    t_fim = 1
    passo = 0.01

    # Instancia a classe e obtém os valores de z
    feet_poses = FeetPoses(T, t_b, t_e, t_inicio, t_fim, passo)

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


