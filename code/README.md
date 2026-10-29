# Code

The analysis runs in three stages. Scripts keep their original Spanish names and comments; they are
the same files archived on Zenodo (v2.0), only arranged in folders.

**Which stages can be re-run from this repository alone?**
Stage 3 (models): yes, from `data/`. Stages 1 and 2: the scripts document exactly what was done, but
need inputs that are not distributed (OpenAlex API key, intermediate screening files, source PDFs).

## 1_search — literature search and screening (PRISMA-IPD)

| Script | What it does | Reads | Writes |
|---|---|---|---|
| `busqueda_openalex.py` | Runs the 15 search strings in OpenAlex | API (`OPENALEX_API_KEY`) | `BUSQUEDA_OpenAlex_<date>.csv`, counts, summary |
| `recuperar_metadatos.py` | Retrieves metadata of the included studies | API | `metadatos_openalex.json` |
| `tamizaje_1636_preparar.py` | Prepares the 1 636 records for screening | search CSV, workbook | `registros.csv`, batches |
| `tamizaje_1636_reglas.py` | Stage 1: excludes only the unambiguous cases by explicit rules | `registros.csv` | rule verdicts, residual batches |
| `tamizaje_1636_consolidar.py` | Merges both stages; destination of every record | verdicts | `TAMIZAJE_FINAL.csv`, `PRISMA_FLUJO.md` |

Stage 2 of the screening (residual batches, title and abstract only) was classified by AI assistants;
those verdict files are not included. Full-text selection was done by the author.

## 2_database — consolidation and audit

| Script | What it does | Reads | Writes |
|---|---|---|---|
| `datos_originales.py`, `datos_originales_v2.py` | The published tables, transcribed verbatim (v2 = 9 studies added later; both are used) | — | in memory |
| `construir_maestra.py`, `construir_maestra_v2.py` | Converts every table to a common notation (v2 appends the later studies) | the above | in memory |
| `construir_base_final.py` | Runs the four scripts above and writes the 45-sheet workbook | `metadatos_openalex.json` | `FCAW_BASE_FINAL.xlsx` |
| `wfs_origen_y_tecnica.py` | Flags whether each wire feed speed was measured or imputed, and the technique | `FCAW_MAESTRA.csv`, `MODELADO.csv` | same files, two new columns |
| `piso_error.py` | Error floor: spread between true replicates | `../FCAW_MAESTRA.csv` (one folder up) | printed summary |

`FCAW_MAESTRA.csv` and `MODELADO.csv` are distributed in `data/`; they are exports of the workbook
sheets, and that export step is not a separate script.

## 3_models — Bayesian hierarchical models (run from `data/`)

| Script | Model | Output in `data/` |
|---|---|---|
| `modelo_01_ancho.R` | Bead width, one-stage IPD model, leave-one-campaign-out | (`validacion_lolo_ancho_A.csv`) |
| `modelo_02_sensibilidad.R` | Width: sensitivity to imputed studies | `sensibilidad_ancho_bayes.csv` |
| `modelo_03_todas_respuestas.R` | Six responses (W, R, P, D, IC, W/P) | `malla_todas_respuestas_bayes.csv` |
| `modelo_03_todas_respuestas.py` | Classical counterpart; leave-one-campaign-out and predictor contrast | `validacion_lolo_ancho.csv`, `contraste_troncal_H044.csv` |
| `modelo_04_conjunto_WRP.R` | Joint model W + R + P | `modelo_conjunto_WRP.rds` |
| `modelo_05_gamma_sensibilidad.R` | Log-normal vs gamma with log link | `malla_gamma_vs_log.csv` |

```bash
cd data
Rscript ../code/3_models/modelo_03_todas_respuestas.R
```

## _working — internal tools (not needed to reproduce)

`anadir_hallazgos_*.py` (one-off notes added to the workbook), `hechos_canonicos.py` (internal summary
of figures for the thesis), `triaje_pdfs_detector.py` (needs the PDFs), `construir_excel.py` (earlier
workbook builder), `modelo_01_ancho.py` and `modelo_02_sensibilidad.py` (first classical versions;
their outputs are not in `data/`). Kept for transparency.
