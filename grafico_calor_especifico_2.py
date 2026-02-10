import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# 1. Preparação dos Dados (Simulação da leitura da matriz completa)
raw_data = []
with open('Dados_Calorimetria.txt', 'r') as f:
    linhas = f.readlines()
    # Pula a cada 10 linhas
    for i in range(0, len(linhas), 20):
        linha = linhas[i].strip()
        if linha:
            partes = linha.replace(',', '.').split(';')
            raw_data.append([float(partes[0]), float(partes[1])])

dados_matriz = np.array(raw_data)
tempo = dados_matriz[:, 0]
temp = dados_matriz[:, 1]

# Função Exponencial para o ajuste: y = a * exp(-b * x) + c
def modelo_exp(x, a, b, c):
    return a * np.exp(-b * x) + c

# 2. Segmentação para Ajustes
# Ajuste 1: 100 a 750 s
mask1 = (tempo >= 100) & (tempo <= 750)
t1, T1 = tempo[mask1], temp[mask1]
popt1, _ = curve_fit(modelo_exp, t1, T1, p0=[20, 0.001, 40])

# Ajuste 2: 1020 s até o final
mask2 = (tempo >= 1020)
t2, T2 = tempo[mask2], temp[mask2]
popt2, _ = curve_fit(modelo_exp, t2, T2, p0=[20, 0.001, 30])

# 3. Intervalos de Extrapolação
t_extrap1 = np.linspace(100, 1150, 500)
t_extrap2 = np.linspace(800, max(tempo), 500)

# 4. Configuração do Gráfico
fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#A28AF9')
ax.set_facecolor('#A28AF9')

# Plotagem dos dados experimentais
ax.scatter(tempo, temp, color='white', s=10, label='Dados Experimentais', 
           edgecolors='black', linewidth=0.3, alpha=0.7)

# Plotagem das curvas de ajuste/extrapolação
ax.plot(t_extrap1, modelo_exp(t_extrap1, *popt1), color='red', 
        label='Ajuste 1 (100-750s, ext. 1150s)', linestyle='--', linewidth=2)
ax.plot(t_extrap2, modelo_exp(t_extrap2, *popt2), color='blue', 
        label='Ajuste 2 (1020s-fim, ext. 800s)', linestyle='--', linewidth=2)

# 5. Estilização Técnica
ax.set_xlabel('Tempo (s)', fontsize=12)
ax.set_ylabel('Temperatura (°C)', fontsize=12)
ax.set_title('Ajustes Exponenciais e Extrapolações - Calorimetria', fontsize=14)

# Ticks para dentro e em todas as bordas
ax.tick_params(axis='both', which='both', direction='in', top=True, right=True)
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)

# Legenda a cada 100s no eixo X
ax.set_xticks(np.arange(0, max(tempo) + 100, 100))

# Legenda apenas para os eixos solicitados (os eixos já estão fixos pelo matplotlib)
ax.legend(loc='best', frameon=True, facecolor='white', fontsize=10)

plt.tight_layout()
plt.show()