# Notas sobre las APM publicadas (ESEF 2025)

Fuente única: paquetes ESEF FY2025 (XHTML) de cada entidad, convertidos a texto con `/home/claude/work_apm/to_text.py`. Todas las cifras de `ratios_publicados.csv` se han comprobado automáticamente (`/home/claude/work_apm/build_csv.py`): la `cita` aparece literalmente en el texto si se ignoran los separadores de celda. En las citas de tablas, " | " separa celdas (columnas en el orden del documento, normalmente 2025 | 2024 | 2023).

## Santander
- Sección 6 "Medidas alternativas de rendimiento (MAR)" del Informe económico y financiero, con fórmula y conciliación.
- **RoE**: denominador = patrimonio neto sin minoritarios **con OCI acumulado** + beneficio + "dividendos y retribuciones". Media de los saldos mensuales.
- **RoTE**: el numerador excluye los ajustes por valoración de fondos de comercio. También publica un **RoTE post-AT1** (16,3 %), que resta el coste de los AT1 y que el banco presenta como "la definición comúnmente utilizada".
- **RoA**: usa el resultado consolidado (incluye minoritarios), no el atribuido. También publica RoRWA.
- **Eficiencia (41,2 %)**: se calcula sobre la cuenta **ordinaria** (costes y margen bruto ajustados por actividad no ordinaria). Con cifras estatutarias saldría 24.711/58.670 ≈ 42,1 %. Ese valor no se publica y aquí solo se da como orientación.
- **Morosidad y cobertura**: incluyen garantías y saldos disponibles a la clientela. Excluyen POCI no deteriorada.
- **CET1**: 13,5 % phased-in en 2025 (13,46 % en la memoria). No publica un CET1 fully loaded para 2025 porque, según el banco, los criterios de CRR3 aún no están definidos. Para 2024 los dos son 12,8 %.
- **No encontrado**: NIM como ratio. Solo hay un balance medio con rendimientos por partida.

## BBVA
- Anexo MAR del Informe de Gestión: fórmula, explicación y tabla numerador/denominador.
- **ROE/ROTE**: denominador = fondos propios medios **+ OCI acumulado medio**, que en BBVA es muy negativo (-18.147 M€). Es la misma base que Santander, pero sin restar el AT1 en el numerador. Las medias son ponderadas mensuales y se ajustan por dividendo-opción.
- **Tasa de mora y cobertura**: en 2025 **cambia la definición** e incluye los préstamos a valor razonable con cambios en OCI (HTC&S). Puede romper la comparabilidad con los datos de 2024 publicados el año anterior. La cobertura usa fondos de stages 1+2+3 sobre stage 3.
- **CET1 12,70 %**: el banco declara que fully loaded = phased-in (impacto transitorio nulo). El dato de 2025 es provisional y bajo CRR3. El de 2024 (12,88 %) es bajo CRR2.
- **No encontrado**: NIM anual (solo un gráfico trimestral sin cifras en el texto) y loan-to-deposit.

## CaixaBank
- Glosario MAR del Informe de Gestión, con tablas (a)…(g).
- **ROE/ROTE/ROA/RORWA**: el numerador **resta el cupón AT1** en las cuatro métricas. El denominador del ROE incluye los ajustes de valoración (OCI). El ROTE descuenta también los intangibles y fondos de comercio de las participadas. Las medias combinan saldos diarios y mensuales, y en el RORWA son trimestrales.
- **Eficiencia**: publica dos ratios. El estándar es 39,4 % (38,5 % en 2024). El otro excluye el gravamen a la banca: 37,3 % en 2024.
- **CET1**: hay dos cifras para 2025. La de gestión es 12,6 %. La **regulatoria** es 12,25 %, porque deduce el exceso sobre el umbral de distribución extraordinaria, como exige el supervisor desde 2025.
- **LTD 86,9 %**: crédito neto de gestión, quitando el crédito de mediación, sobre depósitos más periodificadoras. La tabla del ESEF sale con las filas desalineadas (los importes no cuadran con las etiquetas), pero la ratio es legible.
- **NIM**: no se publica como MAR. Se ha registrado el "diferencial de balance" del 4T anualizado (1,61 %) como aproximación. Los rangos de NIM de la nota de deterioro de fondo de comercio son hipótesis y no se han registrado.

## Sabadell
- Anexo "Medidas alternativas de rendimiento del grupo" del Informe de gestión.
- **ROE/ROTE**: el denominador son los **fondos propios medios sin OCI** y no se resta el AT1. Es la base más distinta de las de BBVA y Santander.
- **Eficiencia (49,3 %)**: suma las **actividades interrumpidas (TSB)** a costes y margen bruto, aunque en la cuenta estatutaria TSB figura en NIIF 5. Con solo actividades continuadas saldría 2.288/4.896 ≈ 46,7 %. Ese valor no se publica y aquí solo se da como orientación.
- **Morosidad/cobertura**: base stage 3, que incluye valores de deuda y entidades de crédito en stage 3. La cobertura usa el total de provisiones.
- **CET1**: publica los dos: 13,11 % fully loaded (con el calendario del output floor) y 13,16 % phased-in. En 2024 los dos son 13,03 %.
- **NIM**: margen de intereses sobre ATM, 1,97 % (2,07 % en 2024). Figura en el texto del informe, no como MAR formal. Publica además el "margen de clientes" (2,97 %).

## Mapfre
- El informe **remite las definiciones MAR a un PDF externo** de mapfre.com, que no está en el ESEF y no se ha consultado. En el ESEF solo hay una definición breve del ROE y del ratio combinado.
- **ROE 12,4 %** (11,1 % en 2024): beneficio atribuible sobre fondos propios medios. No se detalla si incluye OCI.
- **Ratio combinado No Vida**: 90,2 % (93,0 % en 2024). En el anexo de sostenibilidad se define como siniestralidad + gastos "normalmente sobre primas imputadas netas de reaseguro", terminología previa a NIIF 17.
- **Solvencia II**: solo hay **dato a septiembre de 2025 (210,4 %)**. No hay cifra a cierre de 2025 porque el SFCR sale más tarde. El valor de diciembre de 2024 es 207,4 %.
- **No encontrado a nivel Grupo**: ratio de siniestralidad y ratio de gastos. Solo aparecen para la unidad Mapfre Re (siniestralidad 60,8 % y gastos 27,4 % en 2025), que no se han incluido en el CSV por no ser cifras de Grupo. La siniestralidad del 69,1 % del texto es del **sector** a septiembre, no de Mapfre.

## Línea Directa
- No tiene un anexo MAR formal. Las ratios están en "Ratios de gestión", "Rentabilidad sobre patrimonio neto" y "Solvencia II" del Informe de gestión.
- **RoAE 22,9 %**: beneficio después de impuestos, sin minoritarios relevantes, sobre la **media simple de dos cierres** (2024 y 2025). El patrimonio de 2025 se minora por el dividendo complementario propuesto. No publica el valor de 2024.
- **Ratio combinado** (92,6 %): definido en NIIF 17/PAA y neto de reaseguro. La memoria da la fórmula completa: reclamaciones + gastos − recuperaciones de reaseguro, sobre ingresos de seguro − primas cedidas.
- **Incoherencias internas**: la Carta del Presidente da siniestralidad 71,5 % y gastos 21,1 %, mientras que la tabla de gestión da 71,6 % y 21,0 %. El ratio combinado coincide (92,6 %). Se registran ambas.
- **Solvencia II**: hay tres cifras para 2025. Son 188,8 % antes del dividendo complementario, 182,6 % después del dividendo y 183 % en la memoria (redondeado). Son ratios de la **entidad individual**, porque el Grupo no está obligado a calcular una ratio de grupo.

## Diferencias de definición clave entre entidades (material para el TFM)
1. **Denominador del ROE (cuatro bases distintas)**:
   - Santander: PN sin minoritarios con OCI, más dividendos.
   - BBVA: FFPP + OCI.
   - CaixaBank: FFPP + ajustes de valoración, con el **AT1 restado del numerador**.
   - Sabadell: **FFPP sin OCI**.
   - Línea Directa: media de solo **dos cierres**, menos el dividendo propuesto.
   
   Las medias también varían: diarias, mensuales, móviles ponderadas o de dos puntos.
2. **Tratamiento del AT1**: CaixaBank lo resta en ROE, ROTE, ROA y RORWA. Santander lo resta solo en el "RoTE post-AT1". BBVA y Sabadell no lo restan.
3. **Eficiencia con perímetros distintos**: Santander usa la cuenta ordinaria. Sabadell incluye TSB, que está en actividades interrumpidas. CaixaBank publica una versión sin gravamen. BBVA usa el margen bruto estatutario.
4. **Morosidad**: el perímetro del denominador cambia según la entidad. BBVA incluye los préstamos a VR con cambios en OCI desde 2025. Santander incluye los disponibles. Sabadell y CaixaBank incluyen los riesgos contingentes y excluyen las ATA.
5. **CET1 y Solvencia II, varias cifras "oficiales"**:
   - CaixaBank: 12,6 % de gestión frente a 12,25 % regulatoria.
   - Sabadell: 13,11 % fully loaded frente a 13,16 % phased-in.
   - Santander: no da fully loaded en 2025.
   - Línea Directa: tres ratios de Solvencia II.
   - Mapfre: solo dato a septiembre.

## Lo que NO se ha encontrado
- NIM: Santander y BBVA (en texto). En CaixaBank solo hay una aproximación.
- Loan-to-deposit: BBVA.
- Siniestralidad y ratio de gastos del Grupo Mapfre, y definiciones MAR detalladas de Mapfre (documento externo).
- Solvencia II de Mapfre a 31/12/2025.
- RoAE 2024 de Línea Directa.
