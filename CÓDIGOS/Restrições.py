import time
import random
import numpy as np
import pandas as pd
import sys

# R1 - Limitação de memória RAM disponível (simulação para Windows)
def checar_memoria(objetos, max_mb=128):
    total = sum(sys.getsizeof(obj) for obj in objetos)
    if total > max_mb * 1024 * 1024:
        raise MemoryError(f"Limite de memória simulado excedido! ({total/1024/1024:.2f}MB usados)")

# R10 - Execução forçada com interrupções a cada 100ms
def interrupcao():
    time.sleep(0.1)  # Simula concorrência/processo interrompido

# R12 - Simulação de alta latência no acesso a banco de dados
def acesso_banco_simulado():
    delay = random.uniform(0.5, 1.0)  # 500ms até 1000ms
    time.sleep(delay)

# R18 - Simulação de sensores defeituosos (10% das medições anômalas)
def sensor_leitura(valor_real):
    if random.random() < 0.10:  # 10% chance de anomalia
        return valor_real * random.uniform(5, 10)  # valor anômalo
    return valor_real

# R25 - Simula grandes volumes de dados em entrada contínua, forçando reindexação frequente
def simular_entrada_continua(X_train, y_train, n=1000, reindexar_cada=100):
    for i in range(n):
        interrupcao()  # R10
        nova_amostra = np.random.rand(X_train.shape[1])
        novo_target = np.random.rand()
        X_train.loc[len(X_train)] = nova_amostra
        y_train.loc[len(y_train)] = novo_target
        checar_memoria([X_train, y_train])  # R1
        if i % reindexar_cada == 0:
            X_train.reset_index(drop=True, inplace=True)
            y_train.reset_index(drop=True, inplace=True)
            print(f"Reindexação após {i+1} inserções.")