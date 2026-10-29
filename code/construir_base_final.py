# -*- coding: utf-8 -*-
"""BASE DE DATOS FINAL FCAW - libro unico con todo:
   metadatos bibliograficos, tablas originales, tabla estandarizada,
   diccionario, notaciones, banderas, duplicaciones, hallazgos y procedencia."""
import json, csv, math
from collections import Counter, defaultdict
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

exec(open('datos_originales.py').read())
exec(open('datos_originales_v2.py').read())
ORIG.update(ORIG2)
exec(open('construir_maestra.py').read())
exec(open('construir_maestra_v2.py').read())
META = json.load(open('metadatos_openalex.json'))

VERSION = "1.1"; FECHA = "2026-08-20"
AR = lambda b=False,c='000000',s=10: Font(name='Arial',size=s,bold=b,color=c)
HD = PatternFill('solid',fgColor='1F4E79'); SUB=PatternFill('solid',fgColor='DDEBF7')
WARN=PatternFill('solid',fgColor='FCE4D6'); OKF=PatternFill('solid',fgColor='E2EFDA')
TH = Side(style='thin',color='B0B0B0'); BOX=Border(left=TH,right=TH,top=TH,bottom=TH)

def fmt(ws, hrow, widths, freeze=None, wrap_from=1):
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    for c in ws[hrow]:
        c.font=AR(True,'FFFFFF'); c.fill=HD; c.alignment=Alignment(wrap_text=True,vertical='center'); c.border=BOX
    for row in ws.iter_rows(min_row=hrow+1):
        for c in row:
            c.font=AR(); c.border=BOX
            c.alignment=Alignment(wrap_text=(c.column>=wrap_from),vertical='top')
    if freeze: ws.freeze_panes=freeze
    ws.auto_filter.ref=f"A{hrow}:{get_column_letter(ws.max_column)}{ws.max_row}"

wb=Workbook(); wb.remove(wb.active)

# ---------------------------------------------------------------- 00 LEEME
ws=wb.create_sheet("00_LEEME")
L=[["BASE DE DATOS CONSOLIDADA DE GEOMETRIA DE CORDON EN FCAW",""],
["Version",VERSION],["Fecha",FECHA],
["Autor","Osvaldo Torres M."],
["Licencia sugerida","CC BY 4.0 (atribucion)"],
["Como citar","Torres M., O. (2026). Base de datos consolidada de geometria de cordon en FCAW v1.0 [Data set]."],
["",""],
["QUE CONTIENE",""],
["Registros estandarizados",str(len(M))],
["Estudios con tabla original",str(len(ORIG))],
["Corridas del conjunto principal",str(sum(1 for r in M if r['conjunto']=='principal'))],
["Paises representados",", ".join(sorted({p for v in META.values() for p in (v.get('pais') or '').split(', ') if p}))],
["",""],
["ESTRUCTURA DEL LIBRO",""],
["01_ESTUDIOS","Metadatos bibliograficos completos: autores, anio, revista, DOI, institucion, pais"],
["02_MAESTRA","LA TABLA. Un renglon por corrida, notacion canonica, 47 columnas"],
["03_DICCIONARIO","Definicion, unidad, formula y cobertura de cada columna"],
["04_NOTACION","Equivalencia entre la notacion de cada paper y la canonica"],
["05_TRANSFORMACIONES","Reglas aplicadas para pasar del dato original al estandarizado"],
["06_ECUACIONES","Formulas de las variables derivadas, con su fuente normativa"],
["07_BANDERAS","Diccionario de banderas de calidad"],
["08_DUPLICACIONES","Las campanas publicadas mas de una vez, con su verificacion"],
["09_HALLAZGOS","Errores, contradicciones y hallazgos, con destino en la tesis"],
["10_COBERTURA","Cuantos datos hay por variable y por conjunto"],
["11_PISO_ERROR","Dispersion entre replicas verdaderas, por estudio y consolidada"],
["12_PROCEDENCIA","De que paper, que tabla y que pagina sale cada estudio"],
["Pxx_ / Nxx_","Una hoja por estudio con su TABLA ORIGINAL transcrita literal"],
["",""],
["REGLAS DE USO",""],
["1","La unidad de analisis es la CAMPANA EXPERIMENTAL, no el paper. Ver 08_DUPLICACIONES"],
["2","Filtrar por conjunto='principal' para modelar. Los demas conjuntos estan separados por una razon"],
["3","Revisar la columna banderas antes de usar un registro"],
["4","Los valores originales estan VERBATIM en las hojas por estudio, incluidas las erratas"],
["5","A_dep y WFS_TS son colineales (r=1.000) mientras el diametro sea constante: usar solo una"],
["6","HI solo esta disponible en el 12% de los registros: no es un predictor viable"],
]
for r in L: ws.append(r)
ws.column_dimensions['A'].width=34; ws.column_dimensions['B'].width=104
for i,r in enumerate(ws.iter_rows(min_row=1),1):
    r[0].font=AR(True); r[1].font=AR()
    r[0].alignment=Alignment(vertical='top'); r[1].alignment=Alignment(wrap_text=True,vertical='top')
ws['A1'].font=AR(True,'1F4E79',13)

# ---------------------------------------------------------------- 01 ESTUDIOS
ws=wb.create_sheet("01_ESTUDIOS")
ws.append(["id_estudio","autores","anio","titulo","revista","volumen","paginas","DOI","ISSN",
           "institucion","pais","tipo","citas","acceso_abierto","url_texto_completo",
           "n_corridas_base","conjunto_principal","diseno_experimental","proceso","aplicacion",
           "alambre","diam_mm","metal_base","gas","openalex_id","estado_metadatos"])
cnt=Counter(r['paper_id'] for r in M); cntp=Counter(r['paper_id'] for r in M if r['conjunto']=='principal')
def pid(k): return k
for k in sorted(ORIG):
    m=META.get(k,{}); p=pid(k)
    reg=[r for r in M if r['paper_id']==p]
    d=ORIG[k]
    niv=d.get('niveles','')
    dis=("CCD" if 'central composite' in niv.lower() or 'ccd' in niv.lower() else
         "Taguchi" if 'taguchi' in niv.lower() or 'l9' in niv.lower() or 'l25' in niv.lower() else
         "Factorial" if 'factorial' in niv.lower() else
         "Plackett-Burman" if 'plackett' in niv.lower() else "otro")
    r0=reg[0] if reg else {}
    ws.append([k, m.get('autores',''), m.get('anio',''), m.get('titulo',''), m.get('revista',''),
        m.get('volumen',''), m.get('paginas',''), m.get('doi',''), m.get('issn',''),
        m.get('instituciones',''), m.get('pais',''), m.get('tipo',''), m.get('citas',''),
        "SI" if m.get('acceso_abierto') else "no", m.get('url_oa',''),
        cnt.get(p,0), cntp.get(p,0), dis,
        r0.get('variante',''), r0.get('aplicacion',''), r0.get('alambre_clase',''),
        r0.get('alambre_diam_mm',''), r0.get('metal_base',''), r0.get('gas_tipo',''),
        m.get('openalex_id',''), m.get('estado','')])
fmt(ws,1,[26,42,7,52,26,9,11,26,12,34,8,12,7,9,30,9,10,16,10,12,22,8,20,14,14,10],"C2",2)

# ---------------------------------------------------------------- 02 MAESTRA
ws=wb.create_sheet("02_MAESTRA")
ws.append(COLS)
for r in M: ws.append([r.get(c) for c in COLS])
W=[22,22,10,8,12,13,10,12,12,14, 20,10,24,10,16,9,10,10, 8,10,9,10,11,10,10,11,9, 10,11,12, 11,11,10,
   9,9,9,9,10,10,9,9,8,9,9, 54,12,72]
fmt(ws,1,W,"C2",44)
CJ={'principal':'E2EFDA','excluido':'FCE4D6','pulsado':'FFF2CC','comparativo':'D9E1F2',
    'autoprotegido':'E4DFEC','solapado':'F2F2F2'}
ci=COLS.index('conjunto')+1
for row in ws.iter_rows(min_row=2,min_col=ci,max_col=ci):
    v=row[0].value
    if v in CJ: row[0].fill=PatternFill('solid',fgColor=CJ[v])

# ---------------------------------------------------------------- 03 DICCIONARIO
ws=wb.create_sheet("03_DICCIONARIO")
ws.append(["columna","tipo","unidad","definicion","formula_o_regla","n_con_dato","cobertura_%","uso_en_modelo"])
DIC={
"registro_id":("texto","—","Identificador unico de la corrida","paper + numero de corrida",""),
"paper_id":("texto","—","Llave que une con 01_ESTUDIOS y con la hoja de tabla original","",""),
"run_id_original":("texto","—","Numero de corrida tal como aparece en el paper","",""),
"replica":("texto","—","Etiqueta de replica cuando el estudio reporta repeticiones","a / b",""),
"tipo_registro":("texto","—","corrida | validacion | confirmacion","",""),
"conjunto":("texto","—","Particion de uso: principal va al modelo","",""),
"variante":("texto","—","FCAW-G (con gas) | FCAW-S (autoprotegido) | RMD","",""),
"aplicacion":("texto","—","cladding (recargue) | BOP (cordon sobre placa) | filete | tuberia_bisel","",""),
"posicion":("texto","—","Posicion de soldadura","",""),
"nivel_uso":("texto","—","Que tan completo esta el registro","",""),
"metal_base":("texto","—","Material de la placa","",""),
"espesor_mm":("num","mm","Espesor de la placa base","",""),
"alambre_clase":("texto","—","Clasificacion AWS o designacion del consumible","",""),
"alambre_diam_mm":("num","mm","Diametro del alambre tubular","",""),
"gas_tipo":("texto","—","Mezcla de proteccion","",""),
"pct_CO2":("num","%","Porcentaje de CO2 en la mezcla","",""),
"caudal_L_min":("num","L/min","Caudal de gas","",""),
"polaridad":("texto","—","DCEP / DCEN","",""),
"I_amp":("num","A","Corriente de soldadura","Ajustada salvo que I_medida='si'",""),
"I_medida":("texto","—","si | no | estimada. Distingue consigna de medicion","",""),
"V_arco":("num","V","Voltaje de arco. NO es el voltaje en vacio","",""),
"OCV_volt":("num","V","Voltaje en circuito abierto","",""),
"WFS_m_min":("num","m/min","Velocidad de alimentacion del alambre","",""),
"TS_mm_s":("num","mm/s","Velocidad de avance","Convertida desde cm/min o mm/min",""),
"CTWD_mm":("num","mm","Distancia punta de contacto a pieza","NO equivale a NPD",""),
"stickout_mm":("num","mm","Longitud libre de alambre","NO equivale a CTWD",""),
"NPD_mm":("num","mm","Distancia tobera a placa","NO equivale a CTWD",""),
"angulo_deg":("num","grados","Angulo de antorcha","Verificar convencion por estudio",""),
"f_pulso_Hz":("num","Hz","Frecuencia de pulsacion","",""),
"temp_precal_C":("num","degC","Temperatura de precalentamiento","",""),
"HI_J_mm":("num","J/mm","Aporte termico","k*V*I/TS con k=0.80 (ISO/TR 17671-1)",""),
"A_dep_mm2":("num","mm2","Area depositada teorica","phi*(pi/4)*d^2*(WFS/TS)",""),
"WFS_TS":("num","—","Razon alimentacion / avance","WFS/TS, ambas en mm/min",""),
"W_mm":("num","mm","Ancho del cordon","",""),
"R_mm":("num","mm","Altura de refuerzo","",""),
"P_mm":("num","mm","Profundidad de penetracion","",""),
"D_pct":("num","%","Dilucion","AP/(AP+AR)*100",""),
"AP_mm2":("num","mm2","Area de penetracion","",""),
"AR_mm2":("num","mm2","Area de refuerzo","",""),
"ZAT_mm":("num","mm","Zona afectada por el calor","",""),
"IC_pct":("num","%","Indice de convexidad","R/W*100",""),
"W_P":("num","—","Razon ancho / penetracion","W/P",""),
"TD_kg_h":("num","kg/h","Tasa de deposito","",""),
"rend_pct":("num","%","Rendimiento de deposito","",""),
"banderas":("texto","—","Marcas de calidad separadas por ';'. Ver 07_BANDERAS","",""),
"confiabilidad":("texto","—","alta | media | baja","",""),
"observaciones":("texto","—","Notas de la corrida o del estudio","",""),
}
P12=[r for r in M if r['conjunto']=='principal' and r['alambre_diam_mm']==1.2]
for c in COLS:
    t,u,de,fo,_=DIC.get(c,("texto","—","","",""))
    n=sum(1 for r in M if r.get(c) not in (None,'',' '))
    pct=100*n/len(M)
    n12=sum(1 for r in P12 if r.get(c) not in (None,'',' '))
    p12=100*n12/len(P12) if P12 else 0
    uso=("PREDICTOR" if c in ('WFS_TS','TS_mm_s','NPD_mm') else
         "RESPUESTA" if c in ('W_mm','R_mm','P_mm','D_pct','IC_pct','W_P') else
         "AGRUPACION" if c in ('paper_id','aplicacion','alambre_clase') else
         "descartado (<40%)" if p12<40 else "contexto")
    ws.append([c,t,u,de,fo,n,round(pct,1),uso])
fmt(ws,1,[16,7,9,50,44,10,11,20],"A2",4)

# ---------------------------------------------------------------- 04 NOTACION
ws=wb.create_sheet("04_NOTACION")
ws.append(["notacion_en_el_paper","significado","columna_canonica","estudios_que_la_usan","observacion"])
NOT=[
["I, CM, AC, Im, In","Corriente de soldadura","I_amp","Palani, Kumar, Kannan, Moreno, Solovyov","Casi siempre es CONSIGNA, no medicion"],
["Irms, I medida","Corriente eficaz medida","I_medida='si'","Moreno-MAT, CA6M2018, Odhiambo","Difiere de la consigna hasta 15%"],
["V, U, Un, Uset, T","Voltaje de arco","V_arco","Gomes, Senthilkumar, Singh, Yadav, Solovyov","Uset es CONSIGNA; Un es MEDIDO"],
["S, WS, VS, TS, v","Velocidad de avance","TS_mm_s","todos","Unidades: cm/min, mm/min, m/h, mm/s"],
["F, Wf, WFR, WFS, Va, X2","Velocidad de alimentacion","WFS_m_min","Gomes, Balan, Singh, Senthilkumar","Unidades: m/min, mm/min, inch/min"],
["N, NPD, NTD","Distancia tobera-placa","NPD_mm","Palani, Kumar, Kannan, Singh","NO es CTWD"],
["CTWD, DBCP","Distancia punta de contacto-pieza","CTWD_mm","Moreno, Guimaraes, Odhiambo","NO es NPD"],
["stick-out, viliot, vuelo","Longitud libre de alambre","stickout_mm","Sreeraj, Katherasan, Solovyov","La menor de las tres distancias"],
["T, A, ang, phi","Angulo de antorcha","angulo_deg","Kannan, Balan, Katherasan, Odhiambo","OJO: Kannan invierte el orden de niveles"],
["W, B, BW, L, b","Ancho del cordon","W_mm","todos","En recargue oscilado llega a 40 mm"],
["R, H, r","Altura de refuerzo","R_mm","todos",""],
["P, DoP, p","Penetracion","P_mm","todos","Odhiambo mide en junta biselada: NO comparable"],
["D, %D, PD, CHOM, dilution","Dilucion","D_pct","Palani, Gomes, Kannan, Solovyov","CHOM = fraccion de metal base (ucraniano)"],
["WPSF","Weld penetration shape factor = W/P","W_P","Palani, Gomes, Singh","Razon, no dimension"],
["WRFF","Weld reinforcement form factor = W/R","IC_pct = 100/WRFF","Palani, Gomes, Singh","Se invierte para llevarlo a IC"],
["RFF","Reinforcement form factor = R/W","IC_pct = RFF*100","Senthilkumar2014","Definicion INVERSA a WRFF"],
["PFF","Penetration form factor = P/W","W_P = 1/PFF","Senthilkumar2014",""],
["IC","Indice de convexidad = R/W*100","IC_pct","Guimaraes","Nombre en portugues"],
["Ap, AP, PA","Area de penetracion","AP_mm2","Palani, Moreno, Guimaraes",""],
["Ar, AR, RA, Af","Area de refuerzo","AR_mm2","Palani, Moreno, Cavalcante",""],
["At","Area total","AP+AR","Palani","Verificado: At = Ap + Ar"],
["Q, HI, heat input","Aporte termico","HI_J_mm","Moreno-MAT, Odhiambo, Aloraier, Zhang","k=0.80 verificado en 2 laboratorios"],
["FN","Numero de ferrita","(no canonica)","Balan, Senthilkumar2015, Nunes","Respuesta metalurgica, no geometrica"],
["CA","Angulo de contacto","(no canonica)","Senthilkumar2014","Angulo de mojado del cordon"],
["DOS, Epit","Sensibilizacion y potencial de picado","(no canonica)","Nunes2020","Respuestas de corrosion"],
["ChOM, VRM","Fraccion de metal base / tasa","D_pct","Solovyov","Cirilico: ЧОМ"],
]
for r in NOT: ws.append(r)
fmt(ws,1,[30,40,26,42,52],"A2",1)

# ---------------------------------------------------------------- 05..12 y hojas por estudio
def hoja_lista(nombre,cabecera,filas,widths):
    w=wb.create_sheet(nombre); w.append(cabecera)
    for r in filas: w.append(r)
    fmt(w,1,widths,"A2",1); return w

# 08 DUPLICACIONES
DUP=[
["D-1","PALANI2007-RSM","KANNAN2006 'Development of mathematical models' (117 citas)","identica","20/20 filas identicas en P,R,W,%D, incluida la misma errata en las corridas 9-10","Se conserva PALANI2007 (mas columnas: AP, WPSF, WRFF). KANNAN2006 queda como cita alterna"],
["D-2","KANNAN2006-DUPLEX","'Sensitivity Analysis of FCA Cladding Parameters Using RSM'","identica","68% de solape de n-gramas numericos; mismas 31 corridas, mismos 4 factores","Se cuenta una vez. Cita alterna registrada"],
["D-3","GOMES2012","NUNES2020 (Materials Research)","identica","Matriz codificada 31/31 identica; dilucion coincide en las 2 probetas que ambos reportan (18.58/18.6 y 41.08/41.1)","0 corridas nuevas. Se ANEXAN 2 respuestas: DOS y Epit"],
["D-4","KATHERASAN2012","'Modeling and optimization by genetic algorithm and simulated annealing'","identica","22/22 filas legibles identicas en W,R,P. Mismo L25, mismos autores y equipo","Se cuenta una vez. Cambia solo el optimizador (ANN+PSO vs GA+SA)"],
["D-5","MORENO2022-MAT","CA6M2018 (IJAERS, publicacion mas TEMPRANA)","identica","9/9 valores de Irms y Urms identicos","0 corridas nuevas. Se ANEXA aceleracion RMS. RESUELVE la contradiccion de CTWD a favor de 30/33/36"],
["D-6","SREERAJ2014-HYB","SREERAJ2014-UTIL","identica","16 corridas compartidas entre dos publicaciones del mismo autor","Se cuenta una vez"],
["D-7","GUIMARAES2020","MORENO2022-PULS y MORENO2022-MAT","identica","Misma campana 410NiMo, 18 corridas con replica","Se conserva la union de variables"],
["D-8","RODRIGUES2009","PAIVA2010","identica","20 corridas compartidas","Se conserva la union"],
["D-9","PALANI2006-TAGUCHI","PALANI2007-RSM","parcial","3 condiciones compartidas de 9","Marcadas como conjunto='solapado'"],
]
hoja_lista("08_DUPLICACIONES",
 ["id","registro_conservado","publicacion_duplicada","tipo","evidencia_de_la_verificacion","resolucion_aplicada"],
 DUP,[7,26,52,11,64,58])

# 11 PISO DE ERROR
PE=[["refuerzo (R)",7,1.87,2.87,10.26,"PRECISA","Dave, Gomes, Kannan, Kumar, Palani, Singh, Yadav"],
["ancho (W)",7,1.26,3.84,8.13,"PRECISA","Dave, Gomes, Kannan, Kumar, Palani, Singh, Yadav"],
["indice de convexidad (IC)",8,1.91,6.09,15.47,"MEDIA","+ Senthilkumar2014"],
["penetracion (P)",7,2.77,7.92,13.16,"MEDIA","Dave, Gomes, Kannan, Kumar, Palani, Singh, Yadav"],
["W/P",8,6.50,8.96,16.66,"MEDIA","+ Senthilkumar2014"],
["dilucion (D)",6,2.78,10.20,17.29,"RUIDOSA","Balasubramanian, Gomes, Kannan, Kumar, Palani, Yadav"],
["ZAT",1,15.55,15.55,15.55,"RUIDOSA","solo Dave2025"]]
w=hoja_lista("11_PISO_ERROR",
 ["respuesta","n_grupos_de_replicas","CV_min_%","CV_mediana_%","CV_max_%","categoria","estudios_incluidos"],
 PE,[26,20,11,15,11,12,54])
w.append([])
w.append(["NOTA 1: se excluyo 19_Balan2018 porque sus 7 'puntos centrales' repiten valores identicos (R=3.87 cinco veces, P=0.71 seis veces): no son replicas independientes."])
w.append(["NOTA 2: se excluyo 20_Beczkowski2018 del agrupamiento: sus 9 condiciones carecen de predictores publicados y NO son replicas entre si (su dispersion intra-cordon alimenta H-012, no el piso)."])
w.append(["CRITERIO: un modelo cuyo error sea menor que estos valores no esta capturando senal, esta memorizando ruido."])
for r in w.iter_rows(min_row=w.max_row-1):
    for c in r: c.font=AR(True); c.alignment=Alignment(wrap_text=True)

# 12 PROCEDENCIA
PR=[]
for k in sorted(ORIG):
    d=ORIG[k]
    PR.append([k, d.get('tabla',''), d.get('cita','')[:200], "; ".join(map(str,d.get('cols',[])))[:180], len(d.get('rows',[]))])
hoja_lista("12_PROCEDENCIA",
 ["id_estudio","tabla_de_origen_y_pagina","cita_tal_como_se_transcribio","columnas_de_la_tabla_original","n_filas_transcritas"],
 PR,[26,44,72,72,14])

print("hojas base OK")

# ------------------- hojas por estudio: TABLA ORIGINAL -------------------
for k in sorted(ORIG):
    d=ORIG[k]; m=META.get(k,{})
    w=wb.create_sheet(k[:31])
    w.append(["CITA", d.get('cita','')])
    w.append(["DOI", m.get('doi','') or "(sin DOI)"])
    w.append(["REVISTA", f"{m.get('revista','')} {m.get('volumen','')} {m.get('paginas','')}".strip()])
    w.append(["INSTITUCION", m.get('instituciones','') or "(no recuperada)"])
    w.append(["TABLA DE ORIGEN", d.get('tabla','')])
    w.append(["NIVELES / CONSTANTES", d.get('niveles','')])
    w.append(["FIDELIDAD","Valores VERBATIM del paper. Se conservan erratas, comas decimales y celdas vacias."])
    w.append([])
    w.append(list(map(str,d.get('cols',[]))))
    for r in d.get('rows',[]): w.append(list(r))
    hr=9
    for i,ww in enumerate([16]+[13]*(len(d.get('cols',[]))-1 or 1),1):
        w.column_dimensions[get_column_letter(i)].width=ww
    w.column_dimensions['B'].width=112
    for rr in w.iter_rows(min_row=1,max_row=7):
        rr[0].font=AR(True,'1F4E79'); rr[0].alignment=Alignment(vertical='top')
        if len(rr)>1: rr[1].font=AR(); rr[1].alignment=Alignment(wrap_text=True,vertical='top')
    for c in w[hr]:
        c.font=AR(True,'FFFFFF'); c.fill=HD; c.border=BOX; c.alignment=Alignment(wrap_text=True,horizontal='center')
    for row in w.iter_rows(min_row=hr+1):
        for c in row: c.font=AR(); c.border=BOX; c.alignment=Alignment(horizontal='center')
    w.freeze_panes=f"A{hr+1}"

wb.save("../FCAW_BASE_FINAL.xlsx")
print(f"FCAW_BASE_FINAL.xlsx  ->  {len(wb.sheetnames)} hojas")
