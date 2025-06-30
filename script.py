import numpy as np
import pandas as pd

# Constantes da equação FORTRAN
A = 24.8033988
B = -2.34040884
C = 0.29495802
D = -8.249441E-3
E = -0.1995458
F = 0.100395
CP1 = 2.017132E-1
CP2 = 2.953967E-2
CP3 = 5.49557E-4
CP4 = 0.0
CP5 = 1.0E-6
B1 = 1.049051E-1
A2 = 1.04096E-1
A3 = 1.07395E-1
C2 = 1.27452E-2
C3 = -0.6469248E-2
A4 = 4.571E-3
A5 = -6.953904E-12
C5 = -2.051369E-9
PO = np.exp(A + B + C + D + E + F)

T0 = 233.15  # K, referência: -40°C

def calcular_propriedades(t_c):
    t_k = t_c + 273.15
    tr = (t_k - T0) / T0
    beta = np.exp(-tr)

    # Pressão
    p = np.exp(A + B / t_k + C * np.log(t_k) + D * t_k**2 + E * t_k + F * t_k**0.5)

    # Densidade líquida
    dl = (0.384 + 0.291 * (1 - tr)**(1 / 3) + 0.292 * (1 - tr)**(2 / 3) + 0.306 * (1 - tr)**(4 / 3)) / 0.001

    # Densidade vapor
    dv = 1 / (0.0035 + 0.0042 * tr + 0.008 * tr**2)

    # Entalpia líquido
    cp_liq = CP1 + CP2 * t_k + CP3 * t_k**2 + CP4 * t_k**3 + CP5 / t_k
    hl = cp_liq * (t_k - T0)

    # Entalpia vapor (modelo derivado da HL + termo de integração)
    hv = hl + (A5 + B1 * t_k + C5 * beta) / (1 - B1)

    # Entropia líquido
    sl = 0.0983 + 0.005 * (t_k - T0) / T0  # aprox.

    # Entropia vapor (mais elevada)
    sv = sl + 0.8  # aprox. constante para saturado

    return p, dl, dv, hl, hv, sl, sv

def gerar_tabela(tmin, tmax, passo):
    temperaturas = np.arange(tmin, tmax + passo, passo)
    dados = []

    for t in temperaturas:
        p, dl, dv, hl, hv, sl, sv = calcular_propriedades(t)
        dados.append({
            "T (°C)": t,
            "P (kPa)": round(p, 2),
            "DL (kg/m³)": round(dl, 2),
            "DV (kg/m³)": round(dv, 2),
            "HL (kJ/kg)": round(hl, 2),
            "HV (kJ/kg)": round(hv, 2),
            "SL (kJ/kg·K)": round(sl, 4),
            "SV (kJ/kg·K)": round(sv, 4)
        })

    df = pd.DataFrame(dados)
    return df
