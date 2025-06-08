import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simular_cenarios(df, horas_futuras=24, num_cenarios=5):
    # Exemplo simples: simula cenários variando T_out com ruído
    ultimos = df.tail(horas_futuras).copy()
    cenarios = []
    for c in range(num_cenarios):
        simulado = ultimos.copy()
        simulado['T_out'] = simulado['T_out'] + np.random.normal(0, 1, size=horas_futuras)
        simulado['cenario'] = c+1
        cenarios.append(simulado)
    return pd.concat(cenarios)

# Carregar o dataset
df = pd.read_csv('energydata_complete.csv', parse_dates=['date'])

# Adicionar colunas de hora e dia da semana, se ainda não existirem
if 'hora' not in df.columns:
    df['hora'] = df['date'].dt.hour
if 'dia_semana' not in df.columns:
    df['dia_semana'] = df['date'].dt.dayofweek

# Simular cenários futuros
cenarios_df = simular_cenarios(df, horas_futuras=24, num_cenarios=5)

# Visualizar os resultados (exemplo: temperatura externa simulada)
plt.figure(figsize=(12,6))
for cenario in cenarios_df['cenario'].unique():
    plt.plot(
        cenarios_df[cenarios_df['cenario'] == cenario].index,
        cenarios_df[cenarios_df['cenario'] == cenario]['T_out'],
        label=f'Cenário {cenario}'
    )
plt.legend()
plt.tight_layout()
plt.savefig('IMAGENS/simulacao_temperatura_externa.png') # Salva o gráfico como PNG
print("Simulação salva no grafico 'simulacao_temperatura_externa.png'")