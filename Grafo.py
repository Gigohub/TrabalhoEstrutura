import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Carregar dados
data = pd.read_csv('energydata_complete.csv')

# Selecionar variáveis numéricas
features = data.select_dtypes(include=[np.number])

# Matriz de correlação
corr_matrix = features.corr()

# Threshold ajustável pelo usuário
try:
    threshold = float(input("Informe o threshold para correlação (ex.: 0.3): ") or 0.3)
except ValueError:
    print("❌ Threshold inválido. Usando padrão de 0.3.")
    threshold = 0.3

# Criar grafo
G = nx.Graph()

# Categorias
categories = {
    'Temp': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T_out'],
    'Humidity': ['RH_1', 'RH_2', 'RH_3', 'RH_4', 'RH_5', 'RH_6', 'RH_7', 'RH_8', 'RH_9', 'RH_out'],
    'Weather': ['Windspeed', 'Visibility', 'Tdewpoint', 'Press_mm_hg'],
    'Random': ['rv1', 'rv2'],
    'Usage': ['Appliances', 'lights']
}

# Função para definir cor
def node_color(node):
    for cat, vars in categories.items():
        if node in vars:
            return {'Temp': 'tomato', 'Humidity': 'skyblue', 'Weather': 'green',
                    'Random': 'gray', 'Usage': 'gold'}[cat]
    return 'lightgray'

# Adiciona nós com cores
for col in corr_matrix.columns:
    G.add_node(col, color=node_color(col))

# Loop otimizado: triangular superior da matriz
for i, var1 in enumerate(corr_matrix.columns):
    for var2 in corr_matrix.columns[i+1:]:
        weight = corr_matrix.loc[var1, var2]
        if abs(weight) >= threshold:
            G.add_edge(var1, var2, weight=weight)

# Plotar
plt.figure(figsize=(12, 12))

# Layout
pos = nx.spring_layout(G, k=0.5, seed=42)

# Cores dos nós
node_colors = [attr['color'] for _, attr in G.nodes(data=True)]

# Tamanho do nó proporcional ao grau
node_sizes = [300 + 100 * G.degree(n) for n in G.nodes()]

# Largura da aresta proporcional à força da correlação
edge_widths = [abs(G[u][v]['weight']) * 3 for u, v in G.edges()]

# Desenhar grafo
nx.draw_networkx_nodes(G, pos, node_color=node_colors, alpha=0.8, node_size=node_sizes)
nx.draw_networkx_edges(G, pos, alpha=0.5, width=edge_widths)
nx.draw_networkx_labels(G, pos, font_size=8)

plt.title(f'Grafo de Correlação entre Variáveis (Threshold ≥ {threshold})', fontsize=14)
plt.axis('off')

# Salvar figura
plt.savefig('grafo_correlacao_categorias.png')
print(f"✅ Grafo salvo como 'grafo_correlacao_categorias.png'.")
