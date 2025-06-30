import numpy as np
import pandas as pd
import streamlit as st

# Constantes do programa original (baseado no FORTRAN)
A = 24.80339880
B = -20.94038084
C = 2.3450814E-1
D = -8.9055604E-4
E = -1.09954480E-6
F = -1.5095487E3
TO = 233.15  # T0 em K
TC = 374.2
B1 = 0.001
VK = 0.00000001
P0 = 1.0
SU = 0.001
TRNO = (1.0 - (TO / TC)) ** (1.0 / 3.0)
TR = (1.0 - (TO / TC))

# Constantes de entalpia e entropia (parciais)
C1, C2, C3, C4, C5 = 0.0012395, 0.002538, 0.0024762, 0.0, 0.0
CP1, CP2, CP3, CP4, CP5 = 0.0, 0.0, 0.0, 0.0, 0.0

# Interface do usuário
st.title("Tabela de Propriedades Termodinâmicas - R134a")
t_min = st.number_input("Temperatura mínima (°C)", value=-40.0, step=5.0)
t_max = st.number_input("Temperatura máxima (°C)", value=60.0, step=5.0)
t_step = st.number_input("Passo de temperatura (°C)", value=5.0, step=1.0)

temps_C = np.arange(t_min, t_max + 0.1, t_step)
temps_K = temps_C + 273.15

# Inicialização
data = []

for T in temps_K:
    TR = (1.0 - T / TC)
    BET = np.exp(-TR / TC)
    
    # Pressão saturada
    P = np.exp(A + B / T + C * T + D * T**2 + E * (F - T) * np.log(F - T) / T**2)
    
    # Densidade do líquido e vapor
    DL = 1273 - 0.8 * (T - TO)  # aproximação simples
    DV = 285.71 - 0.5 * (T - TO)  # aproximação simples
    
    # Entalpia líquido (HL) e vapor (HV) saturados
    HL = A + B / T + C * T + D * T**2 + E * (F - T) * np.log(F - T) / T**2
    HV = HL + 211  # diferença estimada entre HV e HL para ajuste (refinável)

    # Entropia (SL e SV)
    SL = 0.1 + 0.002 * (T - TO)
    SV = 0.93 - 0.0005 * (T - TO)

    data.append([T - 273.15, round(P, 2), round(DL, 2), round(DV, 2), round(HL, 2), round(HV, 2), round(SL, 4), round(SV, 4)])

# DataFrame com labels em português
df = pd.DataFrame(data, columns=["T (°C)", "P (kPa)", "DL (kg/m³)", "DV (kg/m³)", "HL (kJ/kg)", "HV (kJ/kg)", "SL (kJ/kg·K)", "SV (kJ/kg·K)"])

# Formatação brasileira
df_styled = df.style.format(decimal=",", thousands=".")

# Tabela
st.markdown("### 📊 Tabela de Propriedades")
st.dataframe(df_styled, use_container_width=True)

# Botão para download
csv = df.to_csv(index=False, sep=";", decimal=",").encode("utf-8")
st.download_button("📥 Baixar como CSV", data=csv, file_name="r134a_tabela.csv", mime="text/csv")
