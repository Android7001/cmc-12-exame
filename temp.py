class SwingLeg(Enum):
    RIGHT = "Right"
    LEFT = "Left"

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