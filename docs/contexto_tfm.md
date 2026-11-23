# Contexto del TFM (para quien trabaje en el repo)

**Título ES:** Contextualización semántica de estados financieros para el cálculo e interpretación fiable de ratios en el sector financiero: un prototipo basado en ontologías y modelos de lenguaje.
**Título EN:** Semantic contextualization of financial statements for the reliable calculation and interpretation of financial ratios in the financial sector: an ontology- and LLM-based prototype.
**Autor:** Jorge García · **Tutor:** Víctor Lechuga
**Máster:** Máster ejecutivo N-World en Formación Permanente en Finanzas y Tecnología Aplicadas (título propio, Universidad de La Rioja), curso 2026-2027. 50 % finanzas y 50 % tecnología.

## Problema
Calcular un ratio es fácil; que sea fiable y comparable no. Cada entidad define sus medidas alternativas de rendimiento (APM) a su manera (ROE con patrimonio medio o de cierre, con o sin intangibles, numeradores ajustados), etiqueta sus cifras con extensiones propias incluso en el formato ESEF/XBRL obligatorio, NIIF 9 y NIIF 17 afectan a la comparabilidad, y ratios clave (CET1, morosidad, Solvencia II) están en información regulatoria, no en los estados. Además, los LLM consultados directamente pueden inventar cifras o fórmulas.

## Objetivos
- General: diseñar y validar una herramienta de contextualización semántica que permita calcular e interpretar de forma fiable y trazable los ratios de entidades bancarias y aseguradoras.
- Específicos: (1) analizar los problemas de comparabilidad; (2) diseñar un diccionario semántico que relacione partidas ESEF/XBRL y datos publicados con conceptos canónicos; (3) prototipo que calcule 12 ratios con trazabilidad; (4) validar frente a las APM publicadas y explicar diferencias; (5) evaluar si un LLM apoyado en la capa semántica responde con más fiabilidad que un LLM directo.

## Alcance (decidido)
- 6 entidades, ejercicio 2025 con comparativo 2024: Santander, BBVA, CaixaBank, Sabadell (banca); Mapfre, Línea Directa (seguros). Bankinter y Unicaja quedan como trabajo futuro. Catalana Occidente excluida (deslistada el 05/01/2026).
- 12 ratios: ROE, ROA (comunes); eficiencia, NIM, préstamos/depósitos, morosidad, cobertura, CET1 (banca); siniestralidad, ratio de gastos, ratio combinado, Solvencia II (seguros).
- Metodología: Design Science Research (Hevner et al., 2004; Peffers et al., 2007).
- Evaluación: (a) calculado frente a publicado; (b) 20 preguntas a "LLM solo" frente a "LLM + capa semántica" (sin API: las respuestas del LLM solo las obtiene el autor en un chat).

## Hallazgos ya obtenidos (ESEF 2025)
- Entre el 28 % y el 39 % de los hechos numéricos de cada entidad usan elementos de extensión propios (Santander 29 %, BBVA 34 %, Sabadell 37 %, CaixaBank 28 %, Mapfre 36 %, Línea Directa 39 %).
- Patrimonio atribuido: solo CaixaBank y Mapfre usan ifrs-full:EquityAttributableToOwnersOfParent; BBVA, Sabadell y Línea Directa etiquetan "Fondos propios" con extensiones (no equivalente: excluye OCI).
- Margen de intereses: todos los bancos usan ifrs-full:InterestRevenueExpense, ninguno InterestIncomeExpenseNet.
- Margen bruto: los cuatro bancos usan ifrs-full:GrossProfit (elemento pensado para ventas menos coste de ventas en la industria).
- BBVA desglosa préstamos y depósitos por cartera contable; CaixaBank y Sabadell dan el total.

## Normas de la memoria
20–50 páginas (objetivo ~35). Portada con título ES/EN; resumen y abstract 150–200 palabras; máximo 5 palabras clave; introducción (objetivo, metodología y estado de la cuestión), desarrollo, conclusiones, bibliografía APA, anexos. Calibri 12, justificado. Tablas: "Tabla N. Título" encima y "Fuente: ..." debajo; figuras igual.

## Estructura prevista
1. Introducción (~8 págs.) · 2. Marco financiero (~7) · 3. Diseño e implementación (~8) · 4. Resultados (~8) · 5. Conclusiones (~3) · Referencias · Anexos.
