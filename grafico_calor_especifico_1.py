import matplotlib.pyplot as plt
import numpy as np

# 1. Extração e Tratamento de Dados
data_str = """0,62;63,88
1,23;63,88
1,85;63,88
...""" # O código abaixo lê do arquivo carregado

# Simulando a leitura do arquivo e conversão para matriz
# Substitua pelo caminho do arquivo se rodar localmente
raw_data = []
with open('Dados_Calorimetria.txt', 'r') as f:
    linhas = f.readlines()
    # Pula a cada 10 linhas
    for i in range(0, len(linhas), 20):
        linha = linhas[i].strip()
        if linha:
            partes = linha.replace(',', '.').split(';')
            raw_data.append([float(partes[0]), float(partes[1])])

# Convertendo para uma matriz NumPy para manipulação técnica
dados_matriz = np.array(raw_data)
tempo = dados_matriz[:, 0]
temperatura = dados_matriz[:, 1]

# 2. Configuração do Gráfico
fig, ax = plt.subplots(figsize=(12, 7))

# Definindo a cor de fundo (violeta solicitado)
ax.set_facecolor('#A28AF9')
fig.patch.set_facecolor('#A28AF9')

# Plotagem dos dados (símbolos discretos)
ax.scatter(tempo, temperatura, color='white', s=25, label='Dados Experimentais', edgecolors='black', linewidth=0.5)

# 3. Estilização dos Eixos e Ticks
ax.set_xlabel('Tempo (s)', fontsize=12)
ax.set_ylabel('Temperatura (°C)', fontsize=12)
ax.set_title('Curva de Resfriamento/Aquecimento - Calorimetria', fontsize=14, pad=15)

# Eixos em todas as bordas (spine)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)

# Ticks voltados para dentro em todas as direções
ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, length=6)

# Legenda a cada 100s no eixo X
plt.xticks(np.arange(0, max(tempo) + 1, 100))

# 4. Ajustes Finais
ax.legend(loc='upper right', frameon=True, facecolor='white')
plt.tight_layout()

# Exibir gráfico
plt.show()