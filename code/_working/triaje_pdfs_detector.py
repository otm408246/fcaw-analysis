# -*- coding: utf-8 -*-
# Recuperado de la transcripcion de la sesion 59e7b4a7 (agosto 2026): detector de tablas de datos en PDF
# que produjo _busqueda/TRIAJE_nueva.csv. Se conserva como documentacion de las columnas ver/seq/resp/dis/nnum/pag/arch.
import fitz, os, re, csv, sys

ARCH=os.environ.get("FCAW_ARCHIVOS", ".")  # folder with the PDFs (not distributed: copyright)
RESP={"W":r"bead width|weld width|\bwidth\b","P":r"penetration|\bdop\b","R":r"reinforc",
      "D":r"dilut","A":r"penetration area|reinforcement area|\bap\b|\bar\b","S":r"wpsf|wrff|shape factor|form factor"}
DIS=r"central composite|box[- ]behnken|taguchi|orthogonal|factorial|response surface|plackett|\bl9\b|\bl16\b|\bl25\b|\bl27\b"

def seq_ascendente(lineas):
    """en texto extraido por columnas, la col. de No. de corrida aparece
       como enteros aislados 1,2,3... en lineas consecutivas o cercanas"""
    idx=[(i,int(l.strip())) for i,l in enumerate(lineas)
         if re.fullmatch(r"\d{1,2}", l.strip()) and 1<=int(l.strip())<=60]
    mejor=0
    for a in range(len(idx)):
        if idx[a][1]!=1: continue
        esp=1; last=idx[a][0]
        for b in range(a+1,len(idx)):
            if idx[b][1]==esp+1 and idx[b][0]-last<60:
                esp+=1; last=idx[b][0]
        mejor=max(mejor,esp)
    return mejor

def analizar(p):
    d=fitz.open(p); npg=len(d)
    txt="\n".join(pg.get_text() for pg in d); d.close()
    car=len(txt)
    if car/max(npg,1)<300: return dict(esc=True,pag=npg)
    lin=txt.split("\n")
    nnum=sum(1 for l in lin if re.fullmatch(r"[-+]?\d{1,5}[.,]?\d*",l.strip()))
    low=txt.lower()
    return dict(esc=False,pag=npg,seq=seq_ascendente(lin),nnum=nnum,
                resp="".join(sorted(k for k,pt in RESP.items() if re.search(pt,low))),
                dis=",".join(sorted(set(re.findall(DIS,low))))[:30])

def veredicto(a):
    if a.get("esc"): return "ESCANEADO"
    s,r = a["seq"], len(a["resp"])
    if s>=9 and r>=3: return "SI"
    if s>=6 and r>=3: return "PROBABLE"
    if s>=9 and r>=2: return "PROBABLE"
    if r>=3 and a["nnum"]>150: return "REVISAR"
    return "NO"

# ---------- validacion sobre los 22 que SI tienen tablas ----------
print("### VALIDACION DEL DETECTOR sobre los 22 ya transcritos ###")
V=os.path.join(ARCH,"papers_FCAW"); ok=0; tot=0
for f in sorted(os.listdir(V)):
    if not f.lower().endswith(".pdf"): continue
    tot+=1; a=analizar(os.path.join(V,f)); v=veredicto(a)
    if v in ("SI","PROBABLE"): ok+=1
    else: print(f"   fallo->{v:9s} seq={a.get('seq',0):>2} resp={a.get('resp','')} | {f[:58]}")
print(f"   detectados {ok}/{tot}  ({100*ok/tot:.0f}%)\n")

# ---------- triaje de nueva ----------
NUEVA=os.path.join(ARCH,"papers_FCAW/nueva")
SKIP={"Prediction of steady state dilution in multipass hardfacing overlays deposited by self shielded ¯ ux cored arc welding.pdf",
"Role of Welding Parameters Using the Flux Cored Arc Welding Process of Low Alloy Steels on Bead Geometry and Mechanical Properties .pdf",
"Optimization of the FCAW process by weld bead geometry analysis.pdf",
"Performance optimization and investigation of metal-cored filler wires for high-strength steel during gas metal arc welding.pdf",
"Effect of Minor Additives on Bead Geometry and Shape Relationship Using Submerged Arc Welding Fluxes.pdf",
"Modeling and optimization of features of bead geometry including percentage dilution in submerged arc welding using mixture of fresh flux and fused slag.pdf",
"Prediction and Control of Weld Bead Geometry in Gas Metal Arc Welding Process Using Simulated Annealing Algorithm.pdf",
"Prediction of weld bead geometry and penetration in electric arc welding using artificial neural networks.pdf",
"Residual stresses in flux cored arc welding process in bead-on-plate specimens.pdf",
"ВосстаноВительная наплаВКа Деталей из титаноВого сплаВа Вт22.pdf"}
rows=[]
for f in sorted(os.listdir(NUEVA)):
    if not f.lower().endswith(".pdf") or f in SKIP: continue
    a=analizar(os.path.join(NUEVA,f)); a["ver"]=veredicto(a); a["arch"]=f; rows.append(a)

ORD={"SI":0,"PROBABLE":1,"REVISAR":2,"NO":3,"ESCANEADO":4}
rows.sort(key=lambda r:(ORD[r["ver"]],-r.get("seq",0)))
tot=0
for v in ORD:
    g=[r for r in rows if r["ver"]==v]
    if not g: continue
    print(f"\n{'='*96}\n{v}  ({len(g)})\n{'='*96}")
    for r in g:
        if v in ("SI","PROBABLE"): tot+=r.get("seq",0)
        print(f"  corridas~{r.get('seq',0):>2}  resp=[{r.get('resp',''):<6}] {r.get('dis','')[:24]:<24} | {r['arch'][:52]}")
print(f"\n>>> CORRIDAS ESTIMADAS RECUPERABLES: ~{tot}")
out=os.path.join(ARCH,"dataset/TRIAJE_nueva.csv")
with open(out,"w",newline="",encoding="utf-8-sig") as fh:
    w=csv.DictWriter(fh,fieldnames=["ver","seq","resp","dis","nnum","pag","arch"]); w.writeheader()
    for r in rows: w.writerow({k:r.get(k,"") for k in w.fieldnames})
print(f"escrito {out}")
