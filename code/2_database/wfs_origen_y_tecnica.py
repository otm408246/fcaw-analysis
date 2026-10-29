# -*- coding: utf-8 -*-
"""
Anade dos columnas a FCAW_MAESTRA.csv y MODELADO.csv (pendientes de TRASPASO §6):

  WFS_origen   imputada        WFS derivada por ESTA consolidacion desde la corriente
                               (huella: corr(I,WFS) = 1.00000 dentro del estudio)  -> H-048
               medida          I y WFS publicadas ambas, corr < 1: medicion independiente
               no_verificable  WFS publicada, corriente NO publicada: la huella no aplica
               (vacio)         el estudio no tiene WFS

  tecnica      oscilado        antorcha con oscilacion (cordones de 16 a 40 mm)
               recto           cordon recto (stringer), el resto

La clasificacion de WFS_origen se DERIVA de los datos, no se escribe a mano.
Se ejecuta desde dataset/.
"""
import numpy as np, pandas as pd

OSCILADO = {"02_Kannan2006", "17_Senthilkumar2015"}   # 'oscil' en observaciones, W hasta 40 mm

def clasificar(g):
    if g.WFS_m_min.notna().sum() == 0:
        return ""
    gg = g.dropna(subset=["I_amp", "WFS_m_min"])
    if len(gg) < 3 or gg.I_amp.nunique() < 3 or gg.WFS_m_min.nunique() < 2:
        return "no_verificable"          # sin variacion no hay huella que evaluar
    r = np.corrcoef(gg.I_amp, gg.WFS_m_min)[0, 1]
    return "imputada" if r > 0.99999 else "medida"

m = pd.read_csv("FCAW_MAESTRA.csv")
m = m[[c for c in m.columns if not c.startswith(("WFS_origen", "tecnica"))]]   # idempotente
origen = {p: clasificar(g) for p, g in m.groupby("paper_id")}
m["WFS_origen"] = m.paper_id.map(origen)
m["tecnica"] = np.where(m.paper_id.isin(OSCILADO), "oscilado", "recto")
m.to_csv("FCAW_MAESTRA.csv", index=False)

d = pd.read_csv("MODELADO.csv")
d = d[[c for c in d.columns if not c.startswith(("WFS_origen", "tecnica"))]]   # idempotente
d = d.merge(m[["registro_id", "WFS_origen", "tecnica"]], on="registro_id", how="left")
d.to_csv("MODELADO.csv", index=False)

print("MAESTRA  WFS_origen:", m.WFS_origen.replace("", "sin_WFS").value_counts().to_dict())
print("MAESTRA  tecnica   :", m.tecnica.value_counts().to_dict())
w = d[d.W_mm.notna()]
print(f"\nMODELADO con ancho ({len(w)} corridas · {w.paper_id.nunique()} estudios):")
print(w.groupby("WFS_origen").agg(corridas=("registro_id", "size"), estudios=("paper_id", "nunique")).to_string())
print(w.groupby("tecnica").agg(corridas=("registro_id", "size"), estudios=("paper_id", "nunique")).to_string())
