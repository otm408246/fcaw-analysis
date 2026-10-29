# -*- coding: utf-8 -*-
"""Recupera DOI, autores completos, revista y AFILIACIONES desde OpenAlex."""
import json, re, time, urllib.parse, urllib.request, os, unicodedata, difflib

KEY  = os.environ.get("OA_KEY","")
MAIL = os.environ.get("CONTACT_EMAIL", "")

TITULOS = {
"P01_SREERAJ2014-UTIL":"Analysis and parametric optimization of flux cored arc welding process for IS 2062 mild steel plates using Taguchi and utility concept",
"P02_SREERAJ2014-HYB":"Analysis of flux cored arc welding process parameters by hybrid taguchi approach",
"P03_MORENO2022-PULS":"Analyze and Optimize the Welding Parameters of the Process by Pulsed Tubular Wire FCAW Based on the Geometry of the Weld Beads",
"P04_RAHMAN2014-2F":"Correlation between Welding Parameter and Bead Geometry of Flux Cored Arc Welding FCAW In Horizontal Position",
"P05_KURTULMUS2015":"Effects of welding current and arc voltage on FCAW weld bead geometry",
"P06_GUIMARAES2020":"Estudo dos parametros de soldagem em um revestimento de aco martensitico 410 NiMo pelo processo FCAW pulsado",
"P07_SADEK2001":"Effect of welding parameters of FCAW process and shielding gas type on weld bead geometry and hardness distribution",
"P08_KUMAR2011":"Effect of FCAW Process Parameters on Weld Bead Geometry in Stainless Steel Cladding",
"P09_ZHANG2016":"Heat input and metal transfer influences on the weld geometry and microstructure during underwater wet FCAW",
"P10_BECZKOWSKI2018":"Influence of cladding parameters with FCAW on bead geometry with Plackett-Burman experiment",
"P11_GOMES2012":"Mathematical modeling of weld bead geometry quality and productivity for stainless steel claddings deposited by FCAW",
"P12A_DAVE2025-FCAW":"Multiobjective optimization of welding process variables in RMD and FCAW techniques using a heat transfer search algorithm for 316LN stainless steel",
"P13_BALASUB2025":"Optimization of flux cored arc welding parameters to minimize the dilution percentage of AISI 316L stainless steel cladding on mild steel",
"P14_RODRIGUES2009":"Optimization of the FCAW process by weld bead geometry analysis",
"P15_PAIVA2010":"Otimizacao do processo de soldagem FCAW usando o erro quadratico medio multivariado",
"P16_PALANI2007-RSM":"Optimization of weld bead geometry for stainless steel claddings deposited by FCAW",
"P17_CAVALCANTE2020":"Otimizacao de parametros operacionais do processo de soldagem FCAW para aplicacao em revestimento duro",
"P18_RAZAK2017-1G":"Prediction of Flux Core Arc Welding FCAW Bead Geometry and Welding Parameters for 1G Position",
"P19_RAHMAN2014-3F":"Prediction of Flux Cored Arc Welding FCAW Parameters And Bead Geometry In Downhill Position",
"P20_PALANI2006-TAGUCHI":"Process parameter selection for optimising weld bead geometry in stainless steel cladding using Taguchi approach",
"P21_MORENO2022-MAT":"Pulsed FCAW of Martensitic Stainless Clads onto Mild Steel Microstructure Hardness and Residual Stresses",
"P22_KATHERASAN2012":"Simulation and parameter optimization of flux cored arc welding using artificial neural network and particle swarm optimization algorithm",
"N01_KANNAN2006-DUPLEX":"Effect of flux cored arc welding process parameters on duplex stainless steel clad quality",
"N02_BALAN2018-FC2507":"Optimization of cladding parameters for resisting corrosion on low carbon steels using simulated annealing algorithm",
"N03_SENTHILKUMAR2014-2507":"Effect of Flux Cored Arc Welding process parameters on bead geometry in super duplex stainless steel claddings",
"N05_SINGH2021-201LN":"Study of weld bead characteristics and optimization during FCAW of AISI 201LN",
"N07_ODHIAMBO2025-API5L":"Optimization of Flux Cored Arc Welding Parameters using Artificial Neural Networks for ASTM A335 Grade B API 5L Schedule 40 Pipes",
"N08_YADAV2022-308L":"Effect of input parameters on weld bead geometry and weld dilution for weld surfacing of flux cored 308L stainless steel on low carbon steel",
"N09_SENTHILKUMAR2015-L9":"Optimization of flux-cored arc welding process parameters by using genetic algorithm",
"N10_ALORAIER2025-PRECAL":"Analysis of the combined effects of preheating and welding wire feed rates on the FCAW bead geometric characteristics of 1020 steel",
"N12_SOLOVYOV2023-FCAWS":"Vykorystannia neironnykh merezh dlia kontroliu ta keruvannia rezhymamy duhovoho naplavlennia poroshkovymy drotamy",
}

def norm(s):
    s=unicodedata.normalize("NFKD",(s or "").lower())
    s="".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+"," ",s).strip()

def buscar(titulo):
    p={"search":titulo,"mailto":MAIL,"per-page":"5"}
    if KEY: p["api_key"]=KEY
    u="https://api.openalex.org/works?"+urllib.parse.urlencode(p)
    r=urllib.request.Request(u,headers={"User-Agent":"thesis/1.0"})
    try:
        d=json.load(urllib.request.urlopen(r,timeout=60))
    except Exception as e:
        return None,str(e)
    nt=norm(titulo); mejor=None;sc=0
    for w in d.get("results",[]):
        s=difflib.SequenceMatcher(None,nt,norm(w.get("display_name"))).ratio()
        if s>sc: mejor,sc=w,s
    return (mejor,round(sc,2)) if sc>=0.62 else (None,f"sin match (mejor {sc:.2f})")

OUT={}
for k,t in TITULOS.items():
    w,info=buscar(t); time.sleep(0.25)
    if not w:
        OUT[k]=dict(estado="NO_ENCONTRADO",nota=info); print(f"  {k[:30]:30s} -> {info}"); continue
    auts=[a["author"]["display_name"] for a in w.get("authorships",[])]
    afil=[]
    for a in w.get("authorships",[]):
        for inst in a.get("institutions",[]):
            n=inst.get("display_name"); c=inst.get("country_code")
            if n and (n,c) not in afil: afil.append((n,c))
    loc=w.get("primary_location") or {}
    src=(loc.get("source") or {})
    OUT[k]=dict(estado="OK",similitud=info,
        titulo=w.get("display_name"), anio=w.get("publication_year"),
        doi=(w.get("doi") or "").replace("https://doi.org/",""),
        autores="; ".join(auts), n_autores=len(auts),
        revista=src.get("display_name"), issn=(src.get("issn_l") or ""),
        volumen=w.get("biblio",{}).get("volume"), paginas=(w.get("biblio",{}).get("first_page") or "")+"-"+(w.get("biblio",{}).get("last_page") or ""),
        tipo=w.get("type"), citas=w.get("cited_by_count"),
        acceso_abierto=bool((w.get("open_access") or {}).get("is_oa")),
        url_oa=(w.get("open_access") or {}).get("oa_url") or "",
        instituciones="; ".join(f"{n} ({c})" for n,c in afil),
        pais=", ".join(sorted({c for _,c in afil if c})),
        openalex_id=w.get("id","").split("/")[-1])
    print(f"  {k[:30]:30s} -> {w.get('publication_year')} | {OUT[k]['doi'] or 'sin DOI'} | {OUT[k]['pais']}")

json.dump(OUT, open("metadatos_openalex.json","w"), ensure_ascii=False, indent=1)
ok=sum(1 for v in OUT.values() if v["estado"]=="OK")
print(f"\nrecuperados {ok}/{len(TITULOS)} | con DOI: {sum(1 for v in OUT.values() if v.get('doi'))}")
print(f"con afiliacion: {sum(1 for v in OUT.values() if v.get('instituciones'))}")
import os
