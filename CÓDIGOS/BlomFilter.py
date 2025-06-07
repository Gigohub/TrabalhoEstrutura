import pandas as pd
import hashlib
import math
import bitarray

# ----------------------------
# Estrutura de Bloom Filter
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

# ----------------------------
# Carregando o dataset real

try:
    df = pd.read_csv('energydata_complete.csv')
    print("Dataset carregado com sucesso.")
except FileNotFoundError:
    print("Arquivo 'energydata_complete.csv' não encontrado. Verifique o caminho e tente novamente.")
    exit()

# Selecionar colunas numéricas (int64 e float64)
colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns

print("\nColunas numéricas detectadas:")
for c in colunas_numericas:
    print(f"- {c} (tipo: {df[c].dtype})")

# Criar Bloom Filter para cada coluna numérica
bloom_filters = {}

# Parâmetros do Bloom Filter
N = len(df)  # número de elementos
p = 0.01     # taxa de falso positivo (1%)

# Tamanho ótimo do bit array e número de hashes
m = - (N * math.log(p)) / (math.log(2) ** 2)
k = (m / N) * math.log(2)

m = int(m)
k = int(k)

print(f"\nParâmetros do Bloom Filter: tamanho bit array = {m}, número de funções hash = {k}")

for coluna in colunas_numericas:
    print(f"\nCriando Bloom Filter para a coluna: {coluna}")
    bloom = BloomFilter(size=m, hash_count=k)
    valores = df[coluna].dropna().unique()
    for valor in valores:
        bloom.add(valor)
    bloom_filters[coluna] = bloom
    print(f"Bloom Filter criado com {len(valores)} valores únicos.")

# ----------------------------
# Teste de operação

col_teste = input("\nDigite o nome da coluna para testar busca com Bloom Filter: ")

if col_teste not in bloom_filters:
    print(f"Coluna '{col_teste}' não encontrada entre as colunas numéricas.")
    exit()

bloom = bloom_filters[col_teste]

while True:
    print("\nOperações disponíveis:")
    print("1 - Verificar se valor possivelmente está no conjunto")
    print("0 - Sair")
    opcao = input("Escolha a operação: ")

    if opcao == '0':
        print("Encerrando.")
        break

    if opcao != '1':
        print("Opção inválida. Tente novamente.")
        continue

    valor = input("Digite o valor (numérico): ")
    try:
        valor = float(valor)
    except ValueError:
        print("Valor inválido, deve ser numérico.")
        continue

    resultado = bloom.check(valor)
    print(f"Resultado: {'Possivelmente está presente' if resultado else 'Com certeza não está presente'}")
    