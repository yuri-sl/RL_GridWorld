import numpy as np

class Agente:
    def __init__(self, tamanho, alfa=0.1, gamma=0.9, epsilon=0.2):
        self.q_table = np.zeros((tamanho, tamanho, 4))  # 4 ações
        self.alfa = alfa
        self.gamma = gamma
        self.epsilon = epsilon
        self.tamanho = tamanho

    def escolher_acao(self, estado):
        x, y = estado
        if np.random.rand() < self.epsilon:
            return np.random.randint(4)
        return np.argmax(self.q_table[x, y])

    def atualizar(self, estado, acao, recompensa, novo_estado):
        x, y = estado
        nx, ny = novo_estado
        valor_atual = self.q_table[x, y, acao]
        melhor_valor = np.max(self.q_table[nx, ny])
        self.q_table[x, y, acao] = valor_atual + self.alfa * (recompensa + self.gamma * melhor_valor - valor_atual)
