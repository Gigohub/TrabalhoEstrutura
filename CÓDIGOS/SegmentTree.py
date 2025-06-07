import pandas as pd
import numpy as np

# =====================
# Classe Segment Tree
class SegmentTree:
    def __init__(self, data):
        self.n = len(data)
        self.tree = [0.0] * (2 * self.n)
        self.build(data)
    
    def build(self, data):
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]
    
    def update(self, index, value):
        index += self.n
        self.tree[index] = value
        while index > 1:
            index //= 2
            self.tree[index] = self.tree[2 * index] + self.tree[2 * index + 1]
    
    def remove(self, index):
        self.update(index, 0.0)
    
    def query(self, left, right):
        result = 0.0
        left += self.n
        right += self.n
        while left < right:
            if left % 2 == 1:
                result += self.tree[left]
                left += 1
            if right % 2 == 1:
                right -= 1
                result += self.tree[right]
            left //= 2
            right //= 2
        return result

# =====================
# Carregar dataset
data = pd.read_csv('energydata_complete.csv')

# Selecionar colunas numéricas
num_cols = data.select_dtypes(include=[np.number]).columns

# Criar Segment Trees para cada coluna
segment_trees = {}

for col in num_cols:
    print(f"✅ Criando Segment Tree para coluna: {col}")
    segment_trees[col] = SegmentTree(data[col].values)

# =====================
# Interface de operações

def consulta_soma(coluna, inicio, fim):
    if coluna not in segment_trees:
        print("❌ Coluna não encontrada.")
        return
    resultado = segment_trees[coluna].query(inicio, fim)
    print(f"✅ Soma de {coluna} no intervalo [{inicio}, {fim}): {resultado}")

def atualizar_valor(coluna, indice, novo_valor):
    if coluna not in segment_trees:
        print("❌ Coluna não encontrada.")
        return
    segment_trees[coluna].update(indice, novo_valor)
    print(f"✅ Valor atualizado na coluna {coluna}, índice {indice}, novo valor: {novo_valor}")

def remover_valor(coluna, indice):
    if coluna not in segment_trees:
        print("❌ Coluna não encontrada.")
        return
    segment_trees[coluna].remove(indice)
    print(f"✅ Valor removido (zerado) na coluna {coluna}, índice {indice}")

# =====================
# ✅ Exemplo de uso

col_teste = 'T1'
print(f"\n➡️ Exemplo de operações na coluna: {col_teste}")

consulta_soma(col_teste, 0, 10)
atualizar_valor(col_teste, 5, 100.0)
consulta_soma(col_teste, 0, 10)
remover_valor(col_teste, 5)
consulta_soma(col_teste, 0, 10)

