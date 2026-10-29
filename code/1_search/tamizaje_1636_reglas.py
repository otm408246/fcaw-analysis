# -*- coding: utf-8 -*-
"""
PRE-TAMIZAJE POR REGLAS (etapa 1 de 2) sobre los 1 636 registros.

Solo decide lo INEQUIVOCO, con reglas conservadoras y documentadas:
  E5_FUERA_TEMA   no es soldadura por arco (metadato ruidoso)
  E1_NO_FCAW      hay resumen, no aparece ningun termino de alambre tubular y SI aparece
                  un proceso distinto con claridad
  E4_ADITIVA      fabricacion aditiva por arco (WAAM), aunque use alambre tubular
  E3_SIN_DATOS    el titulo es de revision/estado del arte y no hay senal de datos propios
Todo lo demas -> RESIDUO para tamizaje por agentes (etapa 2).
Regla de duda: ante cualquier ambiguedad, NO se excluye.
Escribe veredicto_reglas.csv y residuo_lote_1..K.csv. Se ejecuta desde dataset/.
"""
import re, pandas as pd, numpy as np
D = "_busqueda/TAMIZAJE_1636"
r = pd.read_csv(f"{D}/registros.csv"); r["resumen"] = r.resumen.fillna(""); r["titulo"] = r.titulo.fillna("")
txt = (r.titulo + " || " + r.resumen).str.lower()
tit = r.titulo.str.lower()

TUB   = r"flux[\s-]*cored|fcaw|fcw\b|tubular wire|arame tubular|alambre tubular|fil fourr|metal[\s-]*cored|cored wire|порошков|порошк|self[\s-]*shield|fca[\s-]*weld|fca[\s-]*process|rutile|basic wire|e71t|e70t|e81t|e91t|e110t|e316lt|e309lt|e308lt|e2209t|t-1\b|t-5\b|t-8\b|t-11\b"
OTRO  = r"submerged arc|\bsaw\b|shielded metal arc|\bsmaw\b|stick electrode|covered electrode|\bgtaw\b|\btig\b|tungsten inert|laser|plasma|friction stir|\bfsw\b|electroslag|electro-slag|electrogas|resistance spot|\bspot weld|ultrasonic weld|explos|diffusion bond|brazing|solder|strip cladd|strip surfac|electron beam|\bebw\b|cold metal transfer|\bcmt\b|solid wire|er70s|er308l|er316l|er2209"
SOLD  = r"weld|sold|surfac|cladd|overlay|hardfac|deposit|наплав|свар|arc\b|arco|bead|cord"
WAAM  = r"additive manufactur|\bwaam\b|wire arc additive|wire-arc additive|3d print|layer[\s-]*by[\s-]*layer|multi-layer deposition|thin[\s-]*wall.*(build|deposit)|manufatura aditiva|fabricaci[oó]n aditiva"
REV   = r"^(a |an |the )?(critical |systematic |comprehensive |brief |short |literature )?(review|survey|overview|state[\s-]*of[\s-]*the[\s-]*art|revis[aã]o|revisi[oó]n)\b|: a review|- a review|a review of|review of"
DATOS = r"experiment|specimen|trial|were welded|was welded|design of experiment|taguchi|response surface|orthogonal|anova|regression|measured|\bruns?\b|ensaio|experimento|probeta"

r["t_tub"]  = txt.str.contains(TUB,  regex=True)
r["t_otro"] = txt.str.contains(OTRO, regex=True)
r["t_sold"] = txt.str.contains(SOLD, regex=True)
r["t_waam"] = txt.str.contains(WAAM, regex=True)
r["t_rev"]  = tit.str.contains(REV,  regex=True)
r["t_dat"]  = txt.str.contains(DATOS,regex=True)
r["tiene_resumen"] = r.resumen.str.len() > 50

ver, cod, mot = [], [], []
for _, x in r.iterrows():
    if not x.t_sold and not x.t_tub:
        v, c, m = "EXCLUIR", "E5_FUERA_TEMA", "sin ningun termino de soldadura ni de alambre tubular en titulo/resumen"
    elif x.t_waam:
        v, c, m = "EXCLUIR", "E4_ADITIVA", "fabricacion aditiva por arco (WAAM) en titulo/resumen"
    elif x.t_rev and not x.t_dat:
        v, c, m = "EXCLUIR", "E3_SIN_DATOS", "titulo de revision/estado del arte sin senal de datos propios"
    elif x.tiene_resumen and not x.t_tub and x.t_otro:
        v, c, m = "EXCLUIR", "E1_NO_FCAW", "resumen sin termino de alambre tubular y con proceso distinto explicito"
    elif x.tiene_resumen and not x.t_tub:
        # regla E1b, justificada por la prueba de sensibilidad: los 24 estudios del corpus nombran el
        # proceso en titulo o resumen (24/24); un resumen que no lo nombra no es un estudio FCAW de geometria
        v, c, m = "EXCLUIR", "E1_NO_FCAW", "resumen presente que no nombra ningun proceso de alambre tubular (regla E1b; 24/24 del corpus si lo nombran)"
    else:
        v, c, m = "RESIDUO", "", ""
    ver.append(v); cod.append(c); mot.append(m)
r["veredicto_reglas"] = ver; r["codigo_reglas"] = cod; r["motivo_reglas"] = mot

print("PRE-TAMIZAJE POR REGLAS")
print(r.veredicto_reglas.value_counts().to_string()); print(r[r.veredicto_reglas=="EXCLUIR"].codigo_reglas.value_counts().to_string())
# prueba de sensibilidad: ninguno del corpus debe salir EXCLUIR
mal = r[(r.ya_en_corpus.fillna("") != "") & (r.veredicto_reglas == "EXCLUIR")]
print(f"\nPRUEBA DE SENSIBILIDAD: {len(mal)} del corpus excluidos por reglas (debe ser 0)")
if len(mal): print(mal[["ya_en_corpus","codigo_reglas","titulo"]].to_string())
r.to_csv(f"{D}/veredicto_reglas.csv", index=False)

res = r[r.veredicto_reglas == "RESIDUO"].copy()
cols = ["n","openalex_id","doi","anio","tipo","idioma","citas","revista","ejes","ya_en_corpus","en_317_agosto","titulo","resumen"]
K = max(1, -(-len(res) // 110))          # ~110 por lote
tam = -(-len(res) // K)
for j in range(K): res[cols].iloc[j*tam:(j+1)*tam].to_csv(f"{D}/residuo_lote_{j+1}.csv", index=False)
print(f"\nRESIDUO para agentes: {len(res)} registros en {K} lotes de ~{tam}")
print("  con resumen:", int(res.tiene_resumen.sum()), "· con termino tubular:", int(res.t_tub.sum()), "· del corpus:", int((res.ya_en_corpus.fillna('')!='').sum()))
