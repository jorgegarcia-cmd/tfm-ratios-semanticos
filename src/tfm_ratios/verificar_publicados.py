"""Verificación de los ratios publicados extraídos de los informes de gestión.

La extracción la hizo un modelo de lenguaje leyendo el texto de los informes. Este módulo
comprueba de forma determinista que cada registro es verificable:
  V1  la cita aparece literalmente en el informe ESEF de la entidad
  V2  el valor registrado aparece dentro de su cita

    PYTHONPATH=src python -m tfm_ratios.verificar_publicados
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

import pandas as pd
import yaml
from lxml import etree

RAIZ = Path(__file__).resolve().parents[2]
ESEF = RAIZ / "data/raw/esef"
LEI = yaml.safe_load((RAIZ / "config/diccionario_semantico.yaml").read_text(encoding="utf-8"))["lei"]


def texto_informe(lei: str) -> str:
    with zipfile.ZipFile(next(ESEF.glob(f"{lei}-*.xbri"))) as z:
        nombre = next(n for n in z.namelist() if "/reports/" in n and n.endswith((".xhtml", ".html")))
        raiz = etree.fromstring(z.read(nombre), etree.XMLParser(huge_tree=True, recover=True))
    return " ".join(raiz.itertext())


def _compacto(s: str) -> str:
    return re.sub(r"[\s|]+", "", s)


def _formatos(v: float) -> set[str]:
    return {f"{v:.2f}".replace(".", ","), f"{v:.1f}".replace(".", ","), f"{v:g}".replace(".", ","), f"{v:.0f}"}


def verificar() -> pd.DataFrame:
    pub = pd.read_csv(RAIZ / "data/published/ratios_publicados.csv")
    textos = {n: _compacto(texto_informe(lei)) for n, lei in LEI.items()}
    pub["v1_cita_en_informe"] = [_compacto(r.cita) in textos[r.entidad] for r in pub.itertuples()]
    pub["v2_valor_en_cita"] = [any(f in r.cita for f in _formatos(r.valor_pct)) for r in pub.itertuples()]
    return pub


def main():
    d = verificar()
    print(f"{len(d)} ratios publicados · V1 cita literal en el informe: {d.v1_cita_en_informe.sum()} · "
          f"V2 valor dentro de la cita: {d.v2_valor_en_cita.sum()}")
    fallos = d[~(d.v1_cita_en_informe & d.v2_valor_en_cita)]
    if len(fallos):
        print(fallos[["entidad", "ratio", "ejercicio", "valor_pct", "cita"]].to_string())


if __name__ == "__main__":
    main()
