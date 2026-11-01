"""Parser de Inline XBRL (ESEF) sin dependencia de taxonomías externas.

Lee directamente el paquete ESEF (.zip / .xbri), extrae:
  - los hechos numéricos (ix:nonFraction) con su contexto (periodo y dimensiones),
  - las etiquetas en español de los elementos de extensión de la entidad (_lab-es.xml).

Ventaja frente a Arelle: funciona sin conexión (no descarga las taxonomías ESMA/IFRS),
a cambio de no validar el documento. Para el TFM basta con leer las cifras.

Uso:
    python -m tfm_ratios.ixbrl_parser ruta/al/paquete.xbri [más paquetes...]
Genera data/processed/<LEI>_<fecha>_facts.csv
"""
from __future__ import annotations

import re
import sys
import zipfile
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pandas as pd
from lxml import etree

NS = {
    "ix": "http://www.xbrl.org/2013/inlineXBRL",
    "xbrli": "http://www.xbrl.org/2003/instance",
    "xbrldi": "http://xbrl.org/2006/xbrldi",
    "link": "http://www.xbrl.org/2003/linkbase",
    "xlink": "http://www.w3.org/1999/xlink",
}

# Rol de etiqueta estándar
LABEL_ROLE = "http://www.xbrl.org/2003/role/label"


@dataclass
class Contexto:
    id: str
    lei: str
    periodo_tipo: str  # "instante" | "duracion"
    fecha_inicio: str | None
    fecha_fin: str
    dimensiones: str  # "Eje=Miembro;Eje2=Miembro2" ("" si no hay)


# ---------------------------------------------------------------------------
# Transformaciones numéricas de Inline XBRL (ixt / ixt4)
# ---------------------------------------------------------------------------
def _normalizar_numero(texto: str, formato: str | None) -> Decimal | None:
    t = (texto or "").strip().replace(" ", " ").replace(" ", "")
    fmt = (formato or "").split(":")[-1].lower()

    if fmt in ("fixed-zero", "zerodash", "fixed-empty", "nocontent") or t in ("-", "—", "–", ""):
        return Decimal(0)
    if "comma-decimal" in fmt or fmt in ("numdotcomma", "numspacecomma", "numcommadecimal"):
        # 1.234.567,89  ->  1234567.89
        t = t.replace(".", "").replace("'", "").replace(",", ".")
    else:
        # num-dot-decimal y por defecto: 1,234,567.89 -> 1234567.89
        t = t.replace(",", "").replace("'", "")
    t = re.sub(r"[^0-9.\-]", "", t)
    if t in ("", ".", "-"):
        return None
    try:
        return Decimal(t)
    except InvalidOperation:
        return None


# ---------------------------------------------------------------------------
# Lectura del paquete
# ---------------------------------------------------------------------------
def _leer_paquete(ruta: Path) -> tuple[bytes, list[bytes]]:
    with zipfile.ZipFile(ruta) as z:
        nombres = z.namelist()
        xhtml = [n for n in nombres if "/reports/" in n and n.endswith((".xhtml", ".html"))]
        if not xhtml:
            raise ValueError(f"No hay informe XHTML en {ruta}")
        labels = [z.read(n) for n in nombres if re.search(r"_lab-[a-z]{2}\.xml$", n)]
        return z.read(xhtml[0]), labels


def _etiquetas(labels_xml: list[bytes]) -> dict[str, str]:
    """Devuelve {nombre_local_elemento: etiqueta estándar} de los elementos de extensión."""
    resultado: dict[str, str] = {}
    for contenido in labels_xml:
        raiz = etree.fromstring(contenido)
        for link in raiz.iter("{%s}labelLink" % NS["link"]):
            loc_a_href = {
                loc.get("{%s}label" % NS["xlink"]): loc.get("{%s}href" % NS["xlink"])
                for loc in link.iter("{%s}loc" % NS["link"])
            }
            etiquetas = {
                lab.get("{%s}label" % NS["xlink"]): (lab.text or "").strip()
                for lab in link.iter("{%s}label" % NS["link"])
                if lab.get("{%s}role" % NS["xlink"]) == LABEL_ROLE
            }
            for arco in link.iter("{%s}labelArc" % NS["link"]):
                desde = loc_a_href.get(arco.get("{%s}from" % NS["xlink"]))
                texto = etiquetas.get(arco.get("{%s}to" % NS["xlink"]))
                if desde and texto:
                    # href: "...xsd#prefijo_Elemento"
                    fragmento = desde.split("#")[-1]
                    nombre = fragmento.split("_", 1)[-1]
                    resultado[nombre] = texto
    return resultado


def _contextos(raiz: etree._Element) -> dict[str, Contexto]:
    ctxs: dict[str, Contexto] = {}
    for c in raiz.iter("{%s}context" % NS["xbrli"]):
        lei = c.findtext("xbrli:entity/xbrli:identifier", namespaces=NS) or ""
        inst = c.findtext("xbrli:period/xbrli:instant", namespaces=NS)
        dims = []
        for m in c.iterfind(".//xbrldi:explicitMember", namespaces=NS):
            dims.append(f"{m.get('dimension').split(':')[-1]}={(m.text or '').strip().split(':')[-1]}")
        for m in c.iterfind(".//xbrldi:typedMember", namespaces=NS):
            dims.append(f"{m.get('dimension').split(':')[-1]}={''.join(m.itertext()).strip()}")
        ctxs[c.get("id")] = Contexto(
            id=c.get("id"),
            lei=lei.strip(),
            periodo_tipo="instante" if inst else "duracion",
            fecha_inicio=None if inst else c.findtext("xbrli:period/xbrli:startDate", namespaces=NS),
            fecha_fin=(inst or c.findtext("xbrli:period/xbrli:endDate", namespaces=NS) or "").strip(),
            dimensiones=";".join(sorted(dims)),
        )
    return ctxs


def extraer_hechos(ruta: str | Path) -> pd.DataFrame:
    ruta = Path(ruta)
    xhtml, labels_xml = _leer_paquete(ruta)
    parser = etree.XMLParser(huge_tree=True, recover=True)
    raiz = etree.fromstring(xhtml, parser)
    ctxs = _contextos(raiz)
    etiquetas = _etiquetas(labels_xml)

    filas = []
    for h in raiz.iter("{%s}nonFraction" % NS["ix"]):
        if h.get("{http://www.w3.org/2001/XMLSchema-instance}nil") == "true":
            continue
        nombre = h.get("name", "")
        prefijo, _, local = nombre.partition(":")
        valor = _normalizar_numero("".join(h.itertext()), h.get("format"))
        if valor is None:
            continue
        valor = valor * (Decimal(10) ** int(h.get("scale", "0")))
        if h.get("sign") == "-":
            valor = -valor
        ctx = ctxs.get(h.get("contextRef"))
        if ctx is None:
            continue
        filas.append(
            {
                "lei": ctx.lei,
                "prefijo": prefijo,
                "concepto": local,
                "etiqueta_extension": etiquetas.get(local, ""),
                "valor": float(valor),
                "unidad": h.get("unitRef"),
                "decimales": h.get("decimals"),
                "periodo_tipo": ctx.periodo_tipo,
                "fecha_inicio": ctx.fecha_inicio,
                "fecha_fin": ctx.fecha_fin,
                "dimensiones": ctx.dimensiones,
                "id_hecho": h.get("id"),
            }
        )
    df = pd.DataFrame(filas)
    # Un mismo hecho puede aparecer varias veces en el documento (p. ej. en estados y notas)
    clave = ["prefijo", "concepto", "fecha_inicio", "fecha_fin", "dimensiones", "unidad"]
    return df.drop_duplicates(subset=clave + ["valor"]).reset_index(drop=True)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    salida_dir = Path("data/processed")
    salida_dir.mkdir(parents=True, exist_ok=True)
    for arg in sys.argv[1:]:
        ruta = Path(arg)
        df = extraer_hechos(ruta)
        nombre = ruta.stem
        salida = salida_dir / f"{nombre}_facts.csv"
        df.to_csv(salida, index=False)
        sin_dims = (df["dimensiones"] == "").sum()
        ext = (df["prefijo"] != "ifrs-full").sum()
        print(f"{nombre}: {len(df)} hechos ({sin_dims} sin dimensiones, {ext} de extensión) -> {salida}")


if __name__ == "__main__":
    main()
