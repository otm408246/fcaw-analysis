# -*- coding: utf-8 -*-
"""
Busqueda REPRODUCIBLE en OpenAlex para la figura PRISMA-IPD.

Motivo: la busqueda original (agosto de 2026) dejo 317 candidatos triados en
_busqueda/BUSQUEDA_OpenAlex_candidatos.csv pero NO conservo las cadenas de
consulta ni el conteo bruto (el '4 115' de TRASPASO no traza a ningun archivo).
Este script define cadenas explicitas por eje, registra fecha y conteos, y
mide la cobertura de la busqueda documentada sobre (a) los 317 candidatos y
(b) los 31 PDF del corpus. Lo que la busqueda no recupere se declara en PRISMA
como 'identificado por otras fuentes'.

Se ejecuta desde dataset/. Salidas en _busqueda/ con fecha en el nombre.
"""
import urllib.request, urllib.parse, json, time, csv, re, os
from datetime import date
import pandas as pd

KEY  = os.environ.get("OPENALEX_API_KEY", "")
HOY  = date.today().isoformat()
MAX_POR_CONSULTA = 2000                       # tope de registros descargados por cadena (el conteo bruto se guarda aparte)

# Cadenas de busqueda por eje. OpenAlex 'search' busca en titulo+resumen; soporta frases entre comillas.
# No soporta OR fiable: cada alternativa es una consulta y se unen por id.
EJES = {
  "recargue":    ['"flux cored arc welding" cladding', '"flux cored arc welding" overlay',
                  '"flux cored arc welding" hardfacing', '"flux cored" cladding "bead geometry"',
                  'FCAW cladding dilution'],
  "BOP/general": ['"flux cored arc welding" "bead geometry"', '"flux cored arc welding" penetration "bead width"',
                  '"flux cored" "weld bead" geometry', 'FCAW "bead geometry" parameters',
                  '"flux cored arc welding" "response surface"', '"flux cored arc welding" Taguchi bead'],
  "subacuatica": ['"flux cored" underwater welding bead', 'underwater "flux cored arc welding"'],
  "estructural": ['"flux cored arc welding" fillet "bead geometry"', '"flux cored arc welding" "weld joint" geometry parameters'],
}
FILTRO = "type:article|preprint|book-chapter|dissertation"

def consulta(q, cursor="*"):
    url = ("https://api.openalex.org/works?search=" + urllib.parse.quote(q) +
           f"&filter={urllib.parse.quote(FILTRO)}&per-page=200&cursor={cursor}"
           f"&select=id,doi,title,publication_year,cited_by_count,primary_location&api_key={KEY}")
    for intento in range(4):
        try:
            return json.load(urllib.request.urlopen(url, timeout=60))
        except Exception as e:
            time.sleep(2 * (intento + 1))
    raise RuntimeError(f"OpenAlex no respondio: {q}")

registros, conteos = {}, []
for eje, cadenas in EJES.items():
    for q in cadenas:
        d = consulta(q); total = d["meta"]["count"]; bajados = 0; cursor = d["meta"].get("next_cursor")
        def absorber(res):
            global bajados
            for r in res:
                k = r["id"]; bajados += 1
                if k not in registros:
                    src = ((r.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
                    registros[k] = dict(openalex_id=k, doi=(r.get("doi") or "").replace("https://doi.org/", "").lower(),
                                        titulo=r.get("title") or "", anio=r.get("publication_year"),
                                        citas=r.get("cited_by_count", 0), revista=src, ejes=set())
                registros[k]["ejes"].add(eje)
        absorber(d["results"])
        while cursor and bajados < MAX_POR_CONSULTA:
            d = consulta(q, cursor); absorber(d["results"]); cursor = d["meta"].get("next_cursor")
            time.sleep(0.2)
        conteos.append(dict(eje=eje, cadena=q, conteo_bruto=total, descargados=bajados))
        print(f"  [{eje:12s}] {total:6d} brutos · {bajados:5d} descargados · {q}")

union = pd.DataFrame([{**v, "ejes": ";".join(sorted(v["ejes"]))} for v in registros.values()])
print(f"\nUNION sin duplicados por id: {len(union)} registros")

# ---- cobertura sobre los 317 candidatos originales y los 31 PDF del corpus
cand = pd.read_csv("_busqueda/BUSQUEDA_OpenAlex_candidatos.csv")
cand_doi = set(cand.doi.dropna().astype(str).str.replace("https://doi.org/", "", regex=False).str.lower())
est = pd.read_excel("FCAW_BASE_FINAL.xlsx", "01_ESTUDIOS")
dcol = [c for c in est.columns if "doi" in c.lower()][0]
corpus_doi = set(est[dcol].dropna().astype(str).str.replace("https://doi.org/", "", regex=False).str.lower())
u_doi = set(union.doi.dropna()) - {""}
def norm_t(t): return re.sub(r"[^a-z0-9]", "", str(t).lower())[:60]
u_tit = set(union.titulo.map(norm_t))
tcol = [c for c in est.columns if "titulo" in c.lower() or "title" in c.lower()]
corpus_tit = set(est[tcol[0]].dropna().map(norm_t)) if tcol else set()

cob_cand = len(cand_doi & u_doi); cob_corp_doi = len(corpus_doi & u_doi); cob_corp_tit = len(corpus_tit & u_tit)
print(f"cobertura: {cob_cand}/{len(cand_doi)} candidatos con DOI · {cob_corp_doi}/{len(corpus_doi)} DOI del corpus · "
      f"{cob_corp_tit}/{len(corpus_tit)} titulos del corpus")

# ---- salidas fechadas
os.makedirs("_busqueda", exist_ok=True)
union.sort_values("citas", ascending=False).to_csv(f"_busqueda/BUSQUEDA_OpenAlex_{HOY}.csv", index=False)
pd.DataFrame(conteos).to_csv(f"_busqueda/BUSQUEDA_OpenAlex_{HOY}_conteos.csv", index=False)
with open(f"_busqueda/BUSQUEDA_OpenAlex_{HOY}_resumen.md", "w", encoding="utf-8") as f:
    f.write(f"# Búsqueda OpenAlex reproducible — {HOY}\n\n")
    f.write(f"Filtro de tipo: `{FILTRO}`. Campos: título + resumen (`search`). Tope por cadena: {MAX_POR_CONSULTA} descargados; "
            f"el conteo bruto se registra íntegro.\n\n## Cadenas y conteos\n\n| eje | cadena | conteo bruto | descargados |\n|---|---|---|---|\n")
    for c in conteos: f.write(f"| {c['eje']} | `{c['cadena']}` | {c['conteo_bruto']} | {c['descargados']} |\n")
    f.write(f"\n**Suma de conteos brutos:** {sum(c['conteo_bruto'] for c in conteos)} (con solapes entre cadenas)  \n")
    f.write(f"**Unión sin duplicados por id:** {len(union)}\n\n## Cobertura de la búsqueda documentada\n\n")
    f.write(f"- Candidatos originales (317, agosto 2026) con DOI recuperados hoy: **{cob_cand} / {len(cand_doi)}**\n")
    f.write(f"- Estudios del corpus (`01_ESTUDIOS`) recuperados por DOI: **{cob_corp_doi} / {len(corpus_doi)}**; por título: **{cob_corp_tit} / {len(corpus_tit)}**\n")
    f.write("- Lo no recuperado se declara en PRISMA-IPD como *identificado por otras fuentes* (colección previa del autor, búsqueda manual, referencias cruzadas).\n")
print(f"\nGuardados en _busqueda/: BUSQUEDA_OpenAlex_{HOY}.csv, _conteos.csv, _resumen.md")
import os
