# Anexo A. Diccionario semántico

El diccionario completo está en `config/diccionario_semantico.yaml` del repositorio. Este anexo resume el catálogo de ratios; las reglas de mapeo por entidad se resumen en el apartado 3.4.2 y se recogen completas, con el motivo de cada excepción, en la sección `mapeo` del fichero.

**Tabla 1. Catálogo de ratios del diccionario semántico**

| Ratio | Aplica a | Fórmula | Fuente |
|---|---|---|---|
| Rentabilidad sobre recursos propios (ROE) | banca, seguros | `resultado_atribuido / media(patrimonio_atribuido)` | Calculado (ESEF) |
| Rentabilidad sobre activos (ROA) | banca, seguros | `resultado_ejercicio / media(activo_total)` | Calculado (ESEF) |
| Ratio de eficiencia (cost-to-income) | banca | `gastos_explotacion_banca / margen_bruto` | Calculado (ESEF) |
| Margen de intereses sobre activos medios (NIM) | banca | `margen_intereses / media(activo_total)` | Calculado (ESEF) |
| Préstamos sobre depósitos (loan-to-deposit) | banca | `prestamos_clientela / depositos_clientela` | Calculado (ESEF) |
| Tasa de morosidad (NPL ratio) | banca | `riesgos_dudosos / riesgo_crediticio_total` | Publicado por la entidad |
| Tasa de cobertura de dudosos | banca | `provisiones_insolvencias / riesgos_dudosos` | Publicado por la entidad |
| Ratio de capital CET1 | banca | `capital_cet1 / activos_ponderados_por_riesgo` | Publicado por la entidad |
| Ratio de siniestralidad (no vida) | seguros | `siniestralidad_neta / ingresos_seguros` | Calculado (ESEF) |
| Ratio de gastos | seguros | `(gastos_servicio_seguro - siniestralidad_neta) / ingresos_seguros` | Calculado (ESEF) |
| Ratio combinado (no vida) | seguros | `gastos_servicio_seguro / ingresos_seguros` | Calculado (ESEF) |
| Ratio de solvencia (Solvencia II) | seguros | `fondos_propios_admisibles / scr` | Publicado por la entidad |

Fuente: Elaboración propia.

# Anexo B. Preguntas de evaluación

**Tabla 2. Preguntas de evaluación y respuestas de referencia**

| Id | Tipo | Pregunta | Respuesta de referencia |
|---|---|---|---|
| P01 | cifra | ¿Cuál fue el ROE de BBVA en 2025? | 18,4 % publicado por BBVA (fondos propios + OCI, medias mensuales); 18,60 % calculado sobre patrimonio atribuido medio |
| P02 | cifra | ¿Cuál fue el ratio de eficiencia de CaixaBank en 2025? | 39,4 % publicado; 39,43 % calculado |
| P03 | cifra | ¿Cuál fue el ROA de Santander en 2025? | 0,84 % publicado y calculado |
| P04 | cifra | ¿Cuál fue el ratio combinado de Línea Directa en 2025? | 92,6 % publicado (no vida, neto de reaseguro); 91,49 % calculado bruto de reaseguro desde ESEF |
| P05 | cifra | ¿Cuál fue el margen de intereses sobre activos medios (NIM) de Sabadell en 2025? | 1,97 % publicado (margen de intereses / ATM, con TSB); 1,46 % calculado: margen sin TSB sobre activo total medio (incluye TSB como mantenido para la venta) |
| P06 | cifra | ¿Cuál fue el ROE de Mapfre en 2025? | 12,4 % publicado; 12,38 % calculado |
| P07 | regulatorio | ¿Cuál fue el ratio CET1 de Santander a cierre de 2025? | 13,5 % phased-in (13,46 % en la memoria); Santander no publica fully loaded para 2025 |
| P08 | regulatorio | ¿Cuál fue la tasa de morosidad de CaixaBank en 2025? | 2,1 % |
| P09 | regulatorio | ¿Cuál fue la tasa de cobertura de BBVA en 2025? | 85 % (definición ampliada en 2025 con préstamos a valor razonable con cambios en OCI) |
| P10 | regulatorio | ¿Cuál fue el ratio de Solvencia II de Mapfre a 31 de diciembre de 2025? | No publicado en el informe anual; el último dato es 210,4 % a septiembre de 2025 |
| P11 | regulatorio | ¿Cuál fue el ratio de siniestralidad de Línea Directa en 2025? | 71,6 % publicado; no calculable desde ESEF (solo etiqueta el total de gastos del servicio de seguro) |
| P12 | comparacion | ¿Qué banco tuvo mayor ROE en 2025: Santander, BBVA, CaixaBank o Sabadell? | BBVA (18,60 % calculado con la misma definición; 18,4 % publicado), seguido de CaixaBank, Santander y Sabadell |
| P13 | comparacion | Ordena BBVA, CaixaBank, Santander y Sabadell por ratio de eficiencia en 2025 | BBVA 38,8 %, CaixaBank 39,4 %, Santander 42,1 % (41,2 % ordinaria publicada), Sabadell 46,7 % (49,3 % publicada con TSB) |
| P14 | comparacion | ¿Qué aseguradora tuvo mejor ratio combinado en 2025, Mapfre o Línea Directa? | Mapfre (no vida 90,2 % frente a 92,6 % publicados), con la salvedad de perímetro: el de Mapfre es solo no vida |
| P15 | comparacion | ¿Mejoró la tasa de morosidad de Sabadell en 2025 respecto a 2024? | Sí: de 2,84 % a 2,37 % |
| P16 | semantica | ¿Cuál es el ROE de Santander en 2025 calculado sobre fondos propios y sobre patrimonio atribuido? | 10,21 % sobre fondos propios y 13,98 % sobre patrimonio atribuido; la diferencia se debe al otro resultado global acumulado negativo |
| P17 | semantica | ¿Son comparables los ROE publicados por CaixaBank y BBVA en 2025? | No directamente: CaixaBank resta el cupón de AT1 del numerador y BBVA no, y los denominadores difieren (CaixaBank 14,9 %; BBVA 18,4 %) |
| P18 | semantica | ¿Por qué Sabadell publica una eficiencia del 49,3 % en 2025 si el cálculo desde sus cuentas da 46,7 %? | Porque incluye TSB, clasificado como actividad interrumpida en las cuentas consolidadas |
| P19 | no disponible | ¿Cuál es el ratio préstamos/depósitos de Santander en 2025 según sus estados ESEF? | No calculable: Santander no etiqueta préstamos ni depósitos de la clientela; publica 98 % en el informe de gestión |
| P20 | no disponible | ¿Qué NIM publica BBVA para 2025? | BBVA no publica el NIM en el informe anual; calculado: 3,22 % sobre activo total medio |

Fuente: Elaboración propia a partir del motor de ratios y de los informes de las entidades.

# Anexo C. Repositorio y estructura del código

El código, los datos derivados y esta memoria están en el repositorio privado https://github.com/jorgegarcia-cmd/tfm-ratios-semanticos, al que el autor dará acceso al tutor y al tribunal.

- `src/tfm_ratios/ixbrl_parser.py`: lector de Inline XBRL sin taxonomías externas.
- `config/diccionario_semantico.yaml`: diccionario semántico (conceptos, ratios y reglas de mapeo).
- `src/tfm_ratios/motor.py`: motor de ratios con trazabilidad.
- `src/tfm_ratios/comparacion.py`: validación frente a los ratios publicados.
- `src/tfm_ratios/consulta.py`: capa de consulta y esquema de la herramienta para un modelo de lenguaje.
- `app.py`: interfaz de demostración en Streamlit.
- `data/published/`: ratios publicados por las entidades, con su definición y una cita verificable.
- `data/results/`: ratios calculados, trazas y comparación.
- `docs/evaluacion/`: preguntas, respuestas y rúbrica de la evaluación.
