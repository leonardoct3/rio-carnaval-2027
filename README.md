# Rio 2027 · Nosso Carnaval

Painel público e responsivo para discutir hospedagens para três adultos no Rio no Carnaval de 2027.

**Site:** https://leonardoct3.github.io/rio-carnaval-2027/

## O que tem

- 114 registros da amostra completa; filtro para os 111 do consolidado.
- Booking, Airbnb e Hostelworld; períodos A (05–09/02) e B (06–09/02).
- Busca, filtros, teto por pessoa, ordenação, cards e tabela.
- Ficha com todos os campos coletados, textos de evidência e links diretos.
- Comparação de até quatro registros e da mesma propriedade em A/B.
- Favoritos locais e link de seleção compartilhável (sem sincronização de votos).
- Recomendações do relatório, CSVs completos e exportação dos resultados filtrados.

Preços coletados em **23/11/2026**, não preços em tempo real. Totais confirmados, totais anunciados sem composição integral das taxas e tarifas por cama/quarto são apresentados separadamente. Valores ausentes não são inventados. HTML e screenshots originais permanecem no projeto local de pesquisa, não neste repositório.

## Desenvolvimento

Sem dependências de frontend e sem build:

```sh
python3 -m http.server 8080
# Abrir http://localhost:8080
python3 tests/test_data.py
node --check assets/app.js
```

`index.html` é a entrada; `assets/` contém CSS/JavaScript; `data/hospedagens.json` tem todos os dados. O script `scripts/importar.py` reimporta a pesquisa local original, quando disponível, retirando caminhos locais dos dados e copiando somente evidências textuais públicas. Ajuste `SOURCE` ao reutilizá-lo.

## Publicação

GitHub Pages usa GitHub Actions. Cada push em `main` valida dados/JavaScript, prepara somente os arquivos públicos e publica. Também é possível executar o workflow manualmente. Implementação conforme a [documentação oficial de workflows do Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

Nenhum login, reserva, pagamento ou coleta automática adicional ocorre no painel. Favoritos usam localStorage; seleção compartilhada está no fragmento da URL. Sem analytics ou serviços externos de dados.

## Validação em navegador

`tests/browser.py` usa Python Playwright e Chromium. Com o servidor local rodando, execute `python tests/browser.py`. `TEST_URL` permite testar a URL publicada. Verifica filtros, comparação A/B, favoritos, seleção compartilhada, exportação CSV, tabela, ausência de erros JavaScript e overflow em 360, 390, 768 e 1440 px. Capturas ficam em `qa/` (ignorado pelo Git).
