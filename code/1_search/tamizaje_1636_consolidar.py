# -*- coding: utf-8 -*-
"""
Consolida el tamizaje en dos etapas y produce el flujo PRISMA-IPD:
  veredicto_reglas.csv (etapa 1, 1 636) + veredicto_residuo_1..6.csv (etapa 2, 555)
  -> TAMIZAJE_FINAL.csv   una fila por registro con veredicto final, etapa, codigo, motivo
  -> PRISMA_FLUJO.md      cifras de cada caja + diagrama mermaid + prueba de sensibilidad
Se ejecuta desde dataset/.
"""
import glob, pandas as pd
from datetime import date
D = "_busqueda/TAMIZAJE_1636"

r = pd.read_csv(f"{D}/veredicto_reglas.csv")
res = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(f"{D}/veredicto_residuo_*.csv"))], ignore_index=True)
assert res.openalex_id.is_unique, "ids duplicados entre lotes"
res = res.rename(columns={"veredicto": "veredicto_ag", "codigo": "codigo_ag", "motivo": "motivo_ag"})
t = r.merge(res[["openalex_id", "C1", "C2", "C3", "C4", "veredicto_ag", "codigo_ag", "motivo_ag"]], on="openalex_id", how="left")

t["etapa"]     = t.veredicto_reglas.map({"EXCLUIR": "1_reglas", "RESIDUO": "2_agentes"})
t["veredicto"] = t.veredicto_reglas.where(t.veredicto_reglas == "EXCLUIR", t.veredicto_ag)
t["codigo"]    = t.codigo_reglas.where(t.veredicto_reglas == "EXCLUIR", t.codigo_ag)
t["motivo"]    = t.motivo_reglas.where(t.veredicto_reglas == "EXCLUIR", t.motivo_ag)
faltan = t[t.veredicto.isna()]
if len(faltan): print(f"⚠️ {len(faltan)} registros del residuo sin veredicto de agente (lotes incompletos)")

corpus = t.ya_en_corpus.fillna("") != ""
n = len(t); e1 = t[t.etapa == "1_reglas"]; e2 = t[t.etapa == "2_agentes"]
inc = t[t.veredicto == "INCLUIR"]; dud = t[t.veredicto == "DUDOSO"]; exc2 = e2[e2.veredicto == "EXCLUIR"]
tc = inc.shape[0] + dud.shape[0]
sens_inc = int((corpus & (t.veredicto == "INCLUIR")).sum()); sens_dud = int((corpus & (t.veredicto == "DUDOSO")).sum()); sens_exc = int((corpus & (t.veredicto == "EXCLUIR")).sum())

cols = ["n", "openalex_id", "doi", "anio", "tipo", "idioma", "citas", "revista", "titulo", "ya_en_corpus", "en_317_agosto", "etapa", "veredicto", "codigo", "motivo", "C1", "C2", "C3", "C4"]
t[cols].to_csv(f"{D}/TAMIZAJE_FINAL.csv", index=False)

def cod(df): return df.codigo.value_counts().to_dict()
md = f"""# Flujo PRISMA-IPD — búsqueda documentada del 2026-09-14, tamizaje consolidado el {date.today()}

## Cifras

| Caja | n |
|---|---|
| Registros identificados en OpenAlex (15 cadenas, 4 ejes, suma bruta con solapes) | 4 321 |
| **Registros únicos tras eliminar duplicados por identificador** | **{n}** |
| Tamizados por título y resumen — etapa 1, reglas documentadas | {n} |
| Excluidos en etapa 1 | {len(e1)} |
| Residuo a etapa 2, juicio por criterios C1–C4 | {len(e2)} |
| Excluidos en etapa 2 | {len(exc2)} |
| **Candidatos a texto completo** (INCLUIR {len(inc)} + DUDOSO {len(dud)}) | **{tc}** |
| Identificados por otras fuentes (colección previa, búsqueda manual, referencias cruzadas) | 6 |
| Estudios incluidos en el corpus (campañas con datos propios) | 27 |

### Exclusiones por código
- Etapa 1 (reglas): {cod(e1)}
- Etapa 2 (agentes): {cod(exc2)}

## Prueba de sensibilidad
De los **24 estudios del corpus** presentes entre los {n} registros: **INCLUIR {sens_inc} · DUDOSO {sens_dud} · EXCLUIR {sens_exc}**.
Sensibilidad del tamizaje (no excluidos / 24) = **{(24 - sens_exc) / 24:.0%}**. Los DUDOSO son registros sin resumen en OpenAlex; el protocolo los envía a texto completo.

## Cobertura
- Candidatos de agosto (317) presentes entre los {n}: {int(t.en_317_agosto.sum())}
- Corpus (27 con datos propios): 24 recuperados por la búsqueda documentada; 6 filas de `01_ESTUDIOS` no recuperadas (Paiva 2010, Zhang 2016, Guimarães 2020, Singh 2021, Solovyov 2023, Odhiambo 2025: portugués, ucraniano o sin DOI) → *otras fuentes*.

## Diagrama

```mermaid
flowchart TD
  A["Identificados en OpenAlex<br/>4 321 (suma bruta) → <b>{n} únicos</b>"] --> B["Tamizaje título/resumen<br/>etapa 1: reglas documentadas"]
  B -->|excluidos {len(e1)}| X1["E1 no FCAW · E5 fuera de tema<br/>E4 aditiva · E3 revisión"]
  B --> C["Residuo {len(e2)}<br/>etapa 2: criterios C1–C4"]
  C -->|excluidos {len(exc2)}| X2["E2 sin geometría · E1 · E3 · E5"]
  C --> D["Candidatos a texto completo<br/>INCLUIR {len(inc)} + DUDOSO {len(dud)} = <b>{tc}</b>"]
  O["Otras fuentes<br/>colección previa, manual, referencias<br/><b>6</b>"] --> E
  D --> E["Texto completo evaluado<br/>31 PDF con tabla de datos<br/>(4 duplicados + 1 sin matriz + 1 desdoblado)"]
  E --> F["<b>27 campañas incluidas</b><br/>477 registros"]
```

## Archivos
`registros.csv` (entrada) · `veredicto_reglas.csv` (etapa 1) · `veredicto_residuo_1..6.csv` (etapa 2) · `TAMIZAJE_FINAL.csv` (consolidado) · `PROTOCOLO_TAMIZAJE.md` · `_scripts/tamizaje_1636_reglas.py`
"""
open(f"{D}/PRISMA_FLUJO.md", "w", encoding="utf-8").write(md)
print(md)
