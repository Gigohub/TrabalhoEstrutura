import pandas as pd
import math
import time
import tracemalloc
import numpy as np
import bitarray
import hashlib

# Classe Bloom Filter
class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray.bitarray(size)
        self.bit_array.setall(0)

    def _hashes(self, item):
        hashes = []
        item_str = str(item).encode('utf-8')
        for i in range(self.hash_count):
            hash_result = int(hashlib.sha256(item_str + str(i).encode()).hexdigest(), 16)
            hashes.append(hash_result % self.size)
        return hashes

    def add(self, item):
        for hash_val in self._hashes(item):
            self.bit_array[hash_val] = 1

    def check(self, item):
        return all(self.bit_array[hash_val] for hash_val in self._hashes(item))

def benchmark_bloom_filter():
    print("==== Benchmark: Bloom Filter ====")
    # Carregar dados
    df = pd.read_csv('energydata_complete.csv')
    colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns
    target_col = colunas_numericas[0]  # Usar a primeira coluna numérica como exemplo

    valores = df[target_col].dropna().unique()
    N = len(valores)
    p = 0.01  # taxa de falso positivo
    m = int(- (N * math.log(p)) / (math.log(2) ** 2))
    k = int((m / N) * math.log(2))

    # ======================
    # Tempo de inserção
    bloom = BloomFilter(size=m, hash_count=k)

    tracemalloc.start()
    start = time.perf_counter()
    for v in valores:
        bloom.add(v)
    tempo_insercao = time.perf_counter() - start
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"Coluna testada: {target_col}")
    print(f"Elementos inseridos: {N}")
    print(f"Tamanho do bit array: {m}, Nº de funções hash: {k}")
    print(f"Tempo total de inserção: {tempo_insercao:.4f} s")
    print(f"Uso de memória: Atual = {current/1024:.2f} KB, Pico = {peak/1024:.2f} KB")

    # ======================
    # Tempo de busca e taxa de falso positivo
    n_buscas = 1000
    presentes = np.random.choice(valores, size=min(n_buscas, len(valores)), replace=False)
    ausentes = np.random.uniform(
        low=valores.min() - 1000, high=valores.max() + 1000, size=n_buscas
    )
    # Garante que ausentes não estão no conjunto original
    ausentes = [x for x in ausentes if x not in valores][:n_buscas]

    tempos = []
    for val in presentes:
        start = time.perf_counter()
        _ = bloom.check(val)
        tempos.append(time.perf_counter() - start)
    tempo_medio_busca = np.mean(tempos)

    # Taxa de falso positivo: busca de elementos ausentes
    falsos_positivos = 0
    for val in ausentes:
        if bloom.check(val):
            falsos_positivos += 1
    taxa_fp = falsos_positivos / len(ausentes) if len(ausentes) > 0 else 0

    print(f"Tempo médio de busca (presentes): {tempo_medio_busca*1000:.4f} ms")
    print(f"Taxa de falso positivo (busca de ausentes): {taxa_fp:.2%}")

    # ======================
    # Escalabilidade: variar o tamanho do conjunto
    print("\n--- Escalabilidade ---")
    for n_test in [100, 500, 1000, min(5000, N)]:
        val_test = valores[:n_test]
        m_test = int(- (n_test * math.log(p)) / (math.log(2) ** 2))
        k_test = max(1, int((m_test / n_test) * math.log(2)))
        bloom_test = BloomFilter(size=m_test, hash_count=k_test)
        start = time.perf_counter()
        for v in val_test:
            bloom_test.add(v)
        tempo_ins = time.perf_counter() - start
        print(f"{n_test} elementos: Inserção = {tempo_ins:.4f} s, Bit array = {m_test}, N hash = {k_test}")

    # ======================
    # Latência média (inserção + busca)
    latencias = []
    n_lat = min(100, len(valores))
    amostras = np.random.choice(valores, size=n_lat, replace=False)
    for val in amostras:
        start = time.perf_counter()
        bloom.add(val)         # re-inserir (não tem efeito, mas simula operação)
        bloom.check(val)
        latencias.append(time.perf_counter() - start)
    print(f"Latência média (ins + busca): {np.mean(latencias)*1000:.4f} ms")

if __name__ == "__main__":
    benchmark_bloom_filter()