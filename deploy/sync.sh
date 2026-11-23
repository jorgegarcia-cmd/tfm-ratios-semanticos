#!/bin/sh
# Copia al paquete de despliegue el código y los datos actuales del prototipo
cd "$(dirname "$0")"
cp ../src/tfm_ratios/__init__.py ../src/tfm_ratios/consulta.py src/tfm_ratios/
cp ../config/diccionario_semantico.yaml config/
cp ../data/results/*.csv ../data/results/trazas.json data/results/
cp ../data/published/ratios_publicados.csv data/published/
