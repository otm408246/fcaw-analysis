# Corpus consolidado de parámetros de proceso y geometría del cordón en soldadura FCAW

**Versión 2.0 · 2026-10-17 · Osvaldo Torres Mejía** (Instituto Politécnico Nacional, UPIICSA, SEPI)
Licencia: CC BY 4.0 · ORCID: https://orcid.org/0009-0002-9784-4340

## Qué es

Meta-análisis de datos individuales (IPD) sobre geometría del cordón en soldadura por arco con
alambre tubular (FCAW): **477 corridas de 27 campañas experimentales publicadas, de 13 países**,
transcritas de su tabla original, estandarizadas a una notación común y auditadas. Cada registro
es trazable hasta el artículo, la tabla y la página de donde salió.

Es el conjunto de datos que sustenta las tablas y figuras del capítulo:

> Torres-Mejía, O., Aguilar-Fernández, M. y León-Romero, L. P. (2026). *Del conocimiento publicado
> al taller: diseño de un sistema de soporte a la decisión para fijar parámetros de soldadura FCAW
> en MiPyMES metalmecánicas.* ECORFAN.

## Archivos

### `tablas/`
| Archivo | Contenido |
|---|---|
| `FCAW_BASE_FINAL.xlsx` | El libro completo: 45 hojas. Metadatos, tabla maestra, diccionario, notaciones, auditoría de duplicaciones (`08_DUPLICACIONES`), piso de error (`11_PISO_ERROR`), procedencia de cada tabla (`12_PROCEDENCIA`) y las tablas originales por estudio |
| `FCAW_MAESTRA.csv` | Las 477 corridas, 49 columnas |
| `MODELADO.csv` | 300 corridas · 13 estudios. Filtrada: FCAW-G, Ø 1,2 mm, con WFS y velocidad de avance |
| `MODELADO_SENSIBILIDAD.csv` | 343 corridas · 16 estudios. Incluye las que solo reportan corriente |
| `malla_todas_respuestas_bayes.csv` | Resultado del modelo jerárquico bayesiano de las seis respuestas (Box 4 del capítulo) |
| `validacion_lolo_ancho.csv` | Validación dejando una campaña fuera, ancho (Figura 3) |
| `malla_gamma_vs_log.csv` | Sensibilidad: normal-logarítmico frente a gamma con enlace logarítmico |
| `sensibilidad_ancho_bayes.csv` | Sensibilidad del modelo del ancho a la inclusión de estudios imputados |
| `contraste_troncal_H044.csv` | Contraste del predictor troncal: WFS/TS frente a corriente |

Las cantidades del modelo se resumen con la **mediana posterior** y el intervalo de credibilidad
del 95 % (cuantiles 2,5 % y 97,5 %).

### `busqueda/`
| Archivo | Contenido |
|---|---|
| `BUSQUEDA_OpenAlex_2026-09-14.csv` | Los 1 636 registros únicos de la búsqueda (15 cadenas, 4 ejes) |
| `BUSQUEDA_OpenAlex_2026-09-14_resumen.md` | Las cadenas y sus conteos brutos |
| `TAMIZAJE_FINAL.csv` | El destino de cada uno de los 1 636 registros, con su motivo |
| `PROTOCOLO_TAMIZAJE.md` | Las reglas de exclusión de las dos etapas |
| `PRISMA_FLUJO.md` | El flujo PRISMA-IPD |

### `codigo/`
Los guiones que generan todo, de la búsqueda al modelo: consolidación (`construir_*.py`,
`datos_originales*.py`), tamizaje (`tamizaje_1636_*.py`), piso de error (`piso_error.py`) y
modelos (`modelo_01` a `modelo_05`, en R y Python; brms sobre Stan).

Los guiones que consultan OpenAlex leen la clave de la variable de entorno `OPENALEX_API_KEY`
y el correo de contacto de `CONTACT_EMAIL`. No traen credenciales escritas.

## Correcciones de esta versión (2.0) frente a la 1.2

1. **`TAMIZAJE_FINAL.csv`**: Sadek (2001) y Paiva (2010) estaban marcados como excluidos a texto
   completo, cuando los dos forman parte del corpus. Cada uno está indexado dos veces en OpenAlex;
   ahora el registro principal es `INCLUIDO` y su gemelo queda como `DUPLICADO_INDEXACION`, con el
   identificador del registro con el que coincide. Los destinos quedan: 1 348 excluidos en el
   tamizaje, 248 descartados por el autor, 12 excluidos a texto completo con motivo, 2 duplicados
   de indexación y **26 incluidos** (26 documentos de la búsqueda + 5 de otras fuentes = 31
   documentos → 27 campañas).
2. **Países**: 13, no 14. Los 14 contaban también estudios sin datos propios.
3. Se añaden las tablas de resultados del modelo bayesiano, que no estaban en la v1.2.

## Cómo usarlo

Para modelar, filtrar por `conjunto = principal`; los demás conjuntos (subacuático, pulsado,
autoprotegido, otro proceso) están separados a propósito. Revisar la columna `banderas` antes de
usar un registro. `A_dep` y `WFS_TS` son colineales mientras el diámetro sea constante: usar solo
una. `HI_J_mm` existe en el 12 % de los registros y no es un predictor viable.

## Límites declarados

- La unidad de análisis es la **campaña experimental**, no la publicación: nueve publicaciones
  republican datos de otras (hoja `08_DUPLICACIONES`).
- Las tablas se transcribieron a mano desde los PDF y se verificaron por comprobación aritmética
  interna (At = Ap + Ar, D = Ap/At, razones W/P y R/W, sumas de cuadrados contra el ANOVA
  publicado). El proceso detectó errores en 10 de los 31 artículos. Aun así, conviene contrastar
  contra la fuente primaria antes de usar un valor individual en un cálculo crítico.
- 8 de las 27 campañas no tienen país registrado, así que 13 es el número de países distintos
  entre las 19 restantes.
- Tres estudios traían una huella de imputación (correlación exacta de 1,000 entre corriente y
  velocidad de alimentación) y quedan fuera de la especificación preferida.
- **No se incluyen los PDF de los artículos originales**, por derechos de autor. Cada registro
  lleva el DOI o el identificador de su fuente.

## Cómo citar

> Torres-Mejía, O. (2026). *Corpus consolidado de parámetros de proceso y geometría del cordón en
> soldadura FCAW: base de datos, tabla maestra, tablas de modelado y código de consolidación y
> modelado* (versión 2.0) [Conjunto de datos y código]. Zenodo. https://doi.org/10.5281/zenodo.23441900
