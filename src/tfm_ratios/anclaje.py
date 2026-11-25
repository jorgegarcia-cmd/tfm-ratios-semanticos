"""Anclajes ESEF: relación de cada elemento de extensión con el elemento NIIF más próximo.

El Reglamento ESEF obliga a "anclar" cada extensión a un elemento de la taxonomía NIIF de
significado más amplio (wider) o más estrecho (narrower), mediante arcos de la base de
definición con el rol http://www.esma.europa.eu/xbrl/esef/arcrole/wider-narrower.
Este módulo los extrae de los paquetes para usarlos al proponer reglas del diccionario.

    PYTHONPATH=src python -m tfm_ratios.anclaje data/raw/esef/*.xbri
Genera data/processed/anclajes.csv
"""
from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path

import pandas as pd
from lxml import etree

ARCROLE = "http://www.esma.europa.eu/xbrl/esef/arcrole/wider-narrower"
XL = "{http://www.w3.org/1999/xlink}"
LINK = "{http://www.xbrl.org/2003/linkbase}"


def _nombre(href: str) -> tuple[str, str]:
    """'...ifrs-full_2024.xsd#ifrs-full_Equity' -> ('ifrs-full', 'Equity')."""
    frag = href.split("#")[-1]
    prefijo, _, local = frag.partition("_")
    return prefijo, local


def extraer_anclajes(ruta: str | Path) -> pd.DataFrame:
    ruta = Path(ruta)
    filas = []
    with zipfile.ZipFile(ruta) as z:
        for n in (n for n in z.namelist() if re.search(r"_def\.xml$", n)):
            raiz = etree.fromstring(z.read(n))
            for enlace in raiz.iter(f"{LINK}definitionLink"):
                loc = {l.get(f"{XL}label"): _nombre(l.get(f"{XL}href")) for l in enlace.iter(f"{LINK}loc")}
                for arco in enlace.iter(f"{LINK}definitionArc"):
                    if arco.get(f"{XL}arcrole") != ARCROLE:
                        continue
                    amplio = loc.get(arco.get(f"{XL}from"))
                    estrecho = loc.get(arco.get(f"{XL}to"))
                    if not amplio or not estrecho:
                        continue
                    filas.append({"lei": ruta.stem[:20], "amplio": ":".join(amplio), "estrecho": ":".join(estrecho)})
    df = pd.DataFrame(filas).drop_duplicates()
    if df.empty:
        return df
    # la extensión es el lado que no pertenece a la taxonomía NIIF
    df["extension"] = df.apply(lambda r: r.estrecho if not r.estrecho.startswith("ifrs-full:") else r.amplio, axis=1)
    df["ancla"] = df.apply(lambda r: r.amplio if r.extension == r.estrecho else r.estrecho, axis=1)
    df["sentido"] = df.apply(lambda r: "la extensión es más estrecha" if r.extension == r.estrecho else "la extensión es más amplia", axis=1)
    return df[["lei", "extension", "ancla", "sentido"]]


def main() -> None:
    rutas = sys.argv[1:]
    df = pd.concat([extraer_anclajes(r) for r in rutas], ignore_index=True)
    salida = Path("data/processed/anclajes.csv")
    df.to_csv(salida, index=False)
    print(f"{len(df)} anclajes de {df.extension.nunique()} extensiones -> {salida}")
    print(df.groupby("lei").size().to_string())


if __name__ == "__main__":
    main()
