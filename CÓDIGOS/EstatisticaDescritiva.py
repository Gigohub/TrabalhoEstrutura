import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose

# Carregar o dataset uma única vez e processar colunas derivadas
df = pd.read_csv('energydata_complete.csv')
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour
df['day_of_week'] = df['date'].dt.dayofweek
df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)

# Função de estatísticas descritivas
def estatisticas_descritivas(df_numeric):
    """Calcula estatísticas básicas para variáveis numéricas"""
    desc = df_numeric.describe(percentiles=[.01, .05, .25, .5, .75, .95, .99]).T
    desc['skewness'] = df_numeric.skew()
    desc['kurtosis'] = df_numeric.kurtosis()
    desc['IQR'] = desc['75%'] - desc['25%']
    desc['CV'] = desc['std'] / desc['mean']
    return desc

# Gerar estatísticas e salvar tabela
estatisticas = estatisticas_descritivas(df.select_dtypes(include=[np.number]))
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')
table = ax.table(
    cellText=estatisticas.round(4).values,
    colLabels=estatisticas.columns,
    rowLabels=estatisticas.index,
    cellLoc='center',
    loc='center',
    colColours=['lightgray']*len(estatisticas.columns),
    rowColours=['lightgray']*len(estatisticas.index)
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)
plt.savefig('IMAGENS/estatisticas_descritivas.png', dpi=300, bbox_inches='tight')
plt.close()
print("Tabela salva como 'estatisticas_descritivas.png'!")

# Heatmap de correlação
def plot_correlacao(df, variaveis=None):
    """Gera um mapa de calor de correlação entre variáveis numéricas"""
    data = df[variaveis] if variaveis else df.select_dtypes(include=[np.number])
    corr = data.corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', center=0, linewidths=0.5)
    plt.title("Mapa de Correlação entre Variáveis", pad=20, fontsize=16)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.savefig('IMAGENS/correlacao_variaveis.png', dpi=300, bbox_inches='tight')
    plt.close()

plot_correlacao(df, variaveis=['Appliances', 'T_out', 'RH_out', 'Windspeed', 'lights'])

# Análise temporal
def analise_temporal(df, variavel, time_col='date'):
    if time_col not in df.columns or variavel not in df.columns:
        raise ValueError(f"Coluna '{time_col}' ou variável '{variavel}' não encontrada no DataFrame")
    ts = df.set_index(time_col)[variavel]
    plt.figure(figsize=(15, 12))
    # Série original e média móvel
    plt.subplot(311)
    rolmean = ts.rolling(window=24*7).mean()
    plt.plot(ts, label='Original', alpha=0.5)
    plt.plot(rolmean, label='Média Móvel Semanal', color='red', linewidth=2)
    plt.legend()
    plt.title(f'Série Temporal de {variavel}', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    # Desvio padrão móvel
    plt.subplot(312)
    rolstd = ts.rolling(window=24).std()
    plt.plot(rolstd, label='Desvio Padrão Móvel Diário', color='green')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    # Decomposição sazonal
    try:
        decomposition = seasonal_decompose(ts.dropna(), period=24)
        plt.subplot(313)
        decomposition.trend.plot(color='purple')
        plt.title('Componente de Tendência', fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)
    except Exception as e:
        print(f"Erro na decomposição sazonal: {e}")
        plt.subplot(313)
        plt.text(0.5, 0.5, 'Decomposição não disponível', ha='center', va='center')
    plt.tight_layout()
    plt.savefig(f'IMAGENS/temporal_{variavel}.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Análise temporal salva como 'temporal_{variavel}.png'")

analise_temporal(df, 'Appliances')

# Análise de relações entre variáveis
def analise_relacoes(df, target='Appliances'):
    if target not in df.columns:
        raise ValueError(f"Variável target '{target}' não encontrada no DataFrame")
    corr = df.corr()[target].sort_values(ascending=False)
    numeric_vars = df.select_dtypes(include=[np.number]).columns
    top_corr = corr[numeric_vars].drop(target, errors='ignore').head(10)
    plt.figure(figsize=(20, 10))
    plt.suptitle(f'Relações com a variável alvo: {target}', y=1.02, fontsize=16)
    for i, var in enumerate(top_corr.index, 1):
        plt.subplot(2, 5, i)
        sns.regplot(x=df[var], y=df[target], scatter_kws={'alpha': 0.3, 'color': 'skyblue'}, line_kws={'color': 'red'})
        plt.title(f'{var}\nCorr: {top_corr[var]:.2f}', pad=10)
        plt.xlabel('')
        plt.ylabel('')
    plt.tight_layout()
    output_file = f'relacoes_{target}.png'
    plt.savefig('IMAGENS/relacoes_Appliances.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Análise de relações salva como '{output_file}'")
    return corr

try:
    correlacoes = analise_relacoes(df)
    print("\nCorrelações encontradas:")
    print(correlacoes.head(10))
except Exception as e:
    print(f"Erro na análise: {str(e)}")

# Análise por grupos (boxplot, densidade, heatmap)
def analise_grupos_png(df, group_col='is_weekend'):
    group_names = {0: 'Dia Útil', 1: 'Fim de Semana'}
    variaveis = ['Appliances', 'lights', 'T_out', 'RH_out', 'Windspeed', 'Visibility']
    if group_col not in df.columns:
        raise ValueError(f"Coluna '{group_col}' não encontrada!")
    # Boxplot
    plt.figure(figsize=(18, 10))
    for i, var in enumerate(variaveis, 1):
        plt.subplot(2, 3, i)
        sns.boxplot(x=group_col, y=var, data=df, palette="viridis", showmeans=True,
                    meanprops={"marker":"o", "markerfacecolor":"white", "markeredgecolor":"red"})
        plt.title(f'Distribuição de {var}', fontsize=12)
        plt.xticks(ticks=[0, 1], labels=group_names.values())
        plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.suptitle('Comparação entre Grupos - Boxplot', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(f'IMAGENS/boxplot_grupos.png', dpi=300, bbox_inches='tight')
    plt.close()
    # Densidade
    plt.figure(figsize=(15, 8))
    for var in variaveis[:4]:
        for grupo_val, grupo_nome in group_names.items():
            sns.kdeplot(df[df[group_col] == grupo_val][var],
                        label=f'{grupo_nome} - {var}',
                        linewidth=2, alpha=0.7)
    plt.title('Densidade de Distribuição por Grupo', fontsize=16)
    plt.xlabel('Valores')
    plt.legend()
    plt.grid(linestyle='--', alpha=0.3)
    plt.savefig(f'IMAGENS/densidade_grupos.png', dpi=300, bbox_inches='tight')
    plt.close()
    # Heatmap de correlação
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    corr_util = df[df[group_col] == 0][variaveis].corr()
    sns.heatmap(corr_util, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax1, cbar=False)
    ax1.set_title('Correlações - Dias Úteis', fontsize=14)
    corr_fds = df[df[group_col] == 1][variaveis].corr()
    sns.heatmap(corr_fds, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax2)
    ax2.set_title('Correlações - Finais de Semana', fontsize=14)
    plt.suptitle('Diferenças nas Correlações entre Grupos', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(f'IMAGENS/correlacoes_grupos.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("""
    Arquivos PNG gerados com sucesso:
    - boxplot_grupos.png
    - densidade_grupos.png
    - correlacoes_grupos.png
    """)

analise_grupos_png(df)