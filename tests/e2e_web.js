// Nivel 9: prueba extremo a extremo de la versión web en un navegador real.
// Uso: node tests/e2e_web.js [URL]   (por defecto http://localhost:8612)
const { chromium } = require('playwright');
const URL = process.argv[2] || 'http://localhost:8612';
const ok = (c, m) => { if (!c) throw new Error(m); };
(async () => {
  const b = await chromium.launch(); let fallos = 0;
  for (const [nombre, w] of [['escritorio', 1280], ['móvil', 400]]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } }); const errores = [];
    p.on('pageerror', e => errores.push(e.message)); p.on('console', m => m.type() === 'error' && errores.push(m.text()));
    const pasos = [];
    const paso = async (desc, fn) => { try { await fn(); pasos.push(['OK', desc]); } catch (e) { fallos++; pasos.push(['FALLO', desc + ': ' + e.message]); } };
    await p.goto(URL); await p.waitForSelector('.card', { timeout: 15000 });
    await paso('carga la respuesta inicial (2 tarjetas, ROE de Santander y BBVA)', async () => ok((await p.$$('.card')).length === 2, 'tarjetas'));
    await paso('la cifra calculada de Santander es 13,98 %', async () => ok((await p.textContent('.card .fig-num.calc')).includes('13,98'), 'cifra'));
    await paso('un ejemplo cambia la respuesta (préstamos/depósitos de Santander: n/d con motivo)', async () => {
      await p.click('text=Préstamos sobre depósitos de Santander 2025'); await p.waitForTimeout(800);
      const t = await p.textContent('#cards'); ok(t.includes('No calculable desde ESEF'), 'sin motivo'); ok(!t.includes('calculado desde ESEF'), 'muestra cifra inventada');
    });
    await paso('pregunta escrita a mano', async () => {
      await p.fill('#q', 'ratio combinado de Mapfre 2025'); await p.press('#q', 'Enter'); await p.waitForTimeout(800);
      ok((await p.textContent('#cards')).includes('84,42'), 'ratio combinado');
    });
    await paso('pregunta no reconocida muestra ayuda', async () => {
      await p.fill('#q', 'hola'); await p.press('#q', 'Enter'); await p.waitForTimeout(600);
      ok((await p.textContent('#cards')).includes('No he reconocido'), 'mensaje');
    });
    await paso('tabla de banca con 6 ratios y cambio de ejercicio', async () => {
      ok((await p.$$('#tb tbody tr')).length === 6, 'filas'); await p.click('.seg button[data-y="2024"]');
      ok((await p.textContent('#tb')).includes('12,96'), 'ROE 2024 Santander');
    });
    await paso('traza: el ROE de BBVA 2025 muestra sus hechos XBRL', async () => {
      await p.selectOption('#se', 'bbva'); await p.selectOption('#sr', 'roe'); await p.selectOption('#sy', '2025'); await p.waitForTimeout(800);
      const t = await p.textContent('#traza'); ok(t.includes('18,60') && t.includes('ProfitLossAttributableToOwnersOfParent'), 'traza');
    });
    await paso('gráfico calculado/publicado con 37 filas', async () => ok((await p.$$('#diff .row')).length === 37, 'filas'));
    await paso('sin desbordamiento horizontal', async () => ok(await p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), 'scroll lateral'));
    await paso('sin errores de JavaScript', async () => ok(errores.length === 0, errores.join(' | ')));
    console.log(`\n${nombre} (${w}px)`); pasos.forEach(([e, d]) => console.log(`  ${e}  ${d}`));
    await p.close();
  }
  await b.close(); console.log(`\n${fallos ? fallos + ' fallos' : 'todo correcto'}`); process.exit(fallos ? 1 : 0);
})();
