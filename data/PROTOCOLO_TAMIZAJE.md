# PROTOCOLO DE TAMIZAJE POR TÍTULO Y RESUMEN — 1 636 registros

**Propósito:** reconstruir el paso de tamizaje del flujo PRISMA-IPD sobre la búsqueda documentada
del 2026-09-14, con criterios explícitos y un veredicto por registro. Cada agente tamiza **un lote del residuo**
(`residuo_lote_N.csv`, ~93 registros) y escribe `veredicto_residuo_N.csv`.

## Diseño en dos etapas (añadido 2026-09-15)

**Etapa 1 — reglas documentadas** (`_scripts/tamizaje_1636_reglas.py`, salida `veredicto_reglas.csv`):
decide solo lo inequívoco. 1 081 de 1 636 excluidos: E1_NO_FCAW 871 (sin término de alambre tubular en
título ni resumen; regla justificada porque los 24 estudios del corpus sí lo nombran, 24/24), E5 114,
E4_ADITIVA 61, E3 35. **Prueba de sensibilidad: 0 registros del corpus excluidos.**

**Etapa 2 — juicio por agentes** sobre el **residuo de 555** (`residuo_lote_1..6.csv`): los que nombran
alambre tubular (473) y los que no tienen resumen (82). Aquí aplican los criterios de abajo.

## Criterios de inclusión — los CUATRO deben cumplirse

| | Criterio | Sí | No |
|---|---|---|---|
| **C1** | **Proceso:** soldadura por arco con **alambre tubular** (flux-cored, FCAW-G o FCAW-S; también metal-cored si se declara tubular) | FCAW, "flux cored", "flux-cored", "tubular wire", "arame tubular", "порошков", FCAW-S, metal-cored | GMAW/MIG/MAG con alambre **sólido**, SAW, SMAW, GTAW/TIG, láser, plasma, fleje/strip, electroescoria |
| **C2** | **Respuesta:** reporta al menos una **dimensión medida del cordón**: ancho, refuerzo/altura, penetración, dilución, área, ángulo de mojado, relación W/P | cualquiera de esas, aunque sea una sola | solo propiedades mecánicas, microestructura, dureza, corrosión, humos, fatiga, tensiones residuales, composición química |
| **C3** | **Datos:** estudio **experimental con corridas propias** | diseño de experimentos, ensayos, mediciones | revisión, estado del arte, estudio teórico, simulación/FEM sin experimento propio, patente, editorial, capítulo de libro sin datos |
| **C4** | **Aplicación:** recargue, cordón sobre placa, unión, subacuática, tubería | todo eso entra al **corpus** (el modelo filtra después) | **fabricación aditiva por arco (WAAM)** capa sobre capa: se excluye con su propio código |

## Veredictos

```
INCLUIR            cumple C1–C4 (o es muy probable): pasa a texto completo
EXCLUIR  E1_NO_FCAW         falla C1
         E2_SIN_GEOMETRIA   cumple C1, falla C2
         E3_SIN_DATOS       falla C3
         E4_ADITIVA         falla C4 por WAAM
         E5_FUERA_TEMA      no es soldadura por arco; metadato ruidoso de la búsqueda
DUDOSO             la información no alcanza para decidir (típicamente sin resumen, o resumen ambiguo)
                   → pasa a texto completo. Anota qué falta.
```

**Regla de duda:** ante duda real, **INCLUIR o DUDOSO, nunca EXCLUIR.** El costo de un falso negativo
(perder un estudio útil) es mayor que el de un falso positivo (leer un texto completo de más).

**Registros sin resumen (`resumen` vacío):** decide solo por título. Si el título es claro (p. ej.
"bead geometry FCAW"), INCLUIR; si es ambiguo, DUDOSO. No EXCLUIR por falta de resumen salvo E1/E5
evidentes en el título.

**Idioma:** los resúmenes en portugués, español, turco, ucraniano, indonesio, chino se evalúan igual.
No excluyas por idioma.

**Columnas `ya_en_corpus` y `en_317_agosto`:** son información, **no un veredicto**. Evalúa el
registro con los criterios como si no supieras nada. Si un registro `ya_en_corpus` te sale EXCLUIR,
escríbelo igual: esa discrepancia es exactamente lo que queremos medir.

## Formato de salida — `veredicto_residuo_N.csv`

Una fila por registro, mismas `n` y `openalex_id` del lote, en el mismo orden:

```
n,openalex_id,C1,C2,C3,C4,veredicto,codigo,motivo
12,https://openalex.org/W1234,S,S,S,S,INCLUIR,,FCAW cladding con ancho penetracion y dilucion
13,https://openalex.org/W5678,N,?,?,?,EXCLUIR,E1_NO_FCAW,GMAW con alambre solido ER70S-6
14,https://openalex.org/W9012,S,?,S,S,DUDOSO,,sin resumen; titulo menciona FCAW y parametros pero no respuesta
```

- `C1..C4`: `S` sí, `N` no, `?` no determinable con la información disponible
- `codigo`: vacío salvo en EXCLUIR
- `motivo`: **≤ 15 palabras**, en español, con la evidencia concreta (proceso, respuesta, tipo de estudio)

## Cómo trabajar

1. Lee `residuo_lote_N.csv` con pandas. Recorre las filas en orden.
2. Para cada una, lee `titulo` y `resumen`, aplica C1→C4 en ese orden, escribe la fila.
3. No consultes internet ni abras PDF: **solo título y resumen.** Eso es lo que PRISMA llama tamizaje.
4. Escribe el CSV completo al final. Verifica que tenga exactamente las mismas filas que el lote.
5. Responde en 3 líneas: cuántos INCLUIR / EXCLUIR (por código) / DUDOSO, y cuántos `ya_en_corpus`
   te salieron distintos de INCLUIR (esa cifra es la prueba de sensibilidad).
