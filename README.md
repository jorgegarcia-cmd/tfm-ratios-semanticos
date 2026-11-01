# TFM · Contextualización semántica de ratios financieros

Prototipo del Trabajo Fin de Máster *"Contextualización semántica de estados financieros para el cálculo e interpretación fiable de ratios en el sector financiero"*. Máster ejecutivo N-World en Finanzas y Tecnología Aplicadas (Universidad de La Rioja), curso 2026-2027.

- Autor: Jorge García
- Tutor: Víctor Lechuga

## Qué hace

Calcula 12 ratios de banca y seguros a partir de los informes ESEF (XBRL) de 8 entidades cotizadas españolas. Lo hace en cuatro pasos:

1. **Extracción:** lee los hechos XBRL del paquete ESEF.
2. **Diccionario semántico:** relaciona cada partida con un concepto financiero canónico (`config/diccionario_semantico.yaml`).
3. **Motor de ratios:** calcula de forma determinista, con trazabilidad hasta la partida de origen.
4. **Consulta en lenguaje natural:** un LLM interpreta la pregunta y redacta la respuesta, pero nunca genera cifras.

## Estructura

```
config/            diccionario semántico (conceptos + ratios)
data/raw/esef/     paquetes ESEF originales (.zip), no versionados
data/processed/    hechos extraídos y ratios calculados
src/tfm_ratios/    código del prototipo
tests/             pruebas
docs/              notas de diseño
```

## Puesta en marcha

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m tfm_ratios.ixbrl_parser data/raw/esef/*.xbri
```

## Muestra

- **Banca:** Santander, BBVA, CaixaBank, Sabadell, Bankinter, Unicaja.
- **Seguros:** Mapfre, Línea Directa.
- **Ejercicios:** 2024 y 2025.
