# -*- coding: utf-8 -*-
"""
Prepara el RE-TAMIZAJE de los 1 636 registros unicos de la busqueda documentada
(BUSQUEDA_OpenAlex_2026-09-14.csv):

  1. descarga resumen, tipo e idioma de cada registro desde OpenAlex (50 por llamada)
  2. marca los que ya estan en el corpus (01_ESTUDIOS) o en los 317 candidatos de agosto
  3. escribe _busqueda/TAMIZAJE_1636/registros.csv y lo parte en 8 lotes para los agentes

Se ejecuta desde dataset/.
"""
import urllib.request, urllib.parse, json, time, re, os
import pandas as pd

KEY = os.environ.get("OPENALEX_API_KEY", "")
OUT = "_busqueda/TAMIZAJE_1636"; os.makedirs(OUT, exist_ok=True)
u = pd.read_csv("_busqueda/BUSQUEDA_OpenAlex_2026-09-14.csv")

def inv2txt(inv):
    if not inv: return ""
    pos = {}
    for w, ps in inv.items():
        for p in ps: pos[p] = w
    return " ".join(pos[i] for i in sorted(pos))

ids = u.openalex_id.str.replace("https://openalex.org/", "", regex=False).tolist()
meta = {}
for i in range(0, len(ids), 50):
    lote = "|".join(ids[i:i+50])
    url = (f"https://api.openalex.org/works?filter=openalex_id:{lote}&per-page=50"
           f"&select=id,type,language,abstract_inverted_index,title&api_key={KEY}")
    for intento in range(4):
        try:
            d = json.load(urllib.request.urlopen(url, timeout=60)); break
        except Exception: time.sleep(2 * (intento + 1))
    for r in d["results"]:
        meta[r["id"]] = dict(tipo=r.get("type"), idioma=r.get("language"),
                             resumen=inv2txt(r.get("abstract_inverted_index")))
    print(f"  {min(i+50, len(ids))}/{len(ids)}", end="\r")
print()
u["tipo"]    = u.openalex_id.map(lambda k: meta.get(k, {}).get("tipo"))
u["idioma"]  = u.openalex_id.map(lambda k: meta.get(k, {}).get("idioma"))
u["resumen"] = u.openalex_id.map(lambda k: meta.get(k, {}).get("resumen", ""))
print("con resumen:", (u.resumen.str.len() > 50).sum(), "de", len(u))

# ---- marcar lo ya conocido
est = pd.read_excel("FCAW_BASE_FINAL.xlsx", "01_ESTUDIOS")
dc = [c for c in est.columns if "doi" in c.lower()][0]; ic = [c for c in est.columns if "id" in c.lower()][0]
corpus = {str(d).lower().replace("https://doi.org/", ""): i for d, i in zip(est[dc], est[ic]) if pd.notna(d)}
cand = pd.read_csv("_busqueda/BUSQUEDA_OpenAlex_candidatos.csv")
cand_doi = set(cand.doi.dropna().astype(str).str.replace("https://doi.org/", "", regex=False).str.lower())
u["doi"] = u.doi.fillna("").astype(str).str.lower()
u["ya_en_corpus"]    = u.doi.map(lambda d: corpus.get(d, ""))
u["en_317_agosto"]   = u.doi.isin(cand_doi)
print("ya en corpus:", (u.ya_en_corpus != "").sum(), "· en los 317 de agosto:", u.en_317_agosto.sum())

u = u.sort_values(["citas"], ascending=False).reset_index(drop=True)
u.insert(0, "n", range(1, len(u) + 1))
cols = ["n", "openalex_id", "doi", "anio", "tipo", "idioma", "citas", "revista", "ejes", "ya_en_corpus", "en_317_agosto", "titulo", "resumen"]
u[cols].to_csv(f"{OUT}/registros.csv", index=False)
k = 8; tam = -(-len(u) // k)
for j in range(k):
    u[cols].iloc[j*tam:(j+1)*tam].to_csv(f"{OUT}/lote_{j+1}.csv", index=False)
print(f"escritos: registros.csv y lote_1..{k}.csv (~{tam} cada uno) en {OUT}/")
import os
