import random
import pandas as pd

# ----------------------------
# Estrutura de Nó para Skip List
class Node:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)

# ----------------------------
# Estrutura da Skip List
class SkipList:
    def __init__(self, max_lvl, P):
        self.MAXLVL = max_lvl
        self.P = P
        self.header = self.createNode(self.MAXLVL, None)
        self.level = 0

    def createNode(self, lvl, key):
        return Node(key, lvl)

    def randomLevel(self):
        lvl = 0
        while random.random() < self.P and lvl < self.MAXLVL:
            lvl += 1
        return lvl

    def insertElement(self, key):
        update = [None] * (self.MAXLVL + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.key != key:  # evitar repetidos
            rlevel = self.randomLevel()
            if rlevel > self.level:
                for i in range(self.level + 1, rlevel + 1):
                    update[i] = self.header
                self.level = rlevel

            n = self.createNode(rlevel, key)
            for i in range(rlevel + 1):
                n.forward[i] = update[i].forward[i]
                update[i].forward[i] = n

    def searchElement(self, key, verbose=False):
        current = self.header
        path = []
        for i in range(self.level, -1, -1):
            pos = 0
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
                pos += 1
            path.append((i, pos, current.key if current.key is not None else 'Header'))
        current = current.forward[0]
        if current and current.key == key:
            if verbose:
                pass  # Retirado o print
            return True
        else:
            if verbose:
                pass  # Retirado o print
            return False

    def deleteElement(self, key):
        update = [None] * (self.MAXLVL + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    continue
                update[i].forward[i] = current.forward[i]

            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
            # Removido o print
        else:
            # Removido o print
            pass

    def updateElement(self, old_key, new_key):
        if self.searchElement(old_key):
            self.deleteElement(old_key)
            self.insertElement(new_key)
            # Removido o print
        else:
            # Removido o print
            pass

    def displayList(self):
        # Removido o print da Skip List
        pass

# ----------------------------
# Carregando o dataset real

try:
    df = pd.read_csv('energydata_complete.csv')
except FileNotFoundError:
    print("Arquivo 'energydata_complete.csv' não encontrado. Verifique o caminho e tente novamente.")
    exit()

# Selecionar colunas numéricas (int64 e float64)
colunas_numericas = df.select_dtypes(include=['float64', 'int64']).columns

# Criar Skip List para cada coluna numérica
skip_lists = {}

for coluna in colunas_numericas:
    skip_list = SkipList(max_lvl=4, P=0.5)
    valores = df[coluna].dropna().unique()
    for valor in valores:
        skip_list.insertElement(valor)
    skip_lists[coluna] = skip_list

# Interação para testar operações em uma coluna específica
col_teste = input("\nDigite o nome da coluna para testar buscas e atualizações: ")

if col_teste not in skip_lists:
    print(f"Coluna '{col_teste}' não encontrada entre as colunas numéricas.")
    exit()

skip = skip_lists[col_teste]

while True:
    print("\nOperações disponíveis:")
    print("1 - Buscar valor")
    print("2 - Remover valor")
    print("3 - Inserir valor")
    print("4 - Atualizar valor")
    print("0 - Sair")
    opcao = input("Escolha a operação: ")

    if opcao == '0':
        print("Encerrando.")
        break

    if opcao not in ['1','2','3','4','5']:
        print("Opção inválida. Tente novamente.")
        continue

    valor = input("Digite o valor (numérico): ")
    try:
        valor = float(valor)
    except ValueError:
        print("Valor inválido, deve ser numérico.")
        continue

    if opcao == '1':
        encontrado = skip.searchElement(valor, verbose=True)
        print(f"Busca: {'Encontrado' if encontrado else 'Não encontrado'}")
                        
    elif opcao == '2':
        skip.deleteElement(valor)

    elif opcao == '3':
        skip.insertElement(valor)

    elif opcao == '4':
        valor_novo = input("Digite o novo valor para atualização: ")
        try:
            valor_novo = float(valor_novo)
        except ValueError:
            print("Valor inválido, deve ser numérico.")
            continue
        skip.updateElement(valor, valor_novo)

    # Mostrar Skip List após operação (não haverá saída)
    skip.displayList()