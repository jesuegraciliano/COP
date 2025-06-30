import streamlit as st
import pandas as pd

# Dados extraídos da tabela de propriedades para o R134a
dados = {
    "Temperatura (°C)": list(range(-20, 55, 2)),
    "HL (kJ/kg)": [
        25.19, 30.25, 36.61, 43.81, 50.02, 57.05, 63.31, 70.58, 76.60,
        84.35, 91.25, 98.52, 105.36, 112.11, 118.72, 125.34, 132.12,
        138.90, 145.88, 152.92, 159.61, 166.74, 173.45, 180.53, 187.23,
        193.88, 200.45, 207.29, 214.06, 220.75, 227.41, 234.21, 240.98,
        247.94, 254.93, 261.94, 268.85, 275.79
    ],
    "HV (kJ/kg)": [
        251.88, 255.65, 259.57, 263.27, 266.84, 270.40, 273.92, 277.48,
        280.92, 284.33, 287.72, 291.10, 294.39, 297.61, 300.85, 304.01,
        307.21, 310.32, 313.43, 316.42, 319.51, 322.52, 325.47, 328.44,
        331.35, 334.26, 337.14, 339.98, 342.77, 345.57, 348.28, 350.94,
        353.67, 356.37, 359.02, 361.62, 364.17
    ]
}

# Cria o DataFrame
df = pd.DataFrame(dados)

# Título do app
st.title("Propriedades do R134a: HL e HV")

# Seleção da temperatura
temperatura = st.slider("Selecione a temperatura (°C):", min_value=-20, max_value=50, step=2)

# Busca o valor correspondente
linha = df[df["Temperatura (°C)"] == temperatura]
hl = linha["HL (kJ/kg)"].values[0]
hv = linha["HV (kJ/kg)"].values[0]

# Exibição com formatação brasileira
def format_brasil(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

st.subheader("Resultados")
st.write(f"**Entalpia líquida saturada (HL):** {format_brasil(hl)} kJ/kg")
st.write(f"**Entalpia do vapor saturado (HV):** {format_brasil(hv)} kJ/kg")

# Exibe tabela completa
with st.expander("📋 Ver tabela completa"):
    tabela_formatada = df.copy()
    tabela_formatada["HL (kJ/kg)"] = tabela_formatada["HL (kJ/kg)"].apply(format_brasil)
    tabela_formatada["HV (kJ/kg)"] = tabela_formatada["HV (kJ/kg)"].apply(format_brasil)
    st.dataframe(tabela_formatada)
