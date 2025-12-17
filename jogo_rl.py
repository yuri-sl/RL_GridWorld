import pygame
import numpy as np
import time
import random

# Configurações
TAMANHO_GRID = 10
TAMANHO_CELULA = 60
TAMANHO_TELA = TAMANHO_GRID * TAMANHO_CELULA
FPS = 10

# Cores
CINZA = (200, 200, 200)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 100, 255)
BRANCO = (255, 255, 255)

# Ambiente
armadilhas = [(3, 3), (4, 4), (5, 5)]
objetivo = (9, 9)
estado_inicial = (0, 0)

trap_set_one = [(3, 3), (4, 4), (5, 5), (6, 6)]
trap_set_two = [
        (2, 2), (2, 3), (2, 4),
        (4, 5), (5, 5), (6, 5),
        (7, 2), (7, 3),
    ]
trap_set_three = [
        (0, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
        (0, 3), (2, 3), (3, 3), (5, 3),
        (0, 2), (1, 2), (7, 2), (8, 2),
        (0, 1), (1, 1), (3, 1), (5, 1), (6, 1), (7, 1),(6,9),(6,8),(6,7),(5,6),(5,5),
        (3, 0), (4, 0), (5, 0),(8,3),(8,4)
    ]
print("Insira o nível de dificuldade: simples, medio, complexo \n")
ans_challange_lvl = input()
match(ans_challange_lvl):
    case "complexo":
        armadilhas = trap_set_one
    case "medio":
        armadilhas = trap_set_two
    case "simples":
        armadilhas = trap_set_three

# Inicializa Q-table
q_table = np.zeros((TAMANHO_GRID, TAMANHO_GRID, 4))  # 4 ações: cima, baixo, esquerda, direita

# Parâmetros de RL
alfa = 0.1
gamma = 0.9
epsilon = 0.2

# Funções
def escolher_acao(pos):
    if random.random() < epsilon:
        return random.randint(0, 3)
    x, y = pos
    return np.argmax(q_table[x, y])

def mover(pos, acao):
    x, y = pos
    movimentos = [(-1,0),(1,0),(0,-1),(0,1)]  # cima, baixo, esquerda, direita
    dx, dy = movimentos[acao]
    nx, ny = x + dx, y + dy
    if 0 <= nx < TAMANHO_GRID and 0 <= ny < TAMANHO_GRID:
        return (nx, ny)
    return (x, y)

def calcular_recompensa(pos):
    if pos in armadilhas:
        return -10, True
    if pos == objetivo:
        return 10, True
    return -1, False

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((TAMANHO_TELA, TAMANHO_TELA))
relogio = pygame.time.Clock()
pygame.display.set_caption("Agente Aprendendo (Q-Learning)")

# Loop de treinamento
episodios = 1000
for episodio in range(episodios):
    estado = estado_inicial
    for _ in range(100):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

        acao = escolher_acao(estado)
        novo_estado = mover(estado, acao)
        recompensa, terminal = calcular_recompensa(novo_estado)

        #Q-Table calculo
        x, y = estado
        nx, ny = novo_estado
        q_atual = q_table[x, y, acao]
        melhor_q_novo_estado = np.max(q_table[nx, ny])
        q_table[x, y, acao] += alfa * (recompensa + gamma * melhor_q_novo_estado - q_atual)

        estado = novo_estado

        # Desenhar ambiente
        tela.fill(BRANCO)
        for i in range(TAMANHO_GRID):
            for j in range(TAMANHO_GRID):
                pygame.draw.rect(tela, CINZA, (j*TAMANHO_CELULA, i*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA), 1)

        for trap in armadilhas:
            pygame.draw.rect(tela, VERMELHO, (trap[1]*TAMANHO_CELULA, trap[0]*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

        pygame.draw.rect(tela, VERDE, (objetivo[1]*TAMANHO_CELULA, objetivo[0]*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))
        pygame.draw.rect(tela, AZUL, (estado[1]*TAMANHO_CELULA, estado[0]*TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA))

        pygame.display.flip()
        relogio.tick(FPS)

        if terminal:
            break

# Finalização
pygame.quit()
