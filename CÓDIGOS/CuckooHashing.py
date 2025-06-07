import pandas as pd
import hashlib
import numpy as np

class CuckooHashTable:
    def __init__(self, size=0, max_kicks=20):
        # O tamanho deve ser pelo menos 2x o número de chaves para evitar loops
        self.size = size if size > 0 else 101
        self.table1 = [None] * self.size
        self.table2 = [None] * self.size
        self.max_kicks = max_kicks  # Máximo de realocações para evitar loops infinitos
        self.insert_failures = 0

    def hash1(self, key):
        return int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16) % self.size

    def hash2(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % self.size

    def insert(self, key, value):
        for _ in range(self.max_kicks):
            pos1 = self.hash1(key)
            if self.table1[pos1] is None:
                self.table1[pos1] = (key, value)
                return True
            if self.table1[pos1][0] == key:
                self.table1[pos1] = (key, value)
                return True
            # Troca (kick out)
            key, value, self.table1[pos1] = self.table1[pos1][0], self.table1[pos1][1], (key, value)

            pos2 = self.hash2(key)
            if self.table2[pos2] is None:
                self.table2[pos2] = (key, value)
                return True
            if self.table2[pos2][0] == key:
                self.table2[pos2] = (key, value)
                return True
            # Troca (kick out)
            key, value, self.table2[pos2] = self.table2[pos2][0], self.table2[pos2][1], (key, value)
        self.insert_failures += 1
        print("⚠️ Falha na inserção: número máximo de realocações atingido.")
        return False

    def search(self, key):
        pos1 = self.hash1(key)
        if self.table1[pos1] is not None and self.table1[pos1][0] == key:
            return self.table1[pos1][1]
        pos2 = self.hash2(key)
        if self.table2[pos2] is not None and self.table2[pos2][0] == key:
            return self.table2[pos2][1]
        return None

    def remove(self, key):
        pos1 = self.hash1(key)
        if self.table1[pos1] is not None and self.table1[pos1][0] == key:
            self.table1[pos1] = None
            return True
        pos2 = self.hash2(key)
        if self.table2[pos2] is not None and self.table2[pos2][0] == key:
            self.table2[pos2] = None
            return True
        return False

    def has_collision(self):
        # Checa se existe alguma chave duplicada em qualquer tabela (não deve ocorrer)
        seen_hashes1 = set()
        seen_hashes2 = set()
        for slot in self.table1:
            if slot:
                if slot[0] in seen_hashes1:
                    return True
                seen_hashes1.add(slot[0])
        for slot in self.table2:
            if slot:
                if slot[0] in seen_hashes2:
                    return True
                seen_hashes2.add(slot[0])
        return False

    def count_filled(self):
        return sum(1 for slot in self.table1 if slot is not None) + sum(1 for slot in self.table2 if slot is not None)


if __name__ == "__main__":
    # ==================
    # Teste de colisão e exemplo de uso

    df = pd.read_csv('energydata_complete.csv')
    def hash_row(row):
        row_str = ','.join(map(str, row.values))
        return hashlib.sha256(row_str.encode('utf-8')).hexdigest()

    df['hash'] = df.apply(hash_row, axis=1)
    keys = df['hash'].values
    values = df.to_dict(orient='records')

    tamanho_tabela = 2 * len(keys)
    cuckoo = CuckooHashTable(size=tamanho_tabela)

    # Inserção
    for k, v in zip(keys, values):
        assert cuckoo.insert(k, v), "Falha ao inserir (provavelmente tabela pequena demais)"

    # Verificação de colisão
    assert not cuckoo.has_collision(), "Foi detectada colisão na tabela cuckoo!"

    print(f"Total de chaves: {len(keys)}")
    print(f"Total de slots ocupados: {cuckoo.count_filled()}")
    print(f"Inserções que falharam (max_kicks): {cuckoo.insert_failures}")
    print("✅ Nenhuma colisão detectada: Cuckoo Hashing distribuiu todas as chaves sem colisão.")

    # Exemplo de busca
    idx = np.random.randint(0, len(keys))
    test_key = keys[idx]
    print("\nBusca por hash:", test_key)
    result = cuckoo.search(test_key)
    if result:
        print("Encontrado:", result)
    else:
        print("Não encontrado.")

    # Exemplo de remoção
    cuckoo.remove(test_key)
    print("Após remoção:", cuckoo.search(test_key))