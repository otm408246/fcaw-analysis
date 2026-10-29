# -*- coding: utf-8 -*-
"""
MODELO 2 - ANALISIS DE SENSIBILIDAD DEL ANCHO (version clasica, statsmodels)

Reajusta el modelo mixto del ancho bajo distintas exclusiones y covariables, y
reporta para cada configuracion las cantidades de Nakagawa et al. (2017):

  ICC ajustado   = s2_alpha / (s2_alpha + s2_eps)          <- el que se reporta
  ICC no ajust.  = s2_alpha / (s2_f + s2_alpha + s2_eps)
  R2 marginal    = s2_f / (s2_f + s2_alpha + s2_eps)        solo efectos fijos
  R2 condicional = (s2_f + s2_alpha) / (...)                fijos + laboratorio

donde s2_f = var(X beta) es la varianza explicada por los efectos fijos.
Respuesta: log(W_mm). Requiere las columnas WFS_origen y tecnica en MODELADO.csv
(generadas por _scripts/wfs_origen_y_tecnica.py).
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, statsmodels.formula.api as smf

IMPUTADOS = ["03_Palani2006", "04_Palani2007", "07_Kumar2011"]
OSCILADO  = "17_Senthilkumar2015"
KUMAR     = "07_Kumar2011"

d0 = pd.read_csv("MODELADO.csv").dropna(subset=["W_mm", "WFS_TS", "TS_mm_s"]).copy()
d0["familia"] = np.where(d0.alambre_clase.str.contains("316|317|308|2209|2507|2594|inox", regex=True), "inox", "carbono")
d0["lW"] = np.log(d0.W_mm)

def ajustar(d, con_tecnica=False):
    d = d.copy()
    d["lQ"]  = np.log(d.WFS_TS)  - np.log(d.WFS_TS).mean()
    d["lTS"] = np.log(d.TS_mm_s) - np.log(d.TS_mm_s).mean()
    terms = ["lQ", "lTS"]
    for v in ["familia"] + (["tecnica"] if con_tecnica else []):
        if d[v].nunique() > 1: terms.append(f"C({v})")
    m = smf.mixedlm("lW ~ " + " + ".join(terms), d, groups=d.paper_id).fit(reml=True)
    s2a, s2e = float(m.cov_re.iloc[0, 0]), float(m.scale)
    s2f = float(np.var(m.model.exog @ m.fe_params.values, ddof=0))   # var(X beta): Nakagawa ec. 2.6
    tot = s2f + s2a + s2e
    return dict(n=len(d), estudios=d.paper_id.nunique(),
                sd_lab=np.sqrt(s2a), sd_res=np.sqrt(s2e),
                ICC_aj=s2a/(s2a+s2e), ICC_noaj=s2a/tot,
                R2_marg=s2f/tot, R2_cond=(s2f+s2a)/tot,
                b_lQ=m.fe_params["lQ"], b_lTS=m.fe_params["lTS"])

CONF = {
 "A  todo":                                (d0, False),
 "B  sin los 3 imputados (H-048)":         (d0[~d0.paper_id.isin(IMPUTADOS)], False),
 "C  sin Senthilkumar2015 (oscilado)":     (d0[d0.paper_id != OSCILADO], False),
 "D  sin Kumar2011":                       (d0[d0.paper_id != KUMAR], False),
 "E  sin Kumar2011 ni Senthilkumar2015":   (d0[~d0.paper_id.isin([KUMAR, OSCILADO])], False),
 "F  todo + tecnica como covariable":      (d0, True),
 "G  sin imputados + tecnica":             (d0[~d0.paper_id.isin(IMPUTADOS)], True),
 "H  sin imputados ni oscilado":           (d0[~d0.paper_id.isin(IMPUTADOS + [OSCILADO])], False),
}
rows = []
for k, (d, t) in CONF.items():
    r = ajustar(d, t); r["config"] = k; rows.append(r)
res = pd.DataFrame(rows).set_index("config")
pd.set_option("display.width", 160)
print("=" * 110); print(" SENSIBILIDAD DEL MODELO DE ANCHO  -  cantidades de Nakagawa et al. (2017)"); print("=" * 110)
print(res[["n", "estudios", "ICC_aj", "ICC_noaj", "R2_marg", "R2_cond", "sd_lab", "sd_res", "b_lQ", "b_lTS"]].round(3).to_string())
print()
print("  ICC_aj   = ICC AJUSTADO (el que se reporta)   R2_marg = solo parametros   R2_cond = parametros + laboratorio")
print("  brecha R2_cond - R2_marg = contribucion del laboratorio = lo que la calibracion puede recuperar")
print(f"  piso de error del ancho (H-034): 3.84 %  ->  sd_res comparable ~ 0.038 en log")
res.round(4).to_csv("sensibilidad_ancho.csv")
print("\n  Guardado: sensibilidad_ancho.csv")
