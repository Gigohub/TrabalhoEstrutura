import pandas as pd
import numpy as np
import networkx as nx
import time
import tracemalloc
import random

def node_color(node, categories):
    for cat, vars in categories.items():
        if node in vars:
            return {'Temp': 'tomato', 'Humidity': 'skyblue', 'Weather': 'green',
                    'Random': 'gray', 'Usage': 'gold'}[cat]
    return 'lightgray'

def benchmark_grafo():
    print("==== Benchmark: Grafo (NetworkX) ====")
    # Carregar dados
    data = pd.read_csv('energydata_complete.csv')
    data['date'] = pd.to_datetime(data['date'])
    features = data.select_dtypes(include=[np.number])
    corr_matrix = features.corr()
    threshold = 0.3

    # Categorias para cores dos nós
    categories = {
        'Temp': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T_out'],
        'Humidity': ['RH_1', 'RH_2', 'RH_3', 'RH_4', 'RH_5', 'RH_6', 'RH_7', 'RH_8', 'RH_9', 'RH_out'],
        'Weather': ['Windspeed', 'Visibility', 'Tdewpoint', 'Press_mm_hg'],
        'Random': ['rv1', 'rv2'],
        'Usage': ['Appliances', 'lights']
    }

    # === Tempo de Inserção (nós e arestas) e uso de memória ===
    tracemalloc.start()
    start = time.perf_counter()
    G = nx.Graph()
    for col in corr_matrix.columns:
        G.add_node(col, color=node_color(col, categories))
    for i in corr_matrix.columns:
        for j in corr_matrix.columns:
            if i != j and abs(corr_matrix.loc[i, j]) >= threshold:
                G.add_edge(i, j, weight=corr_matrix.loc[i, j])
    tempo_insercao = time.perf_counter() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    n_nodes = G.number_of_nodes()
    n_edges = G.number_of_edges()
    print(f"Nós inseridos: {n_nodes} | Arestas inseridas: {n_edges}")
    print(f"Tempo de inserção (total): {tempo_insercao:.6f} s")
    print(f"Uso de memória: Atual = {current/1024:.2f} KB, Pico = {peak/1024:.2f} KB")

    # === Tempo de busca (nó e aresta) ===
    busca_nos = random.sample(list(G.nodes), min(10, n_nodes))
    tempos_nos = []
    for node in busca_nos:
        start = time.perf_counter()
        _ = node in G
        tempos_nos.append(time.perf_counter() - start)
    tempo_medio_busca_no = np.mean(tempos_nos)

    busca_arestas = random.sample(list(G.edges), min(10, n_edges))
    tempos_arestas = []
    for u, v in busca_arestas:
        start = time.perf_counter()
        _ = G.has_edge(u, v)
        tempos_arestas.append(time.perf_counter() - start)
    tempo_medio_busca_aresta = np.mean(tempos_arestas)

    print(f"Tempo médio de busca de nó: {tempo_medio_busca_no*1000:.6f} ms")
    print(f"Tempo médio de busca de aresta: {tempo_medio_busca_aresta*1000:.6f} ms")

    # === Tempo de remoção (nó e aresta) ===
    # Remover e reinserir para não alterar o grafo original
    tempos_remover_nos = []
    for node in busca_nos:
        G.add_node(node)  # Garante que existe
        start = time.perf_counter()
        G.remove_node(node)
        tempos_remover_nos.append(time.perf_counter() - start)
        G.add_node(node)  # Reinsere para repetição justa

    tempos_remover_arestas = []
    for u, v in busca_arestas:
        G.add_edge(u, v)
        start = time.perf_counter()
        G.remove_edge(u, v)
        tempos_remover_arestas.append(time.perf_counter() - start)
        G.add_edge(u, v)

    print(f"Tempo médio de remoção de nó: {np.mean(tempos_remover_nos)*1000:.6f} ms")
    print(f"Tempo médio de remoção de aresta: {np.mean(tempos_remover_arestas)*1000:.6f} ms")

    # === Tempo médio de acesso (busca aleatória de nós e arestas) ===
    tempos_acesso = tempos_nos + tempos_arestas
    print(f"Tempo médio de acesso (nós/arestas): {np.mean(tempos_acesso)*1000:.6f} ms")

    # === Latência média de operações combinadas ===
    latencias = []
    for _ in range(10):
        node = random.choice(list(G.nodes))
        u, v = random.choice(list(G.edges))
        start = time.perf_counter()
        G.add_node(node)
        G.has_edge(u, v)
        G.remove_node(node)
        latencias.append(time.perf_counter() - start)
        G.add_node(node)  # Reinsere para não modificar
    print(f"Latência média (ins+busca+remoção): {np.mean(latencias)*1000:.6f} ms")

    # === Escalabilidade ===
    print("\n--- Escalabilidade ---")
    for n_feat in [5, 10, 20, len(features.columns)]:
        cols = features.columns[:n_feat]
        corr_matrix_small = features[cols].corr()
        tracemalloc.start()
        start = time.perf_counter()
        G_small = nx.Graph()
        for col in corr_matrix_small.columns:
            G_small.add_node(col, color=node_color(col, categories))
        for i in corr_matrix_small.columns:
            for j in corr_matrix_small.columns:
                if i != j and abs(corr_matrix_small.loc[i, j]) >= threshold:
                    G_small.add_edge(i, j, weight=corr_matrix_small.loc[i, j])
        t = time.perf_counter() - start
        mem, mem_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{n_feat} variáveis: Inserção = {t:.6f} s, Memória = {mem/1024:.2f} KB (pico {mem_peak/1024:.2f} KB), Nós = {G_small.number_of_nodes()}, Arestas = {G_small.number_of_edges()}")
