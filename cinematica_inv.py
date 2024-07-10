import math
import numpy as np

class Angles:
    def __init__(self, x_l, y_l, z_l, psi_l):
        self.T = 1
        self.t_inicio = 0
        self.t_fim = 1
        self.passo = 0.01
        self.a = 2 # tamanho da coxa
        self.b = 1 # tamanho da canela

        # Precisa pegar os valores corretos
        # _l_t2h: significa left do torço para a coxa
        self.x_l_t2h = 0.2
        self.y_l_t2h = 0.2
        self.z_l_t2h = 0.2

        # _l_a2f: significa left do calcanhar para o pé
        self.x_l_a2f = 0.1
        self.y_l_a2f = 0.1
        self.z_l_a2f = 0.1

        self.vetor_tempo = np.arange(self.t_inicio, self.t_fim, self.passo)
        self.x_l = x_l
        self.y_l = y_l
        self.z_l = z_l
        self.psi_l = psi_l

    def _calculate_common_terms(self, t):
        w_l = np.array([[self.x_l[t]], [self.y_l[t]], [self.z_l[t]], [self.psi_l[t]]])
        w_l_t2h = w_l[:3, :] - np.array([[self.x_l_t2h], [self.y_l_t2h], [self.z_l_t2h]])

        x_l_h2f = w_l_t2h[0, 0]
        y_l_h2f = w_l_t2h[1, 0]
        z_l_h2f = w_l_t2h[2, 0]

        rotacao = np.array([[math.cos(self.psi_l[t]), -math.sin(self.psi_l[t])],
                            [math.sin(self.psi_l[t]), math.cos(self.psi_l[t])]])

        [x1_l_h2f, y1_l_h2f] = np.dot(rotacao, [x_l_h2f, y_l_h2f]) # cálculo de x' left hip to foot

        x2_l_h2f = x1_l_h2f - self.x_l_a2f
        y2_l_h2f = y1_l_h2f - self.y_l_a2f
        z2_l_h2f = z_l_h2f - self.z_l_a2f

        c = math.sqrt(x2_l_h2f**2 + y2_l_h2f**2 + z2_l_h2f**2)
        h = math.sqrt(y2_l_h2f**2 + z2_l_h2f**2)

        alpha = math.acos((self.b**2 + c**2 - self.a**2) / (2 * self.b * c))
        beta = math.acos((self.a**2 + c**2 - self.b**2) / (2 * self.a * c))
        gama = math.acos((self.a**2 + self.b**2 - c**2) / (2 * self.a * self.b))

        return x2_l_h2f, h, alpha, beta, gama, z2_l_h2f

    def get_theta_hp(self):
        vetor_theta_hp = []
        for t in range(len(self.vetor_tempo)):
            x2_l_h2f, h, _, beta, _, _ = self._calculate_common_terms(t)
            theta_hp = -(math.atan2(x2_l_h2f, h) + beta)
            vetor_theta_hp.append(theta_hp)
        return vetor_theta_hp

    def get_theta_k(self):
        vetor_theta_k = []
        for t in range(len(self.vetor_tempo)):
            _, _, _, _, gama, _ = self._calculate_common_terms(t)
            theta_k = math.pi - gama
            vetor_theta_k.append(theta_k)
        return vetor_theta_k

    def get_theta_ap(self):
        vetor_theta_ap = []
        for t in range(len(self.vetor_tempo)):
            x2_l_h2f, h, alpha, _, _, _ = self._calculate_common_terms(t)
            theta_ap = alpha - math.atan2(h, x2_l_h2f)
            vetor_theta_ap.append(theta_ap)
        return vetor_theta_ap

    def get_theta_hr(self):
        vetor_theta_hr = []
        for t in range(len(self.vetor_tempo)):
            x2_l_h2f, _, _, _, _, z2_l_h2f = self._calculate_common_terms(t)
            theta_hr = math.atan2(x2_l_h2f, z2_l_h2f)
            vetor_theta_hr.append(theta_hr)
        return vetor_theta_hr

    def get_theta_fr(self):
        vetor_theta_fr = []
        for t in range(len(self.vetor_tempo)):
            x2_l_h2f, _, _, _, _, z2_l_h2f = self._calculate_common_terms(t)
            theta_hr = math.atan2(x2_l_h2f, z2_l_h2f)
            theta_fr = -theta_hr
            vetor_theta_fr.append(theta_fr)
        return vetor_theta_fr


# Parâmetros de tempo
t_inicio = 0
t_fim = 1
passo = 0.01
vetor_tempo = np.arange(t_inicio, t_fim, passo)

# Preenchendo os vetores com valores
x_l = np.linspace(0, 1, len(vetor_tempo))
y_l = np.linspace(0, 1, len(vetor_tempo))
z_l = np.linspace(0, 1, len(vetor_tempo))
psi_l = np.linspace(0, 2 * np.pi, len(vetor_tempo))

# Instancia a classe e calcula os ângulos
angles = Angles(x_l,y_l,z_l,psi_l)
vetor_theta_hp = angles.get_theta_hp()
vetor_theta_k = angles.get_theta_k()
vetor_theta_ap = angles.get_theta_ap()
vetor_theta_hr = angles.get_theta_hr()
vetor_theta_fr = angles.get_theta_fr()

# Exibição dos resultados
print("vetor_theta_hp:", vetor_theta_hp)
print("vetor_theta_k:", vetor_theta_k)
print("vetor_theta_ap:", vetor_theta_ap)
print("vetor_theta_hr:", vetor_theta_hr)
print("vetor_theta_fr:", vetor_theta_fr)
