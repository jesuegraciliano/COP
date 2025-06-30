import numpy as np
import pandas as pd

def calcular_psat(t):
    a1 = -7.17959
    a2 = 1.87191
    a3 = -0.0278335
    a4 = 0.00013842
    lnp = a1 + a2 * t + a3 * t**2 + a4 * t**3
    return np.exp(lnp)

def calcular_entalpia_liquido(t):
    # Ajuste polinomial baseado em dados do R134a saturado (líquido)
    return 0.00145 * t**3 + 0.1253 * t**2 + 1.865 * t + 23.97

def calcular_entalpia_vapor(t):
    # Ajuste polinomial baseado em dados do R134a saturado (vapor)
    return -0.00086 * t**3 + 0.0635 * t**2 + 0.771 * t + 235.02

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
    hl = calcular_entalpia_liquido(t_celsius)
    hv = calcular_entalpia_vapor(t_celsius)
    s = calcular_entropia(t_kelvin)
    rho = calcular_densidade(t_kelvin)
    return psat, hl, hv, s, rho

def gerar_tabela(tmin, tmax, passo):
    temperaturas = np.arange(tmin, tmax + passo, passo)
    dados = []

    for t in temperaturas:
        psat, hl, hv, s, rho = calcular_propriedades(t)
        dados.append({
            "Temperatura (°C)": t,
            "Pressão sat (kPa)": round(psat, 2),
            "h Líquido (kJ/kg)": round(hl, 2),
            "h Vapor (kJ/kg)": round(hv, 2),
            "Entropia (kJ/kg·K)": round(s, 4),
            "Densidade (kg/m³)": round(rho, 2)
        })

    return pd.DataFrame(dados)

