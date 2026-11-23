# Plan de pruebas del prototipo

**Objetivo:** demostrar que cada cifra que muestra la herramienta es correcta, trazable y estable, y que la herramienta no inventa datos cuando no los tiene.

**Ejecución:** `PYTHONPATH=src pytest -q tests/` (las pruebas que necesitan los paquetes ESEF originales se omiten si no están en `data/raw/esef/`).

| Nivel | Qué se prueba | Fichero | Criterio de aceptación |
|---|---|---|---|
| 1. Unitarias: lector ESEF | Transformaciones numéricas (coma o punto decimal, guion como cero), escala, signo, hechos nulos, contextos con dimensiones, etiquetas de extensión, deduplicación | `test_parser.py` | Valores idénticos a los esperados en un paquete ESEF sintético |
| 2. Unitarias: motor | Reglas de mapeo (suma, resta con y sin minoritarios, no disponible, excepción por entidad), media frente a saldo de cierre, ratios derivados | `test_motor.py` | Cada regla produce el valor y el aviso esperados |
| 3. Unitarias: consulta | Interpretación de preguntas (entidades, varios años, dos definiciones), avisos (no publicado, diferencia con lo publicado, base del ROE), dato no disponible | `test_consulta.py` | Nunca devuelve una cifra que no esté en los resultados del motor |
| 4. Unitarias: validación | Elección de la variante publicada, exclusión de aproximaciones, base comparable por entidad, umbral estricto de 0,5 p.p. | `test_comparacion.py` | Emparejamientos y conteos según la regla documentada |
| 5. Integración | Lectura de los 6 paquetes reales, pipeline completo, coherencia contable (activo = pasivo + patrimonio, patrimonio atribuido ≤ patrimonio total) | `test_integracion.py` | 6.835 hechos; 64 de 72 valores; identidades contables con error < 1 M€ |
| 6. Regresión | Valores clave de la memoria (ROE, eficiencia, NIM, ratio combinado…) y resultados de la validación | `test_regresion.py` | Coinciden con las cifras citadas en la memoria |
| 7. Calidad de datos | Cada hecho de cada traza existe en el informe con el mismo valor; cada cita de un ratio publicado aparece literalmente en el informe | `test_calidad_datos.py` | 100 % de trazas y citas verificadas |
| 8. API | Endpoints de la versión web: códigos, estructura, ausencia de NaN, preguntas vacías, desconocidas, demasiado largas o con caracteres especiales | `test_api.py` | Respuestas válidas en JSON y sin errores 500 |
| 9. Extremo a extremo | Página web en un navegador real: carga, consulta, tabla, traza y gráfico, sin errores de JavaScript; sin desbordamiento horizontal a 400 px | `e2e_web.js` | Todo visible y sin errores en escritorio y móvil |
| 10. Rendimiento | Tiempo de lectura de los 6 paquetes y latencia de la API | `test_integracion.py`, `test_api.py` | Lectura < 30 s; respuesta de la API < 1 s en local |
| 11. Producción | Prueba de humo de https://tfm-ratios-semanticos.vercel.app | manual asistida | Las cuatro secciones responden |
