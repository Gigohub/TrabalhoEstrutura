import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score

# 1. Carregar dados
data = pd.read_csv('energydata_complete.csv')
data['date'] = pd.to_datetime(data['date'])
data['hour'] = data['date'].dt.hour
data['day_of_week'] = data['date'].dt.dayofweek
data['is_weekend'] = data['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

# 2. Variáveis explicativas e target
X = data[['lights', 'T1', 'RH_1', 'T2', 'RH_2', 'T3', 'RH_3', 'T4', 'RH_4',
          'T5', 'RH_5', 'T6', 'RH_6', 'T7', 'RH_7', 'T8', 'RH_8', 'T9', 'RH_9',
          'T_out', 'Press_mm_hg', 'RH_out', 'Windspeed', 'Visibility', 'Tdewpoint',
          'hour', 'is_weekend']]
y = data['Appliances']

# 3. Divisão temporal
train_size = int(0.8 * len(data))
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# 4. Modelo
model = DecisionTreeRegressor(
    max_depth=4,
    min_samples_leaf=20,
    min_impurity_decrease=0.005,
    random_state=42
)
model.fit(X_train, y_train)

# 5. Avaliação
y_pred = model.predict(X_test)
print(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.2f}')
print(f'R²: {r2_score(y_test, y_pred):.2f}')

# 6. Visualização - salva ao invés de exibir
plt.figure(figsize=(20, 10))
plot_tree(model, feature_names=X.columns, filled=True, rounded=True, fontsize=8, max_depth=2)
plt.savefig("arvore_decisao.png")
print("✅ Árvore de decisão salva como 'arvore_decisao.png'.")

# ========================================
# ✅ Função de busca
def buscar_predicao(model, X, idx=None):
    """
    Busca a predição para uma linha do conjunto de dados.
    idx: índice da linha no DataFrame X, se None, permite inserção manual.
    """
    if idx is not None:
        if idx < 0 or idx >= len(X):
            print("Índice fora do intervalo!")
            return
        entrada = X.iloc[idx].values.reshape(1, -1)
        pred = model.predict(entrada)
        print(f"Predição para o índice {idx}: {pred[0]:.2f}")
        print("Valores de entrada:", X.iloc[idx].to_dict())
    else:
        print("Insira os valores das seguintes variáveis:")
        entrada = []
        for col in X.columns:
            val = float(input(f"{col}: "))
            entrada.append(val)
        entrada = np.array(entrada).reshape(1, -1)
        pred = model.predict(entrada)
        print(f"Predição: {pred[0]:.2f}")

# ========================================
# ✅ Exemplo de uso:

# Buscar por índice:
buscar_predicao(model, X_test, idx=10)

# Ou buscar inserindo valores manualmente:
# buscar_predicao(model, X_test)
plot_tree(model, feature_names=X.columns, filled=True, rounded=True, fontsize=8)
plt.savefig("arvore_completa.png")