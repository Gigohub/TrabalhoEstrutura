import pandas as pd
import hashlib
import time
import tracemalloc
import numpy as np
from collections import defaultdict

def hash_row(row):
    row_str = ','.join(map(str, row.values))
    hash_object = hashlib.sha256(row_str.encode('utf-8'))
    return hash_object.hexdigest()

def benchmark_hashing():
    print("==== Benchmark: Hashing ====")
    # Carregar dataset
    df = pd.read_csv('energydata_complete.csv')
    
    # Gerar coluna de hash
    start = time.perf_counter()
    df['hash'] = df.apply(hash_row, axis=1)
    tempo_hash = time.perf_counter() - start

    # Preparação para benchmarking
    hash_table = {}
    duplicates = defaultdict(list)
    indices = df.index.tolist()
    n = len(df)
    
    # Tempo de inserção, uso de memória, taxa de colisão
    tracemalloc.start()
    colisoes = 0
    start = time.perf_counter()
    for idx, row in df.iterrows():
        hash_key = row['hash']
        if hash_key in hash_table:
            colisoes += 1
            duplicates[hash_key].append(idx)
        else:
            hash_table[hash_key] = row.to_dict()
    tempo_insercao = time.perf_counter() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"Linhas inseridas: {n}")
    print(f"Tempo total para gerar hashes: {tempo_hash:.4f} s")
    print(f"Tempo total de inserção na tabela hash: {tempo_insercao:.4f} s")
    print(f"Uso de memória hash table: Atual = {current/1024:.2f} KB | Pico = {peak/1024:.2f} KB")
    print(f"Taxa de colisão: {colisoes}/{n} = {colisoes/n:.4%}")

    # Tempo de busca (por índice aleatório)
    n_buscas = min(100, n)
    busca_indices = np.random.choice(indices, size=n_buscas, replace=False)
    tempos_busca = []
    for idx in busca_indices:
        row = df.loc[idx]
        hash_key = row['hash']
        start = time.perf_counter()
        _ = hash_table.get(hash_key)
        tempos_busca.append(time.perf_counter() - start)
    tempo_medio_busca = np.mean(tempos_busca)
    print(f"Tempo médio de busca: {tempo_medio_busca*1000:.4f} ms")

    # Tempo de remoção (por índice aleatório)
    tempos_remover = []
    for idx in busca_indices:
        row = df.loc[idx]
        hash_key = row['hash']
        # Reinsere antes para garantir remoção
        hash_table[hash_key] = row.to_dict()
        start = time.perf_counter()
        if hash_key in hash_table:
            del hash_table[hash_key]
        tempos_remover.append(time.perf_counter() - start)
        # Reinsere para não alterar o estado para outras buscas/rem
        hash_table[hash_key] = row.to_dict()
    tempo_medio_remover = np.mean(tempos_remover)
    print(f"Tempo médio de remoção: {tempo_medio_remover*1000:.4f} ms")

    # Tempo médio de acesso (busca por hash)
    tempos_acesso = []
    for idx in busca_indices:
        row = df.loc[idx]
        hash_key = row['hash']
        start = time.perf_counter()
        _ = hash_table.get(hash_key)
        tempos_acesso.append(time.perf_counter() - start)
    print(f"Tempo médio de acesso (busca hash): {np.mean(tempos_acesso)*1000:.4f} ms")
    
    # Latência média (inserção + busca + remoção)
    latencias = []
    for idx in busca_indices:
        row = df.loc[idx]
        hash_key = row['hash']
        start = time.perf_counter()
        hash_table[hash_key] = row.to_dict()
        _ = hash_table.get(hash_key)
        if hash_key in hash_table:
            del hash_table[hash_key]
        latencias.append(time.perf_counter() - start)
        # Reinsere para não afetar próximas rodadas
        hash_table[hash_key] = row.to_dict()
    print(f"Latência média (ins + busca + rem): {np.mean(latencias)*1000:.4f} ms")

    # Escalabilidade com teste de colisões
    print("\n--- Escalabilidade (com teste de colisões) ---")
    for n_test in [100, 500, 1000, min(5000, n)]:
        hash_table_test = {}
        colisoes_test = 0
        test_indices = indices[:n_test]
        start = time.perf_counter()
        for idx in test_indices:
            row = df.loc[idx]
            hash_key = row['hash']
            if hash_key in hash_table_test:
                colisoes_test += 1
            else:
                hash_table_test[hash_key] = row.to_dict()
        t = time.perf_counter() - start
        print(f"{n_test} elementos: Inserção = {t:.6f} s, Colisões = {colisoes_test}, Taxa = {colisoes_test/n_test:.4%}")
    
if __name__ == "__main__":
    benchmark_hashing()