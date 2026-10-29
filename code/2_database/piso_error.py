# -*- coding: utf-8 -*-
"""Consolidacion del PISO DE ERROR: dispersion entre replicas verdaderas.
   Solo usa grupos de corridas con parametros identicos dentro de un mismo estudio."""
import csv, statistics as st
from collections import defaultdict

RESP = ["W_mm","R_mm","P_mm","D_pct","IC_pct","W_P","ZAT_mm"]
PRED = ["I_amp","V_arco","WFS_m_min","TS_mm_s","CTWD_mm","stickout_mm","NPD_mm",
        "angulo_deg","temp_precal_C","f_pulso_Hz"]

rows=list(csv.DictReader(open("../FCAW_MAESTRA.csv",encoding="utf-8-sig")))
def f(v):
    try: return float(v)
    except: return None

# --- agrupar por (estudio, combinacion de predictores) ---
g=defaultdict(list)
for r in rows:
    if r["conjunto"] in ("comparativo",): continue
    key=(r["paper_id"], tuple(r[c] for c in PRED))
    g[key].append(r)

EXCL={"19_Balan2018"}   # centrales no independientes (valores copiados)

print("="*94)
print("PISO DE ERROR - grupos de replicas verdaderas (>=3 corridas, mismos parametros)")
print("="*94)
res=defaultdict(list)
detalle=[]
for (pid,key),grp in sorted(g.items()):
    if len(grp)<3: continue
    if all(v in (None,"","None") for v in key): continue   # sin predictores (Beczkowski): no son replicas
    nota = "EXCLUIDO (replicas no independientes)" if pid in EXCL else ""
    fila={"paper":pid,"n":len(grp),"nota":nota}
    for c in RESP:
        v=[f(r[c]) for r in grp]; v=[x for x in v if x is not None]
        if len(v)<3: continue
        m=st.mean(v)
        if m==0: continue
        cv=100*st.stdev(v)/m
        mapd=100*st.mean(abs(x-m) for x in v)/m      # desviacion absoluta media porcentual: homogenea con el MAPE
        fila[c]=round(cv,2)
        if not nota: res[c].append((pid,cv,len(v),mapd))
    detalle.append(fila)

hdr=f"{'estudio':26s}{'n':>3}  "+"".join(f"{c:>9s}" for c in RESP)
print(hdr); print("-"*len(hdr))
for d in detalle:
    print(f"{d['paper'][:26]:26s}{d['n']:3d}  "+"".join(f"{d.get(c,'—'):>9}" for c in RESP)+("  "+d["nota"] if d["nota"] else ""))

print()
print("="*94)
print("CV CONSOLIDADO POR RESPUESTA  (excluye grupos con replicas no independientes)")
print("="*94)
print(f"{'respuesta':10s}{'grupos':>8}{'CV min':>9}{'CV med':>9}{'CV max':>9}{'mediana':>9}   estudios")
print("-"*94)
resumen={}
for c in RESP:
    L=res.get(c,[])
    if not L: continue
    cvs=[x[1] for x in L]; mapds=[x[3] for x in L]
    resumen[c]=(len(L),min(cvs),st.mean(cvs),max(cvs),st.median(cvs),st.median(mapds))
    print(f"{c:10s}{len(L):8d}{min(cvs):9.2f}{st.mean(cvs):9.2f}{max(cvs):9.2f}{st.median(cvs):9.2f}   "
          + ", ".join(x[0].split('20')[0][:9] for x in L))

print()
print("="*94)
print("CONCLUSION")
print("="*94)
if resumen:
    ord_=sorted(resumen.items(), key=lambda kv: kv[1][4])
    for c,(n,mn,me,mx,md,mapd) in ord_:
        cat = "PRECISA" if md<5 else ("MEDIA" if md<10 else "RUIDOSA")
        print(f"  {c:10s} mediana CV = {md:5.2f}%   mediana MAPD = {mapd:5.2f}%   [{mn:.2f}-{mx:.2f}]   n={n} grupos   -> {cat}")
