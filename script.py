import numpy as np
import pandas as pd

# Constantes
T0 = 273.15
A = 24.8033988
B = -0.5403825
C = -0.24503582
D = 0.003420833
E = 1168.17
F = 227.971
TC = 374.21
CP1 = 0.52549765
CP2 = 2.219052e-2
CP3 = -1.54896e-5
CP4 = 0.0
CP5 = 0.0
B1 = 1.0
DLOG = np.log
DEXP = np.exp
DABS = np.abs

def calcular_propriedades(temp_min, temp_max, passo):
    resultados = []

    for T_C in np.arange(temp_min, temp_max + 0.1, passo):
        T = T_C + T0
        TR = T / TC
        F_T = (F - T)
        F_FT = F_T / T
        log_term = np.log(F_T / T)

        P = DEXP(A + B / T + C * T0 + D * (T0 ** 2) + E * F_FT * log_term)

        BET = DEXP(-B / T + C * T + D * T ** 2 + E * F_FT * log_term)
        DL = (0.9992 + 0.00144 * (1.0 - TR) + 0.0039 * (1.0 - TR) ** 2 +
              0.0026 * (1.0 - TR) ** 3 + 0.0014 * (1.0 - TR) ** 4) / TR

        VL = 1.0 / DL

        # Newton-Raphson para encontrar VV
        VV = 1.0 / DL
        for _ in range(100):
            FVV = (R := T * (VV - B1)) - (A + B2 := T0 + C2 := DEXP(-BET / TC)) * DEXP(-BET / TC) / (VV - B1)
            DFVV = ((FVV - R) / 0.00001)
            VV -= FVV / DFVV
            if abs(FVV) < 0.00001:
                break

        DV = 1.0 / VV

        # HL e HV (entalpias líquida e vapor)
        UV1 = CP1 * (T - T0) + CP2 * (T ** 2 - T0 ** 2) / 2 + CP3 * (T ** 3 - T0 ** 3) / 3
        UV2 = CP4 * (DEXP(DLOG(T / T0) * 4.0) - DEXP(DLOG(T0) * 4.0)) / 4 + CP5 * (T - T0)
        UV3 = (A ** 2 + (1.0 + BET * T / TC) * C2 * BET) * (1.0 / (VV - B1) - 1.0 / (VL - B1))
        UV4 = (A3 := 3 + 3 * A4 := 4.0) * (1.0 / (VV - B1) ** 2 - 1.0 / (VL - B1) ** 2)
        UV = UV1 + UV2 + UV3 + UV4
        HV = UV + P * VV
        HL = UV + P * VL

        # Entropias
        S1 = CP1 * DLOG(T / T0) + CP2 * (T - T0) + CP3 * (T ** 2 - T0 ** 2) / 2
        S2 = CP4 * DLOG(DABS(VL - B1)) - DLOG(DABS(VV - B1))
        S3 = -B2 * C2 * BET / TC * BET * (1.0 / (VV - B1) - 1.0 / (VL - B1))
        S4 = (B3 := C3 * BET * TC * BET) * (1.0 / (VV - B1) ** 2 - 1.0 / (VL - B1) ** 2)
        SL = S1 + S2 + S3 + S4
        SV = SL + (HV - HL) / T

        resultados.append({
            "T (°C)": round(T_C, 2),
            "P (kPa)": round(P, 2),
            "DL (kg/m³)": round(DL, 2),
            "DV (kg/m³)": round(DV, 2),
            "HL (kJ/kg)": round(HL, 2),
            "HV (kJ/kg)": round(HV, 2),
            "SL (kJ/kg·K)": round(SL, 4),
            "SV (kJ/kg·K)": round(SV, 4),
        })

    return pd.DataFrame(resultados)
