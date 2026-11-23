# Respuestas del prototipo (capa semántica con intérprete por reglas)

Generado con `tfm_ratios.consulta.responder`.

## P01 · ¿Cuál fue el ROE de BBVA en 2025?

Interpretación: entidades=['bbva'], ratios=['roe'], ejercicios=[2025]

```
ROE de BBVA en 2025:
18.60 % calculado (resultado_atribuido / media(patrimonio_atribuido); 10,511 / 56,506 M€).
La entidad publica 18.40 %: Resultado atribuido / (fondos propios medios + OCI acumulado medio); medias móviles ponderadas de cierres mensuales, ajustadas por dividendo-opción
Comparables del mismo grupo y definición: BBVA 18.60 %, CaixaBank 15.64 %, Banco Santander 13.98 %, Banco Sabadell 12.23 %.
Base del denominador: media de saldos inicial y final.
El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.
Interpretación: Mayor es mejor; debe compararse con el coste de capital de la entidad.
```

## P02 · ¿Cuál fue el ratio de eficiencia de CaixaBank en 2025?

Interpretación: entidades=['caixabank'], ratios=['eficiencia'], ejercicios=[2025]

```
Ratio de eficiencia de CaixaBank en 2025:
39.43 % calculado (gastos_explotacion_banca / margen_bruto; 6,415 / 16,270 M€).
La entidad publica 39.40 %: Gastos de administración y amortización / margen bruto
La entidad publica 39.40 % (sin gravamen a la banca): Gastos de administración y amortización / (margen bruto - gravamen a la banca); 2025 sin gravamen
Comparables del mismo grupo y definición: Banco Sabadell 46.74 %, Banco Santander 42.12 %, CaixaBank 39.43 %, BBVA 38.81 %.
Interpretación: Menor es mejor; por debajo del 40–50 % se considera eficiente.
```

## P03 · ¿Cuál fue el ROA de Santander en 2025?

Interpretación: entidades=['santander'], ratios=['roa'], ejercicios=[2025]

```
ROA de Banco Santander en 2025:
0.84 % calculado (resultado_ejercicio / media(activo_total); 15,500 / 1,852,298 M€).
La entidad publica 0.84 % (RoA): Resultado consolidado del ejercicio (incl. minoritarios) / promedio de activos totales (media mensual)
La entidad publica 2.44 % (RoRWA): Resultado consolidado / promedio de activos ponderados por riesgo (criterios CRR)
Comparables del mismo grupo y definición: BBVA 1.36 %, CaixaBank 0.91 %, Banco Santander 0.84 %, Banco Sabadell 0.73 %.
Base del denominador: media de saldos inicial y final.
Interpretación: En banca, valores típicos por debajo del 1 %; muy sensible al apalancamiento.
```

## P04 · ¿Cuál fue el ratio combinado de Línea Directa en 2025?

Interpretación: entidades=['linea_directa'], ratios=['ratio_combinado'], ejercicios=[2025]

```
Ratio combinado de Línea Directa en 2025:
91.49 % calculado (gastos_servicio_seguro / ingresos_seguros; 985 / 1,077 M€).
La entidad publica 92.60 % (no vida (total, neto de reaseguro)): (Reclamaciones incurridas + otros gastos atribuibles al servicio del seguro) / ingresos de seguro, todo neto de reaseguro (PAA, NIIF 17)
Comparables del mismo grupo y definición: Línea Directa 91.49 %, Mapfre 84.42 %.
El valor calculado difiere -1.11 p.p. del publicado por la entidad: las definiciones no coinciden (ver definición de la entidad).
Interpretación: Por debajo del 100 % hay beneficio técnico antes de ingresos financieros.
```

## P05 · ¿Cuál fue el margen de intereses sobre activos medios (NIM) de Sabadell en 2025?

Interpretación: entidades=['sabadell'], ratios=['nim'], ejercicios=[2025]

```
Margen de intereses sobre activos medios (NIM) de Banco Sabadell en 2025:
1.46 % calculado (margen_intereses / media(activo_total); 3,537 / 242,495 M€).
La entidad publica 1.97 % (margen de intereses / ATM): Margen de intereses / activos totales medios (no definido como MAR formal)
Comparables del mismo grupo y definición: BBVA 3.22 %, Banco Santander 2.29 %, CaixaBank 1.65 %, Banco Sabadell 1.46 %.
Base del denominador: media de saldos inicial y final.
El valor calculado difiere -0.51 p.p. del publicado por la entidad: las definiciones no coinciden (ver definición de la entidad).
Interpretación: Muy sensible al ciclo de tipos de interés.
```

## P06 · ¿Cuál fue el ROE de Mapfre en 2025?

Interpretación: entidades=['mapfre'], ratios=['roe'], ejercicios=[2025]

```
ROE de Mapfre en 2025:
12.38 % calculado (resultado_atribuido / media(patrimonio_atribuido); 1,133 / 9,149 M€).
La entidad publica 12.40 %: Beneficio neto atribuible a la sociedad matriz (deducidos socios externos) / fondos propios medios (detalle de cálculo remitido a documento MAR externo)
Comparables del mismo grupo y definición: Línea Directa 22.47 %, Mapfre 12.38 %.
Base del denominador: media de saldos inicial y final.
El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.
Interpretación: Mayor es mejor; debe compararse con el coste de capital de la entidad.
```

## P07 · ¿Cuál fue el ratio CET1 de Santander a cierre de 2025?

Interpretación: entidades=['santander'], ratios=['cet1'], ejercicios=[2025]

```
Ratio CET1 de Banco Santander en 2025:
La entidad publica 13.50 % (phased-in): CET1 / APR; phased in incluye tratamiento transitorio NIIF 9 (art. 473 bis CRR); 2025 bajo CRR3
La entidad publica 13.46 % (phased-in (memoria, 2 decimales)): Coeficiente de capital ordinario de nivel 1 = CET1 computable / APR
Interpretación: Comparar con el requerimiento SREP de cada entidad, no con un umbral único.
```

## P08 · ¿Cuál fue la tasa de morosidad de CaixaBank en 2025?

Interpretación: entidades=['caixabank'], ratios=['morosidad'], ejercicios=[2025]

```
Tasa de morosidad de CaixaBank en 2025:
La entidad publica 2.10 %: Deudores dudosos (crédito clientela + riesgos contingentes) / (crédito a la clientela + riesgos contingentes), brutos
Interpretación: Menor es mejor; contextualizar por mix de cartera y geografía.
```

## P09 · ¿Cuál fue la tasa de cobertura de BBVA en 2025?

Interpretación: entidades=['bbva'], ratios=['cobertura'], ejercicios=[2025]

```
Tasa de cobertura de BBVA en 2025:
La entidad publica 85.00 %: Fondo de cobertura stages 1+2+3 (correcciones de valor + provisiones riesgos contingentes) / saldo dudoso (stage 3)
Interpretación: Mayor es más prudente; depende de las garantías de la cartera.
```

## P10 · ¿Cuál fue el ratio de Solvencia II de Mapfre a 31 de diciembre de 2025?

Interpretación: entidades=['mapfre'], ratios=['solvencia_ii'], ejercicios=[2025]

```
Ratio de Solvencia II de Mapfre en 2025:
La entidad publica 210.40 % (grupo, septiembre 2025 (último disponible)): Fondos propios admisibles / SCR del Grupo; SCR recalculado trimestralmente con estimaciones; dato a 30/09/2025, no a cierre
Interpretación: Por encima del 100 % cumple; las aseguradoras suelen fijar objetivos internos del 150–200 %.
```

## P11 · ¿Cuál fue el ratio de siniestralidad de Línea Directa en 2025?

Interpretación: entidades=['linea_directa'], ratios=['siniestralidad'], ejercicios=[2025]

```
Ratio de siniestralidad de Línea Directa en 2025:
La entidad publica 71.60 % (total (tabla ratios de gestión)): Siniestralidad neta de reaseguro / ingresos de seguro netos de reaseguro
La entidad publica 71.50 % (Carta del Presidente): Sin definición; cifra redondeada distinta de la tabla de gestión (71,6 %)
No calculable desde ESEF: solo etiqueta el total de gastos del servicio de seguro.
Interpretación: Menor es mejor; muy dependiente del ramo (autos, hogar, salud).
```

## P12 · ¿Qué banco tuvo mayor ROE en 2025: Santander, BBVA, CaixaBank o Sabadell?

Interpretación: entidades=['santander', 'bbva', 'caixabank', 'sabadell'], ratios=['roe'], ejercicios=[2025]

```
ROE de Banco Santander en 2025:
13.98 % calculado (resultado_atribuido / media(patrimonio_atribuido); 14,101 / 100,886 M€).
La entidad publica 13.90 %: Beneficio atribuido a la dominante / promedio de patrimonio neto sin minoritarios (capital y reservas + OCI acumulado + beneficio atribuido + dividendos y retribuciones); promedio = media de saldos mensuales
Comparables del mismo grupo y definición: BBVA 18.60 %, CaixaBank 15.64 %, Banco Santander 13.98 %, Banco Sabadell 12.23 %.
Base del denominador: media de saldos inicial y final.
El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.
Interpretación: Mayor es mejor; debe compararse con el coste de capital de la entidad.

ROE de BBVA en 2025:
18.60 % calculado (resultado_atribuido / media(patrimonio_atribuido); 10,511 / 56,506 M€).
La entidad publica 18.40 %: Resultado atribuido / (fondos propios medios + OCI acumulado medio); medias móviles ponderadas de cierres mensuales, ajustadas por dividendo-opción
Comparables del mismo grupo y definición: BBVA 18.60 %, CaixaBank 15.64 %, Banco Santander 13.98 %, Banco Sabadell 12.23 %.
Base del denominador: media de saldos inicial y final.
El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.
Interpretación: Mayor es mejor; debe compararse con el coste de capital de la entidad.

ROE de CaixaBank en 2025:
15.64 % calculado (resultado_atribuido / media(patrimonio_atribuido); 5,891 / 37,670 M€).
La entidad publica 14.90 %: (Resultado atribuido - cupón AT1) / (fondos propios + ajustes de valoración) medios 12M (media de saldos medios mensuales)
Comparables del mismo grupo y definición: BBVA 18.60 %, CaixaBank 15.64 %, Banco Santander 13.98 %, Banco Sabadell 12.23 %.
Base del denominador: media de saldos inicial y final.
El valor calculado difiere +0.74 p.p. del publicado por la entidad: las definiciones no coinciden (ver definición de la entidad).
El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.
Interpretación: Mayor es mejor; debe compararse con el coste de capital de la entidad.

ROE de Banco Sabadell en 2025:
12.23 % calculado (resultado_atribuido / media(patrimonio_atribuido); 1,775 / 14,523 M€).
La entidad publica 11.90 %: Beneficio atribuido al grupo / fondos propios medios (media aritmética del último día de cada mes, 12 meses); sin OCI ni ajuste AT1
Comparables del mismo grupo y definición: BBVA 18.60 %, CaixaBank 15.64 %, Banco Santander 13.98 %, Banco Sabadell 12.23 %.
Base del denominador: media de saldos inicial y final.
El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.
Interpretación: Mayor es mejor; debe compararse con el coste de capital de la entidad.
```

## P13 · Ordena BBVA, CaixaBank, Santander y Sabadell por ratio de eficiencia en 2025

Interpretación: entidades=['santander', 'bbva', 'caixabank', 'sabadell'], ratios=['eficiencia'], ejercicios=[2025]

```
Ratio de eficiencia de Banco Santander en 2025:
42.12 % calculado (gastos_explotacion_banca / margen_bruto; 24,711 / 58,670 M€).
La entidad publica 41.20 % (ordinaria): Costes de explotación ordinarios (gastos generales de administración + amortizaciones, ajustados por actividad no ordinaria) / margen bruto ordinario
Comparables del mismo grupo y definición: Banco Sabadell 46.74 %, Banco Santander 42.12 %, CaixaBank 39.43 %, BBVA 38.81 %.
El valor calculado difiere +0.92 p.p. del publicado por la entidad: las definiciones no coinciden (ver definición de la entidad).
Interpretación: Menor es mejor; por debajo del 40–50 % se considera eficiente.

Ratio de eficiencia de BBVA en 2025:
38.81 % calculado (gastos_explotacion_banca / margen_bruto; 14,332 / 36,931 M€).
La entidad publica 38.80 %: Gastos de explotación (personal + otros gastos de administración + amortización) / margen bruto estatutario
Comparables del mismo grupo y definición: Banco Sabadell 46.74 %, Banco Santander 42.12 %, CaixaBank 39.43 %, BBVA 38.81 %.
Interpretación: Menor es mejor; por debajo del 40–50 % se considera eficiente.

Ratio de eficiencia de CaixaBank en 2025:
39.43 % calculado (gastos_explotacion_banca / margen_bruto; 6,415 / 16,270 M€).
La entidad publica 39.40 %: Gastos de administración y amortización / margen bruto
La entidad publica 39.40 % (sin gravamen a la banca): Gastos de administración y amortización / (margen bruto - gravamen a la banca); 2025 sin gravamen
Comparables del mismo grupo y definición: Banco Sabadell 46.74 %, Banco Santander 42.12 %, CaixaBank 39.43 %, BBVA 38.81 %.
Interpretación: Menor es mejor; por debajo del 40–50 % se considera eficiente.

Ratio de eficiencia de Banco Sabadell en 2025:
46.74 % calculado (gastos_explotacion_banca / margen_bruto; 2,288 / 4,896 M€).
La entidad publica 49.30 % (incl. actividades interrumpidas (TSB)): Total costes de explotación (administración + amortización) / margen bruto, sumando actividades continuadas e interrumpidas (TSB)
Comparables del mismo grupo y definición: Banco Sabadell 46.74 %, Banco Santander 42.12 %, CaixaBank 39.43 %, BBVA 38.81 %.
El valor calculado difiere -2.56 p.p. del publicado por la entidad: las definiciones no coinciden (ver definición de la entidad).
Interpretación: Menor es mejor; por debajo del 40–50 % se considera eficiente.
```

## P14 · ¿Qué aseguradora tuvo mejor ratio combinado en 2025, Mapfre o Línea Directa?

Interpretación: entidades=['mapfre', 'linea_directa'], ratios=['ratio_combinado'], ejercicios=[2025]

```
Ratio combinado de Mapfre en 2025:
84.42 % calculado (gastos_servicio_seguro / ingresos_seguros; 22,246 / 26,352 M€).
La entidad publica 90.20 % (no vida): Relación entre costes del seguro y volumen de ingresos No Vida; suma de siniestralidad y gastos, 'normalmente sobre primas imputadas netas de reaseguro' (bajo NIIF 17)
Comparables del mismo grupo y definición: Línea Directa 91.49 %, Mapfre 84.42 %.
El valor calculado difiere -5.78 p.p. del publicado por la entidad: las definiciones no coinciden (ver definición de la entidad).
Interpretación: Por debajo del 100 % hay beneficio técnico antes de ingresos financieros.

Ratio combinado de Línea Directa en 2025:
91.49 % calculado (gastos_servicio_seguro / ingresos_seguros; 985 / 1,077 M€).
La entidad publica 92.60 % (no vida (total, neto de reaseguro)): (Reclamaciones incurridas + otros gastos atribuibles al servicio del seguro) / ingresos de seguro, todo neto de reaseguro (PAA, NIIF 17)
Comparables del mismo grupo y definición: Línea Directa 91.49 %, Mapfre 84.42 %.
El valor calculado difiere -1.11 p.p. del publicado por la entidad: las definiciones no coinciden (ver definición de la entidad).
Interpretación: Por debajo del 100 % hay beneficio técnico antes de ingresos financieros.
```

## P15 · ¿Mejoró la tasa de morosidad de Sabadell en 2025 respecto a 2024?

Interpretación: entidades=['sabadell'], ratios=['morosidad'], ejercicios=[2024, 2025]

```
Tasa de morosidad de Banco Sabadell en 2024:
La entidad publica 2.84 %: Riesgos stage 3 (activos + garantías) / (inversión crediticia bruta sin ATA + garantías concedidas)
Interpretación: Menor es mejor; contextualizar por mix de cartera y geografía.

Tasa de morosidad de Banco Sabadell en 2025:
La entidad publica 2.37 %: Riesgos stage 3 (activos + garantías) / (inversión crediticia bruta sin ATA + garantías concedidas)
Interpretación: Menor es mejor; contextualizar por mix de cartera y geografía.
```

## P16 · ¿Cuál es el ROE de Santander en 2025 calculado sobre fondos propios y sobre patrimonio atribuido?

Interpretación: entidades=['santander'], ratios=['roe_fondos_propios', 'roe'], ejercicios=[2025]

```
ROE sobre fondos propios de Banco Santander en 2025:
10.21 % calculado (resultado_atribuido / media(fondos_propios); 14,101 / 138,170 M€).
Comparables del mismo grupo y definición: CaixaBank 15.42 %, BBVA 14.10 %, Banco Sabadell 11.83 %, Banco Santander 10.21 %.
Base del denominador: media de saldos inicial y final.
El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.
Interpretación: Mayor es mejor; debe compararse con el coste de capital de la entidad.

ROE de Banco Santander en 2025:
13.98 % calculado (resultado_atribuido / media(patrimonio_atribuido); 14,101 / 100,886 M€).
La entidad publica 13.90 %: Beneficio atribuido a la dominante / promedio de patrimonio neto sin minoritarios (capital y reservas + OCI acumulado + beneficio atribuido + dividendos y retribuciones); promedio = media de saldos mensuales
Comparables del mismo grupo y definición: BBVA 18.60 %, CaixaBank 15.64 %, Banco Santander 13.98 %, Banco Sabadell 12.23 %.
Base del denominador: media de saldos inicial y final.
El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.
Interpretación: Mayor es mejor; debe compararse con el coste de capital de la entidad.
```

## P17 · ¿Son comparables los ROE publicados por CaixaBank y BBVA en 2025?

Interpretación: entidades=['bbva', 'caixabank'], ratios=['roe'], ejercicios=[2025]

```
ROE de BBVA en 2025:
18.60 % calculado (resultado_atribuido / media(patrimonio_atribuido); 10,511 / 56,506 M€).
La entidad publica 18.40 %: Resultado atribuido / (fondos propios medios + OCI acumulado medio); medias móviles ponderadas de cierres mensuales, ajustadas por dividendo-opción
Comparables del mismo grupo y definición: BBVA 18.60 %, CaixaBank 15.64 %, Banco Santander 13.98 %, Banco Sabadell 12.23 %.
Base del denominador: media de saldos inicial y final.
El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.
Interpretación: Mayor es mejor; debe compararse con el coste de capital de la entidad.

ROE de CaixaBank en 2025:
15.64 % calculado (resultado_atribuido / media(patrimonio_atribuido); 5,891 / 37,670 M€).
La entidad publica 14.90 %: (Resultado atribuido - cupón AT1) / (fondos propios + ajustes de valoración) medios 12M (media de saldos medios mensuales)
Comparables del mismo grupo y definición: BBVA 18.60 %, CaixaBank 15.64 %, Banco Santander 13.98 %, Banco Sabadell 12.23 %.
Base del denominador: media de saldos inicial y final.
El valor calculado difiere +0.74 p.p. del publicado por la entidad: las definiciones no coinciden (ver definición de la entidad).
El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.
Interpretación: Mayor es mejor; debe compararse con el coste de capital de la entidad.
```

## P18 · ¿Por qué Sabadell publica una eficiencia del 49,3 % en 2025 si el cálculo desde sus cuentas da 46,7 %?

Interpretación: entidades=['sabadell'], ratios=['eficiencia'], ejercicios=[2025]

```
Ratio de eficiencia de Banco Sabadell en 2025:
46.74 % calculado (gastos_explotacion_banca / margen_bruto; 2,288 / 4,896 M€).
La entidad publica 49.30 % (incl. actividades interrumpidas (TSB)): Total costes de explotación (administración + amortización) / margen bruto, sumando actividades continuadas e interrumpidas (TSB)
Comparables del mismo grupo y definición: Banco Sabadell 46.74 %, Banco Santander 42.12 %, CaixaBank 39.43 %, BBVA 38.81 %.
El valor calculado difiere -2.56 p.p. del publicado por la entidad: las definiciones no coinciden (ver definición de la entidad).
Interpretación: Menor es mejor; por debajo del 40–50 % se considera eficiente.
```

## P19 · ¿Cuál es el ratio préstamos/depósitos de Santander en 2025 según sus estados ESEF?

Interpretación: entidades=['santander'], ratios=['ltd'], ejercicios=[2025]

```
Ratio préstamos/depósitos de Banco Santander en 2025:
La entidad publica 98.00 %: Préstamos y anticipos a la clientela netos de fondos de insolvencias / depósitos de la clientela (saldos de cierre)
No calculable desde ESEF: el balance solo etiqueta carteras contables (p. ej. FinancialAssetsAtAmortisedCost), no la clientela.
Interpretación: Por debajo del 100 % indica financiación estable con depósitos.
```

## P20 · ¿Qué NIM publica BBVA para 2025?

Interpretación: entidades=['bbva'], ratios=['nim'], ejercicios=[2025]

```
Margen de intereses sobre activos medios (NIM) de BBVA en 2025:
3.22 % calculado (margen_intereses / media(activo_total); 26,280 / 815,989 M€).
Comparables del mismo grupo y definición: BBVA 3.22 %, Banco Santander 2.29 %, CaixaBank 1.65 %, Banco Sabadell 1.46 %.
Base del denominador: media de saldos inicial y final.
Interpretación: Muy sensible al ciclo de tipos de interés.
```
