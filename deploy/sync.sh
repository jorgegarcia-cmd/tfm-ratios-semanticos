#!/bin/sh
# Copia al paquete de despliegue el código y los datos actuales del prototipo, reducidos a lo que usa la web
cd "$(dirname "$0")"
cp ../src/tfm_ratios/__init__.py ../src/tfm_ratios/consulta.py src/tfm_ratios/
python3 - <<'PY'
import json, yaml, pandas as pd
t = json.load(open('../data/results/trazas.json'))
for x in t:
    for k in ('numerador', 'denominador'):
        for h in x[k]['hechos']:
            h['valor'] = round(h['valor'] / 1e6, 1)
json.dump(t, open('data/results/trazas.json', 'w'), ensure_ascii=False, separators=(',', ':'))
pd.read_csv('../data/published/ratios_publicados.csv').drop(columns=['cita']).to_csv('data/published/ratios_publicados.csv', index=False)
pd.read_csv('../data/results/ratios_calculados.csv').to_csv('data/results/ratios_calculados.csv', index=False)
pd.read_csv('../data/results/comparacion.csv')[['entidad', 'ratio', 'ejercicio', 'diferencia_pp']].to_csv('data/results/comparacion.csv', index=False)
d = yaml.safe_load(open('../config/diccionario_semantico.yaml'))
yaml.safe_dump({'ratios': {k: {'nombre': v['nombre'], 'interpretacion': v['interpretacion'], 'variantes': v['variantes']}
                           for k, v in d['ratios'].items()}}, open('config/diccionario_semantico.yaml', 'w'),
               allow_unicode=True, sort_keys=False, width=200)
PY
