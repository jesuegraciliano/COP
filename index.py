import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título e entrada de parâmetros
st.set_page_config(page_title="R134a - Tabela de Propriedades", layout="centered")
st.title("🌡️ Tabela de Propriedades Termodinâmicas do R134a")

T_min = st.number_input("Temperatura mínima (°C)", value=-40.0, step=5.0, format="%.2f")
T_max = st.number_input("Temperatura máxima (°C)", value=60.0, step=5.0, format="%.2f")
T_step = st.number_input("Passo de temperatura (°C)", value=5.0, step=1.0, format="%.2f")

# Constantes (valores do FORTRAN)
T0 = 233.15
A = 24.803998
B = -0.2405382
C = 0.001225
D = -5.164e-6
E = 6.5e-9
F = 303.15
TC = 374.2
DLOG = np.log
DEXP = np.exp

# Inicialização das listas
T_list = []
P_list = []
DL_list = []
DV_list = []
HL_list = []
HV_list = []
SL_list = []
SV_list = []

for T_C in np.arange(T_min, T_max + T_step, T_step):
    T = T_C + 273.15
    T_list.append(T_C)

    # Cálculo da Pressão
    log_P = (A + B / T + C * T + D * T**2 + E * (F - T) * DLOG(F - T)) * DLOG(F - T)
    P = np.exp(log_P)
    P_list.append(P)

    # Densidade líquida e vapor (simplificado)
    DL = 1400 - 3.5 * (T_C + 40)
    DV = 120 + 4.2 * (T_C + 40)
    DL_list.append(DL)
    DV_list.append(DV)

    # Entalpias (baseado nos dados reais da tabela)
    HL = 23.97 + (T_C + 40) * 4.8      # ajustado com base em HL real
    HV = 235.02 + (T_C + 40) * 1.0     # ajustado com base em HV real
    HL_list.append(HL)
    HV_list.append(HV)

    # Entropias (estimativas ajustadas)
    SL = 0.09983 + (T_C + 40) * 0.00325
    SV = 0.93202 - (T_C + 40) * 0.00044
    SL_list.append(SL)
    SV_list.append(SV)

# Monta o DataFrame
df = pd.DataFrame({
    "T (°C)": T_list,
    "P (kPa)": P_list,
    "DL (kg/m³)": DL_list,
    "DV (kg/m³)": DV_list,
    "HL (kJ/kg)": HL_list,
    "HV (kJ/kg)": HV_list,
    "SL (kJ/kg·K)": SL_list,
    "SV (kJ/kg·K)": SV_list
})

# Formatar com vírgulas (pt-BR)
df_styled = df.style.format(decimal=",", thousands=".")

# Exibir tabela
st.markdown("### 📊 Tabela de Propriedades")
st.dataframe(df_styled, use_container_width=True)

# Baixar como CSV com separador brasileiro
csv = df.to_csv(sep=';', index=False, decimal=",").encode('utf-8')
st.download_button("📥 Baixar como CSV", csv, file_name="tabela_r134a.csv", mime="text/csv")

# Gráfico
st.markdown("## 📈 Gráficos")
fig, ax = plt.subplots()
ax.plot(df["T (°C)"], df["P (kPa)"], marker='o', label="Pressão")
ax.set_xlabel("Temperatura (°C)")
ax.set_ylabel("Pressão (kPa)")
ax.grid(True)
ax.legend()
st.pyplot(fig)
