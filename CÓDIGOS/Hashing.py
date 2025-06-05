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

# 4. Tabela Hash e duplicatas
hash_table = {}
duplicates = defaultdict(list)  # Para armazenar duplicatas

def inserir_linha(indice):
    row = df.loc[indice]
    hash_key = row['hash']
    if hash_key in hash_table:
        print(f"⚠️ Linha {indice} já está presente na tabela hash (duplicata).")
        duplicates[hash_key].append(indice)
    else:
        hash_table[hash_key] = row.to_dict()
        print(f"✅ Linha {indice} inserida na tabela hash.")

def remover_linha(indice):
    row = df.loc[indice]
    hash_key = row['hash']
    if hash_key in hash_table:
        del hash_table[hash_key]
        print(f"✅ Linha {indice} removida da tabela hash.")
    else:
        print(f"❌ Linha {indice} não encontrada na tabela hash.")

def buscar_por_indice(indice):
    row = df.loc[indice]
    hash_key = row['hash']
    result = hash_table.get(hash_key)
    if result:
        print(f"🔎 Linha encontrada: {result}")
    else:
        print("❌ Linha não encontrada na tabela hash.")

def buscar_por_hash(hash_key):
    result = hash_table.get(hash_key)
    if result:
        print(f"🔎 Linha correspondente ao hash {hash_key}: {result}")
    else:
        print("❌ Hash não encontrado na tabela hash.")

def relatorio_duplicatas():
    if duplicates:
        print(f"⚠️ Foram encontradas {len(duplicates)} duplicatas de hash:")
        for h, idxs in duplicates.items():
            print(f"Hash: {h}, Linhas duplicadas: {idxs}")
    else:
        print("✅ Nenhuma duplicata de hash encontrada.")

# Preenche a tabela hash inicialmente
for idx, row in df.iterrows():
    inserir_linha(idx)

print(f"Tamanho inicial da Tabela Hash: {len(hash_table)}")

# Menu interativo
while True:
    print("\nOperações disponíveis:")
    print("1 - Buscar linha por índice")
    print("2 - Inserir linha por índice")
    print("3 - Remover linha por índice")
    print("4 - Buscar linha por hash")
    print("5 - Relatório de duplicatas")
    print("0 - Sair")
    opcao = input("Escolha a operação: ")
    if opcao == '0':
        print("Encerrando.")
        break
    elif opcao == '1':
        indice = int(input("Digite o índice da linha: "))
        buscar_por_indice(indice)
    elif opcao == '2':
        indice = int(input("Digite o índice da linha para inserir: "))
        inserir_linha(indice)
    elif opcao == '3':
        indice = int(input("Digite o índice da linha para remover: "))
        remover_linha(indice)
    elif opcao == '4':
        hash_key = input("Digite o hash (em hexadecimal): ")
        buscar_por_hash(hash_key)
    elif opcao == '5':
        relatorio_duplicatas()
    else:
        print("Opção inválida. Tente novamente.")