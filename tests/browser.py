from playwright.sync_api import sync_playwright
from pathlib import Path
import json,os
ROOT=Path(__file__).resolve().parents[1]
base=os.environ.get('TEST_URL','http://127.0.0.1:8080/')
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page=browser.new_page(viewport={'width':1440,'height':1000},locale='pt-BR')
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto(base);page.wait_for_selector('.stay')
    assert page.locator('.stay').count()==114
    page.screenshot(path=str(ROOT/'qa/desktop.png'),full_page=False)
    page.locator('#period').select_option('B');page.locator('#source').select_option('airbnb')
    assert page.locator('.stay').count()==25
    page.locator('#search').fill('Praia Ipanema')
    assert page.locator('.stay').count()==1
    page.locator('[data-favorite]').click()
    page.locator('#results [data-detail]').click()
    assert page.locator('dialog').is_visible()
    assert page.locator('dialog').inner_text().count('5130')>=1
    pair=page.locator('[data-pair]').first
    assert pair.count()>0
    pair.click()
    assert page.locator('.comparison').is_visible()
    assert page.locator('.comparison th').first.inner_text()=='Informação'
    page.locator('#closeModal').click()
    page.locator('#share').click()
    page.wait_for_function("document.querySelector('#shareLink') || document.querySelector('#toast').classList.contains('show')")
    if page.locator('#shareLink').count():
        shared=page.locator('#shareLink').input_value()
        page.locator('#closeModal').click()
    else:
        shared=page.evaluate('location.origin+location.pathname+"#selecao="+JSON.parse(localStorage.getItem("rio27-compare")).join(",")')
    fresh=browser.new_page();fresh.goto(shared);fresh.wait_for_selector('.stay')
    assert fresh.locator('.stay').count()==2
    page.locator('#reset').click();page.locator('#priceKind').select_option('reference')
    assert page.locator('.stay').count()==13
    page.locator('#budget').fill('2000');assert page.locator('#empty').is_visible()
    page.locator('#reset').click();page.locator('#selectedOnly').check();assert page.locator('.stay').count()==111
    page.locator('#tableView').click();assert page.locator('tbody tr').count()==111
    with page.expect_download() as download:page.locator('#export').click()
    assert download.value.suggested_filename=='rio2027-selecao.csv'
    page.locator('#cardsView').click()
    for width in [360,390,768]:
        page.set_viewport_size({'width':width,'height':844})
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
        page.screenshot(path=str(ROOT/f'qa/mobile-{width}.png'),full_page=False)
    assert not errors,errors
    print('OK: 114 dados, filtros, detalhes, comparação A/B, favoritos, link compartilhado, CSV, tabela e responsividade 360/390/768/1440px; sem erros JS.')
    browser.close()
