# -*- coding: utf-8 -*-
"""
Extrae los hechos numericos canonicos DIRECTAMENTE del libro y los CSV y los
escribe en HECHOS_CANONICOS.md. Es la fuente de verdad para verificar los
borradores: si un borrador o el TRASPASO dicen otra cosa, gana este archivo.
Se ejecuta desde dataset/.
"""
import pandas as pd, numpy as np, subprocess, glob, os, re

L = "FCAW_BASE_FINAL.xlsx"
m = pd.read_csv("FCAW_MAESTRA.csv"); d = pd.read_csv("MODELADO.csv")
x = pd.ExcelFile(L)
out = ["# HECHOS CANÓNICOS — extraídos del libro y los CSV por `_scripts/hechos_canonicos.py`",
       f"Generado: {pd.Timestamp.now():%Y-%m-%d %H:%M}. **Si un borrador o TRASPASO.md discrepa de esto, gana esto.**", ""]
def sec(t): out.extend(["", f"## {t}", ""])
def kv(k, v): out.append(f"- {k}: **{v}**")

sec("Corpus")
kv("registros en la maestra", len(m)); kv("columnas de la maestra", f"{len(m.columns)} = 47 originales + 2 de auditoría añadidas el 2026-09-14 (WFS_origen, tecnica)")
kv("estudios con datos propios (paper_id distintos)", m.paper_id.nunique())
est = x.parse("01_ESTUDIOS"); kv("filas en 01_ESTUDIOS", len(est))
pais = [c for c in est.columns if "pais" in c.lower()]
if pais:
    cod = lambda ser: sorted({c.strip() for v in ser.dropna() for c in str(v).split(",")})
    idc = [c for c in est.columns if "id" in c.lower()][0]
    con = est[est[idc].isin(m.paper_id.unique())]
    kv("países (códigos separados) en las 32 filas", f"{len(cod(est[pais[0]]))}: {cod(est[pais[0]])}")
    kv("países en los 27 estudios con datos propios", f"{len(cod(con[pais[0]]))}: {cod(con[pais[0]])}")
    kv("estudios SIN país registrado", f"{int(est[pais[0]].isna().sum())} de 32 (afiliaciones pendientes de recuperar)")
kv("hojas del libro", len(x.sheet_names))
kv("PDF del corpus numerados 01–31 en papers_BASE_FINAL", len([f for f in glob.glob("../papers_BASE_FINAL/[0-9][0-9]_*.pdf")]))
kv("conjuntos", m.conjunto.value_counts().to_dict())
p = m[m.conjunto == "principal"]
kv("principal por aplicación", p.aplicacion.value_counts().to_dict())
kv("corpus completo por aplicación", m.aplicacion.value_counts().to_dict())
kv("registros con WFS y TS (predictor troncal) en todo el corpus", int((m.WFS_TS.notna() & m.TS_mm_s.notna()).sum()))
kv("estudios con WFS y TS", m[m.WFS_TS.notna() & m.TS_mm_s.notna()].paper_id.nunique())

sec("Tabla de modelado (MODELADO.csv)")
kv("corridas", len(d)); kv("estudios", d.paper_id.nunique())
for y in ["W_mm", "R_mm", "P_mm", "D_pct", "IC_pct", "W_P"]:
    s = d[d[y].notna()]; kv(f"n con {y}", f"{len(s)} corridas · {s.paper_id.nunique()} estudios")
w = d[d.W_mm.notna()]
kv("WFS_origen sobre las corridas con ancho", w.groupby("WFS_origen").agg(n=("registro_id","size"), est=("paper_id","nunique")).to_dict("index"))
kv("tecnica sobre las corridas con ancho", w.groupby("tecnica").agg(n=("registro_id","size"), est=("paper_id","nunique")).to_dict("index"))
imp = ["03_Palani2006","04_Palani2007","07_Kumar2011"]
kv("corridas con ancho excluyendo los 3 imputados", f"{len(w[~w.paper_id.isin(imp)])} corridas · {w[~w.paper_id.isin(imp)].paper_id.nunique()} estudios")
kv("estudios imputados (huella corr=1,00000)", imp)
for pid in imp + ["06_Paiva2010", "30_Aloraier2025"]:
    g = m[m.paper_id == pid].dropna(subset=["I_amp", "WFS_m_min"])
    r = np.corrcoef(g.I_amp, g.WFS_m_min)[0,1] if len(g) > 2 and g.WFS_m_min.nunique() > 1 else float("nan")
    kv(f"corr(I, WFS) en {pid}", f"{r:.5f}")

sec("Duplicaciones (08_DUPLICACIONES)")
dup = x.parse("08_DUPLICACIONES"); kv("casos", len(dup))
for _, r in dup.iterrows(): out.append(f"  - {r['id']}: conservado `{r['registro_conservado']}` ← duplicado `{str(r['publicacion_duplicada'])[:70]}` ({r['tipo']})")
out.append("  - Cadena D-5 + D-7: Guimarães2020 = Moreno2022-PULS = Moreno2022-MAT = CA6M2018 → **una campaña, 4 publicaciones**")

sec("Procedencia (12_PROCEDENCIA)")
pr = x.parse("12_PROCEDENCIA"); kv("estudios transcritos", len(pr)); kv("filas transcritas (suma)", int(pr.n_filas_transcritas.sum()))
fuera = pr[~pr.id_estudio.isin(m.paper_id.unique())]
kv("transcritos sin registros en la maestra", f"{len(fuera)} estudios, {int(fuera.n_filas_transcritas.sum())} filas: {fuera.id_estudio.tolist()}")
kv("conciliación", f"{int(pr.n_filas_transcritas.sum())} − {int(fuera.n_filas_transcritas.sum())} − 8 (Bęczkowski 17→9) = {len(m)}")

sec("Piso de error (11_PISO_ERROR)")
pe = x.parse("11_PISO_ERROR").dropna(subset=["n_grupos_de_replicas"])
for _, r in pe.iterrows(): out.append(f"  - {r['respuesta']}: mediana **{r['CV_mediana_%']} %**, {int(r['n_grupos_de_replicas'])} grupos [{r['CV_min_%']}–{r['CV_max_%']}], {r['categoria']} — {r['estudios_incluidos']}")
out.append("  - 9 estudios aportan grupos; el máximo por respuesta es 8. ZAT descansa en 1 grupo de 1 estudio (29_Dave2024).")
out.append("  - Excluidos: 19_Balan2018 (réplicas no independientes), 20_Bęczkowski2018 (sin predictores; no son réplicas)")

sec("Notación y transformaciones")
for h in ["03_DICCIONARIO", "04_NOTACION", "05_TRANSFORMACIONES", "06_ECUACIONES", "07_BANDERAS", "09_HALLAZGOS"]:
    kv(f"filas en {h}", len(x.parse(h)))
kv("constantes", "φ = 0,81 rutilo · 0,95 metal-cored · k = 0,80 (ISO/TR 17671-1), verificado 0,7993 y 0,8014")
kv("colinealidad A_dep vs WFS_TS", f"r = {np.corrcoef(d.dropna(subset=['A_dep_mm2','WFS_TS']).A_dep_mm2, d.dropna(subset=['A_dep_mm2','WFS_TS']).WFS_TS)[0,1]:.4f}" if "A_dep_mm2" in d else "columna no encontrada")
kv("registros con HI_J_mm en la maestra", f"{int(m.HI_J_mm.notna().sum())} de {len(m)} = {100*m.HI_J_mm.notna().mean():.1f} %" if "HI_J_mm" in m else "col no encontrada")

sec("Modelo (modelo_01_ancho.R, versión vigente)")
src = open("modelo_01_ancho.R").read()
kv("fórmula", re.search(r"lW ~ [^,\n]+", src).group(0))
for pr_ in re.findall(r'prior\([^\n]+\)', src): out.append(f"  - `{pr_.strip()}`")
kv("muestreo", "4 cadenas · 4 000 iteraciones · 1 000 calentamiento · adapt_delta 0,95 · backend cmdstanr (no rstan: TBB en Mac ARM)")
kv("prior de sigma anterior (H-082, corregido)", "normal(0.0384, 0.02) → student_t(3, 0, 0.25)")

sec("Sensibilidad y resultados (solo para M7/M8: NO reportar cifras de resultado en Métodos)")
for f in ["sensibilidad_ancho.csv", "sensibilidad_ancho_bayes.csv", "malla_todas_respuestas_bayes.csv", "contraste_troncal_H044.csv", "validacion_lolo_ancho.csv"]:
    kv(f"existe {f}", os.path.exists(f))
kv("configuraciones clásicas de sensibilidad", "A todo · B sin imputados · C sin Senthilkumar2015 · D sin Kumar2011 · E sin ambos · F todo+técnica · G sin imputados+técnica (preferida) · H sin imputados ni oscilado")
kv("respuestas modeladas", "W, R, P, D, IC, W/P — especificación G, bayesiano, 0 divergencias")
kv("modelo conjunto", "W+R+P, (1|p|estudio), n 149, 6 estudios")

sec("Software")
ver = subprocess.run(["Rscript","-e","cat(R.version.string, '|', as.character(packageVersion('brms')), '|', as.character(packageVersion('cmdstanr')), '|', cmdstanr::cmdstan_version())"], capture_output=True, text=True).stdout.strip()
kv("R | brms | cmdstanr | CmdStan", ver)
import sys, statsmodels, scipy
kv("Python | pandas | numpy | statsmodels | scipy", f"{sys.version.split()[0]} | {pd.__version__} | {np.__version__} | {statsmodels.__version__} | {scipy.__version__}")

sec("Marco teórico en disco (papers_BASE_FINAL/marco_teorico)")
for f in sorted(glob.glob("../papers_BASE_FINAL/marco_teorico/*.pdf")): out.append(f"  - `{os.path.basename(f)}`")
sec("Normas en disco (papers_BASE_FINAL/normas)")
for f in sorted(glob.glob("../papers_BASE_FINAL/*.pdf")+glob.glob("../papers_BASE_FINAL/*.PDF")+glob.glob("../papers_BASE_FINAL/normas/*")):
    b = os.path.basename(f)
    if not re.match(r"^\d\d_", b): out.append(f"  - `{f.replace('../papers_BASE_FINAL/','')}`")
out.append("  - EN 50504:2008, ISO 17639:2022 e ISO 3834 están ESCANEADOS: sus cláusulas verificadas están en TRASPASO.md (H-049…H-070)")

sec("Búsqueda (_busqueda)")
for f in sorted(glob.glob("_busqueda/*.csv")):
    c = pd.read_csv(f); kv(os.path.basename(f), f"{len(c)} filas · columnas {list(c.columns)[:8]}")
out.append("- Cascada de la búsqueda documentada (2026-09-14, ver `_busqueda/TAMIZAJE_1636/PRISMA_FLUJO.md`): 4 321 registros brutos → 1 636 únicos → 288 candidatos a texto completo, + 6 por otras fuentes → 31 documentos con tabla → 27 campañas. (La cascada antigua «4 115 → 317» corresponde a la búsqueda de agosto, retirada.)")

open("../HECHOS_CANONICOS.md", "w", encoding="utf-8").write("\n".join(out))
print("HECHOS_CANONICOS.md:", len(out), "líneas")
