import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# ✅ Carregar dados
data = pd.read_csv('energydata_complete.csv')

# ✅ Conversão de 'date'
data['date'] = pd.to_datetime(data['date'])

# ✅ Seleção de colunas numéricas + data
cols_numericas = data.select_dtypes(include=[np.number]).columns.tolist()
cols_utilizadas = ['date'] + cols_numericas
df = data[cols_utilizadas]

# ✅ Filtro: horário de pico (18h-23h)
df_pico = df[(df['date'].dt.hour >= 18) & (df['date'].dt.hour <= 23)]

# ✅ Ordenar por 'Appliances' (descendente)
df_pico = df_pico.sort_values(by='Appliances', ascending=False).reset_index(drop=True)

# ✅ Gráfico 1: Evolução Temporal do Consumo

plt.figure(figsize=(12, 6))
plt.plot(df_pico['date'], df_pico['Appliances'], color='tomato', linewidth=1)
plt.title('Evolução Temporal do Consumo de Energia (Horário de Pico)', fontsize=14)
plt.xlabel('Data e Hora')
plt.ylabel('Consumo (Wh)')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# ✅ Salvar figura
plt.savefig('evolucao_temporal_consumo.png')
print("✅ Gráfico 'evolucao_temporal_consumo.png' salvo com sucesso.")

plt.close()

# ✅ Gráfico 2: Ranking de Consumo - Top 10 maiores valores

top10 = df_pico.head(10)

plt.figure(figsize=(10, 6))
bars = plt.bar(top10['date'].dt.strftime('%Y-%m-%d %H:%M'), top10['Appliances'], color='goldenrod')
plt.title('Top 10 Maiores Consumos de Energia (Horário de Pico)', fontsize=14)
plt.xlabel('Data e Hora')
plt.ylabel('Consumo (Wh)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# ✅ Rótulos
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, f'{int(yval)}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()

# ✅ Salvar figura
plt.savefig('ranking_top10_consumo.png')
print("✅ Gráfico 'ranking_top10_consumo.png' salvo com sucesso.")

plt.close()

# Selecionar apenas as variáveis numéricas relevantes
features = data.select_dtypes(include=[np.number])

# Matriz de correlação
corr_matrix = features.corr()

# Threshold mais baixo para conexões mais densas
threshold = 0.3

# Criar grafo
G = nx.Graph()

# Adicionar nós ao grafo com categorias
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

# Adiciona nós
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

# Cores
node_colors = [data['color'] for _, data in G.nodes(data=True)]

# Desenhar grafo
nx.draw_networkx_nodes(G, pos, node_color=node_colors, alpha=0.8, node_size=500)
nx.draw_networkx_edges(G, pos, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=8)

plt.title('Grafo de Correlação entre Variáveis (Threshold ≥ 0.3)', fontsize=14)
plt.axis('off')
plt.savefig("Grafo.png")
print("✅ Gráfico 'Grafo.png' salvo com sucesso.")
