# FCAW individual participant data meta-analysis

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23441899.svg)](https://doi.org/10.5281/zenodo.23441899)

Data and code behind the master's thesis *Design of a technological decision support system for
parametric standardization in FCAW welding: data modeling and calibration with qualification test
coupons* (Instituto Politécnico Nacional, UPIICSA, SEPI).

**What it is.** An individual-level database of flux-cored arc welding (FCAW) process parameters and
weld bead geometry: **477 runs from 27 published experimental campaigns in 13 countries**, each
traceable to its source article, table and page; plus the code that searched the literature,
consolidated and audited the tables, and fitted Bayesian hierarchical models that separate the
effect of the process parameters from the deviation of each campaign.

The archived, citable version is on Zenodo: https://doi.org/10.5281/zenodo.23441899.
A Spanish description of every file is in [`LEEME.md`](LEEME.md).

## Contents

| Folder | Content |
|---|---|
| `data/` | Master table (`FCAW_MAESTRA.csv`), modeling tables, full workbook (`FCAW_BASE_FINAL.xlsx`), OpenAlex search and screening records, model outputs |
| `code/` | Python and R scripts: literature search, screening, consolidation, error floor, models `modelo_01`–`modelo_05` |

The source PDFs are **not** included (copyright). Scripts that rebuild the database from the
transcribed tables or query OpenAlex document the process; the models run from `data/` alone.

## Reproduce the models

Requirements: R ≥ 4.5 with `brms`, `cmdstanr` (CmdStan 2.39), `tidyverse`; Python ≥ 3.13 with
`pandas`, `numpy`, `statsmodels`, `scipy`.

```bash
cd data
Rscript ../code/modelo_01_ancho.R              # bead width, hierarchical model
Rscript ../code/modelo_03_todas_respuestas.R   # six responses
Rscript ../code/modelo_05_gamma_sensibilidad.R # log-normal vs gamma sensitivity
```

Scripts that query OpenAlex read the key from `OPENALEX_API_KEY` and the contact e-mail from
`CONTACT_EMAIL`; no credentials are stored in the repository.

## How to cite

Torres-Mejía, O. (2026). *Corpus consolidado de parámetros de proceso y geometría del cordón en
soldadura FCAW* [Data set and code]. Zenodo. https://doi.org/10.5281/zenodo.23441899

## License

Code: MIT. Data: CC BY 4.0 (as published on Zenodo).
