# -*- coding: utf-8 -*-
"""Capa 2 v2: anexa a la maestra los 9 estudios nuevos de papers_FCAW/nueva.
   Se ejecuta DESPUES de construir_maestra.py (usa su M, COLS, add, adep, hi, r2, K_ETA, PHI)."""
import math

# ============================ N01 KANNAN 2006 - duplex 2209 (31) ============================
lv = {'I':{-2:200,-1:225,0:250,1:275,2:300}, 'S':{-2:20,-1:30,0:40,1:50,2:60},
      'N':{-2:22,-1:24,0:26,1:28,2:30},      'T':{-2:20,-1:15,0:10,1:5,2:0}}
K01=[(1,-1,-1,-1,-1,29.50,0.61,4.97,7.86),(2,1,-1,-1,-1,36.62,0.73,5.00,12.10),
(3,-1,1,-1,-1,24.20,0.63,4.23,11.35),(4,1,1,-1,-1,28.00,0.77,4.27,11.98),
(5,-1,-1,1,-1,30.00,0.57,5.00,6.54),(6,1,-1,1,-1,34.98,0.67,5.29,8.82),
(7,-1,1,1,-1,25.59,0.58,4.18,9.69),(8,1,1,1,-1,29.51,0.70,4.20,11.16),
(9,-1,-1,-1,1,28.34,0.73,5.00,8.97),(10,1,-1,-1,1,34.50,0.97,5.10,13.75),
(11,-1,1,-1,1,24.00,1.00,4.00,18.52),(12,1,1,-1,1,27.80,1.20,4.34,20.58),
(13,-1,-1,1,1,29.26,0.60,5.08,7.46),(14,1,-1,1,1,34.80,0.80,5.28,9.14),
(15,-1,1,1,1,25.30,0.97,4.00,18.00),(16,1,1,1,1,27.70,1.00,4.20,14.80),
(17,-2,0,0,0,20.15,0.40,3.98,5.86),(18,2,0,0,0,31.00,1.07,4.90,16.48),
(19,0,-2,0,0,39.53,0.70,5.68,5.31),(20,0,2,0,0,23.10,1.00,3.63,17.35),
(21,0,0,-2,0,25.10,0.83,4.32,11.71),(22,0,0,2,0,28.00,0.63,4.81,9.01),
(23,0,0,0,-2,30.20,0.56,4.17,10.54),(24,0,0,0,2,26.00,0.87,4.87,13.98),
(25,0,0,0,0,27.88,0.70,4.55,10.33),(26,0,0,0,0,29.42,0.83,4.34,13.60),
(27,0,0,0,0,28.00,0.77,4.50,10.73),(28,0,0,0,0,27.90,0.87,4.50,11.71),
(29,0,0,0,0,29.20,0.83,4.32,13.76),(30,0,0,0,0,27.80,0.79,4.58,10.99),
(31,0,0,0,0,27.80,0.80,4.57,10.67)]
for n,i,s,nn,t,W,P,R,D in K01:
    add(registro_id=f"KANNAN2006-r{n}",paper_id="02_Kannan2006",run_id_original=n,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="cladding",posicion="plana",
        nivel_uso="completo" if 25<=n<=31 else "factorial/estrella",
        metal_base="IS 2062 estructural",alambre_clase="2209 duplex",alambre_diam_mm=1.2,
        gas_tipo="Ar-CO2",polaridad="n/d",
        I_amp=lv['I'][i],I_medida="no",TS_mm_s=r2(lv['S'][s]*10/60,3),NPD_mm=lv['N'][nn],angulo_deg=lv['T'][t],
        W_mm=W,R_mm=R,P_mm=P,D_pct=D,IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_oscilado;flag_sin_voltaje;flag_sin_wfs;flag_angulo_invertido"
                 +(";flag_punto_central" if 25<=n<=31 else ""),
        confiabilidad="alta",
        observaciones=("Cordon OSCILADO (W 20-40 mm), poblacion distinta al stringer. "
                       "Niveles de angulo INVERTIDOS: -2=20deg, +2=0deg. "
                       "Cita alterna: Sensitivity Analysis of FCA Cladding Parameters (RSM), mismas 31 corridas"))

# ============================ N02 BALAN 2018 - FC2507 (31) ============================
lb={'F':{-2:150,-1:175,0:200,1:225,2:250},'S':{-2:100,-1:120,0:140,1:160,2:180},
    'N':{-2:16,-1:18,0:20,1:22,2:24},'T':{-2:90,-1:100,0:110,1:120,2:130}}
B02=[(1,-1,-1,-1,-1,8.39,4.13,0.37,5.48),(2,1,-1,-1,-1,9.77,4.62,0.42,6.48),
(3,-1,1,-1,-1,8.05,3.38,0.38,6.45),(4,1,1,-1,-1,8.43,3.79,0.44,6.68),
(5,-1,-1,1,-1,8.52,4.27,0.33,4.72),(6,1,-1,1,-1,10.10,4.78,0.38,5.38),
(7,-1,1,1,-1,8.50,3.69,0.34,6.25),(8,1,1,1,-1,9.00,3.93,0.38,6.33),
(9,-1,-1,-1,1,8.70,3.96,0.33,5.99),(10,1,-1,-1,1,10.12,4.16,0.41,6.75),
(11,-1,1,-1,1,8.52,3.37,0.34,6.78),(12,1,1,-1,1,8.61,3.62,0.43,6.88),
(13,-1,-1,1,1,8.93,4.00,0.32,5.66),(14,1,-1,1,1,10.29,4.69,0.36,5.87),
(15,-1,1,1,1,8.67,3.51,0.33,6.48),(16,1,1,1,1,9.61,3.87,0.36,6.70),
(17,-2,0,0,0,7.72,3.75,0.33,6.20),(18,2,0,0,0,10.00,4.10,0.55,7.62),
(19,0,-2,0,0,10.13,4.84,0.42,4.96),(20,0,2,0,0,8.17,3.41,0.50,8.77),
(21,0,0,-2,0,7.75,3.16,0.83,7.08),(22,0,0,2,0,9.61,4.10,0.27,5.39),
(23,0,0,0,-2,8.93,3.77,0.38,4.03),(24,0,0,0,2,9.79,3.53,0.18,5.58),
(25,0,0,0,0,8.44,3.88,0.71,5.48),(26,0,0,0,0,7.87,3.87,0.71,5.88),
(27,0,0,0,0,8.45,4.28,0.71,5.08),(28,0,0,0,0,8.44,3.87,0.71,5.24),
(29,0,0,0,0,8.45,3.87,0.53,5.01),(30,0,0,0,0,8.45,3.87,0.71,5.05),
(31,0,0,0,0,8.44,3.87,0.71,5.08)]
for n,f,s,nn,t,W,R,P,D in B02:
    wfs=lb['F'][f]*25.4; ts=lb['S'][s]
    add(registro_id=f"BALAN2018-r{n}",paper_id="19_Balan2018",run_id_original=n,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="cladding",posicion="plana",
        nivel_uso="completo" if 25<=n<=31 else "factorial/estrella",
        metal_base="IS 2062",alambre_clase="FC2507 super duplex",alambre_diam_mm=1.2,
        gas_tipo="Ar-CO2",pct_CO2=20,polaridad="n/d",
        I_medida="no",WFS_m_min=r2(wfs/1000,3),TS_mm_s=r2(ts/60,3),NPD_mm=lb['N'][nn],angulo_deg=lb['T'][t],
        A_dep_mm2=r2(adep(0.81,1.2,wfs,ts),2),WFS_TS=r2(wfs/ts,2),
        W_mm=W,R_mm=R,P_mm=P,D_pct=D,IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_sin_voltaje;flag_sin_corriente;flag_Adep_extremo_alto_1_45;flag_IC_alto"
                 +(";flag_punto_central;flag_replicas_no_independientes" if 25<=n<=31 else ""),
        confiabilidad="media",
        observaciones=("Razon A_dep/(2/3*W*R) = 1.45: extremo ALTO del rango del corpus (0.44-1.45, mediana 1.06) pero DENTRO de lo normal. No es incoherencia. "
                       "Los 7 'centrales' repiten valores identicos (R=3.87 x5, P=0.71 x5): "
                       "NO son replicas independientes, NO usar para piso de error. "
                       "Ferrite number tambien reportado (24.20-29.70)"))

# ============================ N03 SENTHILKUMAR 2014 - 2507 CCD (30) ============================
S03=[(1,24,5.715,0.14,0.017,80,0.479,0.025,71.63),(2,24,5.715,0.14,0.021,100,0.483,0.030,75.25),
(3,24,5.715,0.18,0.017,100,0.439,0.048,95.38),(4,24,5.715,0.18,0.021,80,0.506,0.038,92.13),
(5,24,6.985,0.14,0.017,100,0.438,0.029,81.00),(6,24,6.985,0.14,0.021,80,0.517,0.032,72.88),
(7,24,6.985,0.18,0.017,80,0.445,0.043,80.38),(8,24,6.985,0.18,0.021,100,0.462,0.041,86.63),
(9,28,5.715,0.14,0.017,100,0.419,0.013,78.63),(10,28,5.715,0.14,0.021,80,0.539,0.029,77.00),
(11,28,5.715,0.18,0.017,80,0.465,0.060,96.13),(12,28,5.715,0.18,0.021,100,0.428,0.045,96.50),
(13,28,6.985,0.14,0.017,80,0.421,0.033,88.25),(14,28,6.985,0.14,0.021,100,0.446,0.011,68.13),
(15,28,6.985,0.18,0.017,100,0.369,0.029,99.00),(16,28,6.985,0.18,0.021,80,0.451,0.044,87.25),
(17,22,6.320,0.16,0.019,90,0.694,0.038,66.88),(18,30,6.320,0.16,0.019,90,0.446,0.036,81.50),
(19,26,5.080,0.16,0.019,90,0.510,0.054,87.75),(20,26,7.620,0.16,0.019,90,0.404,0.026,83.13),
(21,26,6.320,0.12,0.019,90,0.461,0.013,64.63),(22,26,6.320,0.20,0.019,90,0.414,0.060,99.88),
(23,26,6.320,0.16,0.015,90,0.370,0.033,90.63),(24,26,6.320,0.16,0.023,90,0.452,0.029,83.25),
(25,26,6.320,0.16,0.019,70,0.484,0.036,76.75),(26,26,6.320,0.16,0.019,110,0.426,0.028,78.13),
(27,26,6.320,0.16,0.019,90,0.464,0.031,87.75),(28,26,6.320,0.16,0.019,90,0.408,0.031,100.00),
(29,26,6.320,0.16,0.019,90,0.470,0.041,96.00),(30,26,6.320,0.16,0.019,90,0.426,0.038,98.00)]
for n,v,wfs,ts,npd,a,rff,pff,ca in S03:
    wm=wfs*1000; tm=ts*1000
    add(registro_id=f"SENTHILKUMAR2014-r{n}",paper_id="12_Senthilkumar2014",run_id_original=n,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="cladding",posicion="plana",
        nivel_uso="completo" if n>=27 else "factorial/estrella",
        metal_base="acero estructural bajo carbono",alambre_clase="2507 super duplex",alambre_diam_mm=1.2,
        gas_tipo="Ar-CO2",pct_CO2=20,polaridad="n/d",
        I_medida="no",V_arco=v,WFS_m_min=wfs,TS_mm_s=r2(tm/60,3),NPD_mm=r2(npd*1000,1),angulo_deg=a,
        A_dep_mm2=r2(adep(0.81,1.2,wm,tm),2),WFS_TS=r2(wm/tm,2),
        IC_pct=r2(rff*100,2),W_P=r2(1/pff,2),
        banderas="flag_sin_corriente;flag_solo_razones;flag_contradiccion_IC_vs_N09"
                 +(";flag_punto_central" if n>=27 else ""),
        confiabilidad="alta",
        observaciones=(f"Angulo de contacto CA={ca} deg (respuesta adicional). "
                       "RFF=refuerzo/ancho -> IC_pct ; PFF=penetracion/ancho -> W_P. "
                       "W, R y P individuales NO recuperables. Autores acotan HI a 0.5-1.5 kJ/mm. "
                       "CONTRADICCION: IC medio 45.8% aqui vs 27.3% en N09 del mismo grupo"))

# ============================ N05 SINGH 2021 - AISI 201LN (31) ============================
G05=[(6,1,8,20,280,10,2.23,3.43,9.37),(26,2,7,22,250,15,1.48,3.64,8.75),
(24,3,7,22,250,25,0.82,3.65,7.52),(28,4,7,22,250,15,1.25,3.78,8.99),
(5,5,6,20,280,10,0.99,3.52,7.16),(9,6,6,20,220,20,0.78,3.83,7.20),
(3,7,6,24,220,10,1.58,3.03,10.05),(8,8,8,24,280,10,2.49,3.23,10.68),
(16,9,8,24,280,20,1.54,3.62,9.46),(1,10,6,20,220,10,1.65,3.85,8.01),
(17,11,5,22,250,15,0.72,3.02,7.38),(27,12,7,22,250,15,1.66,4.01,8.86),
(11,13,6,24,220,20,0.89,3.18,9.27),(29,14,7,22,250,15,1.32,3.55,8.27),
(15,15,6,24,280,20,0.82,2.68,8.92),(25,16,7,22,250,15,1.56,3.79,8.33),
(22,17,7,22,310,15,1.16,3.48,8.62),(18,18,9,22,250,15,2.88,3.63,10.03),
(10,19,8,20,220,20,1.83,3.31,8.94),(13,20,6,20,280,20,0.81,3.45,6.59),
(4,21,8,24,220,10,3.45,3.47,10.76),(21,22,7,22,190,15,2.06,3.69,10.38),
(7,23,6,24,280,10,1.48,2.52,10.18),(19,24,7,18,250,15,1.44,3.42,8.17),
(31,25,7,22,250,15,1.45,3.86,8.56),(23,26,7,22,250,5,3.53,3.31,8.91),
(2,27,8,20,220,10,3.53,3.81,10.47),(20,28,7,26,250,15,1.39,2.75,12.08),
(14,29,8,20,280,20,1.19,3.64,7.47),(30,30,7,22,250,15,1.57,3.53,9.00),
(12,31,8,24,220,20,1.69,3.69,10.24)]
for std,o,wfs,v,s,ntd,P,R,W in G05:
    add(registro_id=f"SINGH2021-r{o}",paper_id="23_Singh2021",run_id_original=o,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="BOP",posicion="plana",
        nivel_uso="completo" if std>=25 else "factorial/estrella",
        metal_base="AISI 201LN austenitico",alambre_clase="tubular n/e",alambre_diam_mm=1.2,
        gas_tipo="CO2",pct_CO2=100,caudal_L_min=18,polaridad="n/d",
        I_medida="no",V_arco=v,WFS_m_min=wfs,TS_mm_s=r2(s/60,3),NPD_mm=ntd,
        A_dep_mm2=r2(adep(0.81,1.2,wfs*1000,s),2),WFS_TS=r2(wfs*1000/s,2),
        W_mm=W,R_mm=R,P_mm=P,IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_sin_corriente;flag_gas_CO2_puro;flag_clase_alambre_no_especificada;flag_sin_dilucion"
                 +(";flag_punto_central" if std>=25 else ""),
        confiabilidad="alta",
        observaciones=(f"Orden estandar {std}. UNICO del corpus con CO2 100% sobre inoxidable y base 201LN. "
                       "WPSF=W/P y WRFF=W/R verificados (desv max 0.005). phi=0.81 por defecto"))

# ============================ N07 ODHIAMBO 2025 - API 5L (22) ============================
O07=[(1,15,60,70,15,3,620,6.04,1.44),(2,15,60,120,60,6,360,5.08,0.48),
(3,15,60,170,105,9,250,4.60,0.17),(4,15,130,70,60,9,1340,7.10,3.20),
(5,15,130,120,105,3,780,6.42,1.82),(6,15,130,170,15,6,550,5.66,1.06),
(7,15,200,70,105,6,2060,6.14,3.70),(8,15,200,120,15,9,1200,7.46,3.00),
(9,15,200,170,60,3,850,6.83,2.35),(10,20,60,70,105,9,820,6.61,2.13),
(11,20,60,120,15,3,480,5.45,0.85),(12,20,60,170,60,6,340,4.83,0.23),
(13,20,130,70,15,6,1780,6.56,3.50),(14,20,130,120,60,9,1040,7.48,3.00),
(15,20,130,170,105,3,730,6.22,1.62),(16,20,200,70,60,3,2740,5.64,3.90),
(17,20,200,120,105,6,1600,6.78,3.40),(18,20,200,170,15,9,1130,7.56,2.90),
(19,25,60,70,60,6,1030,7.24,2.76),(20,25,60,120,105,9,600,5.88,1.28),
(21,25,60,170,15,3,420,5.24,0.64),(22,25,130,70,105,3,2230,5.92,3.80)]
for n,v,i,s,a,ct,q,dop,zat in O07:
    add(registro_id=f"ODHIAMBO2025-r{n}",paper_id="31_Odhiambo2025",run_id_original=n,tipo_registro="corrida",
        conjunto="excluido",variante="FCAW-G",aplicacion="tuberia_bisel",posicion="n/d",nivel_uso="subgrupo",
        metal_base="ASTM A335 Gr.B / API 5L Sch40",espesor_mm=7.55,alambre_clase="tubular n/e",
        gas_tipo="n/d",polaridad="n/d",
        I_amp=i,I_medida="si",V_arco=v,TS_mm_s=r2(s/60,3),CTWD_mm=ct,angulo_deg=a,
        HI_J_mm=q,P_mm=dop,ZAT_mm=zat,
        banderas="flag_junta_a_tope_biselada;flag_P_no_comparable_BOP;flag_CTWD_anomalo;flag_L27_incompleto;flag_eta_080_verificado",
        confiabilidad="media",
        observaciones=("EXCLUIDO del conjunto principal: DoP en junta a tope biselada sobre pared de "
                       "7.55 mm, no es penetracion de cordon sobre placa. "
                       "VERIFICACION CLAVE: eta implicito = 0.7993 (0.787-0.804) en las 22 corridas, "
                       "confirma k=0.80 de ISO/TR 17671-1. corr(HI,DoP)=+0.33 pero corr(HI,ZAT)=+0.91: "
                       "el aporte termico NO explica la penetracion (5o caso del corpus). "
                       "L27 declarado, solo 22 publicadas. Autores reportan R=1.000 en train/val/test: sobreajuste"))

# ============================ N08 YADAV 2022 - 308L (21) ============================
# B: el paper rotula 'mm/min' pero la magnitud solo es coherente en cm/min (ver bandera)
ly={'A':{-2:18,-1:20,0:22,1:24,2:26},'B':{-2:3156,-1:6312,0:9468,1:13312,2:17500},
    'C':{-2:152.2,-1:206.7,0:260.8,1:315.7,2:370}}
Y08=[(1,-1,-1,-1,23.73,12.62,2.73,1.02),(2,-1,-1,1,29.81,9.90,2.47,1.22),
(3,-1,1,-1,10.54,14.15,3.27,0.86),(4,-1,1,1,30.06,11.63,2.65,1.76),
(5,1,-1,-1,27.33,13.03,2.28,1.67),(6,1,-1,1,35.76,11.33,2.09,2.09),
(7,1,1,-1,21.57,15.07,2.98,0.99),(8,1,1,1,39.12,14.09,2.88,1.97),
(9,-2,0,0,15.72,8.65,3.85,1.35),(10,2,0,0,40.58,14.40,2.13,1.78),
(11,0,-2,0,32.18,10.69,2.15,1.32),(12,0,2,0,26.95,15.04,3.04,1.12),
(13,0,0,-2,16.69,16.58,3.07,0.85),(14,0,0,2,28.14,11.64,2.10,1.72),
(15,0,0,0,25.23,12.77,2.33,1.34),(16,0,0,0,31.63,12.56,2.48,1.81),
(17,0,0,0,29.73,12.48,2.87,1.59),(18,0,0,0,27.39,13.39,2.41,1.66),
(19,0,0,0,34.75,12.96,2.82,1.65),(20,0,0,0,32.24,13.47,2.19,1.79),
(21,0,0,0,28.53,14.00,2.73,1.27)]
for n,a,b,c,D,W,R,P in Y08:
    add(registro_id=f"YADAV2022-r{n}",paper_id="26_Yadav2022",run_id_original=n,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="cladding",posicion="plana",
        nivel_uso="completo" if n>=15 else "factorial/estrella",
        metal_base="acero bajo carbono",alambre_clase="308L inox tubular",alambre_diam_mm=1.2,
        gas_tipo="n/d",polaridad="n/d",
        I_medida="no",V_arco=ly['A'][a],TS_mm_s=r2(ly['C'][c]/60,3),
        WFS_m_min=r2(ly['B'][b]/1000,3),WFS_TS=r2(ly['B'][b]/ly['C'][c],2),
        A_dep_mm2=r2(adep(0.81,1.2,ly['B'][b],ly['C'][c]),2),
        W_mm=W,R_mm=R,P_mm=P,D_pct=D,IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_sin_corriente;flag_unidad_WFS_corregida;flag_niveles_no_equiespaciados;flag_orden_no_Yates"
                 +(";flag_nivel_TS_inferido" if c==2 else "")
                 +(";flag_punto_central" if n>=15 else ""),
        confiabilidad="media",
        observaciones=(f"Feed rate: el paper lo rotula mm/min ({ly['B'][b]/10:.1f}) pero la magnitud "
                       "solo es coherente en cm/min. Leido como mm/min, A_dep/(2/3*W*R)=0.15, "
                       "2.9x por debajo del minimo del corpus (0.44). Leido como cm/min da 1.50, "
                       "dentro del rango observado (0.44-1.45, mediana 1.06). Se adopta cm/min. "
                       "Niveles +1 y +2 NO equiespaciados: publicados 1331.2 y 1750 cm/min frente a "
                       "1262.4 y 1578 esperados por el paso del diseno. "
                       "Matriz recuperada de la tabla impresa (el PDF perdia los signos). "
                       "Orden NO-Yates: el factor C alterna mas rapido. "
                       "VALIDADO contra su ANOVA: SS modelo 63.12 vs 62.93 publicado (+0.3%)"))

# ============================ N09 SENTHILKUMAR 2015 - L9 (9) ============================
S09=[(1,22,5.08,0.12,0.015,21.63,5.60,27.89),(2,22,6.35,0.16,0.019,17.46,6.53,29.60),
(3,22,7.62,0.20,0.023,16.70,7.13,25.57),(4,26,5.08,0.16,0.023,19.70,5.42,27.93),
(5,26,6.35,0.20,0.015,22.46,4.98,30.47),(6,26,7.62,0.12,0.019,27.64,7.08,29.08),
(7,30,5.08,0.20,0.019,18.11,4.29,28.32),(8,30,6.35,0.12,0.023,26.43,6.18,28.66),
(9,30,7.62,0.16,0.015,29.17,5.06,28.80)]
for n,v,wfs,ts,npd,W,R,fn in S09:
    wm=wfs*1000; tm=ts*1000
    add(registro_id=f"SENTHILKUMAR2015-r{n}",paper_id="17_Senthilkumar2015",run_id_original=n,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="cladding",posicion="plana",nivel_uso="L9",
        metal_base="acero al carbono",alambre_clase="E2594T0-4 super duplex",alambre_diam_mm=1.2,
        gas_tipo="Ar-CO2",pct_CO2=20,polaridad="n/d",
        I_medida="no",V_arco=v,WFS_m_min=wfs,TS_mm_s=r2(tm/60,3),NPD_mm=r2(npd*1000,1),
        A_dep_mm2=r2(adep(0.81,1.2,wm,tm),2),WFS_TS=r2(wm/tm,2),
        W_mm=W,R_mm=R,IC_pct=r2(R/W*100,2),
        banderas="flag_oscilado;flag_sin_corriente;flag_sin_penetracion;flag_sin_dilucion;flag_contradiccion_IC_vs_N03",
        confiabilidad="media",
        observaciones=(f"Numero de ferrita FN={fn}. Cordon oscilado (W 16.7-29.2 mm). "
                       "CONTRADICCION con N03 del mismo grupo: IC medio 27.3% aqui vs 45.8% alli, "
                       "misma definicion declarada. En la condicion casi coincidente "
                       "(22V, ~6.3 m/min, 0.16, 0.019): IC 37.4% aqui vs 69.4% en N03. "
                       "Nivel central de WFS: 6.35 aqui, 6.32 en N03"))

# ============================ N10 ALORAIER 2025 - precalentamiento (12) ============================
A10=[(1,25,2.5,20.2,71,3.2,359,5.22,1.83,0.38,6.87),(2,25,5.0,23.0,151,5.3,521,10.45,1.77,1.20,11.58),
(3,25,10.0,28.0,246,8.0,689,11.79,1.69,2.65,13.86),(4,100,2.5,20.2,74,3.1,389,12.35,4.12,1.11,15.86),
(5,100,5.0,23.0,149,4.6,600,11.14,1.92,1.10,13.61),(6,100,10.0,28.7,239,7.3,755,11.42,1.58,2.20,14.29),
(7,150,2.5,20.0,75,3.5,345,5.40,1.66,0.47,7.56),(8,150,5.0,23.0,150,4.2,656,9.63,1.51,1.31,12.20),
(9,150,10.0,28.7,226,7.6,681,12.91,2.11,1.93,15.07),(10,200,2.5,20.2,73,4.0,295,6.88,1.84,0.93,9.06),
(11,200,5.0,22.7,145,6.7,395,6.90,1.85,0.95,9.12),(12,200,10.0,28.7,230,9.4,561,13.13,2.41,2.25,15.48)]
for n,T,wfs,v,i,ts,q,W,R,P,zat in A10:
    add(registro_id=f"ALORAIER2025-r{n}",paper_id="30_Aloraier2025",run_id_original=n,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="BOP",posicion="plana",nivel_uso="factorial 4x3",
        metal_base="AISI 1020",alambre_clase="E71T-1C rutilico",alambre_diam_mm=1.2,
        gas_tipo="n/d",polaridad="n/d",temp_precal_C=T,
        I_amp=i,I_medida="si",V_arco=v,WFS_m_min=wfs,TS_mm_s=ts,
        HI_J_mm=q,A_dep_mm2=r2(adep(0.81,1.2,wfs*1000,ts*60),2),WFS_TS=r2(wfs*1000/(ts*60),2),
        W_mm=W,R_mm=R,P_mm=P,ZAT_mm=zat,IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_eta_080_verificado;flag_sin_replicas"
                 +(";flag_par_10_11_identico" if n in (10,11) else "")
                 +(";flag_R_atipico" if n==4 else ""),
        confiabilidad="alta" if n not in (4,10,11) else "media",
        observaciones=("EL MAS COMPLETO DEL CORPUS: V, I, TS, WFS, precalentamiento, HI y geometria. "
                       "eta verificado = 0.8014 (0.795-0.807), 2a confirmacion de ISO/TR 17671-1. "
                       "V, I y TS son MEDIDOS por corrida, no niveles nominales. "
                       + ("PAR 10/11: duplican I (73->145 A) y WFS (2.5->5.0) pero devuelven geometria "
                          "identica a 0.02 mm. Implausible; probable fila duplicada por error. "
                          if n in (10,11) else "")
                       + ("R=4.12 mm atipico (resto 1.51-2.41) con la corriente mas baja del conjunto. "
                          if n==4 else "")))

# ============================ N12 SOLOVYOV 2023 - FCAW-S (10) ============================
SO=[(1,"FCAW-S",211,20.0,38.0),(2,"FCAW-S",218,22.3,45.0),(3,"FCAW-S",239,23.7,45.5),
(4,"FCAW-S",265,22.7,43.2),(5,"FCAW-S",285,25.9,45.7),
(6,"FCAW-G",160,23.0,33.0),(7,"FCAW-G",210,23.0,35.5),(8,"FCAW-G",260,24.0,39.5),
(9,"FCAW-G",301,28.3,46.0),(10,"FCAW-G",315,27.5,45.0)]
TS_SOL = 20*1000/3600.0     # 20 m/h -> mm/s
for n,var,i,v,D in SO:
    add(registro_id=f"SOLOVYOV2023-r{n}",paper_id="28_Solovyov2023",run_id_original=n,tipo_registro="corrida",
        conjunto="principal" if var=="FCAW-G" else "autoprotegido",
        variante=var,aplicacion="cladding",posicion="plana",nivel_uso="comparativo de procesos",
        metal_base="n/d",alambre_clase="PP-Np-25Kh5FMS recargue",alambre_diam_mm=1.8,
        gas_tipo="ninguno" if var=="FCAW-S" else "Ar-CO2",polaridad="n/d",
        I_amp=i,I_medida="si",V_arco=v,TS_mm_s=r2(TS_SOL,3),stickout_mm=15,
        HI_J_mm=r2(hi(v,i,TS_SOL,K_ETA),0),D_pct=D,
        banderas="flag_diametro_1_8;flag_solo_dilucion;flag_sin_ancho;flag_sin_penetracion"
                 +(";flag_autoprotegido" if var=="FCAW-S" else ""),
        confiabilidad="media",
        observaciones=("PRIMER FCAW-S del corpus y primer diametro distinto de 1.2 mm. "
                       "CHOM = fraccion de metal base = dilucion. Velocidad 20 m/h, vuelo 15 mm. "
                       "Se excluyeron las 5 corridas bajo fundente AN-26P (arco sumergido). "
                       "El paper declara 75 experimentos FCAW-S mas (Ø1.8/2.4/2.8) pero solo publica rangos. "
                       "Tabla 4: voltaje consigna vs medido = -19.2% a 24V y -5.6% a 32V; "
                       "SD del voltaje cae de 10.3 a 2.0 V al subir la consigna"))

# ============================ 20 BECZKOWSKI 2018 - Plackett-Burman (9) ============================
# El paper NO publica la matriz de diseno: solo da los niveles de los 4 factores y las
# mediciones por condicion M1..M9. Se registran las 9 condiciones con sus MEDIAS y la
# dispersion intra-cordon, SIN predictores (no se sabe que combinacion es cada M).
BEC_Hn=[4.82,3.37,3.46,3.99,4.58,5.13,5.25,4.90,4.16]
BEC_Hw=[1.16,1.89,1.03,1.59,2.06,1.13,1.03,1.46,1.43]
BEC_Hn_r=[[4.52,4.62,4.72,4.82,4.92,5.02,5.02,5.12,4.62],[3.16,3.21,3.36,3.46,3.61,3.76,3.16,3.21,3.36],
 [3.14,3.24,3.34,3.44,3.54,3.74,3.64,3.64,3.44],[3.86,3.76,3.86,4.06,4.46,3.96,3.76,4.06,4.16],
 [4.45,4.85,4.35,4.75,4.55,4.55,4.45,4.45,4.85],[4.82,5.02,5.12,5.12,5.12,5.22,4.82,5.92,5.02],
 [5.26,5.56,5.76,5.16,5.26,5.16,5.06,4.76,5.26],[4.59,4.89,4.69,4.59,4.89,4.69,5.19,5.39,5.19],
 [4.07,4.17,4.07,4.07,4.47,4.17,4.07,4.07,4.27]]
BEC_Hw_r=[[1.32,0.48,1.26,1.17,1.73,0.99],[2.82,2.04,2.03,1.65,1.45,1.36],[0.84,0.68,1.10,1.08,1.22,1.23],
 [1.92,1.67,1.27,1.40,1.53,1.74],[1.36,2.12,2.26,2.29,2.40,1.90],[1.23,1.23,1.16,1.39,1.01,0.73],
 [0.70,1.37,0.85,1.23,1.29,0.75],[1.79,1.39,1.52,1.56,1.59,0.89],[1.34,1.64,1.25,1.60,1.45,1.43]]
import statistics as _st
for i in range(9):
    hn,hw=BEC_Hn[i],BEC_Hw[i]
    cvn=100*_st.stdev(BEC_Hn_r[i])/_st.mean(BEC_Hn_r[i])
    cvw=100*_st.stdev(BEC_Hw_r[i])/_st.mean(BEC_Hw_r[i])
    add(registro_id=f"BECZKOWSKI2018-M{i+1}",paper_id="20_Beczkowski2018",run_id_original=f"M{i+1}",
        tipo_registro="corrida",conjunto="autoprotegido",variante="FCAW-S",aplicacion="cladding",
        posicion="plana",nivel_uso="solo respuestas",
        metal_base="n/d",alambre_clase="autoprotegido recargue",alambre_diam_mm=2.8,
        gas_tipo="ninguno",polaridad="n/d",
        R_mm=hn,P_mm=hw,IC_pct=None,
        banderas="flag_autoprotegido;flag_diametro_2_8;flag_matriz_no_publicada;flag_sin_predictores;"
                 "flag_sin_ancho;flag_sin_dilucion;flag_oscilado",
        confiabilidad="media",
        observaciones=(f"Plackett-Burman de 4 factores; el paper NO publica la matriz de diseno, solo los "
                       f"niveles (VNAP 130/160/190 mm/min, P 10045/11480/12915 W, Le 20/30/40 mm, "
                       f"lambda 0.15/2.15/4.3 W/mK) y las mediciones por condicion. NO se sabe que "
                       f"combinacion corresponde a M{i+1}. Hn=altura de refuerzo (media de 9 cortes, "
                       f"CV={cvn:.1f}%), Hw=penetracion (media de 6 cortes, CV={cvw:.1f}%). "
                       f"Constantes: Vosc 2.4 m/min, Vd 5.8 m/min, oscilacion B=35 mm. "
                       f"EVIDENCIA DE H-012: dispersion INTRA-cordon del mismo deposito"))

# ============================ 10 RAHMAN 2014 (2F) - 3 puntos de figura ============================
# El paper no tabula sus ~80 cupones; estos 3 puntos provienen de rotulos de figura.
RAH2F=[("M32",300,32,10,5.4,6.5,9.2),("M117",300,32,14,4.2,5.2,7.2),("M119",150,26,5,6.0,6.3,8.5)]
for rid,I,V,v,l1,l2,BW in RAH2F:
    add(registro_id=f"RAHMAN2014-2F-{rid}",paper_id="10_Rahman2014",run_id_original=rid,
        tipo_registro="punto_de_figura",conjunto="excluido",variante="FCAW-G",aplicacion="filete",
        posicion="2F horizontal",nivel_uso="contraste",
        metal_base="acero bajo carbono",espesor_mm=9,alambre_clase="E71T-1",alambre_diam_mm=1.2,
        gas_tipo="CO2",pct_CO2=99.9,polaridad="n/d",
        I_amp=I,I_medida="no",V_arco=V,TS_mm_s=v,stickout_mm=15,angulo_deg=45,
        HI_J_mm=r2(hi(V,I,v,K_ETA),0),W_mm=BW,
        banderas="flag_punto_de_figura;flag_respuestas_filete;flag_sin_penetracion;flag_sin_matriz",
        confiabilidad="baja",
        observaciones=(f"El paper declara 120 muestras y ~80 aceptadas pero NO TABULA NINGUNA. "
                       f"Este punto se recupero de un rotulo de figura. Pierna 1={l1} mm, pierna 2={l2} mm "
                       f"(magnitudes de filete, no comparables con cordon sobre placa). "
                       f"Ecuaciones publicadas: Leg=6.0918*HI^0.5373. Robot Daihen-OTC Almega AII-B4"))
