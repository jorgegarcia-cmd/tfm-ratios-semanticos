// Pruebas end-to-end del frontal web (Playwright).
// Uso: node tests/e2e_web.js [URL]   (por defecto http://localhost:8612)
const { chromium } = require('playwright');
const URL = process.argv[2] || 'http://localhost:8612';
let ok = 0, ko = 0;
const check = (cond, msg) => { cond ? ok++ : ko++; console.log(`${cond ? 'OK ' : 'KO '} ${msg}`); };

(async () => {
  const b = await chromium.launch();
  for (const width of [1280, 400]) {
    const p = await b.newPage({ viewport: { width, height: 900 } });
    const errs = []; p.on('pageerror', e => errs.push(e.message));
    console.log(`\n— viewport ${width}px`);

    // Vista Preguntar
    await p.goto(URL + '/');
    await p.waitForSelector('.card');
    check(await p.locator('.card').count() === 2, 'pregunta inicial devuelve 2 fichas (Santander y BBVA)');
    check((await p.locator('.big.calc').first().textContent()).includes('%'), 'la ficha muestra la cifra calculada');
    await p.click('text=Préstamos sobre depósitos de Santander 2025');
    await p.waitForSelector('.big.nd');
    check(await p.locator('.big.nd').count() === 1, 'préstamos/depósitos de Santander aparece como no calculable');
    await p.fill('#q', 'ROE de BBVA en 2025');
    await p.click('button.go');
    await p.waitForFunction(() => document.querySelectorAll('#cards .card').length === 1);
    await p.click('details.tr summary');
    await p.waitForSelector('.trace table');
    check((await p.locator('.trace').textContent()).includes('ifrs-full:Equity'), 'la traza muestra los elementos XBRL de origen');

    // Vista Explorar
    await p.goto(URL + '/#explorar');
    await p.waitForSelector('#mb td.c');
    check(await p.locator('#mb tbody tr').count() >= 6, 'matriz de banca con al menos 6 ratios');
    const v25 = await p.locator('#mb td.c').first().textContent();
    await p.click('#years button[data-y="2024"]');
    const v24 = await p.locator('#mb td.c').first().textContent();
    check(v25 !== v24, 'el selector de ejercicio cambia los valores');
    await p.click('#mb td.c >> nth=1');
    await p.waitForSelector('#detail .card');
    check(await p.locator('#detail .card').count() === 1, 'pulsar una celda abre su ficha');

    // Vista La definición importa
    await p.goto(URL + '/#definicion');
    await p.waitForSelector('#rank .r .v:not(:empty)');
    const primero = () => p.evaluate(() => [...document.querySelectorAll('#rank .r')].find(r => r.querySelector('.pos').textContent === '1.').dataset.b);
    check(await primero() === 'bbva', 'con patrimonio atribuido lidera BBVA');
    await p.click('[data-d="roe_fondos_propios"]');
    check(await primero() === 'caixabank', 'con fondos propios lidera CaixaBank');

    check(!(await p.evaluate(() => document.documentElement.scrollWidth > innerWidth)), 'sin desbordamiento horizontal');
    check(errs.length === 0, 'sin errores de JavaScript' + (errs.length ? ': ' + errs.join('; ') : ''));
    await p.close();
  }
  await b.close();
  console.log(`\n${ok} correctas, ${ko} fallidas`);
  process.exit(ko ? 1 : 0);
})();
