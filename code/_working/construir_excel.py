# -*- coding: utf-8 -*-
import math
from collections import Counter
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
exec(open('datos_originales.py').read())
exec(open('datos_originales_v2.py').read())
ORIG.update(ORIG2)
exec(open('construir_maestra.py').read())
exec(open('construir_maestra_v2.py').read())

AR=lambda b=False,c='000000',s=10: Font(name='Arial',size=s,bold=b,color=c)
HD=PatternFill('solid',fgColor='1F4E79'); SUB=PatternFill('solid',fgColor='DDEBF7')
TH=Side(style='thin',color='D0D0D0'); BD=Border(left=TH,right=TH,top=TH,bottom=TH)

def fmt(ws,hdr_row=1,widths=None,freeze=None,wrap_from=None):
    for c in ws[hdr_row]:
        if c.value is not None:
            c.font=AR(True,'FFFFFF'); c.fill=HD
            c.alignment=Alignment(horizontal='center',vertical='center',wrap_text=True)
    for row in ws.iter_rows(min_row=hdr_row+1):
        for c in row:
            c.font=AR(); c.border=BD
            c.alignment=Alignment(vertical='top',wrap_text=(wrap_from is not None and c.column>=wrap_from))
    if widths:
        for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    ws.row_dimensions[hdr_row].height=32
    if freeze: ws.freeze_panes=freeze
    if ws.max_row>hdr_row: ws.auto_filter.ref=f"A{hdr_row}:{get_column_letter(ws.max_column)}{ws.max_row}"

# ============ LIBRO 1: TABLAS ORIGINALES ============
wb1=Workbook(); wb1.remove(wb1.active)
idx=wb1.create_sheet("00_INDICE")
idx.append(["Hoja","Paper","Tabla de origen","Filas"])
for k,v in ORIG.items():
    ws=wb1.create_sheet(k[:31])
    ws.append(["CITA:",v["cita"]]); ws.append(["TABLA:",v["tabla"]]); ws.append(["NIVELES/CONSTANTES:",v["niveles"]])
    ws.append(["FIDELIDAD:","Transcripcion literal del paper. NO se corrige ningun valor. Correcciones documentadas en 07_TRANSFORMACIONES del libro maestro."])
    ws.append([])
    ws.append(v["cols"])
    for r in v["rows"]: ws.append(r)
    for i in range(1,5):
        ws.cell(i,1).font=AR(True); ws.cell(i,2).alignment=Alignment(wrap_text=True,vertical='top')
    ws.column_dimensions['A'].width=22
    for j in range(2,len(v["cols"])+2): ws.column_dimensions[get_column_letter(j)].width=13
    ws.column_dimensions['B'].width=60
    for c in ws[6]:
        if c.value is not None: c.font=AR(True,'FFFFFF'); c.fill=HD; c.alignment=Alignment(horizontal='center',wrap_text=True)
    for row in ws.iter_rows(min_row=7):
        for c in row: c.font=AR(); c.border=BD
    ws.freeze_panes="A7"
    idx.append([k,v["cita"][:90],v["tabla"][:70],len(v["rows"])])
fmt(idx,1,[30,90,70,8],"A2",2)
wb1.save("FCAW_tablas_originales.xlsx")
print("Libro 1 OK:",len(ORIG),"hojas")

# ============ LIBRO 2: DATASET MAESTRO ============
wb=Workbook(); wb.remove(wb.active)

# 00 LEEME
ws=wb.create_sheet("00_LEEME")
for r in [["FCAW — DATASET CONSOLIDADO",""],["Version","1.0"],["Fecha","2026-08-09"],
["Alcance","22 papers de FCAW revisados; 268 registros transcritos y estandarizados"],["",""],
["ARQUITECTURA DE TRES CAPAS",""],
["Capa 0 — Original","Archivo FCAW_tablas_originales.xlsx. Transcripcion literal, sin correcciones. Es el testigo."],
["Capa 1 — Reglas","Hoja 07_TRANSFORMACIONES. Documenta como se pasa de la capa 0 a la capa 2."],
["Capa 2 — Maestra","Hoja 05_MAESTRA. Tabla plana lista para modelar. Se genera, no se edita a mano."],["",""],
["REGLAS INNEGOCIABLES",""],
["1","Vacio no es cero. Si el paper no reporta el dato, la celda queda en blanco. Nunca se rellena."],
["2","CTWD, stickout y NPD son columnas distintas. Miden cosas fisicamente diferentes."],
["3","OCV_volt esta separado de V_arco. Usar OCV como voltaje de arco falsea el aporte termico."],
["4","La columna 'conjunto' define que filas entran a cada modelo. Filtrar siempre por ella."],["",""],
["COMO FILTRAR PARA MODELAR",""],
["Modelo principal","conjunto = 'principal' (209 registros)"],
["Excluir siempre","conjunto in ('solapado','comparativo')"],
["Subgrupos aparte","'pulsado' (corriente pulsada) y 'excluido' (autoprotegido, subacuatico, otras posiciones)"],["",""],
["HOJAS DE ESTE LIBRO",""],
["01_ESTUDIOS","Un renglon por paper: metadatos, diseno, N corridas, nivel de uso"],
["02_DICCIONARIO","Definicion y unidad de cada columna canonica"],
["03_BANDERAS","Taxonomia de banderas de calidad"],
["04_CONSTANTES","Constantes recuperadas del corpus con su fuente"],
["05_MAESTRA","LA TABLA. 268 registros"],
["06_HALLAZGOS","Registro de errores, contradicciones y hallazgos, con destino en la tesis"],
["07_TRANSFORMACIONES","Reglas de decodificacion y correcciones por paper"],
["08_ECUACIONES","Modelos publicados por los papers"],
["09_COBERTURA","Conteo de datos disponibles por variable"]]:
    ws.append(r)
ws.column_dimensions['A'].width=26; ws.column_dimensions['B'].width=105
for row in ws.iter_rows():
    for c in row: c.font=AR(); c.alignment=Alignment(wrap_text=True,vertical='top')
ws['A1'].font=AR(True,s=14)
for i in (6,11,16,21):
    ws.cell(i,1).font=AR(True); ws.cell(i,1).fill=SUB

# 01 ESTUDIOS
ws=wb.create_sheet("01_ESTUDIOS")
ws.append(["paper_id","autores_ano","proceso","metal_base","alambre","diam_mm","gas","diseno","n_corridas","conjunto","nivel_uso","respuestas","estado","cita_corta"])
EST=[
["SREERAJ2014-HYB","Sreeraj et al. 2014","FCAW-G BOP","IS 2062 6mm","E71T-1C",1.2,"CO2 (inferido)","Taguchi L16",16,"principal","parcial","W,R,P,D","PRIMARIO (fusiona SREERAJ2014-UTIL)","World J. Eng. 11(6):575-588"],
["SREERAJ2014-UTIL","Sreeraj et al. 2014","FCAW-G BOP","IS 2062 6mm","E71T-1C",1.2,"CO2 (inferido)","Taguchi L16",16,"—","—","P,D","DUPLICADO de SREERAJ2014-HYB","J. Eng. Technol. Res. 6(6):94-106"],
["GUIMARAES2020","Guimaraes 2020","FCAW pulsado cladding","SAE 1020 12.7mm","EC410NiMo",1.2,"Ar+2%O2","Taguchi L9 x2 rep",18,"pulsado","completo","W,R,P,IC,AP,AR,D","PRIMARIO (fusiona MORENO x2)","Dissertacao UTFPR"],
["MORENO2022-PULS","Moreno et al. 2022","FCAW pulsado cladding","SAE 1020","EC410NiMo",1.2,"Ar+2%O2","Taguchi L9 x2 rep",18,"—","—","W,R,P,AP,AR,D","DUPLICADO de GUIMARAES2020","J. Mater. Sci. Technol. Res. 9:11-23"],
["MORENO2022-MAT","Moreno et al. 2022","FCAW pulsado cladding","AISI 1020 12.7mm","EC410NiMo",1.2,"Ar+2%O2","Taguchi L9 x2 rep",18,"—","—","W,R,P,CI + Irms,Urms,Q","DUPLICADO. APORTA voltaje y corriente eficaz","Materials 15:2715"],
["KURTULMUS2015","Kurtulmus et al. 2015","FCAW-G BOP","SAE 1015 10mm","E71T-5",1.2,"CO2 12 L/min","OFAT 3 ensayos",3,"principal","completo","W,R,P,D,AP,AR,angulo","PRIMARIO","IJRET 4(9):23-28"],
["SADEK2001","Sadek et al. 2001","FCAW-G BOP","C-Mn 12mm","E71T-5",1.2,"Ar puro / CO2","Grupos A,B,C",9,"principal","parcial","W,R,P,ZAT","PRIMARIO. PDF escaneado","Trans. JWRI 30(2):45-52"],
["KUMAR2011","Vasantha Kumar & Murugan 2011","FCAW-G cladding","IS 2062 20mm","317L",1.2,"n/d","CCD 5f x5n",32,"principal","parcial","W,R,P,D","PRIMARIO","J. Miner. Mater. Charact. Eng. 10(9):827-842"],
["ZHANG2016","Zhang et al. 2016","FCAW-S subacuatico","Q235 8mm","rutilico",1.6,"ninguno","Pareado aire/agua",4,"excluido","subgrupo","W,R,P","PRIMARIO. Autoprotegido","J. Mater. Process. Technol. 238:373-382"],
["BECZKOWSKI2018","Beczkowski 2018","FCAW-S recargue","bimetal","alto Cr",2.8,"ninguno","Plackett-Burman",0,"—","sin_datos","Hn,Hw (135 mediciones)","SIN MATRIZ DE DISENO","Arch. Metall. Mater. 63(2):681-687"],
["GOMES2012","Gomes et al. 2012","FCAW-G cladding","AISI 1020","E316LT1",1.2,"n/d","CCD 4f x5n",31,"principal","completo","W,R,P,D,DR,Y,SF,SA","PRIMARIO","J. Mater. Eng. Perform. 21(9):1862-1872"],
["DAVE2025-FCAW","Dave et al. 2025","FCAW-G BOP 1G","316LN 8mm","E316LT1-4",1.2,"80Ar-20CO2","Box-Behnken",15,"principal","parcial","W,R,P,ZAT","PRIMARIO","Discov. Appl. Sci. 7:12"],
["DAVE2025-RMD","Dave et al. 2025","RMD BOP 1G","316LN 8mm","ER316L solido",1.2,"98Ar-2O2","Box-Behnken",15,"comparativo","referencia","W,R,P,ZAT","PROCESO DISTINTO","Discov. Appl. Sci. 7:12"],
["BALASUB2025","Balasubramanian et al. 2025","FCAW-G cladding","IS 2062 20mm","AISI 316L",1.2,"n/d","CCD 5f x5n",32,"principal","solo_dilucion","D","PRIMARIO","Int. J. Interact. Des. Manuf. 19:55-65"],
["PAIVA2010-EQMM","Paiva et al. 2010","FCAW-G BOP","ABNT 1045 9mm","E71T-1",1.2,"CO2 15 L/min","CCD rotable 3f",20,"principal","completo","P,IC,TD,Y,D","PRIMARIO (fusiona RODRIGUES2009)","Soldag. Insp. 15(1):31-40"],
["RODRIGUES2009","Rodrigues et al. 2009","FCAW-G BOP","ABNT 1045 9mm","E71T-1",1.2,"CO2 15 L/min","CCD rotable 3f",20,"—","—","P,IC","DUPLICADO de PAIVA2010","Welding International 23(4):261-269"],
["PALANI2007-RSM","Palani & Murugan 2007","FCAW-G cladding","IS 2062 20mm","317L",1.2,"95Ar-5CO2 16 L/min","CCD rotable 3f",20,"principal","parcial","W,R,P,D,AP,phi_a,phi_e","PRIMARIO","J. Mater. Process. Technol. 190:291-299"],
["PALANI2006-TAGUCHI","Palani et al. 2006","FCAW-G cladding","IS 2062 20mm","317L",1.2,"95Ar-5CO2 16 L/min","Taguchi L9 x2 rep",9,"principal (6 netas)","parcial","W,R,P,D","PRIMARIO. 3 condiciones solapan con PALANI2007","Mater. Sci. Technol. 22(10):1193-1200"],
["CAVALCANTE2020","Cavalcante et al. 2020","FCAW-S recargue duro","SAE 1020 10mm","FeCrC+Nb",1.6,"ninguno","PCC caras 3f",16,"excluido","subgrupo","W,R,IC,AP,AR,D","PRIMARIO. Autoprotegido","Soldag. Insp. 25:e2522"],
["RAHMAN2014-2F","Abd Rahman et al. 2014","FCAW-G filete 2F","acero bajo C 9mm","E71T-1",1.2,"100% CO2","Barrido continuo",0,"—","ecuaciones","pierna, ancho","SIN MATRIZ. Aporta ecuaciones","Appl. Mech. Mater. 564:549-554"],
["RAZAK2017-1G","Abdul Razak et al. 2017","FCAW-G BOP 1G","acero suave 9mm","E71T-1",1.2,"100% CO2","Barrido continuo",0,"—","metricas","MAD por estrato","SIN MATRIZ","Int. J. Mater. Mech. Manuf. 5(1):55-58"],
["RAHMAN2014-3F","Abd Rahman et al. 2014","FCAW-G filete 3F","acero bajo C 9mm","tubular",1.2,"CO2 99.9%","Barrido continuo",3,"excluido","contraste","BW,pierna,garganta,P","SIN MATRIZ. 3 validaciones","Appl. Mech. Mater. 660:342-346"],
["KATHERASAN2012","Katherasan et al. 2012","FCAW-G BOP","316L(N) 8mm","316LT",1.2,"Ar 15 lpm","Taguchi L25",25,"principal","parcial","W,R,P","PRIMARIO","J. Intell. Manuf. DOI 10.1007/s10845-012-0675-0"]]
for r in EST: ws.append(r)
fmt(ws,1,[24,26,22,20,18,8,18,18,10,16,14,24,34,40],"C2",12)
wb.save("FCAW_dataset_maestro.xlsx")
print("Hojas 00-01 OK")

# 02 DICCIONARIO
ws=wb.create_sheet("02_DICCIONARIO")
ws.append(["columna","grupo","unidad","definicion","nota_critica"])
DIC=[["registro_id","ID","—","Identificador unico y estable de cada cordon","Formato PAPERID-rN. No reordenar"],
["paper_id","ID","—","Llave que une con 01_ESTUDIOS y con el libro de originales",""],
["run_id_original","ID","—","Numero o codigo de corrida tal como aparece en el paper","Permite rastrear a la capa 0"],
["replica","ID","—","a/b cuando el paper publica replicas individuales",""],
["tipo_registro","ID","—","corrida | validacion","Las validaciones no entran al ajuste"],
["conjunto","CLAS","—","principal | pulsado | excluido | comparativo | solapado","FILTRO PRINCIPAL para modelar"],
["variante","CLAS","—","FCAW-G (con gas) | FCAW-S (autoprotegido) | RMD","No mezclar G con S: fisica distinta"],
["aplicacion","CLAS","—","BOP (cordon sobre chapa) | cladding | recargue_duro | filete","Regimenes de dilucion opuestos"],
["posicion","CLAS","—","plana | 1G | 3F | plana/agua","Solo plana y 1G son combinables"],
["nivel_uso","CLAS","—","completo | parcial | solo_dilucion | subgrupo | contraste","Define en que modelos participa"],
["metal_base","MAT","—","Designacion del metal base",""],
["espesor_mm","MAT","mm","Espesor de la placa","Afecta la disipacion de calor"],
["alambre_clase","MAT","—","Clase del consumible","Determina phi (ver 04_CONSTANTES)"],
["alambre_diam_mm","MAT","mm","Diametro nominal del alambre","Incluye el fundente, no solo el metal"],
["gas_tipo","MAT","—","Composicion cualitativa del gas","'n/d' = no reportado por el paper"],
["pct_CO2","MAT","%","Porcentaje de CO2 en la mezcla","Variable continua, mejor que categorica"],
["caudal_L_min","MAT","L/min","Caudal de gas de proteccion",""],
["polaridad","MAT","—","DCEP | DCEN | n/d","DCEP domina en FCAW-G"],
["I_amp","ENT","A","Corriente","Ver I_medida: puede ser consigna o medicion"],
["I_medida","ENT","—","si | no | estimada","CRITICO: 'si' solo en PAIVA2010 y GUIMARAES2020"],
["V_arco","ENT","V","Voltaje de ARCO","NO confundir con OCV"],
["OCV_volt","ENT","V","Voltaje de CIRCUITO ABIERTO","Superior al de arco. NO usar en HI"],
["WFS_m_min","ENT","m/min","Velocidad de alimentacion del alambre",""],
["TS_mm_s","ENT","mm/s","Velocidad de avance de la antorcha","Unidad canonica unica"],
["CTWD_mm","ENT","mm","Distancia tubo de contacto a pieza","NO fusionar con las dos siguientes"],
["stickout_mm","ENT","mm","Extension libre del electrodo","CTWD menos la longitud de arco"],
["NPD_mm","ENT","mm","Distancia boquilla a placa","Mayor que CTWD segun geometria de antorcha"],
["angulo_deg","ENT","grados","Angulo de electrodo o de antorcha","Referencia distinta segun paper"],
["f_pulso_Hz","ENT","Hz","Frecuencia de pulsacion","Solo en el subgrupo pulsado"],
["temp_precal_C","ENT","C","Temperatura de precalentamiento",""],
["HI_J_mm","DER","J/mm","Aporte termico = k*V*I/TS","k=0.80 (ISO/TR 17671-1). Vacio si falta V, I o TS"],
["A_dep_mm2","DER","mm2","Area depositada = phi*(pi/4)*d^2*(WFS/TS)","phi segun consumible (ver 04_CONSTANTES)"],
["WFS_TS","DER","—","Relacion adimensional de deposicion","Proxy robusto cuando falta el diametro"],
["W_mm","RESP","mm","Ancho del cordon","Dispersion tipica 1-5%"],
["R_mm","RESP","mm","Altura de refuerzo","Dispersion tipica 1-3%. La mas estable"],
["P_mm","RESP","mm","Profundidad de penetracion","Dispersion tipica 8-22%. LA MAS INESTABLE"],
["D_pct","RESP","%","Dilucion = AP/(AP+AR)*100","Definicion homogenea verificada en el corpus"],
["AP_mm2","RESP","mm2","Area de penetracion (metal base fundido)","Medida por planimetria o analisis de imagen"],
["AR_mm2","RESP","mm2","Area de refuerzo (metal depositado)","Contrastable con A_dep"],
["ZAT_mm","RESP","mm","Ancho de zona afectada termicamente","Dispersion 10-16%. NO apta para modelar"],
["IC_pct","RESP","%","Indice de convexidad = R/W*100","Adimensional: el mas transferible"],
["W_P","RESP","—","Relacion de aspecto ancho/penetracion","Adimensional"],
["TD_kg_h","RESP","kg/h","Tasa de deposicion","Solo GOMES2012 y PAIVA2010"],
["rend_pct","RESP","%","Rendimiento del proceso = TD/tasa de fusion","Solo GOMES2012 y PAIVA2010"],
["banderas","CTRL","—","Banderas de calidad separadas por ';'","Ver 03_BANDERAS"],
["confiabilidad","CTRL","—","alta | media | baja","Sintesis del juicio sobre la fila"],
["observaciones","CTRL","—","Nota libre especifica de la fila",""]]
for r in DIC: ws.append(r)
fmt(ws,1,[20,8,10,52,48],"A2",4)

# 03 BANDERAS
ws=wb.create_sheet("03_BANDERAS")
ws.append(["bandera","tipo","impacto","descripcion","consecuencia_operativa"])
BAN=[["flag_duplicado","estructural","critico","La corrida ya existe bajo otro paper_id","Contar una sola vez. Conservar la union de variables"],
["flag_solapa","estructural","alto","Condicion identica a otra corrida de otro paper","Excluir del ajuste; usar como verificacion cruzada"],
["flag_sin_tabla","estructural","critico","El paper no publica matriz experimental","Aporta 0 filas"],
["flag_OCV","variable","critico","Reporta voltaje de circuito abierto, no de arco","Excluir de todo modelo con aporte termico"],
["flag_sin_TS","variable","critico","Velocidad de avance no reportada","HI y A_dep no calculables"],
["flag_sin_corriente","variable","critico","Corriente no reportada ni manipulada","HI no calculable"],
["flag_sin_voltaje","variable","critico","Voltaje ausente en cualquier forma","HI no calculable"],
["flag_NPD","variable","alto","Distancia medida a la boquilla, no al tubo de contacto","No comparable con CTWD ni stickout"],
["flag_stickout","variable","medio","Extension libre, no CTWD","Difiere en la longitud de arco"],
["flag_gas","variable","alto","Gas de proteccion no reportado","Impide estimar pct_CO2"],
["flag_gas_atipico","variable","medio","Combinacion gas-consumible inusual","Verificar; posible reporte incompleto"],
["flag_una_respuesta","variable","alto","Solo publica una respuesta","Uso restringido a esa respuesta"],
["flag_sin_areas","variable","medio","No reporta AP ni AR","Dilucion no derivable"],
["flag_autoprotegido","proceso","critico","FCAW-S: sin gas externo","Subgrupo separado. Otra quimica y polaridad"],
["flag_pulsado","proceso","alto","Corriente pulsada","Subgrupo separado. HI requiere producto instantaneo"],
["flag_subacuatico","proceso","critico","Entorno acuatico","Subgrupo separado"],
["flag_posicion_3F","proceso","critico","Posicion distinta de la plana","Excluir: la gravedad altera el bano"],
["flag_respuestas_filete","proceso","critico","Mide pierna y garganta","No equivalentes a refuerzo ni penetracion"],
["flag_diametro_1_6","proceso","alto","Alambre de 1.6 mm en lugar de 1.2","No comparable directamente"],
["flag_recargue_duro","proceso","alto","Aleacion de recargue, no acero comun","phi no determinable"],
["flag_I_estimada","calidad","alto","Corriente deducida, no medida ni ajustada","Marcar como estimacion"],
["flag_promedio","calidad","medio","El valor es promedio; no se publica la dispersion","Favorece precision, impide estimar error"],
["flag_replicas_ambiguo","calidad","alto","Contradiccion sobre el numero de replicas","Afecta el peso de la fila"],
["flag_n_bajo","calidad","alto","Muy pocas corridas","No ajustable por si solo"],
["flag_OFAT","calidad","medio","Diseno no ortogonal, un factor por vez","Efectos confundidos"],
["flag_escaneado","calidad","medio","PDF sin capa de texto; transcripcion visual","Verificar manualmente"],
["flag_signos_pdf","calidad","medio","El PDF perdio los signos; matriz reconstruida","Ver 07_TRANSFORMACIONES"],
["flag_T","error","alto","Magnitud publicada fisicamente inconsistente","Registrar sin transformar"],
["flag_WD_A1","error","bajo","Cociente publicado no coincide con sus componentes","Corregido aritmeticamente"],
["flag_axial_S","error","alto","Codigo axial incompatible con la estructura del CCD","Corregido por estructura"],
["flag_corrida8","error","alto","Corriente incompatible con penetracion y deposicion","Excluir de ajustes con corriente"],
["flag_v3v4","error","bajo","Dos condiciones distintas con respuestas identicas","A verificar"],
["flag_Af_identico","error","bajo","Area repetida exactamente entre replicas","A verificar"],
["flag_material","error","bajo","Designacion de material erronea","Corregido"],
["flag_Ip","error","alto","Corriente de pico contradictoria entre publicaciones","Sin resolucion"],
["flag_caudal","error","alto","Caudal de gas contradictorio entre publicaciones","Sin resolucion"],
["flag_phi_no_aplicable","metodo","medio","phi=0.81 no valido para este consumible","No calcular A_dep"],
["flag_eta_080","metodo","alto","Eficiencia declarada distinta entre papers","Recalcular con k=0.80"],
["flag_voltaje_rango","metodo","medio","Voltaje declarado como intervalo","Se adopta el punto medio"],
["flag_mapeo","metodo","medio","Parametros por corrida reconstruidos del texto","Ver 07_TRANSFORMACIONES"],
["flag_4_mediciones","positivo","—","Geometria promediada en 4 puntos","Mejor protocolo del corpus"],
["flag_replicas_publicadas","positivo","—","Publica las replicas individuales","Fuente directa de repetibilidad"],
["flag_HI_invertido","hallazgo","—","Mayor aporte termico produce menor penetracion","Evidencia argumental"],
["flag_ZAT_dispersa","calidad","alto","ZAT con CV de 10-16%","No apta para modelar"]]
for r in BAN: ws.append(r)
fmt(ws,1,[26,12,10,46,44],"A2",4)

# 04 CONSTANTES
ws=wb.create_sheet("04_CONSTANTES")
ws.append(["constante","simbolo","valor","ambito","fuente","como_se_obtuvo"])
CON=[["Eficiencia de arco FCAW","k",0.80,"Todo el corpus","ISO/TR 17671-1, citada en MORENO2022-MAT","Resuelve la discrepancia entre KURTULMUS2015 (0.86) y ZHANG2016 (0.80). Se adopta el valor normativo"],
["Fraccion metalica rutilico","phi",0.81,"E71T-1, E316LT1, 317L, 316LT","PAIVA2010 y GOMES2012","(TD/rendimiento)/(densidad*WFS). Dos alambres y dos laboratorios coinciden: 0.9127 y 0.9191 mm2 de seccion metalica"],
["Fraccion metalica metal-cored","phi",0.95,"EC410NiMo","GUIMARAES2020 + MORENO2022-MAT","Contraste de AR medida contra A_dep teorica. El nucleo es aleante metalico, no escorificante"],
["Fraccion metalica recargue","phi",None,"FeCrC+Nb","CAVALCANTE2020","NO DETERMINABLE. La razon AR/A_dep oscila 0.85-1.12"],
["Velocidad de alambre vs corriente","Wf","-6.92 + 0.0860*I","317L diam 1.2 mm","PALANI2007-RSM","Publicada por el propio paper. Aplicada a KUMAR2011 y PALANI2006 (mismo alambre). Marcar como estimacion"],
["Densidad del acero","rho",7900,"kg/m3","Valor estandar","Usada en el calculo de la seccion metalica"],
["Repetibilidad del refuerzo","CV_R","1-3 %","FCAW-G","PALANI2006, GOMES2012, DAVE2025","La respuesta mas estable del corpus"],
["Repetibilidad del ancho","CV_W","1-5 %","FCAW-G","GOMES2012 (1.2%), KUMAR2011 (4.6%), PALANI2007 (5.3%)","La diferencia se explica por el numero de secciones promediadas"],
["Repetibilidad de la penetracion","CV_P","8-22 %","FCAW-G","PALANI2006 (11.5%), BECZKOWSKI2018 (22%), RODRIGUES2009 (7.6%), GOMES2012 (7.9%)","PISO DE ERROR: ningun modelo debe reclamar menos"],
["Repetibilidad de la dilucion","CV_D","3-13 %","FCAW-G","GOMES2012 (2.7%), KUMAR2011 (5.9%), BALASUB2025 (9.7%)","Varia mas por laboratorio que por proceso"],
["Desviacion consigna vs corriente real","—","hasta 15 %","FCAW-G","MORENO2022-MAT (Im vs Irms)","Fundamento de la calibracion por probeta"],
["Variacion de corriente entre repeticiones","—","2.7 %","FCAW-G","RODRIGUES2009 (259-278 A en 6 centrales)","Fuente de tension constante: la corriente se autoajusta"]]
for r in CON: ws.append(r)
fmt(ws,1,[30,12,16,24,34,60],"A2",6)
wb.save("FCAW_dataset_maestro.xlsx")
print("Hojas 02-04 OK")

# 05 MAESTRA
ws=wb.create_sheet("05_MAESTRA")
ws.append(COLS)
for r in M: ws.append([r[c] for c in COLS])
W05=[22,20,14,7,12, 12,10,13,14,13, 14,9,22,9,14,8,10,10, 8,10,9,10,11,10,9,10,9, 9,10,11, 10,10,9,
     8,8,8,8,9,9,8,8,7,9,9, 46,12,72]
fmt(ws,1,W05,"F2",44)
for row in ws.iter_rows(min_row=2,max_row=ws.max_row,min_col=6,max_col=6):
    v=row[0].value
    col={'principal':'C6EFCE','pulsado':'FFEB9C','excluido':'FFC7CE','comparativo':'D9D9D9','solapado':'F8CBAD'}.get(v)
    if col: row[0].fill=PatternFill('solid',fgColor=col)

# 06 HALLAZGOS
ws=wb.create_sheet("06_HALLAZGOS")
ws.append(["hallazgo_id","paper_id","tipo","descripcion","evidencia","resolucion","impacto","destino_tesis"])
HA=[
["H-001","VARIOS","estructural","5 duplicaciones y 1 solapamiento en 22 papers","SREERAJ x2 (16 corridas); GUIMARAES/MORENO x3 (18); RODRIGUES/PAIVA x2 (20); PALANI 3 condiciones compartidas","Contar una sola vez; conservar la union de variables","critico","Cap. 3 caracterizacion del corpus"],
["H-002","VARIOS","estructural","Los 22 papers provienen de solo 4 escuelas","Coimbatore (Palani, Kumar, Kannan, Sreeraj); Itajuba (Rodrigues, Paiva, Gomes); UTFPR (Moreno, Guimaraes); UiTM-UniKL (Rahman, Razak, Tham)","Declarar: los experimentos independientes son 10-11, no 22","alto","Cap. 3 y limitaciones del modelo jerarquico"],
["H-003","VARIOS","hallazgo","La penetracion tiene dispersion 4-10 veces mayor que el refuerzo","CV: refuerzo 1-3%; ancho 1-5%; penetracion 8-22%. Seis estudios independientes","Establecer piso de error como criterio de evaluacion de modelos","critico","Cap. 4 metrologia + Cap. 6 discusion"],
["H-004","VARIOS","hallazgo","El error de los modelos publicados iguala al ruido experimental","RAZAK2017 MAD: ancho 4-6%, penetracion 8-17%. Coincide con CV experimental","El techo de precision lo pone el proceso, no el algoritmo","critico","Cap. 6 discusion. NUCLEO DE LA TESIS"],
["H-005","VARIOS","hallazgo","El aporte termico no explica la penetracion por si solo","4 casos: KURTULMUS (misma energia por via distinta); ZHANG (transferencia); RAHMAN-3F (HI mayor da penetracion 15x menor); PALANI2006 corrida 7","Incorporar covariables de transferencia y posicion, o restringir alcance","critico","Cap. 5 modelado"],
["H-006","RODRIGUES2009 / MORENO2022-MAT","hallazgo","Lo nominal no determina lo real","RODRIGUES: 259-278 A en 6 repeticiones identicas (2.7%). MORENO: hasta 15% entre Im ajustada e Irms medida","FUNDAMENTO EMPIRICO de la calibracion por probeta","critico","Cap. 2 marco teorico + Cap. 5 propuesta"],
["H-007","BALASUB2025","hallazgo","La dilucion sigue al area depositada","A_dep 66 mm2 -> D 7.6%; A_dep 24 mm2 -> D 21.1%. Rango mas amplio del corpus","Base de un modelo semi-mecanicista de dilucion","alto","Cap. 5 modelado"],
["H-008","GOMES2012 / KUMAR2011","hallazgo","El protocolo de medicion determina la dispersion tanto como el proceso","CV del ancho: 1.2% con 4 secciones (GOMES) vs 4.6% con 1 seccion (KUMAR)","Justifica el seccionado multiple en la parte experimental propia","alto","Cap. 4 + diseno experimental propio"],
["H-009","GOMES2012 / PAIVA2010","hallazgo","La fraccion metalica del alambre tubular es 0.81, no 1.0","Seccion metalica: 0.9127 mm2 (GOMES) y 0.9191 mm2 (PAIVA). Area nominal de 1.2mm = 1.1310 mm2","Corrige la formula de area depositada para todo el corpus","alto","Cap. 4 estandarizacion"],
["H-010","MORENO2022-MAT / CAVALCANTE2020","hallazgo","phi es especifico del consumible, no una constante universal","Metal-cored EC410NiMo: phi=0.95. Recargue FeCrC+Nb: indeterminable (0.85-1.12)","Registrar phi por clase de alambre","medio","Cap. 4 estandarizacion"],
["H-011","MORENO2022-MAT","hallazgo","Existe referencia normativa para la eficiencia de arco","ISO/TR 17671-1 recomienda k=0.80 para FCAW","Recalcular HI de todo el corpus con criterio normativo, no arbitrario","alto","Cap. 4 estandarizacion"],
["H-012","BECZKOWSKI2018 / ZHANG2016","hallazgo","La penetracion fluctua 15-22% a lo largo del MISMO cordon","BECZKOWSKI: CV intra-cordon 22% en Hw vs 5% en Hn. ZHANG: min 15-22% menor que max","Medir una sola seccion introduce ese error","alto","Cap. 4 + diseno experimental propio"],
["H-013","SREERAJ2014 x2","error","'Wire speed' de 25-53 mm/min es fisicamente imposible en FCAW","Velocidad tipica: 5-15 m/min. El valor publicado es 2 ordenes de magnitud menor","Registrar sin transformar; excluir de modelos con A_dep","alto","Anexo de calidad de datos"],
["H-014","RODRIGUES2009 / PAIVA2010","error","Corrida 8: Im=212 A incompatible con sus respuestas","Corridas 5 y 11 con Im~220 dan P=1.55-1.60; la corrida 8 da P=2.85. Ademas TD=4.52 vs 5.40 con la misma Va","Conservar el dato; excluir de ajustes con corriente","alto","Anexo de calidad de datos"],
["H-015","GUIMARAES2020 + MORENO x2","contradiccion","CTWD: tablas de planificacion dicen 30/35/40; tablas de resultados dicen 30/33/36","La contradiccion existe en las TRES publicaciones, con identico patron. Se origino en la disertacion","Adoptar 30/33/36 (columna asociada a las mediciones)","alto","Anexo de calidad de datos"],
["H-016","GUIMARAES2020 vs MORENO2022-MAT","contradiccion","Corriente de pico 350 A vs 305+/-60 A; caudal 15 vs 18 L/min","Ambas publicaciones describen el mismo experimento","SIN RESOLUCION. Documentar ambas","alto","Anexo de calidad de datos"],
["H-017","SADEK2001","error","Relacion ancho/penetracion de A-1: publica 2.14, es 1.80","10.81/6 = 1.80. Las otras 8 probetas coinciden exactamente","Corregido aritmeticamente","bajo","Anexo de calidad de datos"],
["H-018","PALANI2007-RSM","error","Corridas axiales 9-10 con codigo S=1 donde debe ser 0","Un CCD requiere los demas factores en el centro. Las corridas 11-14 si cumplen","Corregido por estructura del diseno","alto","Anexo de calidad de datos"],
["H-019","BALASUB2025","error","El resumen declara dilucion maxima de 15.2% cuando la matriz contiene 21.1%","Corrida 22 = 21.1%; corrida 19 = 18.1%. El 15.2% proviene de la tabla de validacion","Datos intactos; conclusion publicada erronea","medio","Cap. 6 discusion"],
["H-020","VARIOS","hallazgo","Casi la mitad de los papers contiene al menos un error verificable","10 de 22 papers con errores detectados mediante verificacion aritmetica interna","El protocolo de verificacion es en si una contribucion metodologica","alto","Cap. 4 metodo de consolidacion"],
["H-021","PAIVA2010","hallazgo","Las respuestas estan correlacionadas entre si","Correlacion fuerte P-TD, P-R, TD-R, IC-D. Inexistente P-IC","Ponderar criterios correlacionados como independientes los sobrepondera","medio","Cap. 5 decision multicriterio"],
["H-022","PALANI2006 / BECZKOWSKI2018","hallazgo","Dos ANOVA independientes concluyen que ningun factor explica la penetracion","PALANI2006: F0 = 1.01, 1.60, 1.24 (todos no significativos). BECZKOWSKI: coeficientes despreciables frente a la constante","Coherente con H-003: el ruido supera al efecto","alto","Cap. 6 discusion"],
["H-023","RAZAK2017-1G","oportunidad","Precedente de formulacion inversa estratificada por requisito","El usuario declara la penetracion deseada y el calculador guia la seleccion de parametros","Antecedente directo del modulo de consulta inversa","medio","Cap. 2 revision + Cap. 5 sistema"],
["H-024","RAHMAN2014-2F","oportunidad","Ventana de parametros validada contra AWS D1.1 y publicada como ecuaciones","4 polinomios de limites de velocidad y voltaje en funcion de la corriente","Referencia de contraste para el modulo de consulta inversa","medio","Cap. 5 sistema"],
["H-025","SADEK2001","oportunidad","Variable binaria de agrietamiento en caliente asociada a condiciones","Grietas en A-1, C-1, C-2; ninguna en el resto. A-1 agrieta con la penetracion mas alta del grupo","Tipo de respuesta que el sistema de decision deberia predecir","medio","Cap. 5 sistema"],
["H-026","VARIOS","oportunidad","Ningun paper publica probabilidad de cumplimiento, solo valores puntuales","22 de 22 entregan un numero como si fuera exacto","Hueco que el modelo con incertidumbre llena","alto","Cap. 5 + contribucion"],
["H-027","VARIOS","hallazgo","Ningun paper reporta el conjunto completo de variables","Faltan: gas en 5 estudios, voltaje de arco en 6, velocidad de avance en 3. Solo 4 alcanzan nivel completo","Base para proponer un estandar de reporte minimo","alto","Cap. 6 + contribucion"],
["H-028","VARIOS-NUEVO","estructural","La mitad del material nuevo no era nuevo: 5 duplicaciones en 12 papers revisados","KANNAN2006=PALANI2007 (20/20 filas identicas); SENSITIVITY-RSM=KANNAN2006 (68% de solape); NUNES2020=GOMES2012 (matriz 31/31); KATHERASAN-GA/SA=KATHERASAN-ANN/PSO (22/22); CA6M2018=MORENO2022-MAT (9/9 valores RMS)","Contar campanas, no papers. Conservar union de variables","critico","Cap. 3 y Cap. 4. Refuerza H-001"],
["H-029","ODHIAMBO2025 / ALORAIER2025","hallazgo","La eficiencia de arco k=0.80 queda VERIFICADA contra datos publicados","Despejando k del HI reportado: ODHIAMBO (Kenia, 22 corridas) k=0.7993 [0.787-0.804]; ALORAIER (Kuwait, 12 corridas) k=0.8014 [0.795-0.807]. Dos laboratorios independientes, 2025","k=0.80 deja de ser supuesto normativo y pasa a constante verificada","alto","Cap. 4 estandarizacion. Cierra H-011"],
["H-030","ODHIAMBO2025","hallazgo","El aporte termico explica la ZAT pero NO la penetracion","22 corridas en tuberia API 5L: corr(HI,ZAT)=+0.91 frente a corr(HI,DoP)=+0.33. Ejemplo: 0.25 kJ/mm da DoP 4.60 mm y 2.74 kJ/mm da 5.64 mm","5o caso del corpus. Separa que responde a energia y que no","critico","Cap. 5 modelado. Refuerza H-005"],
["H-031","CA6M2018 + SOLOVYOV2023","hallazgo","La desviacion maquina-consigna es una CURVA, no un desfase constante","CORRIENTE (CA6M2018): a 170 A entrega +13.7%, a 230 A entrega -15.1%; el signo se invierte. VOLTAJE (SOLOVYOV2023): -19.2% a 24 V y -5.6% a 32 V; la SD del voltaje cae de 10.3 a 2.0 V al subir la consigna","Una calibracion de UN punto no basta: se requieren 2-3 puntos a lo largo del rango de trabajo","critico","Cap. 6 diseno de la calibracion por probeta. Refuerza H-006"],
["H-032","SENTHILKUMAR2014 vs SENTHILKUMAR2015","contradiccion","Contradiccion INTRALABORATORIO en el indice de convexidad","Mismo grupo, mismo alambre super duplex, misma definicion declarada (refuerzo/ancho): IC medio 45.8% en el CCD de 2014 frente a 27.3% en el L9 de 2015. En la condicion casi coincidente (22V, ~6.3 m/min, 0.16 m/min, 19 mm): 69.4% vs 37.4%","SIN RESOLUCION. Mas fuerte que una discrepancia entre laboratorios: descarta explicaciones de maquina u operador","alto","Cap. 4 anexo de calidad + Cap. 6 discusion"],
["H-033","10 ESTUDIOS","hallazgo","La formula A_dep = phi*(pi/4)*d^2*(WFS/TS) con phi=0.81 queda VALIDADA contra la geometria medida","Razon A_dep/(2/3*W*R) en 10 estudios: mediana 1.06, media 1.04, rango 0.44-1.45. La razon debe rondar 1.0 porque el metal aportado por el alambre equivale al AREA DE REFUERZO (el resto del cordon es metal base fundido). Valores por estudio: Senthilkumar2015 0.44, Kumar2011 0.50, Palani2007 0.95, Palani2006 1.01, Gomes2012 1.03, Guimaraes2020 1.10, Singh2021 1.26, Aloraier2025 1.32, Katherasan2012 1.38, Balan2018 1.45","phi=0.81 y el factor de forma 2/3 son correctos. La razon sirve ademas como PRUEBA DE COHERENCIA para detectar errores de unidad: asi se detecto el de Yadav2022","alto","Cap. 4 estandarizacion + criterio de validacion de datos"],
["H-039","YADAV2022","error","Unidad de la velocidad de alimentacion mal rotulada en el paper","El paper indica mm/min (315.6 a 1750). Leido asi, A_dep/(2/3*W*R)=0.15, es decir 2.9x por debajo del minimo del corpus (0.44) y fisicamente imposible: el cordon medido no cabe en el metal declarado. Leido como cm/min da 1.50, dentro del rango observado","Se adopta cm/min (3.16 a 17.50 m/min, rango tipico de FCAW Ø1.2). Se recuperan 21 corridas al modelo","medio","Anexo de calidad de datos"],
["H-040","YADAV2022","error","Niveles +1 y +2 del diseno no equiespaciados","Con centro 946.8 y paso 315.6, los niveles esperados serian 1262.4 y 1578; el paper publica 1331.2 y 1750. El lado bajo (-2,-1) si cuadra exacto","Se conservan los valores publicados. Afecta levemente la ortogonalidad del diseno, no la validez de las mediciones","bajo","Anexo de calidad de datos"],
["H-041","KANNAN2006 / SADEK2001 / KURTULMUS2015","hallazgo","Reportar corriente sin velocidad de alimentacion rompe la trazabilidad del proceso","En FCAW-G la fuente es de VOLTAJE CONSTANTE: el operador ajusta alimentacion y voltaje, y la CORRIENTE es la respuesta con que el equipo mantiene la longitud de arco. Kannan aisla la corriente (200-300 A) omitiendo alimentacion Y voltaje; Sadek documenta I, V, TS y distancia pero no la alimentacion que requieren sus 150-380 A; Kurtulmus varia I (200-255 A) y V (26.5-32.0 V) con avance fijo de 4 mm/s, sin alimentacion. Total: 43 corridas","Los tres experimentos NO son reproducibles: nadie puede saber a que alimentacion operaron. Justifica FISICAMENTE adoptar WFS/TS como predictor troncal en lugar de la corriente","critico","Cap. 4 + NORMA MINIMA DE REPORTE + justificacion del modelo (Cap. 5)"],
["H-042","DAVE2024","hallazgo","Sin velocidad de avance el aporte termico es matematicamente incalculable","El estudio documenta corriente, voltaje y caudal de gas y plantea una optimizacion multiobjetivo, pero omite la velocidad de avance tanto del diseno como de los parametros constantes. Relaciona penetracion y ZAT con V e I sin conocer el tiempo de exposicion termica del material","Su modelo predictivo no es verificable por terceros. 15 corridas quedan fuera de cualquier analisis energetico","alto","Cap. 4 + NORMA MINIMA DE REPORTE"],
["H-043","SREERAJ2014","error","Los cuatro puntos de 87 A son empiricamente falsos","La columna rotulada 'wire speed' (25-53 mm/min) es en realidad velocidad de AVANCE en cm/min. Al imputar la alimentacion con la relacion del propio grupo (Wf = -6.92 + 0.0860*I, Palani & Murugan, 317L Ø1.2 mm): a 87 A da 0.56 m/min, que no sostiene arco en Ø1.2 mm. Por nivel: 87 A -> 0.56 (inviable); 123 A -> 3.66 (marginal); 138 A -> 4.95 (ok); 155 A -> 6.41 (ok)","NO se rescatan las corridas: imputar la alimentacion con la ecuacion de otro laboratorio seria fabricar dato, y esa misma ecuacion demuestra que el nivel bajo es falso. Se documenta la reinterpretacion","alto","Anexo de calidad de datos + Cap. 4"],
["H-044","VARIOS","hallazgo","La corriente es una variable de RESPUESTA, no una consigna, en FCAW con fuente de voltaje constante","Consecuencia directa: (a) justifica fisicamente usar WFS/TS y no la corriente como predictor; (b) explica H-006 y H-031, la desviacion consigna-medida de hasta 15% con cambio de signo, porque lo que la maquina muestra es su propia respuesta y depende del stick-out, del alambre y de la resistencia del circuito; (c) unifica las omisiones de Kannan, Sadek y Kurtulmus en una sola falla estructural: reportar la respuesta en lugar de la consigna","Argumento de proceso, no de conveniencia de datos, para la especificacion del modelo","critico","Cap. 5 justificacion del modelo + Cap. 2 marco"],
["H-045","7 ESTUDIOS","hallazgo","La relacion Wf = f(I) es especifica de MAQUINA Y CONSUMIBLE, no una ley del proceso","Se probo la ecuacion Wf = -6.92 + 0.0860*I (Palani & Murugan, 317L Ø1.2 mm) contra los 115 registros del corpus que reportan corriente Y alimentacion MEDIDAS. Error por estudio: Palani2006 0.0%, Palani2007 0.0%, Kumar2011 0.0% (los tres con alambre 317L, mismo laboratorio de origen de la ecuacion); Guimaraes2020 metal-cored EC410NiMo -19%; Paiva2010 E71T-1 de -19% a +40%; Zhang2016 subacuatico de +77% a +113%; Aloraier2025 E71T-1C de -123% a -133%, dando valores NEGATIVOS a baja corriente","PROHIBE imputar la alimentacion desde la corriente en estudios que no la reportan (Kannan2006, Sadek2001, Kurtulmus2015). La ecuacion SI sirve como criterio de plausibilidad para detectar magnitudes imposibles: asi se identifico el nivel de 87 A de Sreeraj (H-043). Evidencia cuantitativa de que la transferencia interlaboratorio no es trivial","critico","Cap. 4 + Cap. 5 justificacion + Cap. 6 fundamento de la calibracion"],
["H-046","KANNAN2006","hallazgo","Verificado: el paper NO publica la velocidad de alimentacion en ninguna seccion","Revision dirigida del texto completo, tablas, pies de tabla y parametros constantes. Sus 31 corridas tienen las cuatro respuestas y 7 puntos centrales legitimos, pero solo corriente como parametro electrico","Permanece fuera del modelo principal. Entra al modelo de SENSIBILIDAD con la corriente como predictor troncal, donde ademas sirve para contrastar empiricamente el H-044","medio","Anexo de calidad de datos"],
["H-049","AWS D1.1:2000 Tabla 4.5","hallazgo","La desviacion maquina-consigna EXCEDE por si sola el umbral de recalificacion de la norma","AWS D1.1:2000, Tabla 4.5, variables esenciales para FCAW: item 13, un cambio de amperaje >10% exige RECALIFICAR el procedimiento; item 15, cambio de voltaje >7%; item 16, cambio de velocidad de alambre >10%; item 17, cambio de velocidad de avance >25%; item 18, aumento de aporte termico >10%. CONTRASTE con lo medido en el corpus: CA6M2018 registra desviaciones consigna-vs-medida de +13.7% y -15.1% en CORRIENTE (H-031), y Solovyov2023 de -19.2% a -5.6% en VOLTAJE. Es decir, la maquina SOLA cruza el umbral de variable esencial sin que nadie toque la perilla","Un taller puede estar operando FUERA de su propio WPS calificado sin saberlo, porque nadie mide la entrega real. Fundamenta normativamente la calibracion por probetas: no es una mejora opcional sino una condicion para que el WPS siga siendo valido","critico","NUCLEO DEL CAP. 6 + justificacion normativa del sistema"],
["H-050","AWS D1.1:2000","oportunidad","El macroataque obligatorio genera exactamente los datos que el sistema necesita","AWS D1.1:2000 clausula 4.8.4 exige preparar la probeta con acabado apto para macroataque y atacarla para dar definicion clara del cordon; la clausula 4.30.2 lo repite para filetes y conexiones T-Y-K. Ese ensayo produce la seccion transversal de donde se miden ancho, refuerzo y penetracion","La probeta de calificacion YA se suelda, corta, pule, ataca y examina por obligacion normativa. El sistema propuesto no agrega ensayos: reutiliza informacion que hoy se archiva sin explotar. Costo incremental cero","critico","Cap. 6 y Cap. 7. Es el argumento economico del sistema"],
["H-051","AWS D1.1:2000 item 17 vs practica manual","hallazgo","La tolerancia de velocidad de avance es 25% en FCAW, y la soldadura manual la excede","AWS D1.1:2000 Tabla 4.5 item 17 admite hasta 25% de variacion en velocidad de avance para FCAW sin recalificar (frente a 15% en SMAW). La velocidad a pulso varia tipicamente +/-30% dentro del MISMO cordon","Justifica normativamente el uso de avance mecanizado en la parte experimental: a mano no se puede garantizar el cumplimiento de la propia variable esencial","alto","Cap. 6 diseno experimental"],
["H-052","ISO 3834-2:2005 + ISO 3834-5:2005","hallazgo","La CADENA NORMATIVA que obliga a calibrar el equipo de soldadura esta completa y nadie la conecta con el modelado","ISO 3834-2:2005 clausula 9.3 exige verificar la CONDICION DE AMPERIMETROS Y VOLTIMETROS usados para operar el equipo de soldadura, y la condicion de alimentadores de alambre y conductos; declara que equipo defectuoso no debe usarse. Su clausula 16 hace al fabricante responsable de la calibracion o validacion del equipo de medicion. ISO 3834-5:2005 Tabla 9 remite explicitamente, para soldadura por arco, a ISO 17662 (Welding - Calibration, verification and validation of equipment used for welding). La cadena es: certificar 3834-2 -> clausula 16 -> ISO 17662 -> calibrar amperimetro, voltimetro y alimentador","La calibracion del equipo NO es una propuesta del autor: ya es requisito normativo internacional. Lo que NO existe es el puente entre esa calibracion obligatoria y los modelos predictivos publicados. Ese puente es la aportacion de esta tesis","critico","Cap. 2 marco normativo + Cap. 6. Da respaldo ISO al sistema"],
["H-053","ISO 3834-5:2005 Tabla 9 + ISO 3834-4","hallazgo","El nivel elemental de calidad NO exige calibrar: ahi esta el hueco del taller pequeno","ISO 3834-5:2005 Tabla 9 asigna ISO 17662 a la clausula 16 de ISO 3834-2 (requisitos comprensivos) y de ISO 3834-3 (requisitos estandar), pero para ISO 3834-4 (requisitos elementales) indica NONE: ningun documento de calibracion exigible","El taller que opera bajo requisitos elementales -tipicamente el pequeno y mediano- no tiene obligacion de calibrar, y es justamente el que mas sufre la no transferibilidad del conocimiento publicado. El sistema propuesto le da una via de bajo costo para cerrar esa brecha","alto","Cap. 1 planteamiento del problema + Cap. 8 implicaciones"],
["H-054","ISO 17639 via ISO 3834-5","hallazgo","El examen macroscopico tiene norma propia y esta en la lista de conformidad","ISO 3834-5:2005 incluye ISO 17639 (Destructive tests on welds in metallic materials - Macroscopic and microscopic examination of welds) entre los documentos de cumplimiento necesario. Complementa a AWS D1.1:2000 clausula 4.8.4, que exige preparar la probeta con acabado apto para macroataque","La medicion de ancho, refuerzo y penetracion sobre la macrografia tiene procedimiento normalizado en ambos sistemas normativos, americano y europeo. Refuerza H-050: el dato que el sistema necesita ya se genera por obligacion","medio","Cap. 6 metodo de medicion"],
["H-055","ISO 17662:2016 Tabla 11","hallazgo","La norma EXIGE validar el amperimetro y el voltimetro del equipo de soldadura","ISO 17662:2016 (BS EN, 38 p.), Tabla 11 Electrical variables: para corriente media dice AMMETERS SHALL BE VALIDATED (ver EN 50504); para voltaje de arco medio dice VOLTMETERS SHALL BE VALIDATED (ver EN 50504); para potencia instantanea remite a ISO/TR 18491. Clausula 4.2: la calibracion, verificacion o validacion se hara UNA VEZ AL ANO salvo que se especifique otra cosa; puede reducirse la frecuencia con registro probado de repetibilidad","Cierra la cadena normativa H-052: la obligacion de validar los instrumentos de la maquina es explicita y esta vigente. La tesis no propone calibrar: propone USAR el dato de esa validacion obligatoria para corregir el modelo predictivo","critico","Cap. 2 marco normativo + Cap. 6"],
["H-056","ISO 17662:2016 Tabla 11 nota","hallazgo","La propia norma advierte del error del multimetro de gancho, que es el instrumento del taller","Nota al pie de la Tabla 11: si se usan pinzas amperimetricas (tong-tests) para medir corriente, debe considerarse la DIFERENCIA ENTRE INSTRUMENTOS DE VALOR MEDIO Y DE VALOR EFICAZ (RMS). Ademas indica que la senal deberia monitorearse de forma continua y que el tiempo de muestreo debe bastar para una lectura razonablemente estable","Valida la advertencia metodologica del capitulo 6: el multimetro promedia y el arco fluctua. Obliga a declarar en la tesis que las mediciones son de VALOR MEDIO durante arco estable, no instantaneas","alto","Cap. 6 metodo de medicion"],
["H-057","ISO 17662:2016 Tabla 12","oportunidad","El metodo de cronometro y regla para medir alimentacion y avance esta NORMALIZADO","Tabla 12 Mechanized or automatic welding: para TRAVEL SPEED y para WIRE FEED SPEED la norma admite medicion por medio de cronometros y reglas o cintas metricas; anade que las reglas de acero apropiadas NO necesitan calibracion, verificacion ni validacion siempre que no esten visiblemente danadas, y que los cronometros pueden validarse por comparacion con cualquier reloj razonablemente exacto","El procedimiento experimental propuesto (alimentar 15 s sin arco, medir el alambre con regla; marcar 150 mm y cronometrar el avance) NO es improvisado: es el metodo que ISO 17662 sanciona. Costo de instrumentacion cero","critico","Cap. 6 diseno experimental. Respaldo normativo del metodo propio"],
["H-058","ISO 17662:2016 clausula 4.2 vs H-031","hallazgo","La periodicidad anual de calibracion no captura una desviacion que depende del punto de operacion","ISO 17662:2016 clausula 4.2 fija la calibracion una vez al ano salvo especificacion contraria. Pero H-031 muestra que la desviacion consigna-vs-entrega CAMBIA DE SIGNO a lo largo del rango: +13.7% a 170 A y -15.1% a 230 A. Una validacion anual en un solo punto de operacion no describe esa curva","HUECO NORMATIVO IDENTIFICADO: la norma regula la FRECUENCIA temporal pero no la COBERTURA del rango de operacion. Propuesta de la tesis: validar en 2-3 puntos del rango de trabajo, no en uno. Es una aportacion concreta a la practica normativa","critico","Cap. 6 + Cap. 8 aportacion y recomendaciones"],
["H-059","AWS D1.1/D1.1M:2020 Tabla 6.5","verificacion","Las tolerancias de variable esencial SE MANTIENEN en la edicion vigente","Verificado directamente en AWS D1.1/D1.1M:2020 (664 p.), Tabla 6.5 PQR Essential Variable Changes Requiring WPS Requalification, p.142-144 del documento. Para FCAW: item 12 amperaje >10% incremento o decremento; item 16 voltaje >7%; item 17 velocidad de alambre >10% si no es controlada por amperaje. La numeracion de clausula cambio de 4 (edicion 2000) a 6 (edicion 2020) y la tabla de 4.5 a 6.5, pero los VALORES son identicos","Los hallazgos H-049 y H-051 quedan validados contra la edicion VIGENTE. Citar como AWS D1.1/D1.1M:2020 Tabla 6.5. Queda resuelto el pendiente de verificacion de edicion","alto","Cap. 2 marco normativo. Cierra el pendiente de H-049"],
["H-060","ISO 17639:2022 clausula 3.1","hallazgo","El examen macroscopico normalizado admite explicitamente ojo desnudo o menos de x50 aumentos","ISO 17639:2022 clausula 3.1 define examen macroscopico como examination of a test specimen by the naked eye, or under low magnification (generally less than x50), with or without etching. La clausula 7 indica que las probetas se orientan perpendiculares al eje del cordon (seccion transversal). La clausula 9 permite examinar antes y/o despues del ataque","El metodo propuesto -fotografia con escala y medicion en ImageJ- cae dentro de la definicion normativa de examen macroscopico. NO se requiere microscopio metalografico ni instrumentacion costosa. Refuerza H-057","alto","Cap. 6 metodo de medicion"],
["H-061","ISO 17639:2022 Tabla 1","hallazgo","La norma distingue que se revela CON ataque y que SIN el: afecta al diseno de la medicion","ISO 17639:2022 Tabla 1, guia de evaluacion de caracteristicas: GEOMETRICAL SHAPE (defecto 500 segun ISO 6520-1), que incluye ancho, refuerzo y perfil del cordon, se revela por macro CON y SIN ataque. En cambio HEAT AFFECTED ZONE solo se revela por macro CON ataque. Lack of fusion/penetration se revela en ambos casos","Consecuencia practica: para medir ancho y refuerzo bastaria pulido sin ataque, pero para ZAT y para distinguir la linea de fusion (y por tanto la penetracion real y la dilucion) el ATAQUE ES OBLIGATORIO. Justifica el uso de Nital en el procedimiento propio","medio","Cap. 6 metodo de medicion"],
["H-062","ISO 17639:2022 clausulas 8.4 a 8.6 y 10","oportunidad","La norma fija el procedimiento de ataque, la seguridad y la DESIGNACION del ensayo","Clausula 8.4 metodos de ataque: inmersion, frotado (swabbing) o electrolitico; el metodo debe especificarse ANTES de atacar; tras el ataque lavar y secar. Clausula 8.5 remite a ISO/TR 16060 para reactivos tipicos. Clausula 8.6 medidas de seguridad obligatorias: proteccion ocular o facial, guantes o pinzas, mezclas bajo campana de extraccion, verter siempre acido sobre agua y nunca al reves. Clausula 10 designacion del ensayo: referencia a ISO 17639, tipo de examen, atacado o sin atacar, y objeto del ensayo","Da el procedimiento completo y citable para el capitulo 6, incluida la seguridad. La designacion normalizada permite reportar los resultados de forma trazable","medio","Cap. 6 procedimiento experimental"],
["H-063","Hevner et al. 2004, MIS Quarterly 28(1):75-105","marco","El proyecto encaja en las siete directrices de Design Science Research","Hevner, March, Park y Ram (2004) Tabla 1: (1) Design as an Artifact: producir un artefacto viable como constructo, modelo, metodo o instanciacion; (2) Problem Relevance: soluciones tecnologicas a problemas de negocio relevantes; (3) Design Evaluation: demostrar utilidad, calidad y eficacia con metodos de evaluacion bien ejecutados; (4) Research Contributions: contribuciones claras y verificables en artefacto, fundamentos o metodologias; (5) Research Rigor: metodos rigurosos en construccion y evaluacion; (6) Design as a Search Process: buscar el artefacto usando medios disponibles y satisfaciendo las leyes del entorno; (7) Communication of Research: comunicar a audiencias tecnicas Y gerenciales","MARCO TEORICO DEL CAP. 2. Mapeo: (1) el artefacto es el sistema de soporte a la decision; (2) la relevancia esta demostrada por H-049 y H-058, huecos normativos reales; (3) la evaluacion es la validacion dejando-un-laboratorio-fuera mas las probetas propias; (4) la contribucion incluye la base consolidada, el piso de error y la norma minima de reporte; (5) el rigor es el modelo jerarquico bayesiano; (6) la busqueda esta acotada por las leyes del entorno, que son AWS D1.1 e ISO 3834/17662; (7) la comunicacion es la herramienta en formato WPS para el taller y la tesis para el ambito academico","critico","Cap. 2 marco teorico. ESTRUCTURA METODOLOGICA DE TODA LA TESIS"],
["H-034","8 ESTUDIOS","hallazgo","PISO DE ERROR CONSOLIDADO sobre replicas verdaderas","Mediana del CV entre replicas con parametros identicos, 8 estudios independientes: refuerzo 2.87% (n=7); ancho 3.84% (n=7); indice de convexidad 6.09% (n=8); penetracion 7.92% (n=7); W/P 8.96% (n=8); dilucion 9.99% (n=6); ZAT 15.55% (n=1). Excluido BALAN2018 por replicas no independientes","Criterio cuantitativo para evaluar cualquier modelo: por debajo del piso no hay senal","critico","Cap. 4 metrologia. Cuantifica H-003 y H-004"],
["H-035","BALAN2018","error","Los 7 puntos centrales no son replicas independientes","R=3.87 mm en cinco de siete; P=0.71 en seis de siete; W=8.44/8.45 en cinco. Replicas reales no coinciden a dos decimales","Excluido del calculo del piso de error","alto","Anexo de calidad de datos"],
["H-036","ALORAIER2025","error","Par de corridas 10-11 fisicamente implausible","Duplican corriente (73->145 A) y alimentacion (2.5->5.0 m/min) y devuelven W 6.88/6.90, R 1.84/1.85, P 0.93/0.95, ZAT 9.06/9.12: variacion menor a 0.07 mm","Probable fila duplicada por error. No usar ese par para estimar el efecto de la alimentacion","medio","Anexo de calidad de datos"],
["H-037","MOSTAFA2006 / SENTHILKUMAR2014","hallazgo","Publicar el modelo sin publicar los datos impide la reutilizacion","MOSTAFA: CCD de 5 factores CON VOLTAJE, 32 corridas; publica matriz codificada y coeficientes, pero las penetraciones medidas solo existen como puntos en una figura. SENTHILKUMAR2014: publica RFF y PFF pero no W, R ni P por separado","Evidencia directa de la no acumulabilidad de la literatura","critico","Cap. 4 y NORMA MINIMA DE REPORTE"],
["H-038","CA6M2018","resolucion","Se resuelve la contradiccion de CTWD de H-015","La publicacion mas TEMPRANA de la campana 410NiMo (IJAERS 2018) usa 30/33/36 mm. Guimaraes 2020 y Moreno 2022 heredan el error de sus Tabelas 5 y 6","Adoptar 30/33/36. H-015 queda RESUELTO","medio","Anexo de calidad de datos"]]
for r in HA: ws.append(r)
fmt(ws,1,[10,26,14,44,60,44,10,32],"A2",4)

# 07 TRANSFORMACIONES
ws=wb.create_sheet("07_TRANSFORMACIONES")
ws.append(["paper_id","regla_decodificacion","problema_extraccion","reconstruccion_o_correccion","validacion_aplicada","derivadas_calculadas"])
TR=[
["SREERAJ2014-HYB","V:1-4 = 20/22/24/25 | I:1-4 = 87/123/138/155 | N:1-4 = 15/20/25/30 | T:1-4 = 25/40/50/53","Encabezado de la Tabla 4 rotula I,S,N,T","Se usan las etiquetas de la Tabla 3 (V,I,N,T) confirmadas por su pie de tabla","Codigos identicos entre Tabla 3 y Tabla 4","IC=R/W*100; W/P. NO A_dep ni HI (falta velocidad de avance)"],
["GUIMARAES2020","Valores reales publicados; sin codificacion","Contradiccion CTWD entre tablas de planificacion y de resultados","Se adopta 30/33/36 de la Tabla 8 y Figura 17, confirmado por MORENO2022-MAT","IC calculado coincide con el publicado en las 18 filas","A_dep con phi=0.95; WFS/TS. HI e Irms/Urms tomados de MORENO2022-MAT"],
["KURTULMUS2015","Sin codificacion","Coma decimal en el original","Conversion a punto decimal","HI verificado con k=0.86 en 3/3; At=Ad+Am en 3/3; D/W en 3/3","Dilucion derivada de Am/At; IC; W/P"],
["SADEK2001","Sin codificacion","PDF escaneado sin capa de texto","Transcripcion por lectura visual de imagenes a 150 dpi","W/P verificado en 8/9; A-1 corregido de 2.14 a 1.80","HI con V=29.5 (punto medio del rango 29-30); IC; W/P"],
["KUMAR2011","I = 200+25*cod | S = 26+2*cod | OCV = 34+2*cod | NPD = 20+3*cod | ang = 15+5*cod","Ninguno","Generador de la media fraccion verificado: A = I*S*V*N en 16/16","Estructura 16 factoriales + 10 axiales + 6 centrales confirmada","WFS estimada con Wf(I) de PALANI2007; A_dep con phi=0.81; IC; W/P. NO HI (OCV)"],
["GOMES2012","Wf = 8.5+1.5*cod | V = 29.5+2.5*cod | S = 40+10*cod | CTWD = 20+5*cod","EL PDF PIERDE TODOS LOS SIGNOS NEGATIVOS","Matriz reconstruida asumiendo orden estandar de Yates (Wf variando mas rapido)","Efectos estimados contra coeficientes publicados: Wf +0.802 vs +0.797; N -0.629 vs -0.629; V +0.702 vs +0.656; S -1.371 vs -1.451","A_dep con phi=0.81; IC; W/P. NO HI (sin corriente)"],
["DAVE2025-FCAW","Valores reales publicados","Ninguno","Estructura Box-Behnken verificada: 3 bloques de 4 + 3 centrales","Ortogonalidad confirmada","IC; W/P. NO HI ni A_dep (sin velocidad de avance ni WFS)"],
["BALASUB2025","OCV = 34+2*cod | F = 13+2*cod | S = 0.34+0.08*cod | NPD = 21+2*cod | ang = 15+5*cod","Ninguno","Generador verificado: E = V*F*S*D en 16/16","Suma de cuadrados de los centrales = 8.60, coincide exactamente con el 'Pure error' del ANOVA publicado","A_dep con phi=0.81. NO HI (OCV y sin corriente)"],
["PAIVA2010-EQMM","Valores reales publicados","Coma decimal","Conversion a punto","Mismos 20 ensayos que RODRIGUES2009: P e IC identicos","HI con V*Im/TS; A_dep con phi=0.81; WFS/TS. Seccion metalica verificada: 0.9191 mm2"],
["PALANI2007-RSM","I = 210+20*cod (axiales 176/244) | S = 34+5*cod (26/42) | NPD = 20+3*cod (15/25)","Ninguno","Corridas 9-10: codigo de S corregido de 1 a 0 por estructura del CCD rotable","phi_a=W/P y phi_e=W/R verificados en 20/20","WFS con la ecuacion del propio paper; A_dep con phi=0.81; IC. NO HI (sin voltaje)"],
["PALANI2006-TAGUCHI","I:1-3 = 190/210/230 | S:1-3 = 290/340/390 | NPD:1-3 = 17/20/23","Ninguno","Se promedian las dos replicas publicadas; las individuales quedan en observaciones","3 condiciones coinciden con PALANI2007-RSM y sus valores son las medias de estas replicas","WFS con Wf(I); A_dep; IC; W/P. NO HI (sin voltaje)"],
["KATHERASAN2012","Valores reales publicados","Ninguno","Ortogonalidad del L25 verificada en los 6 pares de factores","Cada par de niveles aparece exactamente una vez en 25 corridas","A_dep con phi=0.81; IC; W/P. NO HI (sin corriente)"],
["CAVALCANTE2020","U = 30+2*cod | Va = 12+2*cod | Vs = 40+10*cod","Coma decimal","Conversion a punto","R/L verificado en 16/16; Ar/Af en 16/16","DILUCION DERIVADA de Af/(Ar+Af): el paper declara la formula pero no tabula la columna. NO A_dep (phi no aplicable)"],
["ZHANG2016","Sin codificacion","Texto con palabras partidas por linea","Reunificacion de texto","Q = eta*P_ef/v con eta=0.8 verificado en 4/4","Corriente ESTIMADA como P_ef/V; diametro 1.6 mm inferido de la descripcion de la gota"],
["RAHMAN2014-3F","Sin diseno: barrido continuo","Ninguno","Solo se transcriben las 3 probetas de validacion de la Tabla 2","HI verificado en 2/3 (probeta 2 difiere 2.6%)","Ninguna: respuestas de filete no combinables"]]
for r in TR: ws.append(r)
fmt(ws,1,[24,44,34,50,62,46],"A2",2)
wb.save("FCAW_dataset_maestro.xlsx")
print("Hojas 05-07 OK")

# 08 ECUACIONES
ws=wb.create_sheet("08_ECUACIONES")
ws.append(["paper_id","respuesta","ecuacion","variables","ambito_validez","uso_recomendado"])
EQ=[["RAHMAN2014-2F","Tamano de pierna (mm)","y = 6.0918 * x^0.5373","x = aporte termico (kJ/mm)","Filete 2F, chapa 9mm, E71T-1, CO2. Limite: 325 A y 2.2 kJ/mm","Contraste. Exponente ~0.5: la geometria crece con la raiz del aporte termico"],
["RAHMAN2014-2F","Ancho del cordon (mm)","y = 8.8403 * x^0.5033","x = aporte termico (kJ/mm)","Idem","Verificado contra 3 puntos publicados: error -5.9% a +1.5%"],
["RAHMAN2014-2F","Velocidad minima (mm/s)","y = 0.000104x^2 - 0.008225x + 3.056277","x = corriente (A)","Grado A, AWS D1.1, 100-325 A","VENTANA DE PARAMETROS: referencia para el modulo de consulta inversa"],
["RAHMAN2014-2F","Velocidad maxima (mm/s)","y = -0.000123x^2 + 0.087177x - 1.561039","x = corriente (A)","Idem","Idem"],
["RAHMAN2014-2F","Voltaje minimo (V)","y = 0.000035x^2 - 0.000519x + 21.463203","x = corriente (A)","Idem","Idem"],
["RAHMAN2014-2F","Voltaje maximo (V)","y = -0.000315x^2 + 0.146061x + 15.818182","x = corriente (A)","Idem","Idem"],
["PALANI2007-RSM","Velocidad de alambre (m/min)","Wf = -6.92 + 0.0860 * I","I = corriente (A)","317L diam 1.2 mm, 176-244 A","Aplicada para estimar WFS en KUMAR2011 y PALANI2006. Marcar como estimacion"],
["BECZKOWSKI2018","Altura de recargue Hn (mm)","Hn = 4.438 - 0.45*x1 - 0.118*x2 + 0.193*x3 - 0.08*x4","Coeficientes codificados","FCAW-S, alambre 2.8 mm alto Cr","La velocidad de recargue (x1) domina"],
["BECZKOWSKI2018","Penetracion Hw (mm)","Hw = 1.419 - 0.009*x1 + 0.009*x2 + 0.066*x3 - 0.001*x4","Coeficientes codificados","Idem","HALLAZGO: todos los coeficientes son despreciables frente a la constante. Ningun factor explica la penetracion"],
["RAZAK2017-1G","MAD por estrato","Ver 01_ESTUDIOS","—","1G, chapa 9mm","Referencia de precision alcanzable: ancho 4-6%, penetracion 8-17%"],
["MORENO2022-MAT","Aporte termico","Q = k * U * Irms / v con k = 0.8","U (V), Irms (A), v (mm/s)","FCAW, referencia ISO/TR 17671-1","FORMULA CANONICA adoptada para todo el corpus"],
["ZHANG2016","Potencia efectiva","P = (1/T) * integral de u(t)*i(t) dt","Senales instantaneas","Arcos fluctuantes y pulsados","Metodo correcto para procesos con arco inestable. Superior al producto de promedios"]]
for r in EQ: ws.append(r)
fmt(ws,1,[22,26,50,30,42,54],"A2",3)

# 09 COBERTURA
ws=wb.create_sheet("09_COBERTURA")
PRIN=[r for r in M if r["conjunto"]=="principal"]
ws.append(["CONTEO POR CONJUNTO"]); ws.append(["conjunto","registros","uso"])
for k,lbl in [("principal","Modelo principal: FCAW con gas, posicion plana, corriente constante"),
              ("pulsado","Subgrupo: corriente pulsada"),("excluido","Subgrupo: autoprotegido, subacuatico, otras posiciones"),
              ("comparativo","Proceso RMD, solo para capitulo comparativo"),("solapado","Duplicados marcados: NO CONTAR")]:
    ws.append([k,sum(1 for r in M if r["conjunto"]==k),lbl])
ws.append([]); ws.append(["COBERTURA DE VARIABLES EN EL CONJUNTO PRINCIPAL (n=%d)"%len(PRIN)])
ws.append(["variable","con_dato","sin_dato","% cobertura","papers que la aportan","apta para modelar"])
for v in ["I_amp","V_arco","OCV_volt","WFS_m_min","TS_mm_s","CTWD_mm","stickout_mm","NPD_mm","angulo_deg",
          "pct_CO2","caudal_L_min","HI_J_mm","A_dep_mm2","WFS_TS","W_mm","R_mm","P_mm","D_pct","AP_mm2","AR_mm2","ZAT_mm","IC_pct","TD_kg_h"]:
    n=sum(1 for r in PRIN if r[v] not in (None,""))
    ps=sorted({r["paper_id"] for r in PRIN if r[v] not in (None,"")})
    apta="SI" if n>=60 else ("LIMITADA" if n>=25 else "NO (n insuficiente)")
    ws.append([v,n,len(PRIN)-n,round(n/len(PRIN)*100,1),", ".join(p.split('-')[0][:11] for p in ps),apta])
ws.append([]); ws.append(["N DISPONIBLE POR RESPUESTA (conjunto principal)"])
ws.append(["respuesta","n","predictores admisibles","modelo recomendado"])
for resp,pred,mod in [("W_mm","I, V, WFS, TS, CTWD/NPD, angulo, pct_CO2","Lineal mixto con efecto de laboratorio"),
 ("R_mm","Idem","Lineal mixto. La respuesta mas estable del corpus"),
 ("P_mm","Idem + covariables de transferencia","Clasificador ordinal por estratos (<1.5 / 1.5-2.5 / >2.5 mm)"),
 ("D_pct","A_dep como eje principal","Hibrido: fisico D=f(A_dep) + residuo estadistico"),
 ("IC_pct","Idem que W y R","Lineal mixto. Adimensional: el mas transferible"),
 ("AP_mm2","Idem","Solo descriptivo: n bajo y CV 15%"),
 ("ZAT_mm","Idem","NO MODELAR: CV de 10-16%")]:
    ws.append([resp,sum(1 for r in PRIN if r[resp] not in (None,"")),pred,mod])
ws.append([]); ws.append(["COBERTURA POR NIVEL DE VARIABLES CATEGORICAS (conjunto principal)"])
ws.append(["variable","nivel","registros","suficiente"])
for var in ["aplicacion","gas_tipo","alambre_clase","metal_base","espesor_mm"]:
    for nivel,cnt in sorted(Counter(str(r[var]) for r in PRIN).items(),key=lambda x:-x[1]):
        ws.append([var,nivel,cnt,"SI" if cnt>=25 else "NO: efecto no estimable con fiabilidad"])
for i,row in enumerate(ws.iter_rows(),1):
    for c in row:
        c.font=AR(True) if (c.column==1 and isinstance(c.value,str) and c.value.isupper() and len(str(c.value))>20) else AR()
        c.alignment=Alignment(vertical='top',wrap_text=True)
for r_ in (2,8,ws.max_row):
    pass
for row in ws.iter_rows():
    if row[0].value in ("conjunto","variable","respuesta"):
        for c in row:
            if c.value is not None: c.font=AR(True,'FFFFFF'); c.fill=HD
for c_,w_ in zip("ABCDEF",[26,26,12,14,52,44]): ws.column_dimensions[c_].width=w_

wb._sheets.sort(key=lambda s: s.title)
wb.save("FCAW_dataset_maestro.xlsx")
print("COMPLETO")
