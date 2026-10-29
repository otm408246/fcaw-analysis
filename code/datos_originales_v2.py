# -*- coding: utf-8 -*-
"""
CAPA 0 v2 - Transcripciones literales de los papers de la carpeta papers_FCAW/nueva
Convencion identica a datos_originales.py: valores VERBATIM, erratas preservadas.
Los ID llevan prefijo N (nuevos) para no chocar con P01-P22.
"""
ORIG2 = {}

# =====================================================================================
# N01  Kannan & Murugan 2006 - JMPT 176:230-239   (160 citas)
# NOTA: existe una publicacion hermana, 'Sensitivity Analysis of FCA Cladding Parameters
#       Using RSM' (Kannan & Murugan), que reporta ESTAS MISMAS 31 corridas.
# =====================================================================================
ORIG2["02_Kannan2006"] = dict(
 cita="Kannan, T.; Murugan, N. (2006). Effect of flux cored arc welding process parameters "
      "on duplex stainless steel clad quality. J. Mater. Process. Technol. 176:230-239.",
 tabla="Tabla 2 (niveles, p.232) y Tabla 3 (matriz de diseno y valores observados)",
 cols=["Trial","I","S","N","T","W mm","P mm","R mm","D %"],
 rows=[
  [ 1,-1,-1,-1,-1,29.50,0.61,4.97, 7.86],[ 2, 1,-1,-1,-1,36.62,0.73,5.00,12.10],
  [ 3,-1, 1,-1,-1,24.20,0.63,4.23,11.35],[ 4, 1, 1,-1,-1,28.00,0.77,4.27,11.98],
  [ 5,-1,-1, 1,-1,30.00,0.57,5.00, 6.54],[ 6, 1,-1, 1,-1,34.98,0.67,5.29, 8.82],
  [ 7,-1, 1, 1,-1,25.59,0.58,4.18, 9.69],[ 8, 1, 1, 1,-1,29.51,0.70,4.20,11.16],
  [ 9,-1,-1,-1, 1,28.34,0.73,5.00, 8.97],[10, 1,-1,-1, 1,34.50,0.97,5.10,13.75],
  [11,-1, 1,-1, 1,24.00,1.00,4.00,18.52],[12, 1, 1,-1, 1,27.80,1.20,4.34,20.58],
  [13,-1,-1, 1, 1,29.26,0.60,5.08, 7.46],[14, 1,-1, 1, 1,34.80,0.80,5.28, 9.14],
  [15,-1, 1, 1, 1,25.30,0.97,4.00,18.00],[16, 1, 1, 1, 1,27.70,1.00,4.20,14.80],
  [17,-2, 0, 0, 0,20.15,0.40,3.98, 5.86],[18, 2, 0, 0, 0,31.00,1.07,4.90,16.48],
  [19, 0,-2, 0, 0,39.53,0.70,5.68, 5.31],[20, 0, 2, 0, 0,23.10,1.00,3.63,17.35],
  [21, 0, 0,-2, 0,25.10,0.83,4.32,11.71],[22, 0, 0, 2, 0,28.00,0.63,4.81, 9.01],
  [23, 0, 0, 0,-2,30.20,0.56,4.17,10.54],[24, 0, 0, 0, 2,26.00,0.87,4.87,13.98],
  [25, 0, 0, 0, 0,27.88,0.70,4.55,10.33],[26, 0, 0, 0, 0,29.42,0.83,4.34,13.60],
  [27, 0, 0, 0, 0,28.00,0.77,4.50,10.73],[28, 0, 0, 0, 0,27.90,0.87,4.50,11.71],
  [29, 0, 0, 0, 0,29.20,0.83,4.32,13.76],[30, 0, 0, 0, 0,27.80,0.79,4.58,10.99],
  [31, 0, 0, 0, 0,27.80,0.80,4.57,10.67]],
 niveles=("CCD rotable alfa=2 (4 factores: 2^4=16 factorial + 8 estrella + 7 centrales = 31). "
          "I(A) 200/225/250/275/300 | S(cm/min) 20/30/40/50/60 | N(mm) 22/24/26/28/30 | "
          "T(grados desde vertical) 20/15/10/05/00  <-- ORDEN INVERTIDO: -2=20deg, +2=0deg. "
          "Alambre 2209 duplex Ø1.2mm sobre acero estructural IS2062. SIN VOLTAJE, SIN WFS. "
          "Anchos de 20-40 mm => cordon OSCILADO (tejido), no stringer."),
)

# =====================================================================================
# DESCARTADO  Mostafa & Khajavi 2006 - J. Achiev. Mater. Manuf. Eng. 16(1-2)
#   "Optimisation of welding parameters for weld penetration in FCAW"
#   CCD rotable 5 factores (I,S,V,N,angulo), 32 corridas. UNICO del lote con VOLTAJE.
#   NO PUBLICA LOS VALORES OBSERVADOS: solo la matriz codificada y los coeficientes.
#   Modelo: P = 3.531 +0.333I -0.116S +0.200ang +0.112(IS) -0.175(SV) +0.162(VN)
#                  +0.066V -0.058N     (V y N marcados como no significativos)
#   Niveles: I 250-350 A | S 35-55 cm/min | V 27-35 V | N 15-25 mm | ang 90-120 deg
#   -> 0 corridas. Sirve solo como evidencia de "publica modelo, no publica datos".
# =====================================================================================

# =====================================================================================
# N02  Balan, A.V. et al. 2018 - Mater. Res. Express (aceptado)
#      "Optimization of cladding parameters for resisting corrosion on low carbon
#       steels using simulated annealing algorithm"
# =====================================================================================
ORIG2["19_Balan2018"] = dict(
 cita="Balan, A.V. et al. (2018). Optimization of cladding parameters for resisting corrosion "
      "on low carbon steels using simulated annealing algorithm. Mater. Res. Express. "
      "doi:10.1088/2053-1591/aab7cb",
 tabla="Tabla 2 (niveles) y Tabla 3 (matriz de diseno y geometria observada)",
 cols=["Trial","F","S","N","T","W mm","R mm","P mm","% D","FN"],
 rows=[
  [ 1,-1,-1,-1,-1, 8.39,4.13,0.37,5.48,28.01],[ 2, 1,-1,-1,-1, 9.77,4.62,0.42,6.48,27.38],
  [ 3,-1, 1,-1,-1, 8.05,3.38,0.38,6.45,27.00],[ 4, 1, 1,-1,-1, 8.43,3.79,0.44,6.68,25.24],
  [ 5,-1,-1, 1,-1, 8.52,4.27,0.33,4.72,29.70],[ 6, 1,-1, 1,-1,10.10,4.78,0.38,5.38,28.33],
  [ 7,-1, 1, 1,-1, 8.50,3.69,0.34,6.25,28.87],[ 8, 1, 1, 1,-1, 9.00,3.93,0.38,6.33,26.05],
  [ 9,-1,-1,-1, 1, 8.70,3.96,0.33,5.99,27.83],[10, 1,-1,-1, 1,10.12,4.16,0.41,6.75,25.79],
  [11,-1, 1,-1, 1, 8.52,3.37,0.34,6.78,26.30],[12, 1, 1,-1, 1, 8.61,3.62,0.43,6.88,24.69],
  [13,-1,-1, 1, 1, 8.93,4.00,0.32,5.66,28.49],[14, 1,-1, 1, 1,10.29,4.69,0.36,5.87,25.79],
  [15,-1, 1, 1, 1, 8.67,3.51,0.33,6.48,27.73],[16, 1, 1, 1, 1, 9.61,3.87,0.36,6.70,25.09],
  [17,-2, 0, 0, 0, 7.72,3.75,0.33,6.20,28.84],[18, 2, 0, 0, 0,10.00,4.10,0.55,7.62,24.20],
  [19, 0,-2, 0, 0,10.13,4.84,0.42,4.96,27.53],[20, 0, 2, 0, 0, 8.17,3.41,0.50,8.77,25.08],
  [21, 0, 0,-2, 0, 7.75,3.16,0.83,7.08,25.86],[22, 0, 0, 2, 0, 9.61,4.10,0.27,5.39,28.04],
  [23, 0, 0, 0,-2, 8.93,3.77,0.38,4.03,28.33],[24, 0, 0, 0, 2, 9.79,3.53,0.18,5.58,26.78],
  [25, 0, 0, 0, 0, 8.44,3.88,0.71,5.48,27.54],[26, 0, 0, 0, 0, 7.87,3.87,0.71,5.88,26.68],
  [27, 0, 0, 0, 0, 8.45,4.28,0.71,5.08,27.61],[28, 0, 0, 0, 0, 8.44,3.87,0.71,5.24,26.62],
  [29, 0, 0, 0, 0, 8.45,3.87,0.53,5.01,27.13],[30, 0, 0, 0, 0, 8.45,3.87,0.71,5.05,27.88],
  [31, 0, 0, 0, 0, 8.44,3.87,0.71,5.08,27.24]],
 niveles=("CCD alfa=2, 4 factores, 16 factorial + 8 estrella + 7 centrales = 31. "
          "F=wire feed (inch/min) 150/175/200/225/250 -> 3.81/4.45/5.08/5.72/6.35 m/min | "
          "S(mm/min) 100/120/140/160/180 | N(mm) 16/18/20/22/24 | T(gun angle deg) 90/100/110/120/130. "
          "Alambre tubular FC2507 super duplex Ø1.2mm sobre IS2062. Gas 80%Ar-20%CO2. SIN VOLTAJE. "
          "NOTA 1: razon A_dep/(2/3*W*R) = 1.45, extremo ALTO del rango del corpus (0.44-1.45, "
          "mediana 1.06) pero DENTRO de lo normal; NO es incoherencia. "
          "NOTA 2: IC = R/W = 36-51%. Senthilkumar reporta 45.8% y 27.3% con el mismo alambre "
          "en dos papers distintos: contradiccion abierta, ver H-032. "
          "BANDERA: los 7 'centrales' repiten valores identicos (R=3.87 cinco veces, "
          "P=0.71 cinco veces, W=8.44/8.45 cinco veces) -> NO son replicas independientes, "
          "NO usar para el piso de error."),
)

# =====================================================================================
# N03  Senthilkumar, B.; Kannan, T. 2014 - Measurement (Elsevier), MEASUR 3126
#      "Effect of FCAW process parameters on bead geometry in super duplex
#       stainless steel claddings"   doi:10.1016/j.measurement.2014.11.007
#  UNICO del lote con VOLTAJE Y VELOCIDAD DE ALAMBRE simultaneos.
#  RFF = altura de refuerzo / ancho  -> IC_pct = RFF*100
#  PFF = profundidad penetracion / ancho -> W_P = 1/PFF
# =====================================================================================
ORIG2["12_Senthilkumar2014"] = dict(
 cita="Senthilkumar, B.; Kannan, T. (2014). Effect of Flux Cored Arc Welding process parameters "
      "on bead geometry in super duplex stainless steel claddings. Measurement 62:120-128. "
      "doi:10.1016/j.measurement.2014.11.007",
 tabla="Tabla 2 (niveles y codificacion) y Tabla 3 (matriz de diseno con respuestas)",
 cols=["Exp","V (V)","WFS (m/min)","TS (m/min)","NPD (m)","angulo (deg)","RFF","PFF","CA (deg)"],
 rows=[
  [ 1,24,5.715,0.14,0.017, 80,0.479,0.025, 71.63],[ 2,24,5.715,0.14,0.021,100,0.483,0.030, 75.25],
  [ 3,24,5.715,0.18,0.017,100,0.439,0.048, 95.38],[ 4,24,5.715,0.18,0.021, 80,0.506,0.038, 92.13],
  [ 5,24,6.985,0.14,0.017,100,0.438,0.029, 81.00],[ 6,24,6.985,0.14,0.021, 80,0.517,0.032, 72.88],
  [ 7,24,6.985,0.18,0.017, 80,0.445,0.043, 80.38],[ 8,24,6.985,0.18,0.021,100,0.462,0.041, 86.63],
  [ 9,28,5.715,0.14,0.017,100,0.419,0.013, 78.63],[10,28,5.715,0.14,0.021, 80,0.539,0.029, 77.00],
  [11,28,5.715,0.18,0.017, 80,0.465,0.060, 96.13],[12,28,5.715,0.18,0.021,100,0.428,0.045, 96.50],
  [13,28,6.985,0.14,0.017, 80,0.421,0.033, 88.25],[14,28,6.985,0.14,0.021,100,0.446,0.011, 68.13],
  [15,28,6.985,0.18,0.017,100,0.369,0.029, 99.00],[16,28,6.985,0.18,0.021, 80,0.451,0.044, 87.25],
  [17,22,6.320,0.16,0.019, 90,0.694,0.038, 66.88],[18,30,6.320,0.16,0.019, 90,0.446,0.036, 81.50],
  [19,26,5.080,0.16,0.019, 90,0.510,0.054, 87.75],[20,26,7.620,0.16,0.019, 90,0.404,0.026, 83.13],
  [21,26,6.320,0.12,0.019, 90,0.461,0.013, 64.63],[22,26,6.320,0.20,0.019, 90,0.414,0.060, 99.88],
  [23,26,6.320,0.16,0.015, 90,0.370,0.033, 90.63],[24,26,6.320,0.16,0.023, 90,0.452,0.029, 83.25],
  [25,26,6.320,0.16,0.019, 70,0.484,0.036, 76.75],[26,26,6.320,0.16,0.019,110,0.426,0.028, 78.13],
  [27,26,6.320,0.16,0.019, 90,0.464,0.031, 87.75],[28,26,6.320,0.16,0.019, 90,0.408,0.031,100.00],
  [29,26,6.320,0.16,0.019, 90,0.470,0.041, 96.00],[30,26,6.320,0.16,0.019, 90,0.426,0.038, 98.00]],
 niveles=("CCD rotable 5 factores: 16 factorial + 10 estrella + 6 centrales = 32 (30 legibles). "
          "V(V) 22/24/26/28/30 | WFS(m/min) 5.08/5.715/6.32/6.985/7.62 | TS(m/min) 0.12/0.14/0.16/0.18/0.20 | "
          "NPD(m) 0.015/0.017/0.019/0.021/0.023 | angulo(deg) 70/80/90/100/110. "
          "Alambre tubular super duplex 2507 Ø1.2mm sobre acero estructural bajo carbono. Gas 80%Ar-20%CO2. "
          "SIN CORRIENTE -> HI no calculable pese a tener voltaje. Los autores declaran HI acotado a 0.5-1.5 kJ/mm. "
          "Valores dados en unidades SI (m, m/min); convertidos al estandarizar."),
)

# =====================================================================================
# N04  Nunes, M.M.; Gomes, J.H.F.; Brito, T.G.; Renzetti, R.A. (2020)
#      Materials Research 23(6):e20200356   doi:10.1590/1980-5373-MR-2020-0356
#
#  *** NO APORTA CORRIDAS NUEVAS ***  Matriz codificada IDENTICA 31/31 a P11_GOMES2012,
#  mismos niveles, mismo laboratorio (UNIFEI), mismos materiales (E316LT1-1/4 sobre
#  AISI 1020, 75%Ar-25%CO2, Ø1.2mm). Es la MISMA campana experimental: Gomes 2012
#  publico la geometria del cordon; Nunes 2020 publica la corrosion de esas probetas.
#
#  *** SI APORTA DOS RESPUESTAS NUEVAS *** sobre 31 corridas que ya estan en la base:
#     DOS  = grado de sensibilizacion (razon Ir/Ia, DLEPR segun ASTM G108)
#     Epit = potencial de picado (mV)
#  Se ANEXAN a P11_GOMES2012 por numero de corrida (regla: union de variables).
#  Corrida 27: Epit marcado como atipico y eliminado por los autores.
# =====================================================================================
ANEXO_GOMES2012 = dict(
 cita="Nunes, M.M.; Gomes, J.H.F.; Brito, T.G.; Renzetti, R.A. (2020). Effect of Flux Cored arc "
      "Welding Process Parameters on Corrosion Resistance of Austenitic Stainless Steel Claddings. "
      "Mater. Res. 23(6):e20200356.",
 tabla="Tabla 3 (matriz de diseno y respuestas)",
 anexa_a="P11_GOMES2012",
 cols=["Run","DOS","Epit mV"],
 rows=[[1,0.138,193],[2,0.094,165],[3,0.383,160],[4,0.698,180],[5,0.876,145],[6,0.491,136],
  [7,0.870,155],[8,0.891,126],[9,0.005,255],[10,0.002,266],[11,0.052,204],[12,0.005,242],
  [13,0.095,177],[14,0.004,259],[15,0.518,155],[16,0.169,165],[17,0.318,218],[18,0.118,190],
  [19,0.081,221],[20,0.876,144],[21,0.002,275],[22,0.689,128],[23,0.893,138],[24,0.001,260],
  [25,0.369,223],[26,0.375,226],[27,0.287,"elim"],[28,0.236,238],[29,0.185,249],[30,0.173,219],
  [31,0.180,228]],
 extra=("Dilucion medida por los autores solo en 2 probetas: corrida 21 D=18.6%, corrida 8 D=41.1%. "
        "FN Ferritoscopio: corrida 21 = 3.38, corrida 8 = 52.6. HV: 159.1 vs 351.7."),
)

# =====================================================================================
# N05  Singh, V.; Chandrasekaran, M.; Samanta, S. (2021)
#      AIP Conf. Proc. 2317:050021  doi:10.1063/5.0036198
#      "Study of weld bead characteristics and optimization during FCAW of AISI 201LN"
#  UNICO del corpus con GAS 100% CO2 puro sobre inoxidable, y unico con base AISI 201LN.
#  WPSF = W/P ; WRFF = W/R  (verificado: desviacion max 0.005 en las 31 corridas)
#  NTD = nozzle to work distance (equivale a NPD).
# =====================================================================================
ORIG2["23_Singh2021"] = dict(
 cita="Singh, V.; Chandrasekaran, M.; Samanta, S. (2021). Study of weld bead characteristics "
      "and optimization during FCAW of AISI 201LN. AIP Conf. Proc. 2317:050021. "
      "doi:10.1063/5.0036198",
 tabla="TABLE 1. Experimental condition (matriz en valores reales + respuestas)",
 cols=["Std","Orden","WFR m/min","V (V)","S mm/min","NTD mm","P mm","R mm","W mm","WPSF","WRFF"],
 rows=[
  [ 6, 1,8,20,280,10,2.23,3.43, 9.37, 4.20,2.73],[26, 2,7,22,250,15,1.48,3.64, 8.75, 5.91,2.40],
  [24, 3,7,22,250,25,0.82,3.65, 7.52, 9.17,2.06],[28, 4,7,22,250,15,1.25,3.78, 8.99, 7.19,2.38],
  [ 5, 5,6,20,280,10,0.99,3.52, 7.16, 7.23,2.03],[ 9, 6,6,20,220,20,0.78,3.83, 7.20, 9.23,1.88],
  [ 3, 7,6,24,220,10,1.58,3.03,10.05, 6.36,3.32],[ 8, 8,8,24,280,10,2.49,3.23,10.68, 4.29,3.31],
  [16, 9,8,24,280,20,1.54,3.62, 9.46, 6.14,2.61],[ 1,10,6,20,220,10,1.65,3.85, 8.01, 4.85,2.08],
  [17,11,5,22,250,15,0.72,3.02, 7.38,10.25,2.44],[27,12,7,22,250,15,1.66,4.01, 8.86, 5.34,2.21],
  [11,13,6,24,220,20,0.89,3.18, 9.27,10.42,2.92],[29,14,7,22,250,15,1.32,3.55, 8.27, 6.27,2.33],
  [15,15,6,24,280,20,0.82,2.68, 8.92,10.88,3.33],[25,16,7,22,250,15,1.56,3.79, 8.33, 5.34,2.20],
  [22,17,7,22,310,15,1.16,3.48, 8.62, 7.43,2.48],[18,18,9,22,250,15,2.88,3.63,10.03, 3.48,2.76],
  [10,19,8,20,220,20,1.83,3.31, 8.94, 4.89,2.70],[13,20,6,20,280,20,0.81,3.45, 6.59, 8.14,1.91],
  [ 4,21,8,24,220,10,3.45,3.47,10.76, 3.12,3.10],[21,22,7,22,190,15,2.06,3.69,10.38, 5.04,2.81],
  [ 7,23,6,24,280,10,1.48,2.52,10.18, 6.88,4.04],[19,24,7,18,250,15,1.44,3.42, 8.17, 5.67,2.39],
  [31,25,7,22,250,15,1.45,3.86, 8.56, 5.90,2.22],[23,26,7,22,250, 5,3.53,3.31, 8.91, 2.52,2.69],
  [ 2,27,8,20,220,10,3.53,3.81,10.47, 2.97,2.75],[20,28,7,26,250,15,1.39,2.75,12.08, 8.69,4.39],
  [14,29,8,20,280,20,1.19,3.64, 7.47, 6.28,2.05],[30,30,7,22,250,15,1.57,3.53, 9.00, 5.73,2.55],
  [12,31,8,24,220,20,1.69,3.69,10.24, 6.06,2.78]],
 niveles=("CCD alfa=2: 16 factorial + 8 estrella + 7 centrales = 31. Valores REALES en la tabla. "
          "WFR(m/min) 5/6/7/8/9 | V(V) 18/20/22/24/26 | S(mm/min) 190/220/250/280/310 | NTD(mm) 5/10/15/20/25. "
          "Centrales = std 25-31 (7,22,250,15). Base AISI 201LN austenitico bajo niquel. "
          "Alambre tubular Ø1.2mm, CLASE NO ESPECIFICADA en el texto extraible -> phi=0.81 por defecto (bandera). "
          "GAS 100% CO2 puro a 18 L/min: los autores lo contrastan explicitamente frente al Ar+CO2 habitual. "
          "NO reporta dilucion ni areas. SIN CORRIENTE -> HI no calculable pese a tener voltaje."),
)

# =====================================================================================
# N06  Katherasan, D.; Elias, J.V.; Sathiya, P.; Noorul Haq, A.
#      "Modeling and optimization of flux cored arc welding by genetic algorithm
#       and simulated annealing algorithm"  (Multidiscipline Modeling in Mat. & Str.)
#
#  *** NO APORTA CORRIDAS NUEVAS ***
#  Mismo L25 Taguchi, mismos autores, mismo laboratorio (NIT Tiruchirappalli),
#  mismos materiales (316L(N) 100x50x8mm, alambre 316LT Ø1.2mm, Ar 15 lpm,
#  stick-out 15mm, robot ABB MIG-500) y MISMOS VALORES que P22_KATHERASAN2012
#  ("Simulation and parameter optimization of FCAW using ANN and PSO").
#  Verificacion: 22/22 filas legibles identicas en (W, R, P).
#  Cambia unicamente el algoritmo de optimizacion aplicado a los mismos datos:
#     P22 -> ANN + PSO      |      N06 -> algoritmo genetico + recocido simulado
#  Se registra como CITA ALTERNA de P22, no como estudio independiente.
# =====================================================================================
CITA_ALTERNA_KATHERASAN = dict(
 de="P22_KATHERASAN2012",
 cita="Katherasan, D.; Elias, J.V.; Sathiya, P.; Noorul Haq, A. Modeling and optimization of "
      "flux cored arc welding by genetic algorithm and simulated annealing algorithm. "
      "Multidiscip. Model. Mater. Struct.",
 nota="Mismos 25 experimentos L25 que P22. Solo cambia el optimizador (GA+SA vs ANN+PSO).",
)

# =====================================================================================
# N07  Odhiambo, V.O.; Kihiu, J.M.; Mose, B.R.; Odhiambo, J.G. (2025)
#      J. Sustain. Res. Eng. 8(4):250-268  (JKUAT, Kenia)
#      "Optimization of FCAW Parameters using ANN for ASTM A335 Grade B -
#       API 5L Schedule 40 Pipes"
#
#  UNICO del corpus con I, V y TS simultaneos -> HI calculable directo.
#  VERIFICACION CLAVE: eta implicito = 0.7993 (rango 0.787-0.804) en las 22 corridas
#  -> confirma de forma INDEPENDIENTE el k=0.80 de ISO/TR 17671-1 que ya usabamos.
#  Taguchi L27 declarado; la Tabla 9 publica solo 22 corridas (faltan 5).
# =====================================================================================
ORIG2["31_Odhiambo2025"] = dict(
 cita="Odhiambo, V.O.; Kihiu, J.M.; Mose, B.R.; Odhiambo, J.G. (2025). Optimization of Flux "
      "Cored Arc Welding Parameters using Artificial Neural Networks for ASTM A335 Grade B - "
      "API 5L Schedule 40 Pipes. J. Sustain. Res. Eng. 8(4):250-268.",
 tabla="Tabla 4 (niveles) y Tabla 9 (Input Data for Optimization = resultados Taguchi)",
 cols=["Run","V (V)","I (A)","S mm/min","angulo deg","CTWD mm","HI kJ/mm","DoP mm","HAZ mm"],
 rows=[
  [ 1,15, 60, 70, 15,3,0.62,6.04,1.44],[ 2,15, 60,120, 60,6,0.36,5.08,0.48],
  [ 3,15, 60,170,105,9,0.25,4.60,0.17],[ 4,15,130, 70, 60,9,1.34,7.10,3.20],
  [ 5,15,130,120,105,3,0.78,6.42,1.82],[ 6,15,130,170, 15,6,0.55,5.66,1.06],
  [ 7,15,200, 70,105,6,2.06,6.14,3.70],[ 8,15,200,120, 15,9,1.20,7.46,3.00],
  [ 9,15,200,170, 60,3,0.85,6.83,2.35],[10,20, 60, 70,105,9,0.82,6.61,2.13],
  [11,20, 60,120, 15,3,0.48,5.45,0.85],[12,20, 60,170, 60,6,0.34,4.83,0.23],
  [13,20,130, 70, 15,6,1.78,6.56,3.50],[14,20,130,120, 60,9,1.04,7.48,3.00],
  [15,20,130,170,105,3,0.73,6.22,1.62],[16,20,200, 70, 60,3,2.74,5.64,3.90],
  [17,20,200,120,105,6,1.60,6.78,3.40],[18,20,200,170, 15,9,1.13,7.56,2.90],
  [19,25, 60, 70, 60,6,1.03,7.24,2.76],[20,25, 60,120,105,9,0.60,5.88,1.28],
  [21,25, 60,170, 15,3,0.42,5.24,0.64],[22,25,130, 70,105,3,2.23,5.92,3.80]],
 niveles=("Taguchi L27, 5 factores x 3 niveles; SOLO 22 corridas publicadas (faltan 5). "
          "V(V) 15/20/25 | I(A) 60/130/200 | S(mm/min) 70/120/170 | angulo(deg) 15/60/105 | CTWD(mm) 3/6/9. "
          "Tubo ASTM A335 Gr.B / API 5L Sch40: DI 128.2mm, pared 7.55mm. Maquina Prescott MMA/MIG/TIG 200. "
          "BANDERA 1 - DoP NO ES COMPARABLE con P_mm del resto del corpus: 4.6-7.56 mm sobre pared de "
          "7.55 mm en junta a tope con bisel; no es penetracion de cordon sobre placa (BOP). "
          "BANDERA 2 - corr(HI,DoP) = +0.33 solamente: el aporte termico NO explica la penetracion "
          "(5o caso documentado). En cambio corr(HI,HAZ) = +0.91, fuerte y coherente. "
          "BANDERA 3 - CTWD de 3/6/9 mm es anomalo para FCAW (habitual 15-25 mm). "
          "BANDERA 4 - los autores reportan R=1.000 en entrenamiento, validacion Y prueba de la RNA: "
          "ajuste perfecto en las tres fases = sobreajuste, no desempeno. "
          "NO reporta ancho ni refuerzo -> solo aporta DoP y HAZ."),
)

# =====================================================================================
# N08  Yadav, P.; Khanna, P. (2022) - Materials Today: Proceedings (NSUT New Delhi)
#      "Effect of input parameters on weld bead geometry and weld dilution for weld
#       surfacing of flux cored 308L stainless steel on low carbon steel"
#
#  Matriz transcrita de la Tabla 2 del PDF original (el texto extraido perdia los
#  signos negativos; se recuperaron de la tabla impresa).
#  ORDEN NO-YATES: el factor C alterna mas rapido, A el mas lento.
#  VALIDADO contra el ANOVA del propio paper (respuesta ancho):
#     SS modelo  calculado 63.12  vs publicado 62.93   (+0.3%)
#     SSE        calculado  4.73  vs publicado  4.92   (-3.9%)
#     AC 0.819/0.807 | BC 0.106/0.129 | A2 4.38/4.44 | C2 1.50/1.40
#     (las diferencias por termino lineal son convencion de tipo de SS)
#  -> LAS 21 CORRIDAS SON UTILIZABLES.
#
#  CORREGIDO (H-039): la unidad de la alimentacion esta mal rotulada en el paper.
#    Leida como mm/min da A_dep/(2/3*W*R) = 0.15, es decir 2.9x por debajo del minimo
#    del corpus (0.44): fisicamente imposible. Leida como cm/min da 1.50, dentro del
#    rango observado (0.44-1.45, mediana 1.06). Se adopta cm/min.
#  BANDERA (H-040): niveles +1 y +2 no equiespaciados (1331.2 y 1750 frente a 1262.4
#    y 1578 esperados). El lado bajo si cuadra exacto.
#  BANDERA (nivel inferido): el 5o nivel de velocidad de avance quedo cortado en el
#    PDF; 370 mm/min es extrapolado del paso. Afecta solo a la corrida 14.
# =====================================================================================
ORIG2["26_Yadav2022"] = dict(
 cita="Yadav, P.; Khanna, P. (2022). Effect of input parameters on weld bead geometry and weld "
      "dilution for weld surfacing of flux cored 308L stainless steel on low carbon steel. "
      "Mater. Today Proc. doi:10.1016/j.matpr.2022.04.412",
 tabla="Tabla 1 (niveles) y Tabla 2 (Design Matrix)",
 cols=["Specimen","A","B","C","Dilution %","Width mm","height mm","penetration mm"],
 rows=[
  [ 1,-1,-1,-1,23.73,12.62,2.73,1.02],[ 2,-1,-1, 1,29.81, 9.90,2.47,1.22],
  [ 3,-1, 1,-1,10.54,14.15,3.27,0.86],[ 4,-1, 1, 1,30.06,11.63,2.65,1.76],
  [ 5, 1,-1,-1,27.33,13.03,2.28,1.67],[ 6, 1,-1, 1,35.76,11.33,2.09,2.09],
  [ 7, 1, 1,-1,21.57,15.07,2.98,0.99],[ 8, 1, 1, 1,39.12,14.09,2.88,1.97],
  [ 9,-2, 0, 0,15.72, 8.65,3.85,1.35],[10, 2, 0, 0,40.58,14.40,2.13,1.78],
  [11, 0,-2, 0,32.18,10.69,2.15,1.32],[12, 0, 2, 0,26.95,15.04,3.04,1.12],
  [13, 0, 0,-2,16.69,16.58,3.07,0.85],[14, 0, 0, 2,28.14,11.64,2.10,1.72],
  [15, 0, 0, 0,25.23,12.77,2.33,1.34],[16, 0, 0, 0,31.63,12.56,2.48,1.81],
  [17, 0, 0, 0,29.73,12.48,2.87,1.59],[18, 0, 0, 0,27.39,13.39,2.41,1.66],
  [19, 0, 0, 0,34.75,12.96,2.82,1.65],[20, 0, 0, 0,32.24,13.47,2.19,1.79],
  [21, 0, 0, 0,28.53,14.00,2.73,1.27]],
 niveles=("CCD rotable alfa=2: 2^3=8 factorial + 6 estrella + 7 centrales = 21, orden aleatorizado. "
          "A=Voltaje(V) 18/20/22/24/26 | B=Feed rate: el paper lo rotula mm/min (315.6/631.2/946.8/1331.2/1750) pero la magnitud "
          "solo es coherente en cm/min; en la maestra va como 3156/6312/9468/13312/17500 mm/min (ver H-039). "
          "| C=Velocidad avance(mm/min) 152.2/206.7/260.8/315.7/[370 INFERIDO]. "
          "Alambre tubular 308L sobre acero al carbono, recargue. SIN CORRIENTE -> HI no calculable."),
)

# =====================================================================================
# N09  Senthilkumar, B.; Kannan, T.; Madesh, R. (2015)
#      Int. J. Adv. Manuf. Technol.  doi:10.1007/s00170-015-7411-9
#      "Optimization of flux-cored arc welding process parameters by using
#       genetic algorithm"   (Taguchi L9, super duplex cladding)
#
#  MISMO GRUPO que N03 (Senthilkumar & Kannan). Rangos de parametros solapados,
#  pero DISENO DISTINTO (L9 vs CCD) y sin el factor angulo de antorcha.
#  Coincidencia parcial: L9 R2 (22 V, 6.35 m/min, 0.16 m/min, 0.019 m) queda a
#  0.03 m/min de N03 R17 (22, 6.32, 0.16, 0.019, 90 deg) -> condiciones casi iguales.
#
#  *** BANDERA MAYOR - CONTRADICCION INTERNA DEL MISMO LABORATORIO ***
#  Indice de convexidad IC = R/W:
#     N03 (CCD, alambre 2507)      IC = 36.9-69.4 %   media 45.8
#     N09 (L9, alambre E2594T0-4)  IC = 17.3-42.7 %   media 27.3   -> factor 1.7x
#  En la condicion casi coincidente: N03 R17 IC=69.4 % vs N09 R2 IC=37.4 % (1.9x).
#  Ambos papers declaran la misma definicion (altura de refuerzo / ancho de cordon).
#  Esto MATIZA el hallazgo previo de que el IC alto era caracteristico del 2507:
#     Balan2018 (FC2507)      media 44.5 %
#     Senthilkumar2014 (2507) media 45.8 %
#     Senthilkumar2015 (2594) media 27.3 %   <- el mismo autor, la mitad
#  Queda como CONTRADICCION ABIERTA, no como propiedad del alambre.
# =====================================================================================
ORIG2["17_Senthilkumar2015"] = dict(
 cita="Senthilkumar, B.; Kannan, T.; Madesh, R. (2015). Optimization of flux-cored arc welding "
      "process parameters by using genetic algorithm. Int. J. Adv. Manuf. Technol.",
 tabla="Tabla 2 (niveles y codificacion) y Tabla 3 (parametros sin codificar + respuestas)",
 cols=["Ex.No","V (V)","WFS (m/min)","TS (m/min)","NPD (m)","W mm","H mm","FN promedio"],
 rows=[
  [1,22,5.08,0.12,0.015,21.63,5.60,27.89],[2,22,6.35,0.16,0.019,17.46,6.53,29.60],
  [3,22,7.62,0.20,0.023,16.70,7.13,25.57],[4,26,5.08,0.16,0.023,19.70,5.42,27.93],
  [5,26,6.35,0.20,0.015,22.46,4.98,30.47],[6,26,7.62,0.12,0.019,27.64,7.08,29.08],
  [7,30,5.08,0.20,0.019,18.11,4.29,28.32],[8,30,6.35,0.12,0.023,26.43,6.18,28.66],
  [9,30,7.62,0.16,0.015,29.17,5.06,28.80]],
 niveles=("Taguchi L9, 4 factores x 3 niveles, valores SIN CODIFICAR en la tabla. "
          "V(V) 22/26/30 | WFS(m/min) 5.08/6.35/7.62 | TS(m/min) 0.12/0.16/0.20 | NPD(m) 0.015/0.019/0.023. "
          "Alambre tubular E2594T0-4 super duplex sobre acero al carbono. Gas 80%Ar-20%CO2. "
          "Recargue con cordon ancho (W 16.7-29.2 mm) => OSCILADO, no stringer. "
          "SIN CORRIENTE -> HI no calculable. NO reporta penetracion ni dilucion. "
          "OJO: el nivel central de WFS es 6.35 aqui y 6.32 en N03, mismo laboratorio."),
)

# =====================================================================================
# N10  Aloraier, A.; Ikpe, A.E.; Aladwani, H.; Almashmoum, E. (2025)
#      J. Mech. Behav. Mater.  doi:10.1515/jmbm-2025-0067
#      "Analysis of the combined effects of preheating and welding wire feed rates on
#       the FCAW bead geometric characteristics of 1020 steel using fuzzy logic"
#
#  *** EL PAPER MAS COMPLETO DE TODO EL CORPUS ***  Unico con V, I, TS, WFS,
#  temperatura de precalentamiento, aporte termico Y geometria simultaneos.
#  Unico con PRECALENTAMIENTO como factor (llena la columna temp_precal_C).
#
#  VERIFICACION eta: 0.8014 medio (rango 0.795-0.807) en las 12 corridas
#  -> SEGUNDA confirmacion independiente del k=0.80 de ISO/TR 17671-1
#     (la primera fue N07_ODHIAMBO2025 con eta=0.7993).
#
#  BANDERA 1: corridas 10 y 11 (H3S1 vs H3S2). Duplican corriente (73->145 A) y
#    alimentacion (2.5->5.0 m/min) pero devuelven geometria identica a 0.02 mm
#    (W 6.88/6.90, R 1.84/1.85, P 0.93/0.95, ZAT 9.06/9.12). Fisicamente implausible;
#    tiene toda la apariencia de una fila duplicada por error. NO usar ese par para
#    estimar efectos de alimentacion.
#  BANDERA 2: corrida 4 (H1S1) tiene R=4.12 mm frente a 1.51-2.41 en las otras once,
#    con la corriente mas baja del conjunto (74 A). Atipico; A_dep/geometria = 0.36
#    cuando el resto va de 0.77 a 1.87.
# =====================================================================================
ORIG2["30_Aloraier2025"] = dict(
 cita="Aloraier, A.; Ikpe, A.E.; Aladwani, H.; Almashmoum, E. (2025). Analysis of the combined "
      "effects of preheating and welding wire feed rates on the FCAW bead geometric "
      "characteristics of 1020 steel using fuzzy logic-based prediction models. "
      "J. Mech. Behav. Mater. doi:10.1515/jmbm-2025-0067",
 tabla="Tabla 2 (notaciones), Tabla 3 (parametros de entrada), Tabla 4 (geometria y ZAT)",
 cols=["Sample","Plate","V (V)","I (A)","TS mm/s","HI J/mm",
       "W mm","R mm","P mm","ZAT ancho mm","ZAT alto mm"],
 rows=[
  [ 1,"H0S1",20.2, 71,3.2,359, 5.22,1.83,0.38, 6.87,1.48],
  [ 2,"H0S2",23.0,151,5.3,521,10.45,1.77,1.20,11.58,1.82],
  [ 3,"H0S3",28.0,246,8.0,689,11.79,1.69,2.65,13.86,1.57],
  [ 4,"H1S1",20.2, 74,3.1,389,12.35,4.12,1.11,15.86,3.56],
  [ 5,"H1S2",23.0,149,4.6,600,11.14,1.92,1.10,13.61,2.93],
  [ 6,"H1S3",28.7,239,7.3,755,11.42,1.58,2.20,14.29,2.45],
  [ 7,"H2S1",20.0, 75,3.5,345, 5.40,1.66,0.47, 7.56,2.24],
  [ 8,"H2S2",23.0,150,4.2,656, 9.63,1.51,1.31,12.20,2.76],
  [ 9,"H2S3",28.7,226,7.6,681,12.91,2.11,1.93,15.07,2.22],
  [10,"H3S1",20.2, 73,4.0,295, 6.88,1.84,0.93, 9.06,2.12],
  [11,"H3S2",22.7,145,6.7,395, 6.90,1.85,0.95, 9.12,2.20],
  [12,"H3S3",28.7,230,9.4,561,13.13,2.41,2.25,15.48,2.72]],
 niveles=("Factorial completo 4x3 = 12 corridas, cordon sobre placa (BOP), sin replicas. "
          "Precalentamiento H0=ambiente / H1=100 / H2=150 / H3=200 grados C. "
          "Alimentacion S1=2.5 / S2=5.0 / S3=10.0 m/min. "
          "Alambre E71T-1C rutilico Ø1.2mm sobre AISI 1020 bajo carbono. "
          "V, I y TS se MIDIERON por corrida (no son niveles nominales fijos): "
          "V 20.0-28.7 | I 71-246 A | TS 3.1-9.4 mm/s | HI 295-755 J/mm. "
          "SIN REPLICAS -> no aporta al piso de error."),
)

# =====================================================================================
# N11  "Cladding welding of CA6M with pulsed FCAW and results analysis through
#       the L9 TAGUCHI and ANOVA"  - Int. J. Adv. Eng. Res. Sci. 5(5), 2018
#       doi:10.22161/ijaers.5.5.20   (grupo Moreno/Guimaraes, Brasil)
#
#  *** NO APORTA CORRIDAS NUEVAS ***  Las 9 condiciones y sus valores RMS de corriente
#  y voltaje son IDENTICOS (9/9) a P21_MORENO2022-MAT, ya en la base.
#  Es la CUARTA publicacion de la misma campana experimental:
#     2018  N11 (este)              -> Irms, Urms, aceleracion RMS
#     2020  P06_GUIMARAES2020       -> geometria completa, 18 corridas con replica
#     2022  P03_MORENO2022-PULS     -> geometria, 18 corridas
#     2022  P21_MORENO2022-MAT      -> Irms, Urms, Q, geometria promediada
#  Es ademas la PUBLICACION MAS TEMPRANA de esa campana -> cita de prioridad.
#
#  *** SI APORTA UNA VARIABLE NUEVA ***: aceleracion RMS (m/s2) por corrida,
#  senal de vibracion del arco. Se anexa a P21 por numero de muestra.
#
#  CONFIRMA la matriz L9 con CTWD 30/33/36 (no 30/35/40), resolviendo a favor de
#  Tabela 8 / Figura 17 de la disertacion Guimaraes frente a sus Tabelas 5 y 6.
# =====================================================================================
ANEXO_MORENO_MAT = dict(
 cita="Cladding welding of CA6M with pulsed FCAW and results analysis through the L9 TAGUCHI "
      "and ANOVA. Int. J. Adv. Eng. Res. Sci. 5(5), 2018. doi:10.22161/ijaers.5.5.20",
 tabla="Tabla 3 (matriz L9) y Tabla 4 (RMS de corriente, voltaje y aceleracion)",
 anexa_a="P21_MORENO2022-MAT",
 cols=["Sample","I ajustada A","Irms A","Urms V","Aceleracion RMS m/s2"],
 rows=[[1,170,193.2465,15.2346,0.3779],[2,170,185.4450,16.9629,0.3147],
       [3,170,160.5640,17.7862,0.2945],[4,200,191.3540,25.4825,0.2009],
       [5,200,182.2210,26.3488,0.1854],[6,200,178.3370,22.1801,0.2065],
       [7,230,209.9340,27.8447,0.1810],[8,230,215.3950,25.3854,0.1700],
       [9,230,195.2680,25.3066,0.1665]],
 extra=("Base AISI 1020 de 12.7 mm (63.5 x 185 mm), alambre CA6NM/410NiMo Ø1.2 mm, "
        "un solo cordon en posicion plana. "
        "DESVIACION AJUSTADA vs MEDIDA: 170 A -> +13.7 / +9.1 / -5.6 % ; "
        "200 A -> -4.3 / -8.9 / -10.8 % ; 230 A -> -8.7 / -6.3 / -15.1 %. "
        "El signo del error CAMBIA con la consigna: la maquina entrega de mas a 170 A "
        "y de menos a 230 A. No es un desfase constante sino una curva de calibracion."),
)

# =====================================================================================
# DESCARTADO  "Optimisation of Elemental Transfer Efficiency in Fe-C-Cr-Ti-Cu Hardfacing
#              by Self-Shielded Flux-Cored Wire: Taguchi-ANOVA-FD-PCA-GRA"
#              MDPI, 2026.  doi:10.3390/eng7030139
#
#  NO MIDE GEOMETRIA DE CORDON. Ni ancho, ni refuerzo, ni penetracion; una sola
#  mencion de "dilution" en todo el texto y sin tabla.
#  Diseno L9, FCAW-S AUTOPROTEGIDO (habria sido el primero del corpus):
#     EA aditivo exotermico CuO-Al (wt.%) 18/28/38 | CTWD(mm) 35/40/45
#     WFS(m/min) 1.63/1.85/2.07 | Uset(V) 28/31/34
#  Respuestas: coeficientes de transferencia de elementos, factor de recuperacion de Cu,
#  ciclo termico, dureza, y caracteristicas de fusion.
#
#  DATO APROVECHABLE PARA LA DISCUSION DE A_dep (Tabla 1):
#     Tasa de fusion MOR 4.37-5.73 kg/h | Tasa de deposito DR 3.88-5.16 kg/h
#     Factor de salpicadura 3.52-11.12 % | EFICIENCIA DE DEPOSITO 87.55-95.76 %
#  Util como referencia externa al evaluar por que A_dep calculada con phi=0.81 sale
#  sistematicamente 1.3-1.5x por encima de la envolvente geometrica 2/3*W*R en
#  N02_BALAN2018, N08_YADAV2022 y N10_ALORAIER2025.
# =====================================================================================

# =====================================================================================
# N12  Solovyov, V.G.; Lankin, Yu.M.; Romanova, I.Yu. (2023)
#      Avtomatychne Zvaryuvannya (Automatic Welding) No.10:30-  [ucraniano]
#      doi:10.37434/as2023.10.04
#      "Uso de redes neuronales para el control de los regimenes de recargue por arco
#       con alambres tubulares"
#
#  PRIMER FCAW-S (AUTOPROTEGIDO) DEL CORPUS y primer alambre distinto de Ø1.2 mm.
#  Alambre PP-Np-25Kh5FMS (recargue Fe-Cr-V-Mo-Si) en Ø1.8 / 2.4 / 2.8 mm.
#  NO reporta ancho, refuerzo ni penetracion. Unica respuesta geometrica:
#     CHOM (%) = fraccion de metal base en el deposito = DILUCION.
#
#  Tabla 3: comparacion de tres procesos a igual alambre (Ø1.8 mm):
#     arco abierto autoprotegido (FCAW-S) | bajo fundente AN-26P (SAW, FUERA DE ALCANCE)
#     | gas Ar+CO2 (FCAW-G)
# =====================================================================================
ORIG2["28_Solovyov2023"] = dict(
 cita="Solovyov, V.G.; Lankin, Yu.M.; Romanova, I.Yu. (2023). Vykorystannia neironnykh merezh "
      "dlia kontroliu ta keruvannia rezhymamy duhovoho naplavlennia poroshkovymy drotamy. "
      "Avtomatychne Zvariuvannia 10:30. doi:10.37434/as2023.10.04",
 tabla="Tabla 3 (efecto del metodo y regimen sobre la fraccion de metal base)",
 cols=["n","variante","I (A)","U (V)","D % (CHOM)"],
 rows=[
  [1,"FCAW-S",211,20.0,38.0],[2,"FCAW-S",218,22.3,45.0],[3,"FCAW-S",239,23.7,45.5],
  [4,"FCAW-S",265,22.7,43.2],[5,"FCAW-S",285,25.9,45.7],
  [6,"FCAW-G",160,23.0,33.0],[7,"FCAW-G",210,23.0,35.5],[8,"FCAW-G",260,24.0,39.5],
  [9,"FCAW-G",301,28.3,46.0],[10,"FCAW-G",315,27.5,45.0]],
 niveles=("Alambre tubular PP-Np-25Kh5FMS Ø1.8 mm, velocidad de recargue 20 m/h (=5.56 mm/s), "
          "vuelo (stick-out) 15 mm. Se EXCLUYEN las 5 corridas bajo fundente AN-26P (SAW). "
          "Unica respuesta: CHOM = dilucion. SIN ancho, refuerzo ni penetracion. "
          "Con I, U y TS conocidos el aporte termico SI es calculable para estas 10 corridas. "
          "El paper documenta ademas 75 experimentos FCAW-S (19 en Ø1.8, 22 en Ø2.4, 34 en Ø2.8) "
          "pero solo publica sus RANGOS en la Tabla 1, no los valores por corrida."),
)

# --- Hallazgo transversal, no son corridas: consigna vs medida (Tabla 4) ---
CALIBRACION_SOLOVYOV = dict(
 fuente="N12_SOLOVYOV2023-FCAWS, Tabla 4 (Ø2.4 mm, Ar+CO2, 20 m/h)",
 nota="Voltaje de CONSIGNA frente a voltaje MEDIO MEDIDO en el arco, y su desviacion tipica.",
 cols=["U consigna V","U medido V","desv %","SD de U (V)","I medio A","SD de I (A)"],
 rows=[[22,18.8,-14.5,10.3,312,178],[24,19.4,-19.2,8.2,335,169],
       [26,21.6,-16.9,4.0,331,92.9],[28,24.1,-13.9,2.9,342,72.8],
       [30,26.8,-10.7,2.1,360,None],[32,30.2,-5.6,2.0,357.1,None]],
 hallazgo=("El voltaje medido es SIEMPRE menor que la consigna, y la brecha se ESTRECHA al subir: "
           "-19.2% a 24 V frente a -5.6% a 32 V. Ademas la desviacion tipica del voltaje cae de "
           "10.3 V a 2.0 V: a baja consigna el arco es inestable. "
           "Es el equivalente en VOLTAJE de la curva de calibracion en CORRIENTE hallada en "
           "N11 (Moreno/CA6M). Dos senales, dos laboratorios, misma conclusion: la desviacion "
           "maquina-consigna NO es un desfase constante sino una funcion del punto de trabajo."),
)
