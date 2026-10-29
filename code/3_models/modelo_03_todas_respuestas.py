# -*- coding: utf-8 -*-
"""
MODELO 3 - TODAS LAS RESPUESTAS + CONTRASTE CON CORRIENTE COMO TRONCAL
(version clasica, statsmodels; la bayesiana es modelo_03_todas_respuestas.R)

Bloque 1  Malla por respuesta (W, R, P, D, IC, W/P) x especificacion:
            A  todo
            G  sin los 3 imputados (H-048) + tecnica como covariable   <- preferida
            A+ todo + Guimaraes2020 pulsado con covariable 'modo'      <- sensibilidad
          Reporta n, estudios, b_lQ, ICC ajustado, R2 marginal/condicional (Nakagawa 2017)
          y sigma frente al piso de error de esa respuesta (H-034).

Bloque 2  Contraste H-044: mismo modelo con CORRIENTE como troncal (lI en vez de lQ)
          sobre MODELADO_SENSIBILIDAD.csv (343 corridas, 16 estudios) y sobre las
          300 comunes. Si la corriente es respuesta y no consigna, su modelo debe
          transferir PEOR entre laboratorios: mayor sd_lab, peor MAPE dejando-un-lab-fuera.
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd, statsmodels.formula.api as smf

IMPUTADOS = ["03_Palani2006", "04_Palani2007", "07_Kumar2011"]
PISO = {"W_mm": .0384, "R_mm": .0287, "P_mm": .0792, "D_pct": .1020, "IC_pct": .0609, "W_P": .0896}
RESP = list(PISO)

def prep(d):
    d = d.copy()
    d["familia"] = np.where(d.alambre_clase.str.contains("316|317|308|2209|2507|2594|inox", regex=True), "inox", "carbono")
    d["lQ"]  = np.log(d.WFS_TS)  - np.log(d.WFS_TS).mean()
    d["lTS"] = np.log(d.TS_mm_s) - np.log(d.TS_mm_s).mean()
    if d.I_amp.notna().any():
        d["lI"] = np.log(d.I_amp) - np.log(d.I_amp.dropna()).mean()
    return d

def nakagawa(m):
    s2a, s2e = float(m.cov_re.iloc[0, 0]), float(m.scale)
    s2f = float(np.var(m.model.exog @ m.fe_params.values, ddof=0)); tot = s2f + s2a + s2e
    return dict(ICC_aj=s2a/(s2a+s2e), R2_marg=s2f/tot, R2_cond=(s2f+s2a)/tot, sd_lab=np.sqrt(s2a), sigma=np.sqrt(s2e))

def factores(d, cands):
    """Conserva solo factores con >1 nivel y que no dupliquen una particion ya incluida."""
    out, vistas = [], []
    for v in cands:
        if d[v].nunique() < 2: continue
        part = d[v].astype(str).factorize()[0].tolist()
        if any(part == p for p in vistas): continue        # misma particion que otro factor: singular
        vistas.append(part); out.append(f"C({v})")
    return out

def ajustar(d, y, troncal="lQ", extras=()):
    d = d.dropna(subset=[y, troncal, "lTS"]).copy(); d["ly"] = np.log(d[y])
    terms = [troncal, "lTS"] + factores(d, ["familia", *extras])
    m = smf.mixedlm("ly ~ " + " + ".join(terms), d, groups=d.paper_id).fit(reml=True)
    r = nakagawa(m); r.update(n=len(d), estudios=d.paper_id.nunique(), b_troncal=m.fe_params[troncal], b_lTS=m.fe_params["lTS"])
    return r, d

def lolo(d, y, troncal):
    """MAPE dejando-un-laboratorio-fuera, prediciendo solo con efectos fijos."""
    d = d.dropna(subset=[y, troncal, "lTS"]).copy(); d["ly"] = np.log(d[y]); out = []
    for L in d.paper_id.unique():
        tr, te = d[d.paper_id != L], d[d.paper_id == L]
        if len(te) < 3 or tr.paper_id.nunique() < 3: continue
        terms = [troncal, "lTS"] + [t for t in factores(tr, ["familia", "tecnica"]) if set(te[t[2:-1]]) <= set(tr[t[2:-1]])]
        try:
            f = smf.mixedlm("ly ~ " + " + ".join(terms), tr, groups=tr.paper_id).fit(reml=True)
            out.append(dict(estudio=L, n=len(te), MAPE=np.mean(np.abs(np.exp(f.predict(te)) - te[y]) / te[y]) * 100))
        except Exception: pass
    lolo.detalle = pd.DataFrame(out)          # por estudio, para escribir la tabla de validacion
    return lolo.detalle.MAPE.mean(), len(out)

base = prep(pd.read_csv("MODELADO.csv"))
pd.set_option("display.width", 170)

# ======================================================= BLOQUE 1
print("=" * 118); print(" BLOQUE 1 - MALLA POR RESPUESTA  (troncal WFS/TS)      ICC_aj y R2 de Nakagawa et al. 2017"); print("=" * 118)
# H-099: las 7 filas centrales de 19_Balan2018 (runs 25-31) son una observacion repetida (pseudo-replica).
# Se CONSERVAN en G (decision del autor, 2026-09-20) y se reporta la sensibilidad: colapsadas a una fila y sin Balan.
rid = pd.to_numeric(base.run_id_original, errors="coerce")
cen = base[(base.paper_id == "19_Balan2018") & (rid >= 25)]
una = cen.iloc[[0]].copy(); una[RESP] = cen[RESP].mean().values
sinG = base[~base.paper_id.isin(IMPUTADOS)]
rows = []
for y in RESP:
    for nom, d, ex in [("A  todo", base, ()),
                       ("G  sin imputados + tecnica", sinG, ("tecnica",)),
                       ("G-b  G, centro Balan = 1 fila", pd.concat([sinG.drop(cen.index), una]), ("tecnica",)),
                       ("G-c  G sin Balan", sinG[sinG.paper_id != "19_Balan2018"], ("tecnica",))]:
        try:
            r, _ = ajustar(d, y, "lQ", ex); r.update(respuesta=y, config=nom, piso=PISO[y], sigma_piso=r["sigma"]/PISO[y]); rows.append(r)
        except Exception as e:
            rows.append(dict(respuesta=y, config=nom, n=np.nan))
t1 = pd.DataFrame(rows).set_index(["respuesta", "config"])
print(t1[["n", "estudios", "b_troncal", "b_lTS", "ICC_aj", "R2_marg", "R2_cond", "sigma", "piso", "sigma_piso"]].round(3).to_string())
print("\n  b_troncal = elasticidad de la respuesta respecto a WFS/TS.  sigma_piso = residuo / piso de error (>1 = queda senal sin capturar)")

# sensibilidad con pulsado
try:
    ma = pd.read_csv("FCAW_MAESTRA.csv"); pul = ma[(ma.paper_id == "22_Guimaraes2020") & ma.WFS_TS.notna() & ma.TS_mm_s.notna()]
    amp = prep(pd.concat([pd.read_csv("MODELADO.csv"), pul], ignore_index=True)); amp["modo"] = np.where(amp.paper_id == "22_Guimaraes2020", "pulsado", "constante")
    r, _ = ajustar(amp, "W_mm", "lQ", ("modo",))
    print(f"\n  A+ (ancho, + Guimaraes2020 pulsado con covariable modo): n={r['n']} est={r['estudios']} b_lQ={r['b_troncal']:.3f} ICC_aj={r['ICC_aj']:.3f}")
    print("     -> Guimaraes tiene WFS constante: suma 18 filas y ningun grado de libertad para la pendiente. Solo sensibilidad.")
except Exception as e: print("  A+ no disponible:", e)
t1.round(4).to_csv("malla_todas_respuestas.csv")

# ======================================================= BLOQUE 2
print("\n" + "=" * 118); print(" BLOQUE 2 - CONTRASTE H-044: WFS/TS frente a CORRIENTE como troncal, cada uno en su dominio natural"); print("=" * 118)
sens = prep(pd.read_csv("MODELADO_SENSIBILIDAD.csv"))
sens["tecnica"] = np.where(sens.paper_id.isin(["02_Kannan2006", "17_Senthilkumar2015"]), "oscilado", "recto")
ambos = sens.dropna(subset=["WFS_TS", "I_amp"])
print(f"  Corridas con AMBOS troncales: {len(ambos)} de {len(sens)} ({ambos.paper_id.nunique()} estudios); "
      f"{ambos[ambos.paper_id.isin(IMPUTADOS)].shape[0]} de ellas con I y WFS colineales por la imputacion (H-048).")
print("  -> No existe comparacion sobre las mismas filas. Se compara cada troncal en el conjunto que lo reporta.\n")
rows = []
for y in ["W_mm", "R_mm", "P_mm"]:
    for nom, d, tr, ex in [("WFS/TS  (sin imputados + tecnica)", base[~base.paper_id.isin(IMPUTADOS)], "lQ", ("tecnica",)),
                           ("CORRIENTE (todos con I + tecnica)", sens, "lI", ("tecnica",)),
                           ("CORRIENTE (sin imputados* + tecnica)", sens[~sens.paper_id.isin(IMPUTADOS)], "lI", ("tecnica",))]:
        try:
            r, dd = ajustar(d, y, tr, ex); mape, k = lolo(d, y, tr)
            if y == "W_mm" and tr == "lQ" and nom.startswith("WFS/TS"):      # tabla de validacion del ancho, especificacion G (M8 8.2)
                lolo.detalle.to_csv("validacion_lolo_ancho.csv", index=False)
            rows.append(dict(respuesta=y, troncal=nom, n=r["n"], est=r["estudios"], b=r["b_troncal"], ICC_aj=r["ICC_aj"],
                             sd_lab=r["sd_lab"], sigma=r["sigma"], R2_marg=r["R2_marg"], MAPE_LOLO=mape, labs=k))
        except Exception as e: rows.append(dict(respuesta=y, troncal=nom, n=np.nan, err=type(e).__name__))
t2 = pd.DataFrame(rows).set_index(["respuesta", "troncal"])
print(t2.round(3).to_string())
print("\n  * en el modelo de corriente los 3 'imputados' tienen corriente REAL (lo imputado era WFS); se excluyen solo por simetria.")
print("  H-044 predice: la CORRIENTE como troncal transfiere PEOR (sd_lab mayor, MAPE dejando-un-lab-fuera mayor), porque es")
print("  respuesta de cada maquina y no consigna del proceso.")
t2.round(4).to_csv("contraste_troncal_H044.csv")
print("\n  Guardados: malla_todas_respuestas.csv · contraste_troncal_H044.csv")
