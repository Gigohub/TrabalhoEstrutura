import pandas as pd
import hashlib
from collections import defaultdict

# 1. Carregar dataset
df = pd.read_csv('energydata_complete.csv')

# 2. Função para gerar hash SHA256 de uma linha
def hash_row(row):
    row_str = ','.join(map(str, row.values))
    hash_object = hashlib.sha256(row_str.encode('utf-8'))
    return hash_object.hexdigest()

# 3. Criar coluna de hash no DataFrame
df['hash'] = df.apply(hash_row, axis=1)

# 4. Criar a Tabela Hash com detecção de duplicatas
hash_table = {}
duplicates = defaultdict(list)  # Para armazenar duplicatas

for idx, row in df.iterrows():
    hash_key = row['hash']
    
    if hash_key in hash_table:
        # Já existe: é uma duplicata
        duplicates[hash_key].append(idx)
    else:
        # Adiciona à tabela hash
        hash_table[hash_key] = row.to_dict()

# 5. Exemplo: buscar uma linha
some_hash = df.loc[0, 'hash']
result = hash_table.get(some_hash)

print(f"🔑 Hash: {some_hash}")
print(f"📄 Linha correspondente: {result}")

# 6. Relatório de duplicatas
if duplicates:
    print(f"⚠️ Foram encontradas {len(duplicates)} duplicatas de hash:")
    for h, idxs in duplicates.items():
        print(f"Hash: {h}, Linhas duplicadas: {idxs}")
else:
    print("✅ Nenhuma duplicata de hash encontrada.")

# 7. Tamanho da tabela hash
print(f"Tamanho da Tabela Hash: {len(hash_table)}")
