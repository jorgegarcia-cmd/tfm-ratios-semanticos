"""Nivel 7: cada cifra mostrada puede verificarse en el informe oficial."""
import json
import re
import zipfile

import pandas as pd
import yaml
from lxml import etree

from conftest import ESEF, PROCESADOS, RAIZ, requiere_esef, requiere_hechos

LEI = yaml.safe_load(open(RAIZ / "config/diccionario_semantico.yaml"))["lei"]


@requiere_hechos
def test_cada_hecho_de_cada_traza_existe_en_el_informe():
    trazas = json.loads((RAIZ / "data/results/trazas.json").read_text(encoding="utf-8"))
    hechos = {}
    for nombre, lei in LEI.items():
        d = pd.read_csv(next(PROCESADOS.glob(f"{lei}-*_facts.csv")), dtype=str, keep_default_na=False)
        hechos[nombre] = {r.id_hecho: float(r.valor) for r in d.itertuples()}
    comprobados = 0
    for t in trazas:
        for parte in ("numerador", "denominador"):
            for h in t[parte]["hechos"]:
                assert h["id_hecho"] in hechos[t["entidad"]], f"{t['entidad']}: {h['id_hecho']} no existe"
                assert hechos[t["entidad"]][h["id_hecho"]] == h["valor"]
                comprobados += 1
    assert comprobados > 200


@requiere_esef
def test_cada_ratio_publicado_es_verificable():
    """La cita de cada ratio publicado aparece literalmente en el informe y contiene el valor."""
    from tfm_ratios.verificar_publicados import verificar
    d = verificar()
    assert d.v1_cita_en_informe.all(), d[~d.v1_cita_en_informe][["entidad", "ratio", "ejercicio"]].to_string()
    assert d.v2_valor_en_cita.all(), d[~d.v2_valor_en_cita][["entidad", "ratio", "ejercicio"]].to_string()
