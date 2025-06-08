import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# =========================
# Funções para estrutura de dados (grafo)
class MeuGrafo:
    def __init__(self):
        self.G = nx.Graph()

    def inserir_no(self, node, **attrs):
        if node not in self.G:
            self.G.add_node(node, **attrs)
            print(f"✅ Nó '{node}' inserido.")
        else:
            print(f"⚠️ Nó '{node}' já existe no grafo.")

    def inserir_aresta(self, u, v, **attrs):
        self.G.add_edge(u, v, **attrs)
        print(f"✅ Aresta '{u} <-> {v}' inserida.")

    def remover_no(self, node):
        if node in self.G:
            self.G.remove_node(node)
            print(f"✅ Nó '{node}' removido.")
        else:
            print(f"❌ Nó '{node}' não encontrado.")

    def remover_aresta(self, u, v):
        if self.G.has_edge(u, v):
            self.G.remove_edge(u, v)
            print(f"✅ Aresta '{u} <-> {v}' removida.")
        else:
            print(f"❌ Aresta '{u} <-> {v}' não encontrada.")

    def buscar_no(self, node):
        if node in self.G:
            print(f"🔎 Nó '{node}' encontrado.")
            return True
        else:
            print(f"❌ Nó '{node}' não encontrado.")
            return False

    def buscar_aresta(self, u, v):
        if self.G.has_edge(u, v):
            print(f"🔎 Aresta '{u} <-> {v}' encontrada.")
            return True
        else:
            print(f"❌ Aresta '{u} <-> {v}' não encontrada.")
            return False

    def plotar(self, title="Grafo"):
        plt.figure(figsize=(12, 12))
        pos = nx.spring_layout(self.G, k=0.5, seed=42)
        node_colors = [self.G.nodes[n].get('color', 'lightgray') for n in self.G.nodes()]
        nx.draw_networkx_nodes(self.G, pos, node_color=node_colors, alpha=0.8, node_size=500)
        nx.draw_networkx_edges(self.G, pos, alpha=0.5)
        nx.draw_networkx_labels(self.G, pos, font_size=8)
        plt.title(title, fontsize=14)
        plt.axis('off')
        plt.savefig('IMAGENS/Grafo.png')
        print("Imagem salva de 'Grafo.png")

# =========================
# Carregar e preparar dados
data = pd.read_csv('energydata_complete.csv')
data['date'] = pd.to_datetime(data['date'])
cols_numericas = data.select_dtypes(include=[np.number]).columns.tolist()
cols_utilizadas = ['date'] + cols_numericas
df = data[cols_utilizadas]
df_pico = df[(df['date'].dt.hour >= 18) & (df['date'].dt.hour <= 23)]
df_pico = df_pico.sort_values(by='Appliances', ascending=False).reset_index(drop=True)

# =========================
# Construção inicial do grafo de correlação
features = data.select_dtypes(include=[np.number])
corr_matrix = features.corr()
threshold = 0.3

categorias = {
    'Temp': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T_out'],
    'Humidity': ['RH_1', 'RH_2', 'RH_3', 'RH_4', 'RH_5', 'RH_6', 'RH_7', 'RH_8', 'RH_9', 'RH_out'],
    'Weather': ['Windspeed', 'Visibility', 'Tdewpoint', 'Press_mm_hg'],
    'Random': ['rv1', 'rv2'],
    'Usage': ['Appliances', 'lights']
}
def node_color(node):
    for cat, vars in categorias.items():
        if node in vars:
            return {'Temp': 'tomato', 'Humidity': 'skyblue', 'Weather': 'green',
                    'Random': 'gray', 'Usage': 'gold'}[cat]
    return 'lightgray'

meu_grafo = MeuGrafo()

# Adicionar nós e arestas iniciais
for col in corr_matrix.columns:
    meu_grafo.inserir_no(col, color=node_color(col))
for i in corr_matrix.columns:
    for j in corr_matrix.columns:
        if i != j and abs(corr_matrix.loc[i, j]) >= threshold:
            meu_grafo.inserir_aresta(i, j, weight=corr_matrix.loc[i, j])

# =========================
# Menu interativo para operações básicas
while True:
    print("\nOperações disponíveis:")
    print("1 - Inserir nó")
    print("2 - Inserir aresta")
    print("3 - Remover nó")
    print("4 - Remover aresta")
    print("5 - Buscar nó")
    print("6 - Buscar aresta")
    print("7 - Plotar grafo")
    print("0 - Sair")
    opcao = input("Escolha a operação: ")

    if opcao == '0':
        print("Encerrando.")
        break
    elif opcao == '1':
        node = input("Nome do nó: ")
        meu_grafo.inserir_no(node)
    elif opcao == '2':
        u = input("Nó de origem: ")
        v = input("Nó de destino: ")
        meu_grafo.inserir_aresta(u, v)
    elif opcao == '3':
        node = input("Nome do nó: ")
        meu_grafo.remover_no(node)
    elif opcao == '4':
        u = input("Nó de origem: ")
        v = input("Nó de destino: ")
        meu_grafo.remover_aresta(u, v)
    elif opcao == '5':
        node = input("Nome do nó: ")
        meu_grafo.buscar_no(node)
    elif opcao == '6':
        u = input("Nó de origem: ")
        v = input("Nó de destino: ")
        meu_grafo.buscar_aresta(u, v)
    elif opcao == '7':
        meu_grafo.plotar(title="Grafo de Correlação (modificado)")
    else:
        print("Opção inválida. Tente novamente.")