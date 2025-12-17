from ambiente import Ambiente
from agente import Agente
import matplotlib.pyplot as plt

cenarios = ["simples", "medio", "complexo"]
episodios = 500

env = Ambiente(tamanho=10, cenario = "medio")
agent = Agente(tamanho=10)

recompensas = []
for _ in range(episodios):
    estado = env.reset()
    total = 0
    for _ in range(100):
        acao = agent.escolher_acao(estado)
        novo_estado, r, terminado = env.step(acao)
        agent.atualizar(estado, acao, r, novo_estado)
        estado = novo_estado
        total += r
        if terminado:
            break
    recompensas.append(total)

plt.plot(recompensas, label="medio")

plt.title("Recompensa por episódio em diferentes cenários")
plt.xlabel("Episódio")
plt.ylabel("Recompensa total")
plt.legend()
plt.grid(True)
plt.show()
