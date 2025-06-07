import pandas as pd
import numpy as np
import time
import tracemalloc
from SegmentTree import SegmentTree

def benchmark_segment_tree():
    print("==== Benchmark: Segment Tree ====")
    # Carregar dataset
    data = pd.read_csv('energydata_complete.csv')

    # Selecionar colunas numéricas
    num_cols = data.select_dtypes(include=[np.number]).columns
    target_col = num_cols[0]  # Escolha a primeira coluna numérica como exemplo
    arr = data[target_col].values
    n = len(arr)

    # Tempo de construção (inserção) e uso de memória
    tracemalloc.start()
    start = time.perf_counter()
    st = SegmentTree(arr)
    tempo_insercao = time.perf_counter() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Coluna testada: {target_col} | Elementos: {n}")
    print(f"Tempo de construção (inserção): {tempo_insercao:.6f} s")
    print(f"Uso de memória: Atual = {current/1024:.2f} KB | Pico = {peak/1024:.2f} KB")

    # Tempo de atualização (update)
    n_updates = min(100, n)
    update_indices = np.random.choice(n, size=n_updates, replace=False)
    update_values = np.random.uniform(arr.min(), arr.max(), size=n_updates)
    tempos_update = []
    for idx, val in zip(update_indices, update_values):
        start = time.perf_counter()
        st.update(idx, val)
        tempos_update.append(time.perf_counter() - start)
    print(f"Tempo médio de atualização: {np.mean(tempos_update)*1000:.4f} ms")

    # Tempo de remoção (definindo como 0)
    tempos_remove = []
    for idx in update_indices:
        start = time.perf_counter()
        st.remove(idx)
        tempos_remove.append(time.perf_counter() - start)
    print(f"Tempo médio de remoção: {np.mean(tempos_remove)*1000:.4f} ms")

    # Tempo de busca (query de soma em intervalos aleatórios)
    n_queries = min(100, n)
    query_starts = np.random.randint(0, n-10, size=n_queries)
    query_ends = query_starts + np.random.randint(1, 10, size=n_queries)
    tempos_query = []
    for l, r in zip(query_starts, query_ends):
        r = min(r, n)  # Garante que não passa do fim do array
        start = time.perf_counter()
        _ = st.query(l, r)
        tempos_query.append(time.perf_counter() - start)
    print(f"Tempo médio de busca (query): {np.mean(tempos_query)*1000:.4f} ms")

    # Tempo médio de acesso (query aleatória)
    tempos_acesso = []
    for _ in range(n_queries):
        l = np.random.randint(0, n-1)
        r = np.random.randint(l+1, n)
        start = time.perf_counter()
        _ = st.query(l, r)
        tempos_acesso.append(time.perf_counter() - start)
    print(f"Tempo médio de acesso (query aleatória): {np.mean(tempos_acesso)*1000:.4f} ms")

    # Latência média (update + query + remove)
    latencias = []
    for idx, val in zip(update_indices, update_values):
        l = max(0, idx-2)
        r = min(n, idx+3)
        start = time.perf_counter()
        st.update(idx, val)
        st.query(l, r)
        st.remove(idx)
        latencias.append(time.perf_counter() - start)
    print(f"Latência média (update + query + remove): {np.mean(latencias)*1000:.4f} ms")

    # Escalabilidade: testando diferentes tamanhos de entrada
    print("\n--- Escalabilidade ---")
    for n_test in [100, 1000, 5000, min(10000, n)]:
        arr_test = arr[:n_test]
        tracemalloc.start()
        start = time.perf_counter()
        st_test = SegmentTree(arr_test)
        tempo_build = time.perf_counter() - start
        cur, pk = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{n_test} elementos: Construção = {tempo_build:.6f} s, Memória = {cur/1024:.2f} KB (pico {pk/1024:.2f} KB)")

if __name__ == "__main__":
    benchmark_segment_tree()