# 1. Introducción

## 1.1. Contexto y motivación

El análisis por ratios es una de las herramientas más antiguas y extendidas del análisis financiero. Reducir los estados financieros a un conjunto de cocientes permite comparar entidades de tamaño distinto, seguir la evolución de una misma entidad en el tiempo y resumir en pocas cifras su rentabilidad, eficiencia, liquidez o solvencia. En el sector financiero esta práctica está especialmente arraigada: inversores, analistas, agencias de calificación y supervisores siguen de cerca el ROE, la ratio de eficiencia o la tasa de morosidad de los bancos, y el ratio combinado o el ratio de solvencia de las aseguradoras.

Calcular un ratio es, sin embargo, mucho más sencillo que conseguir que sea fiable y comparable. Un ROE exige decidir qué resultado se toma (atribuido o consolidado, estatutario o ajustado), qué patrimonio se usa como denominador (con o sin ajustes por valoración, con o sin instrumentos de capital adicional de nivel 1) y cómo se promedia (saldo de cierre, media de dos puntos, media mensual). Cada entidad toma estas decisiones a su manera y las publica como medidas alternativas de rendimiento (APM). Las Directrices de la Autoridad Europea de Valores y Mercados exigen definirlas y conciliarlas (ESMA, 2015), pero no imponen una definición común. El resultado es que dos ratios con el mismo nombre pueden medir cosas distintas.

La digitalización de la información financiera prometía aliviar este problema. Desde los ejercicios iniciados el 1 de enero de 2020, los emisores con valores admitidos a negociación en mercados regulados de la Unión Europea deben publicar su informe financiero anual en el formato electrónico único europeo (ESEF), con los estados financieros consolidados NIIF etiquetados en XBRL (Reglamento Delegado (UE) 2019/815, 2018). En teoría, cada cifra lleva asociada una etiqueta de una taxonomía común que fija su significado. En la práctica, las entidades pueden crear elementos de extensión propios cuando consideran que la taxonomía base no recoge adecuadamente una partida, y la literatura ha documentado desde hace más de una década que estas extensiones se usan con frecuencia de forma innecesaria (Debreceny et al., 2011). Los datos de este trabajo lo confirman para el sector financiero español: entre el 28 % y el 39 % de los hechos numéricos de los informes ESEF 2025 analizados utilizan extensiones propias, y conceptos tan básicos como el patrimonio atribuido a la dominante se etiquetan de forma heterogénea (capítulo 4).

A esta dificultad se suma la aparición de los grandes modelos de lenguaje (LLM). Su capacidad para leer documentos y responder preguntas en lenguaje natural los convierte en candidatos obvios para automatizar el análisis financiero, pero la evidencia disponible muestra que cometen errores frecuentes cuando deben localizar cifras y operar con ellas. En el banco de pruebas FinanceBench, un modelo de última generación con recuperación de documentos respondió de forma incorrecta o se negó a responder en el 81 % de las preguntas evaluadas (Islam et al., 2023). Un LLM consultado directamente puede, además, proponer una fórmula plausible pero distinta de la que usa la entidad, o inventar una cifra con apariencia de exactitud.

El problema que motiva este Trabajo Fin de Máster se sitúa en la intersección de estas tres circunstancias: la heterogeneidad de las definiciones de los ratios, la calidad desigual del etiquetado XBRL y la falta de fiabilidad numérica de los modelos de lenguaje. La hipótesis de trabajo es que una capa de contextualización semántica, que haga explícito qué significa cada partida y cada ratio, permite calcular ratios trazables y comparables y, al mismo tiempo, ofrecer a un modelo de lenguaje una base factual sobre la que responder sin inventar cifras.

El trabajo se centra en el sector financiero español porque sus entidades cotizadas publican, junto al informe ESEF, información regulatoria específica (Pilar 3 en banca, informe sobre la situación financiera y de solvencia en seguros) que permite contrastar ambas fuentes, y porque la entrada en vigor de la NIIF 17 en 2023 ha alterado la base de los ratios técnicos de las aseguradoras (IASB, 2017b).

## 1.2. Objetivos

El **objetivo general** de este trabajo es diseñar y validar una herramienta de contextualización semántica que permita calcular e interpretar de forma fiable y trazable los ratios de entidades bancarias y aseguradoras.

Este objetivo se descompone en cinco **objetivos específicos**:

1. **OE1.** Analizar los problemas de comparabilidad que afectan a los ratios del sector financiero: definiciones heterogéneas de las APM, efectos de la normativa contable y prudencial, y calidad del etiquetado ESEF/XBRL.
2. **OE2.** Diseñar un diccionario semántico que relacione las partidas ESEF/XBRL y los datos publicados por las entidades con un conjunto de conceptos financieros canónicos.
3. **OE3.** Construir un prototipo que calcule doce ratios (ROE, ROA, eficiencia, margen de intereses sobre activos medios, préstamos sobre depósitos, morosidad, cobertura, CET1, siniestralidad, ratio de gastos, ratio combinado y ratio de Solvencia II) con trazabilidad completa hasta el dato de origen.
4. **OE4.** Validar los ratios calculados frente a las APM publicadas por las entidades y explicar las diferencias encontradas.
5. **OE5.** Evaluar si un modelo de lenguaje apoyado en la capa semántica responde preguntas sobre ratios con mayor fiabilidad que un modelo de lenguaje consultado directamente.

El **alcance** se ha delimitado a seis entidades cotizadas españolas: cuatro bancos (Banco Santander, BBVA, CaixaBank y Banco Sabadell) y dos aseguradoras (Mapfre y Línea Directa Aseguradora). Se analiza el ejercicio 2025 con el comparativo de 2024 que incluye el propio informe. Bankinter y Unicaja, inicialmente consideradas, quedan como trabajo futuro, y Grupo Catalana Occidente se excluye por haber dejado de cotizar el 5 de enero de 2026.

## 1.3. Metodología

### 1.3.1. Enfoque: Design Science Research

El trabajo sigue el paradigma de la investigación orientada al diseño (*Design Science Research*, DSR). A diferencia de la investigación explicativa, que busca describir o predecir fenómenos, la DSR tiene por objeto crear y evaluar artefactos (constructos, modelos, métodos o instanciaciones) que resuelvan problemas relevantes para una organización o un colectivo de usuarios (Hevner et al., 2004). Hevner et al. (2004) proponen siete pautas para este tipo de investigación, entre las que destacan que el resultado sea un artefacto viable, que el problema sea relevante, que la utilidad del artefacto se demuestre mediante métodos de evaluación rigurosos y que la investigación se apoye en la base de conocimiento existente.

Para estructurar el proceso se adopta la metodología de Peffers et al. (2007), que organiza la DSR en seis actividades: identificación del problema y motivación, definición de los objetivos de la solución, diseño y desarrollo, demostración, evaluación y comunicación. La Tabla 1 muestra cómo se concreta cada actividad en este trabajo.

**Tabla 1. Aplicación de las actividades de Design Science Research al trabajo**

| Actividad (Peffers et al., 2007) | Concreción en este trabajo | Capítulo |
|---|---|---|
| Identificación del problema y motivación | Heterogeneidad de las APM, extensiones en ESEF, efectos de NIIF 9 y NIIF 17, errores numéricos de los LLM | 1 y 2 |
| Definición de los objetivos de la solución | Requisitos de fuente oficial, cálculo determinista, trazabilidad, explicitud semántica y transparencia ante la falta de datos | 2 y 3 |
| Diseño y desarrollo | Lector de Inline XBRL, diccionario semántico en YAML, motor de ratios y capa de consulta en lenguaje natural | 3 |
| Demostración | Cálculo de los doce ratios para seis entidades y dos ejercicios | 4 |
| Evaluación | (a) Ratios calculados frente a publicados; (b) veinte preguntas a un LLM solo frente a un LLM con capa semántica | 4 |
| Comunicación | Esta memoria y el repositorio del prototipo | 5 y anexos |

Fuente: Elaboración propia a partir de Peffers et al. (2007).

### 1.3.2. Identificación del problema

La primera fase consiste en caracterizar con precisión los problemas de comparabilidad. Para ello se combinan dos fuentes: la revisión de la normativa y de la literatura (apartado 1.4 y capítulo 2) y una exploración empírica de los informes ESEF de las seis entidades. Esta exploración ha permitido cuantificar el uso de extensiones y detectar patrones de etiquetado que afectan directamente al cálculo de ratios, como el uso de elementos de la taxonomía NIIF pensados para empresas industriales en la cuenta de resultados bancaria.

### 1.3.3. Diseño del artefacto

El artefacto es una herramienta compuesta por cuatro elementos, que se describen en detalle en el capítulo 3:

- **Un lector propio de Inline XBRL**, escrito en Python, que extrae los hechos numéricos del documento XHTML del paquete ESEF junto con su contexto (entidad, periodo y dimensiones), su unidad y su identificador dentro del documento. Se ha optado por un lector propio en lugar de un procesador XBRL completo porque el objetivo es leer cifras, no validar el informe, y porque así se evita la dependencia de la descarga de taxonomías externas.
- **Un diccionario semántico en formato YAML**, que define los conceptos financieros canónicos (por ejemplo, «patrimonio atribuido a la dominante» o «margen de intereses»), su naturaleza de flujo o saldo, las etiquetas XBRL que los representan en cada entidad y el catálogo de ratios con su fórmula, sus variantes de definición conocidas y una pauta de interpretación. El formato YAML se ha elegido porque es legible por un analista financiero sin formación técnica y, a la vez, procesable por un programa.
- **Un motor de ratios determinista**, que calcula cada ratio a partir del diccionario y guarda una traza completa hasta los hechos XBRL de origen.
- **Una capa de consulta en lenguaje natural**, en la que un modelo de lenguaje interpreta la pregunta del usuario y redacta la respuesta, pero obtiene las cifras exclusivamente del motor a través de una herramienta con un esquema de entrada cerrado.

El principio de diseño que articula los cuatro componentes es la separación entre interpretación y cálculo: el conocimiento financiero se hace explícito en el diccionario, el cálculo es determinista y el modelo de lenguaje se limita a las tareas en las que es fiable.

### 1.3.4. Demostración y evaluación

La demostración consiste en aplicar la herramienta a las seis entidades de la muestra para los ejercicios 2024 y 2025. La evaluación se realiza en dos planos:

1. **Validación de los ratios.** Cada ratio calculado se compara con el valor publicado por la entidad. Las diferencias no se tratan como errores sin más, sino que se explican a partir de las diferencias de definición documentadas en el diccionario. Una herramienta fiable no es la que reproduce exactamente la cifra publicada, sino la que permite saber por qué difiere.
2. **Evaluación de la capa de consulta.** Se formula un conjunto de veinte preguntas sobre los ratios de la muestra a un modelo de lenguaje consultado directamente y al mismo modelo apoyado en la capa semántica. Las respuestas del modelo consultado directamente las obtiene el autor mediante una interfaz de chat, sin uso de API, y se valoran según su exactitud numérica, la corrección de la fórmula y la presencia de advertencias de comparabilidad.

### 1.3.5. Fuentes de datos

Se utilizan exclusivamente fuentes oficiales publicadas por las propias entidades:

- **Informes financieros anuales consolidados en formato ESEF** del ejercicio 2025, que incluyen el comparativo de 2024. Son la fuente de los ratios calculados.
- **Informes de gestión y anexos de medidas alternativas de rendimiento**, incluidos en el propio informe anual, como fuente de los ratios publicados y de sus definiciones.
- **Información regulatoria**: los datos de Pilar 3 publicados por los bancos en aplicación del Reglamento (UE) n.º 575/2013 (2013) y los datos de solvencia de las aseguradoras derivados de la Directiva 2009/138/CE (2009), en la medida en que aparecen en el informe de gestión.

### 1.3.6. Herramientas

El prototipo se ha desarrollado en Python, con un número reducido de dependencias (lectura de XML, tratamiento tabular y lectura de YAML). El diccionario semántico se mantiene como un fichero YAML versionado junto al código. La capa de consulta está diseñada para funcionar con un modelo de lenguaje comercial mediante uso de herramientas (*tool use*) y dispone además de un intérprete por reglas que permite demostrarla sin depender de un proveedor externo.

## 1.4. Estado de la cuestión

### 1.4.1. El análisis por ratios en banca y seguros

El análisis por ratios descansa en supuestos que la literatura clásica ya identificó como problemáticos, entre ellos que numerador y denominador guarden una relación proporcional y que las magnitudes se definan de forma homogénea entre empresas (Barnes, 1987). En el sector financiero estos problemas se agravan por la propia naturaleza del negocio. El balance de un banco está formado mayoritariamente por instrumentos financieros, su cuenta de resultados no se organiza en torno a ventas y coste de ventas, y una parte esencial de su desempeño (la calidad de los activos y la solvencia) se mide con magnitudes definidas por la normativa prudencial y no por la contable.

Los supervisores europeos han intentado ofrecer definiciones de referencia. La Autoridad Bancaria Europea (EBA) mantiene una guía metodológica con los indicadores de riesgo que utiliza en sus análisis, entre ellos el ROE, la ratio de eficiencia, la ratio de préstamos sobre depósitos, la tasa de morosidad, la cobertura y la ratio CET1 (EBA, s. f.). La propia guía ilustra hasta qué punto las convenciones importan: el ROE trimestral se calcula con un patrimonio medio entre el último cierre anual y el trimestre en curso, y los flujos acumulados se anualizan. Estas convenciones son razonables, pero no coinciden necesariamente con las que aplica cada banco en sus APM.

En seguros, la NIIF 17 ha sustituido las primas como medida de ingresos por los ingresos por contratos de seguro, que se reconocen a medida que se presta la cobertura y excluyen los componentes de inversión (IASB, 2017a). El propio análisis de efectos del IASB advierte de que el ratio combinado seguirá siendo una métrica central para los contratos de corto plazo, pero calculado con siniestros descontados y que incluyen un ajuste por riesgo, de modo que su variación dependerá de las circunstancias de cada aseguradora (IASB, 2017b). El capítulo 2 desarrolla estos ratios y sus variantes de definición.

### 1.4.2. Información financiera estructurada: XBRL y ESEF

XBRL (*eXtensible Business Reporting Language*) es un estándar para el intercambio de información empresarial en el que cada dato numérico (un «hecho») se asocia a un concepto de una taxonomía, a un periodo, a una entidad y, en su caso, a unas dimensiones. La variante Inline XBRL permite incrustar estas etiquetas en un documento HTML que se visualiza normalmente en un navegador, de modo que un mismo fichero sirve para la lectura humana y para la extracción automática (XBRL International, 2013).

El Reglamento Delegado (UE) 2019/815 (2018) adoptó Inline XBRL como formato del informe financiero anual de los emisores cotizados de la Unión. Los estados financieros consolidados NIIF deben etiquetarse con los elementos de la taxonomía ESEF, basada en la taxonomía NIIF publicada por la IFRS Foundation. Cuando ningún elemento de esta taxonomía es adecuado, el emisor puede crear elementos de extensión propios. Para preservar la comparabilidad, el Manual de Información ESEF de ESMA exige que las extensiones utilizadas en los estados financieros principales se vinculen (*anchoring*) a uno o varios elementos de la taxonomía base de significado más amplio o más restringido (ESMA, 2022a). ESMA ha seguido precisando estas reglas, por ejemplo exigiendo que el elemento de anclaje tenga el mismo tipo de dato que la extensión (ESMA, 2024).

La calidad del etiquetado XBRL ha sido objeto de una línea de investigación consolidada. En el contexto estadounidense, Debreceny et al. (2010) encontraron que aproximadamente una cuarta parte de las primeras presentaciones XBRL ante la SEC de grandes empresas contenían errores en las relaciones de cálculo, es decir, totales que no coincidían con la suma de sus componentes. En un trabajo posterior, Debreceny et al. (2011) analizaron las extensiones y concluyeron que en torno al 40 % eran innecesarias, porque la taxonomía ya contenía un elemento equivalente.

En Europa, la investigación sobre ESEF es más reciente. Heichl et al. (2025) estudian los informes ESEF de las compañías del STOXX Europe 600 de los ejercicios 2021 y 2022 y concluyen que la transparencia y la comparabilidad varían significativamente por país, sector y tamaño, y que el uso de extensiones en lugar de elementos estándar dificulta el análisis. Zvekan (2025), con una muestra de 2.448 informes ESEF entre 2020 y 2023, observa que alrededor del 14 % contienen elementos sin anclar y que el recurso a proveedores externos se asocia a una mayor probabilidad de extensiones innecesarias. XBRL International, por su parte, ha propuesto aprovechar las relaciones de anclaje para agrupar extensiones y detectar prácticas comunes que podrían incorporarse a la taxonomía; en una muestra de informes ESEF de 2021, más de 900 extensiones estaban ancladas al elemento genérico de patrimonio neto (XBRL International, 2024). Este dato es especialmente relevante para este trabajo, porque el patrimonio es el denominador del ROE y, como se verá en el capítulo 4, es precisamente uno de los conceptos peor etiquetados en la muestra.

### 1.4.3. Ontologías financieras

En ingeniería del conocimiento, una ontología es una especificación explícita del vocabulario compartido de un dominio: las clases de objetos que lo componen, sus propiedades y las relaciones entre ellos (Gruber, 1993). Su finalidad es que personas y sistemas distintos interpreten los datos de la misma manera.

En el ámbito financiero, la iniciativa más ambiciosa es FIBO (*Financial Industry Business Ontology*), promovida por el EDM Council y estandarizada en el Object Management Group. FIBO está escrita en OWL y se organiza en módulos sobre entidades, instrumentos financieros, valores, derivados, préstamos, índices y datos de mercado, entre otros (EDM Council, s. f.; Bennett, 2013). Su foco son los contratos y las entidades del sector, no las partidas de los estados financieros ni los ratios, por lo que no resuelve por sí misma el problema que aborda este trabajo.

Una segunda línea de investigación ha tratado las taxonomías XBRL como ontologías. Spies (2010) analiza los principios lógicos de las taxonomías de información financiera y propone representarlas en OWL para integrarlas con otras fuentes de datos. Wunner et al. (2010) señalan que las taxonomías XBRL, incluida la NIIF, carecen del detalle semántico y terminológico necesario para reutilizarlas en tareas de extracción de información, y proponen enriquecerlas con relaciones entre términos e información lingüística. Ambos trabajos coinciden en que una taxonomía XBRL define etiquetas y relaciones de cálculo y presentación, pero no expresa todo el conocimiento necesario para interpretar una cifra: por ejemplo, que unos «fondos propios» etiquetados con una extensión no equivalen al patrimonio atribuido porque excluyen los ajustes por valoración.

Más recientemente, la combinación de grafos de conocimiento y modelos de lenguaje se ha convertido en un campo activo. Pan et al. (2024) proponen una hoja de ruta en la que los grafos de conocimiento aportan a los LLM conocimiento explícito y verificable, y los LLM ayudan a construir y consultar esos grafos. El diccionario semántico de este trabajo se inscribe en esta lógica, aunque con una ambición deliberadamente acotada: no pretende ser una ontología formal completa, sino una capa ligera y revisable por un analista que haga explícitas las equivalencias y diferencias entre conceptos.

### 1.4.4. Modelos de lenguaje en finanzas

El interés por aplicar modelos de lenguaje al ámbito financiero precede a los LLM conversacionales. BloombergGPT, un modelo de 50.000 millones de parámetros entrenado con 363.000 millones de *tokens* de datos financieros y 345.000 millones de datos de propósito general, mostró que un entrenamiento específico de dominio mejoraba los resultados en tareas financieras sin perder capacidad general (Wu et al., 2023).

Para medir la capacidad de razonamiento numérico se han desarrollado bancos de pruebas específicos. FinQA reúne preguntas que exigen combinar texto y tablas de informes financieros y ejecutar varios pasos de cálculo (Chen et al., 2021). TAT-QA plantea un problema similar sobre contenido híbrido tabular y textual de informes financieros (Zhu et al., 2021). FinanceBench evalúa preguntas sobre documentos públicos de empresas cotizadas y, como se ha señalado, revela tasas de error muy elevadas incluso con recuperación de documentos (Islam et al., 2023).

El fenómeno de fondo es la alucinación, entendida como la generación de contenido que no es fiel a la fuente o que no tiene respaldo en ella (Ji et al., 2023). En finanzas tiene consecuencias especialmente graves, porque una cifra inventada tiene la misma apariencia que una correcta. Kang y Liu (2023) documentan alucinaciones relevantes de modelos de uso general en tareas como la explicación de conceptos financieros o la consulta de cotizaciones históricas.

Se han propuesto varias estrategias de mitigación. La generación aumentada por recuperación (RAG) combina el modelo con un recuperador que le proporciona pasajes relevantes de una base documental (Lewis et al., 2020). El uso de herramientas permite que el modelo delegue en sistemas externos, como una calculadora o un motor de búsqueda, las tareas en las que es poco fiable (Schick et al., 2023). Los modelos asistidos por programas generan código que un intérprete ejecuta, de modo que el cálculo deja de depender del modelo (Gao et al., 2023). Kang y Liu (2023) evaluaron varias de estas técnicas, entre ellas RAG y el aprendizaje de herramientas mediante instrucciones, en el contexto financiero.

Dos trabajos recientes conectan directamente los LLM con XBRL. Han et al. (2024) evalúan modelos de lenguaje sobre informes XBRL, constatan sus limitaciones en conocimiento de dominio y cálculo, y muestran que un agente con recuperador y calculadora mejora notablemente la precisión, aunque el cálculo sigue teniendo margen de mejora. Wang et al. (2025) proponen un banco de pruebas de etiquetado XBRL y encuentran que los modelos extraen bien las cifras, pero tienen grandes dificultades para vincularlas al concepto correcto de la taxonomía. Este último resultado es significativo: la dificultad no está tanto en leer números como en saber qué significan.

### 1.4.5. El hueco que cubre este trabajo

La revisión anterior permite situar la aportación de este trabajo. La literatura sobre XBRL ha documentado los problemas de calidad del etiquetado, pero sin conectarlos de forma sistemática con el cálculo de ratios concretos. Las ontologías financieras existentes, como FIBO, no cubren las partidas de los estados ni las definiciones de los ratios. La investigación sobre LLM en finanzas ha mostrado que el anclaje en datos y el uso de herramientas mejoran la fiabilidad, pero suele trabajar con informes estadounidenses y no aborda la heterogeneidad de las APM ni la normativa europea.

Este trabajo integra los tres planos en un artefacto aplicado al sector financiero español: un diccionario semántico que hace explícito el significado de cada partida y de cada ratio, construido a partir de los datos ESEF reales; un motor que calcula los ratios con trazabilidad completa; y una capa de consulta que restringe al modelo de lenguaje a interpretar y redactar. Su aportación no es un modelo nuevo, sino una forma de organizar el conocimiento financiero que permite saber qué se está comparando y por qué dos cifras con el mismo nombre difieren.

## 1.5. Estructura del documento

La memoria se organiza en cinco capítulos, además de las referencias y los anexos:

- **Capítulo 1. Introducción.** Presenta el contexto, los objetivos, la metodología y el estado de la cuestión.
- **Capítulo 2. Marco financiero.** Define los doce ratios del catálogo, sus variantes de definición y los factores normativos (Directrices de ESMA sobre APM, NIIF 9, NIIF 17, Pilar 3 y Solvencia II) que limitan su comparabilidad, y deriva de ello los requisitos de la herramienta.
- **Capítulo 3. Diseño e implementación.** Describe la arquitectura del prototipo y cada uno de sus componentes: lector de Inline XBRL, diccionario semántico, motor de ratios y capa de consulta.
- **Capítulo 4. Resultados.** Presenta los hallazgos sobre el etiquetado ESEF, los ratios calculados, su validación frente a los publicados y la evaluación comparada del modelo de lenguaje con y sin capa semántica.
- **Capítulo 5. Conclusiones.** Resume las aportaciones, las limitaciones y las líneas de trabajo futuro.

Los anexos recogen el diccionario semántico completo, las preguntas de evaluación y la referencia al repositorio del código.
