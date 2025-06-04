import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Carregar dados
data = pd.read_csv('energydata_complete.csv')

# Selecionar apenas as variáveis numéricas relevantes
features = data.select_dtypes(include=[np.number])

# Matriz de correlação
corr_matrix = features.corr()

# Threshold mais baixo para conexões mais densas
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

# Adicionar arestas com base no threshold
for i in corr_matrix.columns:
    for j in corr_matrix.columns:
        if i != j and abs(corr_matrix.loc[i, j]) >= threshold:
            G.add_edge(i, j, weight=corr_matrix.loc[i, j])

# Plotar
plt.figure(figsize=(12, 12))

# Layout
pos = nx.spring_layout(G, k=0.5, seed=42)

# Extrair cores dos nós
node_colors = [attr['color'] for _, attr in G.nodes(data=True)]

# Desenhar grafo
nx.draw_networkx_nodes(G, pos, node_color=node_colors, alpha=0.8, node_size=500)
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=8)

plt.title('Grafo de Correlação entre Variáveis (Threshold ≥ 0.3)', fontsize=14)
plt.axis('off')

# Salvar figura ao invés de mostrar
plt.savefig('grafo_correlacao_categorias.png')
print("✅ Grafo salvo como 'grafo_correlacao_categorias.png'.")
