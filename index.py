import streamlit as st
import matplotlib.pyplot as plt
from script import gerar_tabela

st.set_page_config(page_title="R134a – Tabela de Propriedades", layout="centered")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🔬 Tabela Termodinâmica do R134a")

tmin = st.number_input("Temperatura mínima (°C)", value=-40.0)
tmax = st.number_input("Temperatura máxima (°C)", value=80.0)
passo = st.number_input("Passo de temperatura (°C)", value=5.0)

df = gerar_tabela(tmin, tmax, passo)

st.subheader("📊 Tabela de Propriedades")
st.dataframe(df)

st.download_button("⬇️ Baixar como CSV", df.to_csv(index=False), file_name="r134a_tabela.csv")

st.subheader("📈 Gráficos")

def plot_line(x, y, xlabel, ylabel, title):
    fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    st.pyplot(fig)

plot_line(df["Temperatura (°C)"], df["Pressão sat (kPa)"], "Temperatura (°C)", "Pressão (kPa)", "Temperatura vs Pressão de Saturação")
plot_line(df["Temperatura (°C)"], df["Entalpia (kJ/kg)"], "Temperatura (°C)", "Entalpia (kJ/kg)", "Temperatura vs Entalpia")
plot_line(df["Temperatura (°C)"], df["Entropia (kJ/kg·K)"], "Temperatura (°C)", "Entropia (kJ/kg·K)", "Temperatura vs Entropia")
plot_line(df["Temperatura (°C)"], df["Densidade (kg/m³)"], "Temperatura (°C)", "Densidade (kg/m³)", "Temperatura vs Densidade")
