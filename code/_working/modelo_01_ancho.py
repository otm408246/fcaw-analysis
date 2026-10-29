# -*- coding: utf-8 -*-
"""
MODELO 1 - ANCHO DEL CORDON
Modelo mixto con intercepto aleatorio por estudio (version clasica, corre ya).

Pregunta: ¿cuanto de la variacion del ancho la explica el LABORATORIO
          y cuanto los PARAMETROS?

La version bayesiana (modelo_01_ancho.R con brms) es la definitiva para la
tesis, porque con 10 estudios el metodo clasico subestima la varianza entre
grupos. Esta version da la magnitud y permite avanzar hoy.
"""
import numpy as np, pandas as pd, statsmodels.formula.api as smf

CV_ANCHO = 0.0384          # piso de error medido en replicas (hoja 11_PISO_ERROR)

d = pd.read_csv("MODELADO.csv")
d = d.dropna(subset=["W_mm", "WFS_TS", "TS_mm_s"]).copy()
d["estudio"] = d["paper_id"].astype("category")
d["grupo"]   = (d["aplicacion"] + "_" + np.where(d["alambre_clase"].str.contains("316|317|308|2209|2507|2594|inox", regex=True), "inox", "carbono")).astype("category")
d["familia"] = np.where(d["alambre_clase"].str.contains(
    "316|317|308|2209|2507|2594|inox", regex=True), "inox", "carbono")
# logaritmos: las relaciones del proceso son multiplicativas
d["lW"]  = np.log(d["W_mm"])
d["lQ"]  = np.log(d["WFS_TS"]);  d["lQ"]  -= d["lQ"].mean()
d["lTS"] = np.log(d["TS_mm_s"]); d["lTS"] -= d["lTS"].mean()

print("="*66); print(" MODELO 1 - ANCHO DEL CORDON"); print("="*66)
print(f"  n = {len(d)}   estudios = {d['estudio'].nunique()}")
print(f"  W: {d.W_mm.min():.2f} a {d.W_mm.max():.2f} mm  (media {d.W_mm.mean():.2f})")
print(d["familia"].value_counts().to_string(), "\n")

# (1|estudio) = intercepto aleatorio: el desvio propio de cada laboratorio.
# Ese termino es el equivalente estadistico del factor de calibracion que
# despues estimaras en tu taller con las probetas.
m = smf.mixedlm("lW ~ lQ + lTS + C(familia)", d,
                groups=d["estudio"]).fit(reml=True)
print(m.summary())

sd_lab   = float(np.sqrt(m.cov_re.iloc[0, 0]))
sd_resid = float(np.sqrt(m.scale))
icc      = sd_lab**2 / (sd_lab**2 + sd_resid**2)

print("\n" + "="*66); print(" RESULTADO PRINCIPAL"); print("="*66)
print(f"  sd entre laboratorios : {sd_lab:.4f} (log)  ~ {100*(np.exp(sd_lab)-1):5.1f} %")
print(f"  sd residual (ruido)   : {sd_resid:.4f} (log)  ~ {100*(np.exp(sd_resid)-1):5.1f} %")
print(f"  ICC = {icc:.3f}  ->  el laboratorio explica el {100*icc:.0f} % de la varianza")
print(f"\n  Piso de error medido en replicas: {100*CV_ANCHO:.2f} %")
print(f"  Residuo del modelo             : {100*(np.exp(sd_resid)-1):.2f} %")
print("  Si el residuo se acerca al piso, el modelo toco el techo de precision")
print("  del proceso: no queda senal por capturar, solo ruido.")

print("\n  Desvio de cada laboratorio respecto al promedio:")
re = (pd.Series({k: v.iloc[0] for k, v in m.random_effects.items()})
        .sort_values().rename("efecto").to_frame())
re["desvio_%"] = 100*(np.exp(re["efecto"]) - 1)
print(re.round(3).to_string())

# ---------------- validacion dejando-un-laboratorio-fuera ----------------
# Se predice SIN conocer el desvio del laboratorio excluido: es exactamente
# la situacion de tu taller antes de calibrar.
print("\n  Validacion dejando-un-laboratorio-fuera:")
out = []
for L in d["estudio"].cat.categories:
    tr, te = d[d.estudio != L].copy(), d[d.estudio == L].copy()
    if len(te) < 3 or tr["estudio"].nunique() < 3:
        continue
    # solo se conservan los factores que siguen teniendo 2 niveles al excluir L
    terms = ["lQ", "lTS"]
    for v in ("familia",):
        if tr[v].astype(str).nunique() > 1 and te[v].astype(str).nunique() >= 1:
            terms.append(f"C({v})")
    frm = "lW ~ " + " + ".join(terms)
    try:
        fit = smf.mixedlm(frm, tr, groups=tr["estudio"]).fit(reml=True)
        pred = np.exp(fit.predict(te))                 # efectos fijos solamente
    except Exception as e:
        print(f"    {L}: no converge ({type(e).__name__})"); continue
    out.append({"estudio": L, "n": len(te),
                "MAPE_%": float(np.mean(np.abs(pred - te.W_mm)/te.W_mm)*100)})
res = pd.DataFrame(out)
print(res.round(1).to_string(index=False))
print(f"\n  MAPE medio SIN calibrar = {res['MAPE_%'].mean():.1f} %"
      f"   (piso experimental: {100*CV_ANCHO:.1f} %)")
print("  La diferencia entre ambos es LO QUE LA CALIBRACION PUEDE RECUPERAR.")
res.to_csv("validacion_lolo_ancho_A.csv", index=False)
print("\n  Guardado: validacion_lolo_ancho_A.csv")
