import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ✅ Carregar dados
data = pd.read_csv('energydata_complete.csv')

# ✅ Conversão de 'date'
data['date'] = pd.to_datetime(data['date'])

# ✅ Seleção de colunas numéricas + data
cols_numericas = data.select_dtypes(include=[np.number]).columns.tolist()
cols_utilizadas = ['date'] + cols_numericas
df = data[cols_utilizadas]

# ✅ Filtro: horário de pico (18h-23h)
df_pico = df[(df['date'].dt.hour >= 18) & (df['date'].dt.hour <= 23)]

# ✅ Ordenar por 'Appliances' (descendente)
df_pico = df_pico.sort_values(by='Appliances', ascending=False).reset_index(drop=True)

# ✅ Gráfico 1: Evolução Temporal do Consumo

plt.figure(figsize=(12, 6))
plt.plot(df_pico['date'], df_pico['Appliances'], color='tomato', linewidth=1)
plt.title('Evolução Temporal do Consumo de Energia (Horário de Pico)', fontsize=14)
plt.xlabel('Data e Hora')
plt.ylabel('Consumo (Wh)')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# ✅ Salvar figura
plt.savefig('evolucao_temporal_consumo.png')
print("✅ Gráfico 'evolucao_temporal_consumo.png' salvo com sucesso.")

plt.close()

# ✅ Gráfico 2: Ranking de Consumo - Top 10 maiores valores

top10 = df_pico.head(10)

plt.figure(figsize=(10, 6))
bars = plt.bar(top10['date'].dt.strftime('%Y-%m-%d %H:%M'), top10['Appliances'], color='goldenrod')
plt.title('Top 10 Maiores Consumos de Energia (Horário de Pico)', fontsize=14)
plt.xlabel('Data e Hora')
plt.ylabel('Consumo (Wh)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# ✅ Rótulos
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, f'{int(yval)}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()

# ✅ Salvar figura
plt.savefig('ranking_top10_consumo.png')
print("✅ Gráfico 'ranking_top10_consumo.png' salvo com sucesso.")

plt.close()
