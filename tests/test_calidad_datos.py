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


def _texto(lei):
    with zipfile.ZipFile(next(ESEF.glob(f"{lei}-*.xbri"))) as z:
        nombre = next(n for n in z.namelist() if "/reports/" in n and n.endswith(".xhtml"))
        raiz = etree.fromstring(z.read(nombre), etree.XMLParser(huge_tree=True, recover=True))
    return re.sub(r"\s+", " ", " ".join(raiz.itertext()))


def _norm(s):
    return re.sub(r"[\s|]+", "", s)


@requiere_esef
def test_cada_cita_de_ratio_publicado_aparece_en_el_informe():
    pub = pd.read_csv(RAIZ / "data/published/ratios_publicados.csv")
    textos = {n: _norm(_texto(lei)) for n, lei in LEI.items()}
    fallos = [f"{r.entidad} {r.ratio} {r.ejercicio}" for r in pub.itertuples()
              if _norm(r.cita) not in textos[r.entidad]]
    assert not fallos, f"{len(fallos)} citas no encontradas: {fallos[:10]}"


def test_valor_publicado_aparece_en_su_cita():
    pub = pd.read_csv(RAIZ / "data/published/ratios_publicados.csv")
    for r in pub.itertuples():
        candidatos = {f"{r.valor_pct:.2f}".replace(".", ","), f"{r.valor_pct:.1f}".replace(".", ","),
                      f"{r.valor_pct:g}".replace(".", ","), f"{r.valor_pct:.0f}"}
        assert any(c in r.cita for c in candidatos), f"{r.entidad} {r.ratio} {r.ejercicio}: {r.valor_pct} no está en la cita"
