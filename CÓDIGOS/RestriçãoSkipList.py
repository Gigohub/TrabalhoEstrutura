from Restrições import checar_memoria, interrupcao, acesso_banco_simulado, sensor_leitura, simular_entrada_continua
import BenchMark_SkipList
import time
import random
import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score

# R12: Simular latência ao carregar dados
acesso_banco_simulado()
data = pd.read_csv("energydata_complete.csv")

# R18: Aplica sensores defeituosos em colunas de sensores
sensor_cols = ['T1', 'RH_1', 'T2', 'RH_2', 'T3', 'RH_3', 'T4', 'RH_4',
               'T5', 'RH_5', 'T6', 'RH_6', 'T7', 'RH_7', 'T8', 'RH_8',
               'T9', 'RH_9', 'T_out', 'RH_out', 'Windspeed', 'Visibility', 'Tdewpoint']
for col in sensor_cols:
    data[col] = data[col].apply(sensor_leitura)

# Features e target
data['date'] = pd.to_datetime(data['date'])
data['hour'] = data['date'].dt.hour
data['day_of_week'] = data['date'].dt.dayofweek
data['is_weekend'] = data['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

features = ['lights', 'T1', 'RH_1', 'T2', 'RH_2', 'T3', 'RH_3', 'T4', 'RH_4',
            'T5', 'RH_5', 'T6', 'RH_6', 'T7', 'RH_7', 'T8', 'RH_8', 'T9', 'RH_9',
            'T_out', 'Press_mm_hg', 'RH_out', 'Windspeed', 'Visibility', 'Tdewpoint',
            'hour', 'is_weekend']
target = 'Appliances'

X = data[features].copy()
y = data[target].copy()

train_size = int(0.8 * len(data))
X_train = X[:train_size].copy()
y_train = y[:train_size].copy()
X_test = X[train_size:].copy()
y_test = y[train_size:].copy()

# R1: Checa memória após grandes operações
checar_memoria([X_train, y_train, X_test, y_test, data])

# R25: Simula entrada contínua de dados (modifica X_train e y_train!)
simular_entrada_continua(X_train, y_train, n=1000, reindexar_cada=100)  # n=1000 para não demorar tanto

# R10: Use interrupcao() dentro de loops longos (exemplo)
for i in range(100):
    interrupcao()
    # Aqui entraria o código do loop, se necessário

# Agora rode o benchmark
BenchMark_SkipList.benchmark_skiplist()