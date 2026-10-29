# -*- coding: utf-8 -*-
"""Capa 2: tabla maestra plana. Se genera desde la capa 0 aplicando las reglas de 07_TRANSFORMACIONES."""
import math
K_ETA = 0.80          # ISO/TR 17671-1, eficiencia de arco para FCAW
PHI = {"rutilico":0.81, "inox_rutilico":0.81, "metal_cored":0.95, "recargue":None, "autoprot":None}

def adep(phi, d_mm, wfs_mmmin, ts_mmmin):
    if phi is None or wfs_mmmin is None or ts_mmmin in (None,0): return None
    return phi*(math.pi/4)*d_mm**2*(wfs_mmmin/ts_mmmin)
def hi(V, I, ts_mms, eta=None):
    if None in (V,I,ts_mms) or ts_mms==0: return None
    return (eta if eta else 1.0)*V*I/ts_mms
def r2(x,n=3): return round(x,n) if isinstance(x,(int,float)) else None

COLS = ["registro_id","paper_id","run_id_original","replica","tipo_registro",
 "conjunto","variante","aplicacion","posicion","nivel_uso",
 "metal_base","espesor_mm","alambre_clase","alambre_diam_mm","gas_tipo","pct_CO2","caudal_L_min","polaridad",
 "I_amp","I_medida","V_arco","OCV_volt","WFS_m_min","TS_mm_s","CTWD_mm","stickout_mm","NPD_mm",
 "angulo_deg","f_pulso_Hz","temp_precal_C",
 "HI_J_mm","A_dep_mm2","WFS_TS",
 "W_mm","R_mm","P_mm","D_pct","AP_mm2","AR_mm2","ZAT_mm","IC_pct","W_P","TD_kg_h","rend_pct",
 "banderas","confiabilidad","observaciones"]
M = []
def add(**k):
    row = {c: k.get(c) for c in COLS}
    M.append(row)

# ---------- P01/P02 SREERAJ (16) ----------
lvS = {'V':{1:20,2:22,3:24,4:25},'I':{1:87,2:123,3:138,4:155},'N':{1:15,2:20,3:25,4:30},'T':{1:25,2:40,3:50,4:53}}
S_cod=[(1,1,1,1),(1,2,2,2),(1,3,3,3),(1,4,4,4),(2,1,2,3),(2,2,1,4),(2,3,4,1),(2,4,3,2),
       (3,1,3,4),(3,2,4,3),(3,3,1,2),(3,4,2,1),(4,1,4,2),(4,2,3,1),(4,3,2,4),(4,4,1,3)]
S_resp=[(8.306,1.235,2.815,17.623),(8.243,1.347,2.543,17.462),(8.731,1.388,2.675,17.842),(8.925,1.425,2.931,17.442),
 (9.792,1.657,2.449,18.332),(10.415,1.586,2.779,16.692),(8.869,1.456,2.863,17.823),(8.614,1.738,2.597,20.424),
 (8.908,1.416,2.538,17.912),(9.371,1.537,2.397,18.182),(9.087,1.465,2.432,18.218),(8.853,1.368,2.672,17.512),
 (9.125,1.487,2.423,18.221),(8.753,1.398,2.567,17.943),(8.971,1.457,2.697,17.841),(9.807,1.868,2.243,21.512)]
for i,((v,ii,n,t),(W,P,R,D)) in enumerate(zip(S_cod,S_resp),1):
    add(registro_id=f"SREERAJ2014-r{i}",paper_id="14_Sreeraj2014",run_id_original=i,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="BOP",posicion="plana",nivel_uso="parcial",
        metal_base="IS 2062",espesor_mm=6,alambre_clase="E71T-1C rutilico",alambre_diam_mm=1.2,
        gas_tipo="CO2 (inferido)",pct_CO2=100,polaridad="n/d",
        I_amp=lvS['I'][ii],I_medida="no",V_arco=lvS['V'][v],stickout_mm=lvS['N'][n],
        W_mm=W,R_mm=R,P_mm=P,D_pct=D,IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_T;flag_TS;flag_gas;flag_duplicado(SREERAJ2014-UTIL)",confiabilidad="media",
        observaciones=f"T publicada={lvS['T'][t]} mm/min: magnitud fisicamente inconsistente. Sin velocidad de avance")

# ---------- P06/P03/P21 conjunto 410NiMo (18) ----------
G_par=[(170,18.18,300,30,193.3,15.2,470),(200,20.00,300,33,182.2,26.4,770),(230,22.22,300,36,195.3,25.3,790),
 (230,20.00,350,30,215.4,25.4,750),(170,22.22,350,33,185.5,17.0,430),(200,18.18,350,36,191.4,25.5,670),
 (200,22.22,400,30,178.3,22.2,470),(230,18.18,400,33,209.9,27.8,700),(170,20.00,400,36,160.6,17.8,340)]
G_res=[[(9.240,4.750,1.970,51.407,8.220,33.140,19.874),(8.140,4.350,2.050,53.440,8.770,27.960,23.877)],
 [(10.690,4.110,2.340,38.447,12.480,32.600,27.684),(11.040,4.090,2.690,37.047,13.970,29.870,31.866)],
 [(11.460,3.420,2.230,29.843,12.190,30.330,28.669),(11.510,3.590,2.150,31.190,11.370,30.950,26.867)],
 [(10.060,3.560,2.540,35.388,11.420,26.920,29.786),(10.130,3.610,2.550,35.637,11.560,26.600,30.294)],
 [(8.130,4.110,1.880,50.554,8.500,23.990,26.162),(7.920,4.200,1.860,53.030,7.750,25.180,23.535)],
 [(10.480,3.710,2.820,35.401,13.930,28.230,33.041),(9.860,3.650,2.500,37.018,11.500,26.060,30.618)],
 [(9.810,3.320,2.070,33.843,9.750,23.170,29.617),(9.630,3.270,2.480,33.956,11.950,22.010,35.188)],
 [(9.750,3.520,2.080,36.103,10.660,23.290,31.399),(10.040,3.140,2.130,31.275,10.720,22.230,32.534)],
 [(8.980,3.400,1.980,37.862,9.750,20.540,32.189),(9.120,3.250,1.590,35.636,8.050,20.880,27.826)]]
for c,((Im,pf,ts,ct,Irms,Urms,Q),reps) in enumerate(zip(G_par,G_res),1):
    for rp,(W,R,P,IC,AP,AR,D) in zip("ab",reps):
        add(registro_id=f"GUIMARAES2020-c{c}{rp}",paper_id="22_Guimaraes2020",run_id_original=c,replica=rp,tipo_registro="corrida",
            conjunto="pulsado",variante="FCAW-G",aplicacion="cladding",posicion="plana",nivel_uso="completo",
            metal_base="SAE 1020",espesor_mm=12.7,alambre_clase="EC410NiMo metal-cored",alambre_diam_mm=1.2,
            gas_tipo="Ar+2%O2",pct_CO2=0,caudal_L_min=18,polaridad="DCEP",
            I_amp=Irms,I_medida="si",V_arco=Urms,WFS_m_min=8.5,TS_mm_s=r2(ts/60,3),CTWD_mm=ct,
            f_pulso_Hz=pf,temp_precal_C=200,
            HI_J_mm=Q,A_dep_mm2=r2(adep(PHI["metal_cored"],1.2,8500,ts),2),WFS_TS=r2(8500/ts,2),
            W_mm=W,R_mm=R,P_mm=P,D_pct=D,AP_mm2=AP,AR_mm2=AR,IC_pct=IC,W_P=r2(W/P,2),
            banderas="flag_pulsado;flag_duplicado(MORENO2022-PULS;MORENO2022-MAT);flag_Ip;flag_caudal",
            confiabilidad="alta",observaciones=f"Im ajustada={Im} A vs Irms medida={Irms} A. Q con k=0.8 ISO/TR 17671-1")

# ---------- P05 KURTULMUS (3) ----------
for i,(I,V,Q,P,W,R,ang,At,Am,Ad) in enumerate([(200,26.5,1140,2.17,12.55,3.58,41,42.60,15.78,26.82),
        (255,26.5,1453,3.15,12.57,4.88,64,64.06,20.26,43.79),(255,32.0,1754,3.15,16.39,3.54,37,65.20,26.87,38.33)],1):
    wfs=Ad*4*60/((math.pi/4)*1.2**2)/1000*PHI["rutilico"]
    add(registro_id=f"KURTULMUS2015-r{i}",paper_id="15_Kurtulmus2015",run_id_original=i,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="BOP",posicion="plana",nivel_uso="completo",
        metal_base="SAE 1015",espesor_mm=10,alambre_clase="E71T-5 basico",alambre_diam_mm=1.2,
        gas_tipo="CO2",pct_CO2=100,caudal_L_min=12,polaridad="n/d",
        I_amp=I,I_medida="no",V_arco=V,TS_mm_s=4.0,CTWD_mm=19.5,angulo_deg=80,
        HI_J_mm=r2(hi(V,I,4.0,K_ETA),0),W_mm=W,R_mm=R,P_mm=P,D_pct=r2(Am/At*100,2),AP_mm2=Am,AR_mm2=Ad,
        IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_HI_recalculado_k080;flag_n_bajo;flag_OFAT;flag_promedio",confiabilidad="alta",
        observaciones=f"HI publicado={Q} J/mm (eta implicita 0.86); columna recalculada con k=0.80. Promedio de 12 mediciones. HI con eta=0.86 declarado por el autor. Dilucion derivada de Am/At. Angulo de mojado={ang} grados")

# ---------- P07 SADEK (9) ----------
SA=[("A-1","Ar",0,350,23,6.0,10.81,4.69,2.19,"si"),("A-2","Ar",0,350,25,5.0,11.88,4.69,1.92,"no"),
 ("A-3","Ar",0,350,29,4.5,12.73,4.54,1.78,"no"),("B-1","CO2",100,380,23,4.5,11.39,3.10,1.45,"no"),
 ("B-2","CO2",100,380,25,5.0,11.11,3.10,1.39,"no"),("B-3","CO2",100,380,28,4.0,9.33,2.93,1.33,"no"),
 ("C-1","Ar",0,380,25,8.0,23.60,6.22,2.70,"si"),("C-2","Ar",0,380,25,6.0,15.19,5.60,2.59,"si"),
 ("C-3","Ar",0,380,25,4.0,8.00,3.60,1.11,"no")]
SA_ts=[620,620,620,620,620,620,254,600,1000]
for (rid,g,pc,I,ct,P,W,R,z,crack),ts in zip(SA,SA_ts):
    add(registro_id=f"SADEK2001-{rid}",paper_id="01_Sadek2001",run_id_original=rid,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="BOP",posicion="plana",nivel_uso="parcial",
        metal_base="C-Mn",espesor_mm=12,alambre_clase="E71T-5 basico",alambre_diam_mm=1.2,
        gas_tipo=g,pct_CO2=pc,caudal_L_min=7.5 if g=="Ar" else 11,polaridad="DCEP",
        I_amp=I,I_medida="no",V_arco=29.5,TS_mm_s=r2(ts/60,2),CTWD_mm=ct,
        HI_J_mm=r2(hi(29.5,I,ts/60,K_ETA),0),W_mm=W,R_mm=R,P_mm=P,ZAT_mm=z,
        IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_escaneado;flag_voltaje_rango;flag_mapeo;flag_sin_areas;flag_HI_recalculado_k080"+(";flag_WD_A1" if rid=="A-1" else ""),
        confiabilidad="media",observaciones=f"Voltaje declarado como rango 29-30V; se adopta 29.5. Agrietamiento en caliente: {crack}")

# ---------- P08 KUMAR (32) ----------
lvK={'I':{-2:150,-1:175,0:200,1:225,2:250},'S':{-2:22,-1:24,0:26,1:28,2:30},'V':{-2:30,-1:32,0:34,1:36,2:38},
     'N':{-2:14,-1:17,0:20,1:23,2:26},'A':{-2:5,-1:10,0:15,1:20,2:25}}
KU=[("v1",-1,-1,-1,-1,1,24.20,4.05,0.98,14.72),("v2",1,-1,-1,-1,-1,29.75,4.78,1.05,11.65),("v3",-1,1,-1,-1,-1,24.38,3.60,1.18,19.91),
("v4",1,1,-1,-1,1,24.38,3.60,1.20,20.41),("v5",-1,-1,1,-1,-1,25.63,3.90,1.13,15.91),("v6",1,-1,1,-1,1,30.03,4.78,0.98,13.34),
("v7",-1,1,1,-1,1,24.15,3.73,0.83,14.73),("v8",1,1,1,-1,-1,29.85,4.23,1.15,14.49),("v9",-1,-1,-1,1,-1,24.23,4.08,0.90,11.54),
("v10",1,-1,-1,1,1,28.08,5.13,0.83,9.22),("v11",-1,1,-1,1,1,20.95,3.80,0.78,11.38),("v12",1,1,-1,1,-1,27.95,4.48,1.15,14.12),
("v13",-1,-1,1,1,1,23.10,3.65,0.85,12.47),("v14",1,-1,1,1,-1,29.98,4.68,1.23,16.41),("v15",-1,1,1,1,-1,26.00,3.88,0.95,18.34),
("v16",1,1,1,1,1,25.88,4.90,0.98,13.03),("v17",-2,0,0,0,0,17.80,4.05,0.80,10.42),("v18",2,0,0,0,0,26.48,5.63,1.05,11.02),
("v19",0,-2,0,0,0,27.70,4.58,1.00,13.28),("v20",0,2,0,0,0,22.63,4.28,1.43,15.94),("v21",0,0,-2,0,0,21.23,4.68,1.08,12.41),
("v22",0,0,2,0,0,27.80,3.60,0.93,16.71),("v23",0,0,0,-2,0,27.35,3.85,1.15,17.97),("v24",0,0,0,2,0,23.60,4.50,0.71,10.48),
("v25",0,0,0,0,-2,23.78,4.30,1.10,14.39),("v26",0,0,0,0,2,23.33,4.48,0.85,11.58),("v27",0,0,0,0,0,24.38,4.58,1.28,14.49),
("v28",0,0,0,0,0,24.80,4.53,1.15,13.77),("v29",0,0,0,0,0,24.50,4.63,1.25,14.55),("v30",0,0,0,0,0,23.15,4.58,1.18,14.02),
("v31",0,0,0,0,0,26.65,4.10,1.18,14.75),("v32",0,0,0,0,0,24.38,4.78,1.14,12.50)]
for (rid,i,s,v,n,a,W,R,P,D) in KU:
    I,S,OCV,N,A=lvK['I'][i],lvK['S'][s],lvK['V'][v],lvK['N'][n],lvK['A'][a]
    Wf=-6.92+0.0860*I
    add(registro_id=f"KUMAR2011-{rid}",paper_id="07_Kumar2011",run_id_original=rid,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="cladding",posicion="plana",nivel_uso="parcial",
        metal_base="IS 2062",espesor_mm=20,alambre_clase="317L inox rutilico",alambre_diam_mm=1.2,
        gas_tipo="n/d",polaridad="n/d",
        I_amp=I,I_medida="no",OCV_volt=OCV,WFS_m_min=r2(Wf,2),TS_mm_s=r2(S*10/60,3),NPD_mm=N,angulo_deg=A,
        A_dep_mm2=r2(adep(PHI["inox_rutilico"],1.2,Wf*1000,S*10),2),WFS_TS=r2(Wf*100/S,2),
        W_mm=W,R_mm=R,P_mm=P,D_pct=D,IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_OCV;flag_NPD;flag_gas;flag_sin_areas"+(";flag_v3v4" if rid in("v3","v4") else ""),
        confiabilidad="media",observaciones="OCV no es voltaje de arco: HI no calculable. WFS estimada con Wf=-6.92+0.0860*I (Palani 2007, mismo alambre 317L)")

# ---------- P11 GOMES (31) ----------
lwG={-2:5.5,-1:7.0,0:8.5,1:10.0,2:11.5}; lvG={-2:24.5,-1:27.0,0:29.5,1:32.0,2:34.5}
lsG={-2:20,-1:30,0:40,1:50,2:60}; lnG={-2:10,-1:15,0:20,1:25,2:30}
fac=[]
for n in(-1,1):
    for s in(-1,1):
        for v in(-1,1):
            for w in(-1,1): fac.append((w,v,s,n))
codG=fac+[(-2,0,0,0),(2,0,0,0),(0,-2,0,0),(0,2,0,0),(0,0,-2,0),(0,0,2,0),(0,0,0,-2),(0,0,0,2)]+[(0,0,0,0)]*7
GW=[11.19,12.99,12.70,15.05,9.21,9.96,9.75,11.51,10.32,11.43,11.27,13.34,7.99,8.62,8.48,10.84,9.07,12.21,9.42,11.69,14.93,8.48,11.73,9.22,10.82,10.93,10.74,10.61,10.64,10.59,10.57]
GP=[1.37,1.66,1.69,1.98,1.65,1.94,1.54,2.18,1.25,1.00,1.32,1.10,1.11,1.23,1.37,1.64,1.38,2.14,1.20,1.86,0.95,1.43,2.18,1.28,1.71,1.72,1.62,1.80,1.49,1.49,1.50]
GR=[2.63,3.12,2.50,2.78,2.17,2.67,2.06,2.42,2.87,None,2.85,3.18,2.55,2.80,2.36,2.60,2.21,3.06,3.03,2.46,None,2.25,2.61,2.89,2.60,2.59,2.65,2.50,2.62,2.61,2.56]
GD=[26.44,25.82,31.49,31.25,36.22,33.69,37.12,41.08,22.46,18.32,23.71,21.96,24.96,23.31,28.77,30.19,31.56,30.95,22.84,35.58,18.58,35.78,40.44,24.16,31.05,31.67,30.88,32.83,29.99,31.09,31.02]
GDR=[2.718,3.881,2.699,3.871,2.773,3.924,2.647,3.822,2.740,3.870,2.743,3.885,2.847,3.901,2.832,3.969,2.204,4.454,3.324,3.311,3.319,3.423,3.242,3.385,3.421,3.380,3.402,3.382,3.388,3.398,3.404]
GY=[89.74,89.71,89.14,89.47,91.58,90.70,87.43,88.36,90.49,89.47,90.60,89.81,94.03,90.17,93.52,91.74,92.62,89.52,90.41,90.04,90.27,93.08,88.15,92.05,93.04,91.91,92.51,91.98,92.15,92.40,92.58]
for i in range(31):
    w,v,s,n=codG[i]; Wf,V,S,N=lwG[w],lvG[v],lsG[s],lnG[n]
    add(registro_id=f"GOMES2012-r{i+1}",paper_id="08_Gomes2012",run_id_original=i+1,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="cladding",posicion="plana",nivel_uso="completo",
        metal_base="AISI 1020",alambre_clase="E316LT1 inox rutilico",alambre_diam_mm=1.2,gas_tipo="n/d",polaridad="n/d",
        I_medida="no",V_arco=V,WFS_m_min=Wf,TS_mm_s=r2(S*10/60,3),CTWD_mm=N,
        A_dep_mm2=r2(adep(PHI["inox_rutilico"],1.2,Wf*1000,S*10),2),WFS_TS=r2(Wf*100/S,2),
        W_mm=GW[i],R_mm=GR[i],P_mm=GP[i],D_pct=GD[i],TD_kg_h=GDR[i],rend_pct=GY[i],
        IC_pct=r2(GR[i]/GW[i]*100,2) if GR[i] else None,W_P=r2(GW[i]/GP[i],2),
        banderas="flag_signos_pdf;flag_gas;flag_4_mediciones"+(";flag_outlier_R" if GR[i] is None else ""),
        confiabilidad="alta",observaciones="Codigos reconstruidos por orden de Yates y validados contra los coeficientes publicados. Geometria promediada en 4 puntos. Sin corriente: HI no calculable")

# ---------- P12A DAVE FCAW (15) ----------
DF=[("F1",170,22,15,8.12,2.42,1.23,0.23),("F2",170,22,15,7.63,2.32,1.17,0.22),("F3",130,22,20,8.68,1.30,0.82,0.16),
("F4",170,24,20,9.59,1.50,1.35,0.29),("F5",130,22,10,5.40,1.31,0.83,0.14),("F6",170,20,20,8.39,2.21,1.16,0.11),
("F7",130,24,15,7.10,1.74,1.14,0.20),("F8",170,22,15,7.58,2.36,1.31,0.17),("F9",210,20,15,7.33,3.66,1.50,0.26),
("F10",210,22,10,9.26,3.44,1.91,0.36),("F11",130,20,15,5.87,1.23,0.63,0.12),("F12",170,20,10,5.44,1.74,0.86,0.17),
("F13",210,24,15,9.92,3.47,1.83,0.41),("F14",170,24,10,9.48,2.39,1.64,0.23),("F15",210,22,20,9.66,3.56,1.99,0.27)]
for (rid,I,V,G,W,H,P,Z) in DF:
    add(registro_id=f"DAVE2025-{rid}",paper_id="29_Dave2024",run_id_original=rid,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="BOP",posicion="1G",nivel_uso="parcial",
        metal_base="316LN",espesor_mm=8,alambre_clase="E316LT1-4 inox",alambre_diam_mm=1.2,
        gas_tipo="Ar-CO2",pct_CO2=20,caudal_L_min=G,polaridad="DCEP",
        I_amp=I,I_medida="no",V_arco=V,
        W_mm=W,R_mm=H,P_mm=P,ZAT_mm=Z,IC_pct=r2(H/W*100,2),W_P=r2(W/P,2),
        banderas="flag_sin_TS;flag_sin_WFS;flag_ZAT_dispersa;flag_sin_dilucion",confiabilidad="media",
        observaciones="Velocidad de avance NO reportada: HI y A_dep no calculables. TS estimada 3.5-3.8 mm/s desde el HI declarado (0.98 kJ/mm)")

# ---------- P12B DAVE RMD (15) - proceso comparativo ----------
DR_=[("S1",105,12,10,4.11,3.36,1.43,0.20),("S2",80,18,15,4.63,2.61,1.49,0.19),("S3",80,15,10,4.10,2.27,0.97,0.13),
("S4",130,15,20,9.12,4.13,1.79,0.23),("S5",105,15,15,6.87,3.81,1.31,0.24),("S6",130,18,15,9.21,4.51,1.84,0.35),
("S7",130,15,10,5.96,4.88,1.63,0.31),("S8",105,18,10,7.50,4.33,1.30,0.27),("S9",130,12,15,4.77,4.31,1.23,0.26),
("S10",105,15,15,6.66,3.81,1.26,0.22),("S11",105,18,20,6.85,4.07,1.87,0.28),("S12",105,12,20,6.46,3.48,0.69,0.19),
("S13",80,15,20,3.79,2.57,1.18,0.16),("S14",80,12,15,3.53,2.34,0.71,0.10),("S15",105,15,15,5.94,3.89,1.37,0.27)]
for (rid,I,V,G,W,H,P,Z) in DR_:
    add(registro_id=f"DAVE2025-{rid}",paper_id="29b_Dave2024",run_id_original=rid,tipo_registro="corrida",
        conjunto="comparativo",variante="RMD",aplicacion="BOP",posicion="1G",nivel_uso="referencia",
        metal_base="316LN",espesor_mm=8,alambre_clase="ER316L solido",alambre_diam_mm=1.2,
        gas_tipo="Ar-O2",pct_CO2=0,caudal_L_min=G,polaridad="DCEP",
        I_amp=I,I_medida="no",V_arco=V,W_mm=W,R_mm=H,P_mm=P,ZAT_mm=Z,IC_pct=r2(H/W*100,2),W_P=r2(W/P,2),
        banderas="flag_proceso_distinto;flag_sin_TS",confiabilidad="media",
        observaciones="PROCESO RMD, no FCAW. Solo para el capitulo comparativo")

# ---------- P13 BALASUBRAMANIAN (32) ----------
lvB={'V':{-2:30.0,-1:32.0,0:34.0,1:36.0,2:38.0},'F':{-2:9.0,-1:11.0,0:13.0,1:15.0,2:17.0},
     'S':{-2:0.18,-1:0.26,0:0.34,1:0.42,2:0.50},'D':{-2:17.0,-1:19.0,0:21.0,1:23.0,2:25.0},
     'E':{-2:5.0,-1:10.0,0:15.0,1:20.0,2:25.0}}
BA=[(1,-1,-1,-1,-1,1,8.6),(2,1,-1,-1,-1,-1,9.4),(3,-1,1,-1,-1,-1,8.6),(4,1,1,-1,-1,1,15.2),(5,-1,-1,1,-1,-1,11.1),
(6,1,-1,1,-1,1,10.6),(7,-1,1,1,-1,1,13.5),(8,1,1,1,-1,-1,9.6),(9,-1,-1,-1,1,-1,7.1),(10,1,-1,-1,1,1,12.9),
(11,-1,1,-1,1,1,6.4),(12,1,1,-1,1,-1,10.5),(13,-1,-1,1,1,1,11.4),(14,1,-1,1,1,-1,15.8),(15,-1,1,1,1,-1,11.8),
(16,1,1,1,1,1,14.9),(17,-2,0,0,0,0,8.3),(18,2,0,0,0,0,14.8),(19,0,-2,0,0,0,18.1),(20,0,2,0,0,0,10.7),
(21,0,0,-2,0,0,7.6),(22,0,0,2,0,0,21.1),(23,0,0,0,-2,0,16.4),(24,0,0,0,2,0,11.4),(25,0,0,0,0,-2,11.8),
(26,0,0,0,0,2,12.6),(27,0,0,0,0,0,12.4),(28,0,0,0,0,0,14.4),(29,0,0,0,0,0,14.3),(30,0,0,0,0,0,12.8),
(31,0,0,0,0,0,11.9),(32,0,0,0,0,0,15.2)]
for (n,v,f,s,d,e,D) in BA:
    OCV,F,S,N,A=lvB['V'][v],lvB['F'][f],lvB['S'][s],lvB['D'][d],lvB['E'][e]
    add(registro_id=f"BALASUB2025-r{n}",paper_id="27_Balasubramanian2023",run_id_original=n,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="cladding",posicion="plana",nivel_uso="solo_dilucion",
        metal_base="IS 2062",espesor_mm=20,alambre_clase="AISI 316L inox",alambre_diam_mm=1.2,gas_tipo="n/d",polaridad="n/d",
        I_medida="no",OCV_volt=OCV,WFS_m_min=F,TS_mm_s=r2(S*1000/60,3),NPD_mm=N,angulo_deg=A,
        A_dep_mm2=r2(adep(PHI["inox_rutilico"],1.2,F*1000,S*1000),2),WFS_TS=r2(F/S,2),
        D_pct=D,banderas="flag_una_respuesta;flag_OCV;flag_NPD;flag_sin_corriente;flag_gas;flag_material",
        confiabilidad="media",observaciones="Solo publica dilucion. Material designado 'AISI 2062'; corresponde a IS 2062. Resumen declara max 15.2% cuando la matriz contiene 21.1%")

# ---------- P14/P15 RODRIGUES-PAIVA (20) ----------
RP=[(1,235,29.0,10.0,15.0,1.89,3.62,82.49,32.10,38.76),(2,246,36.0,10.0,15.0,1.93,3.49,79.47,21.68,44.26),
(3,286,29.0,14.0,15.0,2.40,5.14,86.83,55.49,30.26),(4,300,36.0,14.0,15.0,2.88,5.28,86.03,26.10,45.13),
(5,220,29.0,10.0,20.0,1.55,3.74,82.82,29.58,35.51),(6,228,36.0,10.0,20.0,1.94,3.65,81.99,25.52,43.23),
(7,270,29.0,14.0,20.0,1.91,5.40,86.12,50.57,26.95),(8,212,36.0,14.0,20.0,2.85,4.52,85.58,24.70,43.67),
(9,255,26.6,12.0,17.5,1.90,4.63,86.21,50.00,26.88),(10,276,38.4,12.0,17.5,2.40,4.59,84.10,23.80,42.11),
(11,220,32.5,8.6,17.5,1.60,3.11,82.00,32.94,35.22),(12,319,32.5,15.4,17.5,3.40,6.06,89.12,44.21,44.37),
(13,287,32.5,12.0,13.3,2.80,4.88,85.37,25.05,41.66),(14,259,32.5,12.0,21.7,1.90,4.65,86.42,23.75,35.05),
(15,262,32.5,12.0,17.5,1.90,4.55,86.05,27.27,42.43),(16,267,32.5,12.0,17.5,2.28,4.25,83.51,24.91,42.19),
(17,262,32.5,12.0,17.5,2.30,4.37,84.82,26.85,42.65),(18,259,32.5,12.0,17.5,2.15,4.18,86.49,26.79,39.80),
(19,260,32.5,12.0,17.5,2.30,4.22,85.79,25.06,44.30),(20,278,32.5,12.0,17.5,2.35,4.50,86.08,27.15,45.10)]
for (n,Im,V,Va,d,P,TD,rend,IC,D) in RP:
    add(registro_id=f"PAIVA2010-r{n}",paper_id="06_Paiva2010",run_id_original=n,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="BOP",posicion="plana",nivel_uso="completo",
        metal_base="ABNT 1045",espesor_mm=9,alambre_clase="E71T-1 rutilico",alambre_diam_mm=1.2,
        gas_tipo="CO2",pct_CO2=100,caudal_L_min=15,polaridad="DCEP",
        I_amp=Im,I_medida="si",V_arco=V,WFS_m_min=Va,TS_mm_s=r2(500/60,3),CTWD_mm=d,
        HI_J_mm=r2(hi(V,Im,500/60,K_ETA),0),A_dep_mm2=r2(adep(PHI["rutilico"],1.2,Va*1000,500),2),WFS_TS=r2(Va/0.5,2),
        P_mm=P,D_pct=D,IC_pct=IC,TD_kg_h=TD,rend_pct=rend,
        banderas="flag_sin_W_R;flag_duplicado(RODRIGUES2009);flag_HI_recalculado_k080"+(";flag_corrida8" if n==8 else ""),
        confiabilidad="alta" if n!=8 else "baja",
        observaciones="Fuente de tension constante: la corriente se autoajusta. Solo publica IC=(h/b)*100, no separa W ni R"+(". ANOMALIA: Im=212A incompatible con P=2.85 y TD=4.52" if n==8 else ""))

# ---------- P16 PALANI RSM (20) ----------
lvP={'I':{-1.682:176,-1:190,0:210,1:230,1.682:244},'S':{-1.682:26,-1:29,0:34,1:39,1.682:42},'N':{-1.682:15,-1:17,0:20,1:23,1.682:25}}
PA=[(1,-1,-1,-1,0.80,4.50,9.43,3.77,1.38,11.788,2.096),(2,1,-1,-1,1.10,4.75,13.52,7.11,3.90,12.296,2.847),
(3,-1,1,-1,0.75,4.00,8.33,7.72,2.27,11.107,2.082),(4,1,1,-1,1.00,4.25,12.07,10.00,5.61,12.075,2.841),
(5,-1,-1,1,0.90,4.65,9.47,9.18,3.63,10.522,2.036),(6,1,-1,1,1.10,4.85,12.00,8.08,3.23,10.909,2.474),
(7,-1,1,1,0.75,4.10,9.35,7.52,2.30,12.467,2.280),(8,1,1,1,0.76,4.38,11.80,4.48,2.32,15.526,2.697),
(9,-1.682,0,0,0.70,4.12,8.69,7.95,2.54,12.429,2.112),(10,1.682,0,0,1.00,4.70,13.58,7.39,4.08,13.575,2.889),
(11,0,-1.682,0,1.10,5.10,12.03,6.92,3.71,10.932,2.358),(12,0,1.682,0,0.98,4.25,10.00,5.99,2.22,10.204,2.353),
(13,0,0,-1.682,0.90,4.50,11.00,5.68,2.91,12.222,2.444),(14,0,0,1.682,0.85,4.53,12.00,7.45,3.14,14.118,2.649),
(15,0,0,0,0.98,4.40,10.63,6.81,2.77,10.842,2.415),(16,0,0,0,1.00,4.50,10.00,8.11,2.72,10.000,2.222),
(17,0,0,0,0.95,4.24,10.15,7.00,2.30,10.684,2.394),(18,0,0,0,0.94,4.35,10.26,7.66,2.84,10.920,2.359),
(19,0,0,0,0.95,4.49,11.00,6.85,2.05,11.579,2.453),(20,0,0,0,1.00,4.60,9.41,8.00,3.21,9.410,2.046)]
comp={1:"PALANI2006-TAGUCHI-r1",7:"PALANI2006-TAGUCHI-r3",4:"PALANI2006-TAGUCHI-r9"}
for (n,i,s,nn,P,R,W,D,AP,pa,pe) in PA:
    I,S,N=lvP['I'][i],lvP['S'][s],lvP['N'][nn]; Wf=-6.92+0.0860*I
    add(registro_id=f"PALANI2007-r{n}",paper_id="04_Palani2007",run_id_original=n,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="cladding",posicion="plana",nivel_uso="parcial",
        metal_base="IS 2062",espesor_mm=20,alambre_clase="317L inox rutilico",alambre_diam_mm=1.2,
        gas_tipo="Ar-CO2",pct_CO2=5,caudal_L_min=16,polaridad="DCEP",angulo_deg=90,
        I_amp=I,I_medida="no",WFS_m_min=r2(Wf,2),TS_mm_s=r2(S*10/60,3),NPD_mm=N,
        A_dep_mm2=r2(adep(PHI["inox_rutilico"],1.2,Wf*1000,S*10),2),WFS_TS=r2(Wf*100/S,2),
        W_mm=W,R_mm=R,P_mm=P,D_pct=D,AP_mm2=AP,IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_sin_voltaje;flag_NPD"+(";flag_axial_S" if n in(9,10) else "")+(f";flag_solapa({comp[n]})" if n in comp else ""),
        confiabilidad="alta",observaciones="Promedio de 2 secciones. Wf estimada con la ecuacion del propio paper. phi_a=W/P y phi_e=W/R verificados 20/20"+(". Codigo de S corregido de 1 a 0 por estructura del CCD" if n in(9,10) else ""))

# ---------- P20 PALANI TAGUCHI (9, de las cuales 3 solapan) ----------
lvT={'I':{1:190,2:210,3:230},'S':{1:290,2:340,3:390},'N':{1:17,2:20,3:23}}
PT=[(1,1,1,1,(0.77,0.83),(4.5,4.5),(9.5,9.3),(4.31,3.29)),(2,1,2,2,(0.9,1.0),(3.8,3.7),(10.0,9.95),(10.60,10.54)),
(3,1,3,3,(0.8,0.75),(4.1,4.1),(8.8,9.9),(7.19,7.81)),(4,2,1,3,(1.1,1.05),(5.15,5.2),(12.3,12.18),(6.28,5.73)),
(5,2,2,1,(1.1,1.3),(3.5,3.4),(9.7,9.9),(10.50,12.72)),(6,2,3,2,(0.85,0.95),(3.35,3.35),(10.1,10.08),(8.45,10.07)),
(7,3,1,2,(0.4,0.5),(4.5,4.51),(14.3,14.4),(4.63,5.56)),(8,3,2,3,(1.05,1.1),(4.5,4.46),(12.2,12.5),(9.82,9.24)),
(9,3,3,1,(1.1,0.9),(4.0,4.05),(12.06,12.1),(9.5,10.5))]
solapa={1:"PALANI2007-r1",3:"PALANI2007-r7",9:"PALANI2007-r4"}
for (n,i,s,nn,Ps,Rs,Ws,Ds) in PT:
    I,S,N=lvT['I'][i],lvT['S'][s],lvT['N'][nn]; Wf=-6.92+0.0860*I
    P,R,W,D=sum(Ps)/2,sum(Rs)/2,sum(Ws)/2,sum(Ds)/2
    add(registro_id=f"PALANI2006-r{n}",paper_id="03_Palani2006",run_id_original=n,tipo_registro="corrida",
        conjunto="principal" if n not in solapa else "solapado",variante="FCAW-G",aplicacion="cladding",
        posicion="plana",nivel_uso="parcial" if n not in solapa else "duplicado",
        metal_base="IS 2062",espesor_mm=20,alambre_clase="317L inox rutilico",alambre_diam_mm=1.2,
        gas_tipo="Ar-CO2",pct_CO2=5,caudal_L_min=16,polaridad="DCEP",angulo_deg=90,
        I_amp=I,I_medida="no",WFS_m_min=r2(Wf,2),TS_mm_s=r2(S/60,3),NPD_mm=N,
        A_dep_mm2=r2(adep(PHI["inox_rutilico"],1.2,Wf*1000,S),2),WFS_TS=r2(Wf*1000/S,2),
        W_mm=r2(W,3),R_mm=r2(R,3),P_mm=r2(P,3),D_pct=r2(D,3),IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_sin_voltaje;flag_NPD;flag_replicas_publicadas"+(f";flag_solapa({solapa[n]})" if n in solapa else ""),
        confiabilidad="alta",observaciones=f"Media de 2 replicas. Individuales: P={Ps} R={Rs} W={Ws} D={Ds}"+(". NO CONTAR: condicion identica a "+solapa[n] if n in solapa else ""))

# ---------- P22 KATHERASAN (25) ----------
KA=[(1,7,19,5,50,8.034,2.356,2.814),(2,7,21,6,60,8.623,2.485,3.843),(3,7,23,7,70,8.931,2.674,3.876),
(4,7,25,8,80,8.527,2.745,3.334),(5,7,27,9,90,8.234,2.789,3.487),(6,8,19,6,70,8.723,2.945,4.315),
(7,8,21,7,80,8.965,2.864,3.893),(8,8,23,8,90,9.167,2.654,3.756),(9,8,25,9,50,9.583,2.479,3.032),
(10,8,27,5,60,8.869,2.987,4.067),(11,9,19,7,90,8.783,2.843,3.912),(12,9,21,8,50,9.267,2.489,2.889),
(13,9,23,9,60,8.935,2.681,3.445),(14,9,25,5,70,8.347,2.712,4.889),(15,9,27,6,80,8.587,2.567,4.553),
(16,10,19,8,60,8.743,2.145,3.564),(17,10,21,9,70,8.845,2.647,4.078),(18,10,23,5,80,8.384,2.741,4.378),
(19,10,25,6,90,8.457,2.856,4.583),(20,10,27,7,50,9.987,2.146,2.932),(21,11,19,9,80,9.267,2.216,3.348),
(22,11,21,5,90,8.932,2.347,4.392),(23,11,23,6,50,9.124,2.045,3.641),(24,11,25,7,60,9.256,2.249,3.994),
(25,11,27,8,70,9.016,2.198,3.826)]
for (n,F,V,S,A,W,R,P) in KA:
    add(registro_id=f"KATHERASAN2012-r{n}",paper_id="09_Katherasan2012",run_id_original=n,tipo_registro="corrida",
        conjunto="principal",variante="FCAW-G",aplicacion="BOP",posicion="plana",nivel_uso="parcial",
        metal_base="316L(N)",espesor_mm=8,alambre_clase="316LT inox",alambre_diam_mm=1.2,
        gas_tipo="Ar",pct_CO2=0,caudal_L_min=15,polaridad="n/d",
        I_medida="no",V_arco=V,WFS_m_min=F,TS_mm_s=S,stickout_mm=15,angulo_deg=A,
        A_dep_mm2=r2(adep(PHI["inox_rutilico"],1.2,F*1000,S*60),2),WFS_TS=r2(F*1000/(S*60),2),
        W_mm=W,R_mm=R,P_mm=P,IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_replicas_ambiguo;flag_sin_corriente;flag_gas_atipico;flag_sin_dilucion;flag_stickout",
        confiabilidad="media",observaciones="Encabezado declara 5 replicas por combinacion; el texto declara 25 soldaduras. Ar puro con alambre tubular es atipico. Sin corriente: HI no calculable")

# ---------- P17 CAVALCANTE (16) - subgrupo excluido ----------
CA=[(1,28,10,30,11.58,4.30,37.12,45.79,11.14),(2,28,10,50,10.12,3.40,33.61,28.32,12.07),
(3,28,14,30,15.28,4.78,31.28,71.41,26.20),(4,28,14,50,15.03,4.17,27.74,51.11,26.85),
(5,32,10,30,13.97,3.77,26.99,58.41,19.12),(6,32,10,50,12.32,3.33,27.04,33.58,16.75),
(7,32,14,30,16.17,4.55,28.14,66.87,24.00),(8,32,14,50,14.53,3.83,26.35,46.41,18.30),
(9,28,12,40,14.58,3.80,26.06,42.04,19.00),(10,32,12,40,15.27,3.93,25.74,43.67,24.66),
(11,30,10,40,11.07,4.13,37.32,32.19,10.19),(12,30,14,40,13.48,4.28,31.74,43.61,18.07),
(13,30,12,30,16.37,4.30,26.27,55.54,28.20),(14,30,12,50,13.67,3.28,24.00,38.41,18.66),
(15,30,12,40,14.20,4.08,28.73,43.76,17.17),(16,30,12,40,14.67,3.85,26.25,49.83,17.17)]
for (n,U,Va,Vs,L,R,RL,Ar,Af) in CA:
    add(registro_id=f"CAVALCANTE2020-r{n}",paper_id="21_Cavalcante2020",run_id_original=n,tipo_registro="corrida",
        conjunto="excluido",variante="FCAW-S",aplicacion="recargue_duro",posicion="plana",nivel_uso="subgrupo",
        metal_base="SAE 1020",espesor_mm=10,alambre_clase="FeCrC+Nb recargue",alambre_diam_mm=1.6,
        gas_tipo="ninguno",polaridad="n/d",
        I_medida="no",V_arco=U,WFS_m_min=Va,TS_mm_s=r2(Vs*10/60,3),CTWD_mm=35,
        WFS_TS=r2(Va*100/Vs,2),W_mm=L,R_mm=R,D_pct=r2(Af/(Ar+Af)*100,2),AP_mm2=Af,AR_mm2=Ar,IC_pct=RL,
        banderas="flag_autoprotegido;flag_diametro_1_6;flag_recargue_duro;flag_sin_corriente;flag_sin_penetracion;flag_phi_no_aplicable"+(";flag_Af_identico" if n in(15,16) else ""),
        confiabilidad="media",observaciones="AUTOPROTEGIDO: excluido del modelo principal. 3 cortes promediados. Dilucion derivada de Af/(Ar+Af). phi=0.81 NO aplicable a este consumible")

# ---------- P09 ZHANG (4) - subgrupo excluido ----------
ZH=[("A-aire","aire",30,193.3,1052,5265,13.8,2.1,3.5),("A-agua","agua",30,163.6,980,4907,11.8,2.7,3.9),
    ("B-aire","aire",31,174.4,1080,5407,15.8,1.8,3.2),("B-agua","agua",31,158.5,982,4915,10.2,2.6,4.2)]
for (rid,ent,V,Iest,Q,Pef,W,P,R) in ZH:
    add(registro_id=f"ZHANG2016-{rid}",paper_id="18_Zhang2016",run_id_original=rid,tipo_registro="corrida",
        conjunto="excluido",variante="FCAW-S",aplicacion="BOP",posicion=f"plana/{ent}",nivel_uso="subgrupo",
        metal_base="Q235",espesor_mm=8,alambre_clase="rutilico subacuatico",alambre_diam_mm=1.6,
        gas_tipo="ninguno",polaridad="DCEP",
        I_amp=Iest,I_medida="estimada",V_arco=V,WFS_m_min=r2(6.32*0.6,2),TS_mm_s=4.0,
        HI_J_mm=Q,WFS_TS=r2(3792/240,2),W_mm=W,R_mm=R,P_mm=P,IC_pct=r2(R/W*100,2),W_P=r2(W/P,2),
        banderas="flag_autoprotegido;flag_subacuatico;flag_I_estimada;flag_eta_080;flag_diametro_inferido;flag_promedio",
        confiabilidad="media",observaciones=f"Entorno: {ent}. Q=eta*P_ef/v con eta=0.8 y P_ef={Pef} W (integral instantanea). Corriente estimada como P_ef/V. Penetracion fluctua 15-22% a lo largo del cordon")

# ---------- P19 validaciones 3F ----------
V3=[("3F-1","<1mm",150,26,4.0,0.98,10.9,7.65,4.20,0.30),("3F-2","1-3mm",300,30,14.0,0.66,7.50,5.90,4.50,2.50),
    ("3F-3",">3mm",250,26,9.6,0.68,7.10,4.70,6.50,4.50)]
for (rid,cat,I,V,v,Q,BW,leg,T,P) in V3:
    add(registro_id=f"RAHMAN2014-3F-{rid}",paper_id="11_Rahman2014",run_id_original=rid,tipo_registro="validacion",
        conjunto="excluido",variante="FCAW-G",aplicacion="filete",posicion="3F vertical descendente",nivel_uso="contraste",
        metal_base="acero bajo carbono",espesor_mm=9,alambre_clase="tubular",alambre_diam_mm=1.2,
        gas_tipo="CO2",pct_CO2=99.9,polaridad="n/d",
        I_amp=I,I_medida="no",V_arco=V,TS_mm_s=v,stickout_mm=15,HI_J_mm=r2(hi(V,I,v,K_ETA),0),W_mm=BW,P_mm=P,
        banderas="flag_posicion_3F;flag_respuestas_filete;flag_HI_invertido;flag_vernier;flag_HI_recalculado_k080",
        confiabilidad="baja",observaciones=f"HI publicado={Q} kJ/mm (sin eficiencia); columna recalculada con k=0.80. Categoria: {cat}. Pierna={leg} mm, garganta={T} mm (magnitudes de filete). HI mayor produce MENOR penetracion: efecto de gravedad en vertical descendente")
