import pandas as pd
import numpy as np
import time
import tracemalloc
from SkipList import SkipList

def benchmark_skiplist():
    print("==== Benchmark: Skip List ====")
    # Carregar dataset
    df = pd.read_csv('energydata_complete.csv')
    colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
    target_col = colunas_numericas[0]  # Escolhe a primeira coluna numérica para o teste
    valores = df[target_col].dropna().unique()
    n = len(valores)

    # Parâmetros da Skip List
    max_lvl = 4
    P = 0.5

    # Tempo de inserção e uso de memória
    tracemalloc.start()
    start = time.perf_counter()
    skiplist = SkipList(max_lvl=max_lvl, P=P)
    for v in valores:
        skiplist.insertElement(v)
    tempo_insercao = time.perf_counter() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Coluna testada: {target_col} | Elementos únicos inseridos: {n}")
    print(f"Tempo de inserção (total): {tempo_insercao:.6f} s")
    print(f"Uso de memória: Atual = {current/1024:.2f} KB | Pico = {peak/1024:.2f} KB")

    # Tempo de busca (search)
    n_buscas = min(100, n)
    busca_amostras = np.random.choice(valores, size=n_buscas, replace=False)
    tempos_busca = []
    for val in busca_amostras:
        start = time.perf_counter()
        _ = skiplist.searchElement(val)
        tempos_busca.append(time.perf_counter() - start)
    print(f"Tempo médio de busca: {np.mean(tempos_busca)*1000:.4f} ms")

    # Tempo de remoção (delete)
    tempos_remover = []
    for val in busca_amostras:
        skiplist.insertElement(val)  # Garante que está presente
        start = time.perf_counter()
        skiplist.deleteElement(val)
        tempos_remover.append(time.perf_counter() - start)
        skiplist.insertElement(val)  # Reinsere para não alterar para as próximas buscas
    print(f"Tempo médio de remoção: {np.mean(tempos_remover)*1000:.4f} ms")

    # Tempo de atualização (update)
    tempos_update = []
    for val in busca_amostras:
        novo_val = val + 0.123  # valor diferente para atualização
        skiplist.insertElement(val)  # Garante presença
        start = time.perf_counter()
        skiplist.updateElement(val, novo_val)
        tempos_update.append(time.perf_counter() - start)
        skiplist.deleteElement(novo_val)  # Limpa para não acumular
        skiplist.insertElement(val)  # Restaura estado
    print(f"Tempo médio de atualização: {np.mean(tempos_update)*1000:.4f} ms")

    # Tempo médio de acesso (busca)
    tempos_acesso = []
    for val in busca_amostras:
        start = time.perf_counter()
        _ = skiplist.searchElement(val)
        tempos_acesso.append(time.perf_counter() - start)
    print(f"Tempo médio de acesso (busca): {np.mean(tempos_acesso)*1000:.4f} ms")

    # Latência média (ins + busca + rem)
    latencias = []
    for val in busca_amostras:
        novo_val = val + 0.555
        start = time.perf_counter()
        skiplist.insertElement(novo_val)
        skiplist.searchElement(novo_val)
        skiplist.deleteElement(novo_val)
        latencias.append(time.perf_counter() - start)
    print(f"Latência média (ins + busca + rem): {np.mean(latencias)*1000:.4f} ms")

    # Escalabilidade: diferentes tamanhos de entrada
    print("\n--- Escalabilidade ---")
    for n_test in [100, 500, 1000, min(5000, n)]:
        vals = valores[:n_test]
        tracemalloc.start()
        start = time.perf_counter()
        skiplist_test = SkipList(max_lvl=max_lvl, P=P)
        for v in vals:
            skiplist_test.insertElement(v)
        tempo_ins = time.perf_counter() - start
        cur, pk = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        print(f"{n_test} elementos: Inserção = {tempo_ins:.6f} s, Memória = {cur/1024:.2f} KB (pico {pk/1024:.2f} KB)")

if __name__ == "__main__":
    benchmark_skiplist()