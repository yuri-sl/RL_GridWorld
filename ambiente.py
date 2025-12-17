import numpy as np

class Ambiente:
    def __init__(self, tamanho=10,cenario="simples"):
        self.tamanho = tamanho
        self.estado_inicial = (0, 0)
        self.objetivo = (tamanho - 1, tamanho - 1)
        self.definir_armadilhas(cenario)
        self.armadilhas = [(3, 3), (4, 4), (5, 5)]
        self.reset()
    def definir_armadilhas(self,cenario:str):
        if (cenario == "complexo"):
            self.armadilhas = [(3, 3), (4, 4), (5, 5), (6, 6)]
        elif (cenario == "medio"):
            self.armadilhas = [
                (2, 2), (2, 3), (2, 4),
                (4, 5), (5, 5), (6, 5),
                (7, 2), (7, 3),
            ]
        elif(cenario == "facil"):
            self.armadilhas = [
                (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4),
                (0, 3), (1, 3), (2, 3), (3, 3), (5, 3), (6, 3),
                (0, 2), (1, 2), (6, 2), (7, 2), (8, 2),
                (0, 1), (1, 1), (2, 1), (3, 1), (5, 1), (6, 1), (7, 1),
                (2, 0), (3, 0), (4, 0), (5, 0),
            ]
        else:
            raise ValueError(f"Cenário desconhecido: {cenario}")

    def reset(self):
        self.agente_pos = self.estado_inicial
        return self.agente_pos

    def estado_valido(self, pos):
        x, y = pos
        return 0 <= x < self.tamanho and 0 <= y < self.tamanho

    #Função de recompensa
    def step(self, acao):
        x, y = self.agente_pos
        movimentos = {
            0: (-1, 0),  # cima
            1: (1, 0),   # baixo
            2: (0, -1),  # esquerda
            3: (0, 1),   # direita
        }
        dx, dy = movimentos[acao]
        nova_pos = (x + dx, y + dy)

        if self.estado_valido(nova_pos):
            self.agente_pos = nova_pos

        recompensa = -1
        terminado = False

        if self.agente_pos in self.armadilhas:
            recompensa = -10
            terminado = True
        elif self.agente_pos == self.objetivo:
            recompensa = 10
            terminado = True

        return self.agente_pos, recompensa, terminado
