import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# 1. Matriz de Dados (Processamento do arquivo)
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

# Modelo exponencial: T(t) = a * exp(-b * t) + c
def modelo_exp(t, a, b, c):
    return a * np.exp(-b * t) + c

# 2. Ajustes e Extrapolações
# Intervalo 1: 100 a 750 s
mask1 = (tempo >= 100) & (tempo <= 750)
popt1, _ = curve_fit(modelo_exp, tempo[mask1], temp[mask1], p0=[40, 0.001, 20])

# Intervalo 2: 1020 s até o fim
mask2 = (tempo >= 1020)
popt2, _ = curve_fit(modelo_exp, tempo[mask2], temp[mask2], p0=[40, 0.001, 20])

# Gerar pontos para as curvas (extrapoladas conforme solicitado)
t_curva1 = np.linspace(100, 1150, 500)
t_curva2 = np.linspace(800, max(tempo), 500)

# Cálculo das interseções em t = 1060 s
t_alvo = 1045
temp_inter_1 = modelo_exp(t_alvo, *popt1)
temp_inter_2 = modelo_exp(t_alvo, *popt2)

# 3. Configuração Visual
plt.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#A28AF9')
ax.set_facecolor('#A28AF9')

# Plotagem dos Dados e Curvas
ax.scatter(tempo, temp, color='white', s=8, label='Dados Experimentais', edgecolors='black', linewidth=0.2, alpha=0.6)
ax.plot(t_curva1, modelo_exp(t_curva1, *popt1), color='crimson', lw=2, label='Ajuste 1 (Extrapolado até 1150s)')
ax.plot(t_curva2, modelo_exp(t_curva2, *popt2), color='navy', lw=2, label='Ajuste 2 (Extrapolado desde 800s)')

# Linha Vertical e Marcações
ax.axvline(x=t_alvo, color='black', linestyle=':', linewidth=1.5, label=f'Tempo Crítico ({t_alvo}s)')

# Setas e Textos de Interseção
for t_val, label_c, color_c in zip([temp_inter_1, temp_inter_2], ['Curva 1', 'Curva 2'], ['crimson', 'navy']):
    ax.annotate(f'{t_val:.2f} °C', 
                xy=(t_alvo, t_val), xytext=(t_alvo + 150, t_val + (5 if t_val > 50 else -5)),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=6),
                fontsize=11, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=color_c, alpha=0.8))

# 4. Detalhes Técnicos e Moldura
ax.set_xlabel('Tempo (s)', fontsize=12, fontweight='bold')
ax.set_ylabel('Temperatura (°C)', fontsize=12, fontweight='bold')
ax.set_xticks(np.arange(0, max(tempo) + 100, 100))

# Ticks e Bordas em todos os lados
ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, labelsize=10)
for spine in ax.spines.values():
    spine.set_visible(True)

# Legenda (conforme solicitado, focada no conteúdo principal)
ax.legend(loc='upper right', frameon=True, facecolor='white', shadow=True)

plt.tight_layout()
plt.show()