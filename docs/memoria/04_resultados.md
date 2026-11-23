# 4. Resultados

Este capítulo presenta los resultados de aplicar el prototipo a las seis entidades de la muestra. Se organiza en cinco bloques: la heterogeneidad del etiquetado XBRL (4.1), la diversidad de definiciones en las medidas alternativas de rendimiento (4.2), la validación de los ratios calculados frente a los publicados (4.3), la evaluación de la capa de consulta con un modelo de lenguaje (4.4) y el análisis financiero comparado de las entidades (4.5).

## 4.1. Heterogeneidad del etiquetado en los informes ESEF

El primer resultado es descriptivo, pero condiciona todo lo demás: el formato electrónico único no garantiza, por sí mismo, que las mismas magnitudes se etiqueten igual. Como se vio en la Tabla 1, un tercio de los hechos numéricos (2.244 de 6.835) usa elementos de extensión propios de cada entidad. La Tabla 3 recoge los casos concretos que afectan a los ratios del catálogo.

**Tabla 3. Divergencias de etiquetado que afectan al cálculo de ratios**

| Concepto | Lo que se esperaría | Lo que hacen las entidades |
|---|---|---|
| Patrimonio atribuido | `EquityAttributableToOwnersOfParent` | Solo lo usan CaixaBank y Mapfre. CaixaBank etiqueta con él sus fondos propios (38.962 M€), una cifra mayor que su patrimonio neto total (38.526 M€). El resto usa extensiones propias para los fondos propios. |
| Margen de intereses | `InterestIncomeExpenseNet` | Ningún banco lo usa; los cuatro usan `InterestRevenueExpense`. |
| Margen bruto | Sin elemento NIIF específico | Los cuatro bancos usan `GrossProfit`, pensado para «ventas menos coste de ventas» en la industria. |
| Préstamos y depósitos de la clientela | `LoansAndAdvancesToCustomers` / `DepositsFromCustomers` | CaixaBank y Sabadell, el total; BBVA, desglosado por cartera contable; Santander no los etiqueta. |
| Ingresos por contratos de seguro (NIIF 17) | `InsuranceRevenue` | Línea Directa lo usa; Mapfre emplea una extensión propia. |
| Siniestralidad y gastos del servicio de seguro | Desglose en elementos separados | Mapfre los separa con extensiones; Línea Directa solo etiqueta el total. |

Fuente: Elaboración propia a partir de los informes ESEF 2025.

Dos consecuencias se derivan de la tabla. La primera es que un mapeo literal por nombre de elemento produce errores silenciosos: tomaría como patrimonio atribuido de CaixaBank una magnitud distinta de la de Mapfre, y no encontraría ninguna para las otras cuatro entidades. La segunda es que algunos ratios no se pueden calcular desde los estados estructurados de ciertas entidades, por ejemplo la ratio préstamos/depósitos de Santander. Ante esa ausencia, la herramienta informa del motivo y recurre al dato publicado, en lugar de aproximarlo.

## 4.2. Diversidad de definiciones en las medidas alternativas de rendimiento

Las directrices de ESMA obligan a definir y conciliar cada medida alternativa de rendimiento (ESMA, 2015). Los cuatro bancos lo hacen en un anexo específico del informe de gestión; Mapfre remite a un documento externo y Línea Directa explica sus ratios en el propio informe. Sin embargo, el análisis de sus definiciones muestra que el mismo nombre esconde cálculos distintos. El caso más claro es el ROE (Tabla 4).

**Tabla 4. Definición del ROE publicado por cada entidad (ejercicio 2025)**

| Entidad | ROE publicado | Denominador | Tratamiento del AT1 | Tipo de media |
|---|---|---|---|---|
| BBVA | 18,4 % | Fondos propios + otro resultado global acumulado | No se resta | Mensual ponderada |
| CaixaBank | 14,9 % | Fondos propios + ajustes de valoración | Se resta el cupón del numerador | Diaria y mensual |
| Santander | 13,9 % | Patrimonio sin minoritarios con OCI, más dividendos | No se resta (sí en el «RoTE post-AT1») | Mensual |
| Sabadell | 11,9 % | Fondos propios sin OCI | No se resta | Mensual (último día de cada mes) |
| Mapfre | 12,4 % | Fondos propios medios | — | No detallada en el informe |
| Línea Directa | 22,9 % | Media simple de dos cierres, menos el dividendo propuesto | — | Dos puntos |

Fuente: Elaboración propia a partir de los informes de gestión 2025 de las entidades (anexos de medidas alternativas de rendimiento, en el caso de los bancos).

Las diferencias no se limitan al ROE:

- **Eficiencia:** Santander la calcula sobre su cuenta de resultados «ordinaria». Sabadell suma las actividades interrumpidas (TSB), aunque en sus cuentas consolidadas figuran por separado. CaixaBank publica además una versión sin el gravamen a la banca.
- **Morosidad y cobertura:** el perímetro del denominador varía, y BBVA modificó su definición en 2025 para incluir los préstamos valorados a valor razonable con cambios en otro resultado global, lo que afecta a la comparación con las cifras de 2024 publicadas el año anterior.
- **Solvencia:** varias entidades publican más de una cifra «oficial». CaixaBank distingue un CET1 de gestión (12,6 %) y uno regulatorio (12,25 %). Línea Directa ofrece tres ratios de Solvencia II para 2025, todas de la entidad individual. Mapfre solo publica la de septiembre de 2025.

La Figura 2 muestra el efecto cuantitativo de la base de patrimonio sobre el ROE de 2025, calculado por el prototipo con las dos definiciones.

**Figura 2. ROE 2025 de los bancos según la base de patrimonio**

[FIGURA: fig2_roe_bases.png]

Fuente: Elaboración propia a partir de los informes ESEF 2025.

La diferencia entre ambas bases alcanza 4,5 puntos en BBVA y 3,8 en Santander, cuyo otro resultado global acumulado es muy negativo. En CaixaBank y Sabadell es inferior a medio punto. Cada valor publicado se sitúa junto a la definición que usa la entidad: BBVA y Santander, junto al cálculo con otro resultado global; Sabadell, junto al cálculo sobre fondos propios. Comparar directamente el ROE publicado de Sabadell con el de BBVA, por tanto, mezcla dos magnitudes distintas.

## 4.3. Validación: ratios calculados frente a publicados

Para validar el motor se ha comparado cada ratio calculado con el que publica la propia entidad, cuando existe. Cuando una entidad publica el ROE sobre fondos propios (Sabadell), se compara con la variante calculada sobre esa misma base; las aproximaciones que la entidad no presenta como el mismo ratio (el diferencial de balance de CaixaBank frente al NIM) se excluyen. Se obtienen así 37 pares comparables entre los dos ejercicios. La Figura 3 muestra la diferencia de cada par.

**Figura 3. Diferencia entre el ratio calculado y el publicado**

[FIGURA: fig3_validacion.png]

Fuente: Elaboración propia.

En 23 de los 37 pares (62 %) la diferencia es inferior a 0,5 puntos porcentuales en valor absoluto, y la diferencia absoluta mediana del conjunto es de 0,22 puntos. Los ROA de los cuatro bancos coinciden en todos los casos con una diferencia de 0,04 puntos o menos, y la eficiencia de BBVA y de CaixaBank, con 0,03 o menos.

Los 14 pares restantes no apuntan a errores de extracción: las diferencias se explican principalmente por diferencias de definición o de perímetro, en la mayoría de los casos documentadas por la propia entidad, y en algunos por convenciones del propio motor, como el uso del saldo de cierre cuando falta el inicial (Tabla 5).

**Tabla 5. Causa de las diferencias iguales o superiores a 0,5 puntos**

| Pares | Diferencia (p.p.) | Causa |
|---|---|---|
| Eficiencia de Santander (2024 y 2025) | +1,3 y +0,9 | Santander publica la ratio sobre su cuenta ordinaria; el motor usa las cifras estatutarias |
| ROE de CaixaBank 2025 | +0,7 | Principalmente, CaixaBank resta el cupón del AT1 del numerador; también difiere el método de cálculo de la media (en 2024 la diferencia es de 0,4) |
| ROE de Sabadell 2024 (sobre fondos propios) | −0,5 | El motor usa el saldo de cierre porque los fondos propios de 2023 no están etiquetados; Sabadell usa medias mensuales |
| Eficiencia de Sabadell (2024 y 2025) | −3,1 y −2,6 | Sabadell incluye TSB, clasificado como actividad interrumpida (IASB, 2004) |
| NIM de Sabadell (2024 y 2025) | −0,5 y −0,5 | Sabadell no lo define como medida alternativa; el motor usa el margen sin TSB sobre el activo total (que incluye TSB como mantenido para la venta) y, en 2024, el saldo de cierre |
| Préstamos/depósitos de Sabadell 2025 | −3,7 | Perímetro: los saldos de TSB se presentan como mantenidos para la venta (NIIF 5) y dejan de figurar en préstamos y depósitos de la clientela |
| Préstamos/depósitos de CaixaBank (2024 y 2025) | −2,6 y −3,1 | CaixaBank usa un crédito de gestión sin crédito de mediación y añade periodificaciones a los depósitos |
| Ratio combinado de Mapfre (2024 y 2025) | −6,5 y −5,8 | Mapfre publica el ratio solo de no vida y neto de reaseguro; el motor lo calcula para todo el grupo y bruto |
| Ratio combinado de Línea Directa 2025 | −1,1 | El publicado es neto de reaseguro; el calculado, bruto |

Fuente: Elaboración propia.

La validación confirma dos cosas. Por un lado, que el motor reproduce las cifras de los informes cuando las definiciones son próximas; conviene matizar que algunos pares coincidentes no comparten exactamente la definición (Santander añade dividendos al denominador de su ROE) y que un umbral absoluto de 0,5 puntos es holgado para ratios de nivel bajo, como el ROA, aunque en ese caso las diferencias observadas no superan 0,04 puntos. Por otro, que las diferencias restantes son exactamente el tipo de información que la capa semántica debe hacer visible al usuario. Por eso la herramienta muestra siempre el valor publicado junto al calculado, con la definición de la entidad y un aviso cuando difieren en más de medio punto.

## 4.4. Evaluación de la capa de consulta

### 4.4.1. Diseño de la prueba

Se ha diseñado un conjunto de 20 preguntas de cinco tipos (Anexo B):

- seis de cifra directa;
- cinco sobre ratios regulatorios o publicados;
- cuatro de comparación entre entidades;
- tres de matiz semántico, como la comparabilidad de dos ROE;
- dos sobre datos no disponibles.

Cada pregunta tiene una respuesta de referencia obtenida del motor y de los datos publicados.

Las preguntas se plantean en dos condiciones:

- **Condición A:** un asistente de IA generalista, sin búsqueda web ni documentos.
- **Condición B:** el prototipo, en el que la cifra procede siempre de la función de consulta.

Las respuestas se puntúan con una rúbrica de tres criterios binarios: exactitud de la cifra (±0,5 p.p.), trazabilidad (definición y fuente) y ausencia de invención con advertencia de los límites de comparabilidad. Para evitar que el autor del prototipo evalúe su propio trabajo, la puntuación la realiza un evaluador independiente sobre las respuestas anonimizadas y en orden aleatorio.

### 4.4.2. Resultados

[PENDIENTE: resultados de la condición A y puntuación de ambas condiciones.]

En la condición B, el intérprete por reglas identificó correctamente la entidad, el ratio y el ejercicio en las 20 preguntas. Todas las respuestas con valor calculado incluyen la fórmula y la fuente. En las dos preguntas sobre datos no disponibles, la herramienta lo declara sin inventar una cifra: en la ratio préstamos/depósitos de Santander explica que el dato no está etiquetado y ofrece el publicado, y en el NIM de BBVA advierte de que la entidad no lo publica y ofrece solo el calculado.

## 4.5. Análisis financiero comparado (ejercicio 2025)

Los ratios calculados con una definición común permiten una comparación coherente de las entidades; los publicados (morosidad, cobertura y CET1) mantienen la definición de cada entidad y deben leerse con esa cautela. La Tabla 6 resume los indicadores de 2025.

**Tabla 6. Indicadores de banca, ejercicio 2025**

| Indicador | BBVA | CaixaBank | Santander | Sabadell |
|---|---|---|---|---|
| ROE (patrimonio atribuido, calculado) | 18,6 % | 15,6 % | 14,0 % | 12,2 % |
| ROE (fondos propios, calculado) | 14,1 % | 15,4 % | 10,2 % | 11,8 % |
| ROA (calculado) | 1,36 % | 0,91 % | 0,84 % | 0,73 % |
| Eficiencia (calculada, estatutaria) | 38,8 % | 39,4 % | 42,1 % | 46,7 % |
| NIM (calculado, sobre activo total medio) | 3,22 % | 1,65 % | 2,29 % | 1,46 % |
| Préstamos/depósitos (calculado) | 92,8 % | 83,8 % | n/d (98 % publicado) | 89,8 % |
| Tasa de morosidad (publicada) | 2,7 % | 2,1 % | 2,91 % | 2,37 % |
| Tasa de cobertura (publicada) | 85 % | 76,9 % | 66,5 % | 63,8 % |
| CET1 (publicado) | 12,70 % | 12,25 % regulatorio | 13,5 % phased-in | 13,16 % phased-in |

Fuente: Elaboración propia a partir de los informes ESEF 2025.

**Rentabilidad.** BBVA presenta la mayor rentabilidad sobre activos y el mayor margen de intereses de la muestra, previsiblemente por el peso de su negocio fuera de la zona euro, aunque este trabajo no descompone el margen por geografías. Su ventaja en ROE desaparece con la base de fondos propios (14,1 % frente al 15,4 % de CaixaBank), porque su patrimonio contable está minorado por un otro resultado global acumulado muy negativo. Es un ejemplo directo de cómo la elección de la definición puede alterar la clasificación de las entidades.

**Eficiencia y calidad del activo.** BBVA y CaixaBank mantienen ratios de eficiencia por debajo del 40 %, frente a valores superiores en Santander y Sabadell. CaixaBank publica la menor tasa de morosidad de los cuatro bancos, con una cobertura elevada. Estas comparaciones deben hacerse con cautela: el perímetro del denominador de la morosidad difiere entre entidades y BBVA cambió su definición en 2025 (apartado 4.2).

**Liquidez y solvencia.** Todas las entidades con dato presentan una ratio préstamos/depósitos inferior al 100 %, lo que indica una financiación apoyada en depósitos. Las ratios CET1 se sitúan entre el 12,25 % y el 13,5 %, aunque no son estrictamente comparables entre sí: la de CaixaBank es la regulatoria (su CET1 de gestión es del 12,6 %), las de Santander y Sabadell son *phased-in* y la de BBVA coincide en ambas variantes.

**Seguros.** Línea Directa obtiene un ROE muy superior al de Mapfre (22,5 % frente a 12,4 %, calculados), con un negocio mucho más pequeño y centrado en no vida. Mapfre publica un ratio combinado mejor (90,2 % frente a 92,6 %), con la salvedad de que el suyo corresponde solo al negocio de no vida. La comparación de solvencia está limitada: Mapfre solo publica su ratio de Solvencia II a septiembre de 2025 (210,4 %), y la de Línea Directa (182,6 % tras el dividendo complementario) corresponde a la entidad individual, no al grupo.

**Cambios de perímetro.** La interpretación de 2025 exige tener en cuenta los cambios de perímetro. En Sabadell, TSB figura como actividad interrumpida. Santander presenta 75.011 M€ de activos no corrientes mantenidos para la venta. Ambos hechos afectan a los saldos de balance y a la comparación interanual. Un analista debe incorporar este contexto antes de extraer conclusiones, y la herramienta lo facilita al mostrar la traza de cada cifra.
