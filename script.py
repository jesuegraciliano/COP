import numpy as np
import pandas as pd

def calcular_psat(t_c):
    """Pressão de saturação (kPa) via equação Antoine"""
    t_k = t_c + 273.15
    # Antoine para R134a entre -40°C e 60°C
    A = 6.87678
    B = 1171.53
    C = 224.366
    log10_p = A - (B / (t_k - C))
    psat = 10 ** log10_p  # retorna em kPa
    return psat

def calcular_entalpia_liquido(t):
    # Ajuste polinomial com base em dados da sua imagem
    return 0.0016 * t**3 + 0.106 * t**2 + 1.82 * t + 23.97

def calcular_entalpia_vapor(t):
    # Ajuste com base nos dados da tabela final
    return -0.0008 * t**3 + 0.045 * t**2 + 1.12 * t + 235.02

def calcular_entropia(t_k):
    # Ajuste simplificado baseado em T Kelvin
    return 0.0005 * (t_k - 233.15) + 0.0983

def calcular_densidade(t_k):
    # Ajuste polinomial da densidade do líquido saturado
    return 1358.47 - 3.2 * (t_k - 233.15) + 0.005 * (t_k - 233.15)**2

def calcular_propriedades(t_c):
    t_k = t_c + 273.15
    psat = calcular_psat(t_c)
    hl = calcular_entalpia_liquido(t_c)
    hv = calcular_entalpia_vapor(t_c)
    s = calcular_entropia(t_k)
    rho = calcular_densidade(t_k)
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
