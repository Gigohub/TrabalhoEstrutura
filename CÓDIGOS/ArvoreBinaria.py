import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score

# ======== Carregar e preparar dados ========
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

train_size = int(0.8 * len(data))
X_train = X[:train_size].copy()
y_train = y[:train_size].copy()
X_test = X[train_size:].copy()
y_test = y[train_size:].copy()

# ======== Modelo ========
def treinar_modelo(X_train, y_train):
    model = DecisionTreeRegressor(
        max_depth=4,
        min_samples_leaf=20,
        min_impurity_decrease=0.005,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

model = treinar_modelo(X_train, y_train)

def avaliar_modelo(model, X_test, y_test):
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    print(f'\n✅ Avaliação do Modelo:')
    print(f'RMSE: {rmse:.2f}')
    print(f'R²: {r2:.2f}\n')

avaliar_modelo(model, X_test, y_test)

# ======== Funções ========
def buscar_predicao(model, X):
    idx = int(input("Digite o índice para predição (0 a {}): ".format(len(X)-1)))
    if 0 <= idx < len(X):
        entrada = X.iloc[idx].values.reshape(1, -1)
        pred = model.predict(entrada)
        print(f"\n✅ Predição para o índice {idx}: {pred[0]:.2f}")
        print("🔹 Valores de entrada:", X.iloc[idx].to_dict())
    else:
        print("❌ Índice inválido.")

def inserir_amostra(X_train, y_train):
    print("\n➡️ Insira os valores das seguintes variáveis:")
    nova_amostra = []
    for col in X_train.columns:
        val = float(input(f"{col}: "))
        nova_amostra.append(val)
    novo_target = float(input("Valor para Appliances: "))
    X_train.loc[len(X_train)] = nova_amostra
    y_train.loc[len(y_train)] = novo_target
    print("✅ Nova amostra inserida.")

def remover_amostra(X_train, y_train):
    idx = int(input("Digite o índice da amostra a ser removida (0 a {}): ".format(len(X_train)-1)))
    if 0 <= idx < len(X_train):
        X_train.drop(index=idx, inplace=True)
        y_train.drop(index=idx, inplace=True)
        X_train.reset_index(drop=True, inplace=True)
        y_train.reset_index(drop=True, inplace=True)
        print(f"✅ Amostra no índice {idx} removida.")
    else:
        print("❌ Índice inválido.")

def visualizar_arvore(model, filename="arvore_interativa.png"):
    plt.figure(figsize=(20, 10))
    plot_tree(model, feature_names=X.columns, filled=True, rounded=True, fontsize=8)
    plt.savefig('IMAGENS/{filename}')
    plt.close()
    print(f"✅ Árvore de decisão salva como '{filename}'.")

# ======== Sistema Interativo ========
while True:
    print("\n🔸 Menu de operações:")
    print("1 - Buscar predição")
    print("2 - Inserir nova amostra")
    print("3 - Remover uma amostra")
    print("4 - Visualizar e salvar árvore de decisão")
    print("5 - Avaliar modelo")
    print("6 - Sair")
    
    opcao = input("Escolha a opção: ")

    if opcao == '1':
        buscar_predicao(model, X_test)
    elif opcao == '2':
        inserir_amostra(X_train, y_train)
        model = treinar_modelo(X_train, y_train)
        print("✅ Modelo re-treinado após inserção.")
    elif opcao == '3':
        remover_amostra(X_train, y_train)
        model = treinar_modelo(X_train, y_train)
        print("✅ Modelo re-treinado após remoção.")
    elif opcao == '4':
        visualizar_arvore(model)
    elif opcao == '5':
        avaliar_modelo(model, X_test, y_test)
    elif opcao == '6':
        print("✅ Sistema encerrado.")
        break
    else:
        print("❌ Opção inválida. Tente novamente.")

        