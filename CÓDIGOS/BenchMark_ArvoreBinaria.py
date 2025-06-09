import pandas as pd
import numpy as np
import time
import tracemalloc
from sklearn.tree import DecisionTreeRegressor

def treinar_modelo(X_train, y_train):
    model = DecisionTreeRegressor(
        max_depth=4,
        min_samples_leaf=20,
        min_impurity_decrease=0.005,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def tempo_predicao(model, X_test, n=100):
    idxs = np.random.choice(len(X_test), size=n, replace=False)
    tempos = []
    for idx in idxs:
        entrada = X_test.iloc[[idx]]  # Mantém como DataFrame para evitar warning
        start = time.perf_counter()
        _ = model.predict(entrada)
        tempos.append(time.perf_counter() - start)
    return np.mean(tempos)

def benchmark_arvore_binaria():
    print("==== Benchmark: Árvore Binária ====")
    # Carregar dados
    data = pd.read_csv('energydata_complete.csv')
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

    # Escalabilidade: diferentes tamanhos de dataset
    for n_amostras in [100, 1000, 5000, 10000, len(X)]:
        print(f"\n--- Testando com {n_amostras} amostras ---")
        X_sample = X.iloc[:n_amostras].copy()
        y_sample = y.iloc[:n_amostras].copy()

        tracemalloc.start()
        # Tempo de inserção (treinar)
        start = time.perf_counter()
        model = treinar_modelo(X_sample, y_sample)
        tempo_insercao = time.perf_counter() - start

        # Tempo de busca (predição)
        tempo_busca = tempo_predicao(model, X_sample, n=100 if n_amostras >= 100 else n_amostras)

        # Tempo de remoção (remover última amostra e re-treinar)
        X_rem = X_sample.iloc[:-1, :].copy()
        y_rem = y_sample.iloc[:-1].copy()
        start = time.perf_counter()
        model_rem = treinar_modelo(X_rem, y_rem)
        tempo_remocao = time.perf_counter() - start

        # Uso de memória
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Latência média (inserção + busca + remoção)
        start = time.perf_counter()
        model_lat = treinar_modelo(X_sample, y_sample)
        _ = model_lat.predict(X_sample.iloc[[0]])  # usa DataFrame
        model_lat2 = treinar_modelo(X_sample.iloc[:-1,:], y_sample.iloc[:-1])
        latencia_media = (time.perf_counter() - start) / 3

        print(f"Tempo de inserção (treino): {tempo_insercao:.4f} s")
        print(f"Tempo de busca médio (predição): {tempo_busca*1000:.4f} ms")
        print(f"Tempo de remoção (re-treino): {tempo_remocao:.4f} s")
        print(f"Uso de memória: {current/1024:.2f} KB (atual), {peak/1024:.2f} KB (pico)")
        print(f"Latência média (ins+busca+rem): {latencia_media:.4f} s")