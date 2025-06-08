import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Carrega o dataset
df = pd.read_csv('energydata_complete.csv')

# Seleciona apenas colunas numéricas (descarta data e variáveis categóricas)
X = df.select_dtypes(include=['float64', 'int64'])

# Padroniza os dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reduz a dimensionalidade para 2 componentes principais para visualização
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Aplica KMeans com 3 clusters (ajuste n_clusters conforme necessidade)
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Adiciona os clusters ao DataFrame original para análise
df['cluster'] = clusters

# Visualização dos clusters nos primeiros dois componentes principais
plt.figure(figsize=(8,6))
plt.scatter(X_pca[:,0], X_pca[:,1], c=clusters, cmap='viridis', alpha=0.5)
plt.title('Clusters encontrados pelo KMeans (PCA)')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.colorbar(label='Cluster')
plt.savefig('IMAGENS/Clusterização.png')
print("Imagem salva")

# Mostra quantos pontos existem em cada cluster
print(df['cluster'].value_counts())