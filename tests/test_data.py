import csv,json,unittest
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
ROOT=Path(__file__).resolve().parents[1]
class DataTest(unittest.TestCase):
    def test_public_dataset(self):
        rows=json.loads((ROOT/'data/hospedagens.json').read_text())
        self.assertEqual(len(rows),114)
        self.assertEqual(len({r['id'] for r in rows}),114)
        self.assertEqual(sum(r['selecionado'] for r in rows),111)
        self.assertEqual({r['Site'] for r in rows},{'booking','airbnb','hostelworld'})
        for r in rows:
            self.assertNotIn('/home/',json.dumps(r))
            self.assertEqual(r['Noites'],'4' if r['Busca']=='A' else '3')
            self.assertEqual(urlsplit(r['Link direto']).scheme,'https')
            for evidence in r['Evidência'].split('; '):
                self.assertTrue((ROOT/evidence).is_file(),evidence)
            if r['Total BRL']!='não disponível':
                self.assertAlmostEqual(float(r['Total BRL'])/3,float(r['Preço por pessoa BRL']),places=2)
    def test_downloads(self):
        for source in ['booking','airbnb','hostelworld']:
            for period in ['A','B']:
                file=ROOT/'downloads'/f'{source}_{period}.csv'
                with file.open(encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
                self.assertTrue(rows)
                self.assertTrue(all(r['Site']==source and r['Busca']==period for r in rows))
if __name__=='__main__':unittest.main()
