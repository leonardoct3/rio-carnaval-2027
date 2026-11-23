"""Importa somente dados públicos da pesquisa local. Não publica HTML, cookies ou perfis."""
import csv,json,hashlib,re
from urllib.parse import urljoin
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('/home/carvalho_leonardo/carnaval-2027')
def clean(row):
    row=dict(row)
    row["Link direto"]=urljoin({"booking":"https://www.booking.com", "airbnb":"https://www.airbnb.com.br", "hostelworld":"https://www.hostelworld.com"}[row["Site"]],row["Link direto"])
    evidence=[]
    for base in row['Evidência'].split('; '):
        p=Path(base+'.txt')
        if p.exists():
            name=p.parent.name+'--'+p.name
            (ROOT/'evidencias'/name).write_text(p.read_text())
            evidence.append('evidencias/'+name)
    row['Evidência']='; '.join(evidence)
    return row
def key(r):return (r['Site'],urljoin({'booking':'https://www.booking.com','airbnb':'https://www.airbnb.com.br','hostelworld':'https://www.hostelworld.com'}[r['Site']],r['Link direto']).split('?')[0],r['Tipo'],r['Busca'])
selected=list(csv.DictReader((SOURCE/'resultados/consolidado.csv').open(encoding='utf-8-sig')))
keys={key(r) for r in selected}
rows=[clean(r) for r in csv.DictReader((SOURCE/'resultados/amostra_completa.csv').open(encoding='utf-8-sig'))]
for r in rows:
    r['id']=hashlib.sha256('|'.join(key(r)).encode()).hexdigest()[:12]
    r['selecionado']=key(r) in keys
(ROOT/'data/hospedagens.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for file in (SOURCE/'resultados').glob('*.csv'):
    raw=list(csv.DictReader(file.open(encoding='utf-8-sig')))
    if not raw:continue
    with (ROOT/'downloads'/file.name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=raw[0].keys());w.writeheader()
        w.writerows(clean(r) if 'Evidência' in r else r for r in raw)
report=(SOURCE/'RELATORIO_CONSOLIDADO.md').read_text()
(ROOT/'downloads/relatorio.md').write_text(report)
print(f'{len(rows)} registros; {len(keys)} na seleção consolidada.')
