import streamlit as st
from script import calcular_propriedades

st.set_page_config(layout="wide")
st.title("Tabela de Propriedades Termodinâmicas – R134a")

temp_max = st.number_input("Temperatura máxima (°C)", value=80.0, step=5.0, format="%.2f")
passo_temp = st.number_input("Passo de temperatura (°C)", value=5.0, step=1.0, format="%.2f")

df = calcular_propriedades(-40, temp_max, passo_temp)

st.markdown("### 📊 Tabela de Propriedades")
df_styled = df.style.format(decimal=",", thousands=".")
st.dataframe(df_styled, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Baixar como CSV", data=csv, file_name="propriedades_r134a.csv", mime="text/csv")
