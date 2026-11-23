# Resultados de la ejecución de pruebas (23/11/2026)

Resultado global: **89 pruebas automáticas superadas de 89**, **20 de 20 comprobaciones de navegador** (escritorio y móvil) y **prueba de humo en producción superada**.

| Nivel | Pruebas | Resultado | Evidencia clave |
|---|---|---|---|
| 1. Lector ESEF | 8 | 8 superadas | Coma y punto decimal, guion como cero, escala, signo, nulos, dimensiones, etiquetas de extensión y deduplicación sobre un paquete sintético |
| 2. Motor | 7 | 7 superadas | Suma, resta con y sin minoritarios (con aviso), no disponible con motivo, media frente a cierre, solo ejercicios completos |
| 3. Consulta | 14 | 14 superadas | Las 72 cifras de la consulta coinciden exactamente con el motor; sin cifra cuando el dato no existe |
| 4. Validación | 5 | 5 superadas | Variante RoA frente a RoRWA, exclusión de aproximaciones, base de Sabadell, umbral estricto (−0,50 no coincide) |
| 5. Integración | 9 | 9 superadas | 6.835 hechos en los 6 paquetes; 64 de 72 valores; activo = pasivo + patrimonio en las 6 entidades y los 2 ejercicios; patrimonio atribuido ≤ total |
| 6. Regresión | 30 | 30 superadas | Las 28 cifras de la memoria, el resultado de la validación (23 de 37; 0,22) y la diferencia de 4,5 puntos del ROE |
| 7. Calidad de datos | 3 | 3 superadas | Los 203 hechos de las trazas existen en el informe con el mismo valor; las 104 citas de ratios publicados aparecen literalmente en el informe |
| 8. API | 13 | 13 superadas | JSON válido sin NaN; entradas vacías, HTML, comillas y caracteres especiales sin errores 500; más de 300 caracteres rechazados (422) |
| 9. Extremo a extremo | 20 | 20 superadas | Consulta, ejemplos, tabla, cambio de ejercicio, traza y gráfico en Chromium a 1.280 y 400 px, sin errores de JavaScript ni desbordamiento lateral |
| 10. Rendimiento | 2 | 2 superadas | Lectura de los 6 paquetes < 30 s (unos 4 s); API < 1 s por consulta en local |
| 11. Producción | 1 | Superada | https://tfm-ratios-semanticos.vercel.app: 2 tarjetas iniciales, 13,98 % de Santander, sin cifra en préstamos/depósitos de Santander, 6 filas de banca, 37 filas del gráfico, traza de BBVA 18,60 %, 422 para entradas largas, latencia de la API 169 ms, sin desbordamiento lateral |

## Reproducir

```bash
pip install -r requirements.txt pytest httpx fastapi
cp <carpeta con los .xbri>/*.xbri data/raw/esef/   # necesario para los niveles 5 y 7
PYTHONPATH=src python -m tfm_ratios.ixbrl_parser data/raw/esef/*.xbri
pytest -q
(cd deploy && uvicorn main:app --port 8612) & node tests/e2e_web.js
```
