# 3. Diseño e implementación del prototipo

Este capítulo describe el artefacto construido siguiendo el enfoque de *Design Science Research* presentado en el capítulo 1: una herramienta que añade una capa de contextualización semántica entre los informes financieros oficiales y el cálculo e interpretación de ratios. Se presentan primero los requisitos y la arquitectura, y después cada componente: la extracción de datos, el diccionario semántico, el motor de ratios y la capa de consulta en lenguaje natural. El código completo está disponible en el repositorio del proyecto (Anexo C).

## 3.1. Requisitos de diseño

Los requisitos se derivan directamente de los problemas de comparabilidad descritos en el capítulo 2:

1. **Fuente oficial y verificable.** Las cifras deben proceder de los informes financieros anuales en formato ESEF depositados por las entidades, no de bases de datos de terceros ni de documentos PDF.
2. **Cálculo determinista.** Un mismo ratio, con los mismos datos, debe producir siempre el mismo resultado. Ningún componente probabilístico, incluido el modelo de lenguaje, puede generar cifras.
3. **Trazabilidad completa.** Cada ratio debe poder seguirse hasta los hechos XBRL concretos que lo componen: etiqueta, valor, fecha e identificador dentro del documento.
4. **Explicitud semántica.** Las decisiones sobre qué partida representa cada concepto financiero deben estar escritas, ser revisables por un analista y poder variar por entidad cuando su etiquetado lo exija.
5. **Transparencia ante la ausencia de datos.** Cuando un concepto no está etiquetado, la herramienta debe decirlo y explicar el motivo, en lugar de aproximarlo en silencio.
6. **Contextualización.** El resultado debe acompañarse del valor publicado por la propia entidad, de los comparables homogéneos y de los avisos de comparabilidad pertinentes.

## 3.2. Arquitectura general

La herramienta se organiza en una cadena de siete componentes (Figura 1). Los cinco primeros forman un flujo de datos lineal: fuentes, extracción, diccionario semántico, motor de ratios y contextualización. Los dos últimos, la consulta en lenguaje natural y la interfaz, se apoyan en ese flujo sin alterarlo.

**Figura 1. Arquitectura del prototipo**

[FIGURA: arquitectura_prototipo.png]

Fuente: Elaboración propia

El principio de diseño central es la separación de responsabilidades entre el modelo de lenguaje y el resto del sistema. El modelo de lenguaje interpreta la pregunta del usuario y redacta la respuesta, pero las cifras proceden siempre del motor determinista a través de una herramienta (*tool*) con un esquema cerrado. Este patrón, conocido como uso de herramientas o anclaje (*grounding*), reduce el riesgo de cifras inventadas descrito en el capítulo 1.

La implementación se ha realizado en Python, con un número reducido de dependencias: `lxml` para leer los documentos, `pandas` para el tratamiento tabular y `PyYAML` para el diccionario semántico.

## 3.3. Extracción de datos desde ESEF

### 3.3.1. Fuentes

Se han utilizado los informes financieros anuales consolidados del ejercicio 2025 de seis entidades: Banco Santander, BBVA, CaixaBank y Banco Sabadell (banca), y Mapfre y Línea Directa Aseguradora (seguros) (Banco Santander, 2026; Banco Bilbao Vizcaya Argentaria, 2026; CaixaBank, 2026; Banco de Sabadell, 2026; Mapfre, 2026; Línea Directa Aseguradora, 2026). Cada informe incluye las cifras comparativas de 2024, lo que permite analizar ambos ejercicios con un único documento por entidad. Los paquetes, en formato de paquete de informe XBRL (`.xbri`), contienen un documento XHTML con XBRL incrustado (*Inline XBRL*) y la taxonomía de extensión de la entidad (esquema y bases de enlaces de cálculo, presentación, definición y etiquetas).

### 3.3.2. Un lector propio de Inline XBRL

La opción habitual para procesar XBRL es un procesador completo como Arelle. Sin embargo, este necesita descargar las taxonomías de ESMA y del IFRS Foundation para cargar el documento, lo que introduce una dependencia de red y de versiones. Como el objetivo del prototipo es leer cifras y no validar el documento, se ha desarrollado un lector propio (`ixbrl_parser.py`, unas 200 líneas) que trabaja solo con el contenido del paquete:

- **Contextos:** lee los contextos XBRL (entidad, periodo instantáneo o de duración y dimensiones explícitas o tipadas).
- **Hechos numéricos:** extrae los elementos `ix:nonFraction` y aplica las transformaciones de formato numérico (separadores de miles y decimales a la española o a la anglosajona, guiones como cero), el factor de escala (`scale`) y el signo (`sign`).
- **Etiquetas:** recupera de la base de enlaces de etiquetas del paquete el nombre en español de cada elemento de extensión, lo que permite interpretarlos sin consultar fuentes externas.
- **Deduplicación:** elimina los hechos repetidos, ya que una misma cifra aparece a menudo en los estados y en las notas.

El resultado es una tabla plana por entidad con una fila por hecho numérico. El procesamiento de los seis paquetes, que suman unos 157 MB, tarda menos de diez segundos en el entorno de desarrollo utilizado y produce 6.835 hechos (Tabla 1).

**Tabla 1. Hechos numéricos extraídos por entidad (informe ESEF 2025)**

| Entidad | Hechos | Sin dimensiones | De extensión propia | % extensión |
|---|---|---|---|---|
| Banco Santander | 1.725 | 656 | 492 | 29 % |
| BBVA | 1.634 | 862 | 558 | 34 % |
| Banco Sabadell | 1.217 | 652 | 450 | 37 % |
| CaixaBank | 1.088 | 722 | 306 | 28 % |
| Mapfre | 713 | 405 | 260 | 36 % |
| Línea Directa | 458 | 332 | 178 | 39 % |
| **Total** | **6.835** | **3.629** | **2.244** | **33 %** |

Fuente: Elaboración propia a partir de los informes ESEF de las entidades.

Un tercio de las cifras utiliza elementos de extensión propios de cada entidad en lugar de los de la taxonomía NIIF común. Este dato, por sí solo, justifica la necesidad de una capa que traduzca las etiquetas a conceptos comparables.

### 3.3.3. Alcance de la extracción

El motor trabaja con los hechos **sin dimensiones**, que corresponden a las cifras totales de los estados principales. Los hechos con dimensiones (desgloses por segmento, cartera o componente del patrimonio) se conservan en la tabla, pero no se usan en esta versión. Esta decisión simplifica la resolución de conceptos a cambio de no aprovechar los desgloses de las notas, que en ESEF solo están etiquetados en bloque de texto.

## 3.4. El diccionario semántico

### 3.4.1. Estructura

El diccionario semántico (`config/diccionario_semantico.yaml`, Anexo A) es el núcleo de la contextualización. Es un fichero declarativo, legible por un analista sin conocimientos de programación, con tres secciones:

1. **Conceptos canónicos.** Son las magnitudes financieras que intervienen en los ratios (resultado atribuido, patrimonio atribuido, margen bruto, ingresos por contratos de seguro, etc.). Cada una indica si es un flujo del periodo o un saldo a fecha.
2. **Ratios.** Recoge los doce ratios del catálogo. Para cada uno se indica la fórmula sobre conceptos canónicos, el tipo de entidad al que aplica, la fuente (calculable desde ESEF o dato publicado), las variantes de definición conocidas y una pauta de interpretación.
3. **Mapeo.** Contiene las reglas que resuelven cada concepto canónico en datos XBRL concretos.

### 3.4.2. Reglas de mapeo

Las reglas de mapeo admiten cuatro formas, que cubren todos los casos encontrados en las seis entidades:

- **Suma de etiquetas:** el concepto es la suma de uno o varios elementos. Así se resuelven, por ejemplo, los préstamos a la clientela de BBVA, desglosados por cartera contable.
- **Diferencia:** el concepto es la diferencia entre dos elementos. Es el caso del patrimonio atribuido: patrimonio total menos intereses minoritarios.
- **Regla por defecto y excepción:** cada concepto tiene una regla por defecto para todas las entidades o para un grupo (banca o seguros), que una regla específica de entidad puede sustituir.
- **No disponible con motivo:** el concepto no está etiquetado en el informe de esa entidad y la regla documenta por qué.

La Tabla 2 resume las reglas aplicadas a los conceptos donde el etiquetado de las entidades diverge.

**Tabla 2. Reglas de mapeo para los conceptos con etiquetado heterogéneo**

| Concepto | Regla aplicada | Motivo |
|---|---|---|
| Patrimonio atribuido | Equity − NoncontrollingInterests (todas; si no hay minoritarios etiquetados, Equity) | Solo dos entidades usan el elemento estándar, y una de ellas lo usa para otra magnitud |
| Fondos propios (variante) | Extensión propia (Santander, BBVA, Sabadell, Línea Directa); elemento NIIF mal usado (CaixaBank); no disponible (Mapfre) | No existe un elemento NIIF equivalente de uso común |
| Margen de intereses | InterestRevenueExpense (banca) | Ningún banco usa InterestIncomeExpenseNet |
| Margen bruto | GrossProfit (banca) | Los bancos reutilizan un elemento pensado para la industria |
| Préstamos y depósitos de la clientela | Total (CaixaBank, Sabadell); suma de carteras (BBVA); no disponible (Santander) | Distinto nivel de desglose |
| Ingresos por contratos de seguro | InsuranceRevenue (Línea Directa); extensión propia (Mapfre) | Mapfre no usa el elemento NIIF |
| Siniestralidad y gastos | Extensiones de Mapfre; no disponible (Línea Directa) | Línea Directa solo etiqueta el total de gastos del servicio de seguro |

Fuente: Elaboración propia.

### 3.4.3. La regla del patrimonio atribuido

La regla del patrimonio atribuido merece una explicación detallada, porque ilustra el valor de la capa semántica. La taxonomía NIIF ofrece un elemento específico para esta magnitud (`EquityAttributableToOwnersOfParent`), pero solo CaixaBank y Mapfre lo utilizan. En el caso de CaixaBank, además, la cifra etiquetada con ese elemento (38.962 millones de euros) es mayor que su patrimonio neto total (38.526 millones). Esto solo es posible si en realidad corresponde a los fondos propios, que excluyen el otro resultado global acumulado, negativo en esta entidad. El resto de bancos etiqueta sus fondos propios con extensiones propias.

Un mapeo literal por nombre de elemento habría tomado para CaixaBank los fondos propios y para las demás entidades nada, o la extensión que cada una haya elegido. La regla adoptada, patrimonio total menos minoritarios, se basa en dos elementos estándar. Las seis entidades etiquetan el patrimonio total y cinco de ellas los minoritarios; Línea Directa, sin minoritarios relevantes, no los etiqueta, y Sabadell no lo hace en el saldo de 2023. En esos casos se toma el patrimonio total y el motor lo indica en la traza. El resultado es una magnitud homogénea. La variante sobre fondos propios se conserva como ratio separado, porque es la base que muchas entidades usan en sus medidas alternativas de rendimiento.

## 3.5. Motor de ratios

### 3.5.1. Funcionamiento

El motor (`motor.py`) recorre las entidades y los ejercicios 2024 y 2025. Para cada ratio aplicable al tipo de entidad, resuelve el numerador y el denominador mediante las reglas del diccionario y calcula el cociente. Se aplican tres convenciones:

- **Flujos:** se toman los hechos cuyo periodo cubre el año natural completo (del 1 de enero al 31 de diciembre).
- **Saldos promedio:** para los denominadores de rentabilidad (patrimonio y activo) se usa la media de los saldos inicial y final. Si el saldo inicial no está etiquetado, lo que ocurre con el ejercicio 2023 en algunas entidades, se usa el saldo de cierre y el resultado se marca con un aviso.
- **Ratios derivados de seguros:** el ratio de gastos se obtiene como la diferencia entre los gastos del servicio de seguro y la siniestralidad, sobre los ingresos por contratos de seguro. El ratio combinado es el cociente entre el total de gastos del servicio de seguro y esos ingresos, bruto de reaseguro.

### 3.5.2. Trazabilidad

Cada ratio se guarda con su traza completa en `data/results/trazas.json`: la regla aplicada a cada componente, las etiquetas XBRL utilizadas, sus valores y fechas, y el identificador de cada hecho en el documento XHTML. Con ese identificador se puede localizar la cifra exacta en el informe oficial. El ejemplo siguiente muestra la traza del ROE de BBVA en 2025:

- **Numerador:** resultado atribuido, etiqueta `ifrs-full:ProfitLossAttributableToOwnersOfParent`, 10.511 millones de euros.
- **Denominador:** media del patrimonio atribuido a 31/12/2024 y 31/12/2025. Cada saldo se calcula como `ifrs-full:Equity` menos `ifrs-full:NoncontrollingInterests`, y la media resulta en 56.506 millones de euros.
- **Resultado:** 18,60 %.

### 3.5.3. Cobertura

El motor calcula 64 de los 72 valores que le corresponden (89 %): los ocho ratios derivables de ESEF más la variante del ROE sobre fondos propios, para cada entidad a la que aplican y para los dos ejercicios. Los ocho restantes no son calculables a partir de los datos etiquetados: la ratio préstamos/depósitos de Santander, la siniestralidad y el ratio de gastos de Línea Directa en ambos ejercicios, y el ROE sobre fondos propios de Mapfre. En todos los casos la herramienta informa del motivo. Los ratios regulatorios (morosidad, cobertura, CET1 y Solvencia II) no se calculan: proceden de la información publicada por las entidades y se tratan en el apartado siguiente.

## 3.6. Datos publicados por las entidades

Los ratios regulatorios y las medidas alternativas de rendimiento que publica cada entidad se han extraído del informe de gestión incluido en el propio paquete ESEF. Para cada uno se ha registrado el valor, la variante (por ejemplo, CET1 *fully loaded* o *phased-in*), la definición que da la entidad, la sección donde aparece y una cita literal breve que permite verificarlo (`data/published/ratios_publicados.csv`). Estos datos cumplen dos funciones: completan el catálogo con los ratios que no se pueden calcular y sirven de referencia para validar el motor (capítulo 4).

## 3.7. Capa de consulta en lenguaje natural

### 3.7.1. Diseño

La capa de consulta (`consulta.py`) expone una única función, `consultar(entidad, ratio, ejercicio)`, que devuelve una respuesta estructurada con:

- el valor calculado, la fórmula y las cifras de origen;
- el valor o valores publicados por la entidad, con su definición;
- los comparables del mismo grupo calculados con la misma definición;
- los avisos de comparabilidad, como una base de saldo de cierre, una diferencia significativa con el valor publicado o la sensibilidad del ROE a la base de patrimonio;
- la pauta de interpretación del diccionario.

Esta función se ofrece a un modelo de lenguaje como herramienta, con un esquema de entrada cerrado: la entidad, el ratio y el ejercicio solo pueden tomar los valores del catálogo. La descripción de la herramienta indica al modelo que debe usarla para cualquier cifra y que no debe calcularlas ni recordarlas por su cuenta. El modelo queda limitado a dos tareas en las que es fiable: traducir la pregunta a una o varias llamadas y redactar la respuesta a partir del resultado.

### 3.7.2. Funcionamiento sin modelo de lenguaje

Para que la herramienta pueda demostrarse y evaluarse sin depender de un proveedor comercial, el módulo incluye un intérprete por reglas, que identifica entidades, ratio y ejercicio mediante patrones, y una redacción por plantilla. Ante la pregunta «¿Cuál fue el ROE de Santander y de BBVA en 2025?», el prototipo responde con el valor calculado de cada entidad, su fórmula y cifras de origen, los comparables homogéneos y el aviso de que el ROE depende de la base de patrimonio elegida. Ante una pregunta sobre la ratio préstamos/depósitos de Santander, responde que no es calculable desde ESEF y explica el motivo, en lugar de ofrecer una cifra.

## 3.8. Limitaciones del diseño

- **Muestra:** el diccionario se ha verificado con seis entidades. Su extensión a otras exige revisar sus etiquetas de extensión, aunque las reglas por defecto cubren la mayoría de conceptos.
- **Hechos con dimensiones:** no se usan, lo que impide, por ejemplo, separar el negocio de vida y no vida de Mapfre.
- **Mapeo manual asistido:** las reglas se han definido a partir de la exploración de los datos. La propuesta inicial de usar un modelo de lenguaje para sugerir el mapeo de extensiones queda como línea de trabajo futuro.
- **Perímetro:** los cambios de perímetro, como activos mantenidos para la venta o desinversiones en curso, afectan a los saldos y deben interpretarse con la información narrativa del informe (capítulo 4).
