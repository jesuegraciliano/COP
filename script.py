import numpy as np
import pandas as pd

def calcular_psat(t):
    a1 = -7.17959
    a2 = 1.87191
    a3 = -0.0278335
    a4 = 0.00013842
    lnp = a1 + a2 * t + a3 * t**2 + a4 * t**3
    return np.exp(lnp)

def calcular_entalpia(t):
    b1 = 2.1131
    b2 = 1.8423
    b3 = 0.003261
    b4 = -3.49e-6
    return b1 + b2 * t + b3 * t**2 + b4 * t**3

def calcular_entropia(t):
    c1 = -2.357
    c2 = 0.011502
    c3 = -5.93e-6
    return c1 + c2 * t + c3 * t**2

def calcular_densidade(t):
    d1 = 1746.6
    d2 = -5.2632
    d3 = 0.012045
    return d1 + d2 * t + d3 * t**2

def calcular_propriedades(t_celsius):
    t_kelvin = t_celsius + 273.15
    psat = calcular_psat(t_kelvin)
    h = calcular_entalpia(t_kelvin)
    s = calcular_entropia(t_kelvin)
    rho = calcular_densidade(t_kelvin)
    return psat, h, s, rho

def gerar_tabela(tmin, tmax, passo):
    temperaturas = np.arange(tmin, tmax + passo, passo)
    dados = []

    for t in temperaturas:
        psat, h, s, rho = calcular_propriedades(t)
        dados.append({
            "Temperatura (°C)": t,
            "Pressão sat (kPa)": round(psat, 2),
            "Entalpia (kJ/kg)": round(h, 2),
            "Entropia (kJ/kg·K)": round(s, 4),
            "Densidade (kg/m³)": round(rho, 2)
        })

    return pd.DataFrame(dados)
