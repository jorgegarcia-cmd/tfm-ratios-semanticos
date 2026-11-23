# 5. Conclusiones

## 5.1. Respuesta a los objetivos

El objetivo general de este trabajo era diseñar y validar una herramienta de contextualización semántica que permitiera calcular e interpretar de forma fiable y trazable los ratios financieros de entidades bancarias y aseguradoras. A continuación se revisa cada objetivo específico.

**Objetivo 1. Analizar los problemas de comparabilidad.** El trabajo ha identificado y cuantificado tres fuentes de falta de comparabilidad que coexisten en la información oficial de las entidades:

- **Etiquetado heterogéneo:** un tercio de las cifras de los informes ESEF usa extensiones propias, y conceptos básicos como el patrimonio atribuido, el margen bruto o los préstamos a la clientela se etiquetan de forma distinta, o no se etiquetan.
- **Definiciones divergentes:** las medidas alternativas de rendimiento se definen de forma distinta pese a llevar el mismo nombre; el ROE de los seis informes usa al menos cuatro bases de patrimonio diferentes.
- **Perímetro y normativa:** los cambios de perímetro y las distintas variantes regulatorias (CET1 *phased-in*, *fully loaded* o de gestión; Solvencia II individual o de grupo) impiden comparar cifras que en apariencia son homogéneas.

**Objetivo 2. Diseñar un diccionario semántico.** Se ha construido un diccionario declarativo con diecisiete conceptos canónicos y doce ratios. Sus reglas de mapeo (suma, diferencia, excepción por entidad y no disponibilidad motivada) bastan para resolver todos los casos encontrados en las seis entidades. La regla del patrimonio atribuido como diferencia entre patrimonio total e intereses minoritarios es un buen ejemplo: sustituye a un elemento NIIF que las entidades usan de forma inconsistente por una definición homogénea basada en dos elementos estándar, con un tratamiento explícito y trazado de los casos en que falta uno de ellos.

**Objetivo 3. Desarrollar un prototipo trazable.** El prototipo calcula 64 de los 72 valores que le corresponden (los ocho ratios derivables de ESEF y la variante del ROE sobre fondos propios) a partir de los informes oficiales, e integra los cuatro ratios regulatorios publicados. Cada cifra conserva su traza hasta el hecho XBRL de origen y, cuando un dato no está etiquetado, el sistema lo declara con su motivo. El lector propio de Inline XBRL procesa los seis informes en pocos segundos y sin conexión a internet.

**Objetivo 4. Validar frente a las cifras publicadas.** En 23 de 37 comparaciones el ratio calculado coincide con el publicado con una diferencia absoluta inferior a 0,5 puntos; la diferencia absoluta mediana es de 0,22 puntos. Las 14 diferencias restantes se explican principalmente por diferencias de definición o de perímetro, en su mayoría documentadas por las propias entidades. Esto valida el motor y, a la vez, confirma la utilidad de mostrar ambas cifras con sus definiciones.

**Objetivo 5. Evaluar la capa de consulta con un modelo de lenguaje.** [PENDIENTE: completar con los resultados de la sección 4.4.2.]

## 5.2. Contribuciones

Desde el punto de vista financiero, el trabajo documenta con datos reales que comparar ratios publicados por distintas entidades puede llevar a conclusiones erróneas sin un análisis previo de sus definiciones. El caso del ROE de BBVA es ilustrativo: con la base de patrimonio que usa la entidad lidera la muestra, y con la base de fondos propios queda por detrás de CaixaBank.

Desde el punto de vista tecnológico, el trabajo propone una arquitectura en la que el modelo de lenguaje no genera cifras, y la demuestra con un intérprete por reglas. Sus funciones se limitan a interpretar la pregunta y redactar la respuesta, mientras que un motor determinista y trazable, gobernado por un diccionario semántico explícito, produce los datos. Este diseño hace que la respuesta sea verificable por un analista, requisito imprescindible para su uso en un entorno financiero.

## 5.3. Limitaciones

- **Muestra reducida:** seis entidades y dos ejercicios. El diccionario debe revisarse para incorporar nuevas entidades, aunque las reglas por defecto cubren la mayoría de conceptos.
- **Solo hechos sin dimensiones:** no se aprovechan los desgloses dimensionales, lo que impide, por ejemplo, separar los negocios de vida y no vida.
- **Mapeo manual asistido:** las reglas se han definido a partir de la exploración de los datos, no de forma automática.
- **Ratios regulatorios no calculables:** la morosidad, la cobertura, el CET1 y la Solvencia II dependen de la información publicada, porque no están en los estados estructurados.
- **Evaluación limitada:** se ha usado un número reducido de preguntas y un único modelo generalista, y la capa de consulta se ha probado con un intérprete por reglas, sin integrar un modelo de lenguaje por API.
- **Tolerancia de validación:** el umbral absoluto de 0,5 puntos es holgado para ratios de nivel bajo; una tolerancia relativa o específica por ratio daría una validación más exigente.

## 5.4. Trabajo futuro

- **Ampliar la muestra:** incorporar Bankinter y Unicaja y una serie temporal más larga.
- **Usar las dimensiones XBRL** para calcular ratios por segmento.
- **Automatizar el mapeo de extensiones:** las extensiones ESEF deben anclarse a un elemento de la taxonomía NIIF, y un modelo de lenguaje podría proponer reglas para que un analista las valide.
- **Integrar un modelo de lenguaje por API** con llamada a herramientas y repetir la evaluación con un conjunto de preguntas más amplio.
- **Incorporar la información regulatoria estructurada** (Pilar 3 y los informes de Solvencia II) para calcular, y no solo consultar, los ratios de solvencia y calidad del activo.
