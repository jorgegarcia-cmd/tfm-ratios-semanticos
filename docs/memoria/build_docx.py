"""Genera la memoria del TFM en Word sobre la plantilla oficial del máster.

    python docs/memoria/build_docx.py <plantilla.docx> <salida.docx>

Lee 00_preliminares.yaml, los capítulos 0N_*.md, referencias.md y anexos.md de esta carpeta.
Markdown admitido: #/##/###/#### títulos (se elimina la numeración manual: la plantilla numera sola),
párrafos con **negrita**, *cursiva* y `código`, listas con "- " y "1. ", tablas con "|",
"**Tabla N. ...**" / "**Figura N. ...**" como pies, "[FIGURA: fichero.png]" e imágenes.
"""
from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

import yaml
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AQUI = Path(__file__).parent
FIG = AQUI / "figuras"


# ---------------------------------------------------------------------------
# utilidades XML
# ---------------------------------------------------------------------------
def borrar(elemento):
    elemento.getparent().remove(elemento)


def campo_toc(parrafo, instruccion: str, texto: str):
    """Inserta un campo de índice que Word actualiza al abrir (F9 para refrescar)."""
    def run(xml_tag, **attrs):
        r = OxmlElement("w:r")
        el = OxmlElement(xml_tag)
        for k, v in attrs.items():
            el.set(qn(k), v)
        r.append(el)
        return r
    p = parrafo._p
    p.append(run("w:fldChar", **{"w:fldCharType": "begin", "w:dirty": "true"}))
    r = OxmlElement("w:r"); t = OxmlElement("w:instrText"); t.set(qn("xml:space"), "preserve")
    t.text = f" {instruccion} "; r.append(t); p.append(r)
    p.append(run("w:fldChar", **{"w:fldCharType": "separate"}))
    r = OxmlElement("w:r"); t = OxmlElement("w:t"); t.text = texto; r.append(t); p.append(r)
    p.append(run("w:fldChar", **{"w:fldCharType": "end"}))


def fijar_texto(parrafo, texto: str):
    for r in parrafo.runs[1:]:
        borrar(r._r)
    if parrafo.runs:
        parrafo.runs[0].text = texto
    else:
        parrafo.add_run(texto)


def numeracion(doc) -> tuple[int, int]:
    """Crea definiciones de lista con viñeta y numerada; devuelve sus numId."""
    np_ = doc.part.numbering_part.element
    ids = [int(a.get(qn("w:abstractNumId"))) for a in np_.findall(qn("w:abstractNum"))]
    nums = [int(n.get(qn("w:numId"))) for n in np_.findall(qn("w:num"))]
    res = []
    for formato, texto in (("bullet", "•"), ("decimal", "%1.")):
        aid = max(ids + [0]) + 1 + len(res)
        a = OxmlElement("w:abstractNum"); a.set(qn("w:abstractNumId"), str(aid))
        lvl = OxmlElement("w:lvl"); lvl.set(qn("w:ilvl"), "0")
        for tag, val in (("w:start", "1"), ("w:numFmt", formato), ("w:lvlText", texto), ("w:lvlJc", "left")):
            e = OxmlElement(tag); e.set(qn("w:val"), val); lvl.append(e)
        ppr = OxmlElement("w:pPr"); ind = OxmlElement("w:ind")
        ind.set(qn("w:left"), "567"); ind.set(qn("w:hanging"), "283"); ppr.append(ind); lvl.append(ppr)
        if formato == "bullet":
            rpr = OxmlElement("w:rPr"); f = OxmlElement("w:rFonts")
            f.set(qn("w:ascii"), "Symbol"); f.set(qn("w:hAnsi"), "Symbol"); rpr.append(f); lvl.append(rpr)
            lvl.find(qn("w:lvlText")).set(qn("w:val"), "")
        a.append(lvl)
        primero_num = np_.find(qn("w:num"))
        if primero_num is not None:
            primero_num.addprevious(a)
        else:
            np_.append(a)
        nid = max(nums + [0]) + 1 + len(res)
        n = OxmlElement("w:num"); n.set(qn("w:numId"), str(nid))
        ref = OxmlElement("w:abstractNumId"); ref.set(qn("w:val"), str(aid)); n.append(ref); np_.append(n)
        res.append(nid)
    return res[0], res[1]


def lista_nueva(doc, abstract_num_id_de: int) -> int:
    """Instancia nueva de una lista numerada para que cada lista empiece en 1."""
    np_ = doc.part.numbering_part.element
    base = [n for n in np_.findall(qn("w:num")) if n.get(qn("w:numId")) == str(abstract_num_id_de)][0]
    aid = base.find(qn("w:abstractNumId")).get(qn("w:val"))
    nid = max(int(n.get(qn("w:numId"))) for n in np_.findall(qn("w:num"))) + 1
    n = OxmlElement("w:num"); n.set(qn("w:numId"), str(nid))
    ref = OxmlElement("w:abstractNumId"); ref.set(qn("w:val"), aid); n.append(ref)
    ov = OxmlElement("w:lvlOverride"); ov.set(qn("w:ilvl"), "0")
    so = OxmlElement("w:startOverride"); so.set(qn("w:val"), "1"); ov.append(so); n.append(ov)
    np_.append(n)
    return nid


def poner_lista(parrafo, num_id: int):
    ppr = parrafo._p.get_or_add_pPr()
    numpr = OxmlElement("w:numPr")
    il = OxmlElement("w:ilvl"); il.set(qn("w:val"), "0"); numpr.append(il)
    ni = OxmlElement("w:numId"); ni.set(qn("w:val"), str(num_id)); numpr.append(ni)
    ppr.append(numpr)


# ---------------------------------------------------------------------------
# texto con formato en línea
# ---------------------------------------------------------------------------
TOKENS = re.compile(r"(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)")


def texto_rico(parrafo, texto: str, negrita_base=False, tam=None):
    for trozo in TOKENS.split(texto):
        if not trozo:
            continue
        if trozo.startswith("**"):
            r = parrafo.add_run(trozo[2:-2]); r.bold = True
        elif trozo.startswith("*") and len(trozo) > 2:
            r = parrafo.add_run(trozo[1:-1]); r.italic = True
        elif trozo.startswith("`"):
            r = parrafo.add_run(trozo[1:-1]); r.font.name = "Consolas"; r.font.size = Pt(10)
        else:
            r = parrafo.add_run(trozo)
        if negrita_base:
            r.bold = True
        if tam:
            r.font.size = tam


# ---------------------------------------------------------------------------
# conversión de Markdown a la plantilla
# ---------------------------------------------------------------------------
def renumerar(textos: list[tuple[str, str]]) -> list[str]:
    """Numera tablas y figuras de forma correlativa en todo el documento y actualiza las referencias.
    Una referencia sin pie en su propio fichero se resuelve en el fichero anterior más cercano."""
    pies = []  # (indice_fichero, tipo, numero_original)
    for k, (_, t) in enumerate(textos):
        for m in re.finditer(r"(?m)^\*\*(Tabla|Figura) (\d+)\.", t):
            pies.append((k, m.group(1), int(m.group(2))))
    nuevo, cont = {}, {"Tabla": 0, "Figura": 0}
    for k, tipo, n in pies:
        cont[tipo] += 1
        nuevo[(k, tipo, n)] = cont[tipo]
    salida = []
    for k, (_, t) in enumerate(textos):
        def sub(m):
            tipo, n = m.group(1), int(m.group(2))
            for j in range(k, -1, -1):
                if (j, tipo, n) in nuevo:
                    return f"{tipo} {nuevo[(j, tipo, n)]}"
            return m.group(0)
        salida.append(re.sub(r"\b(Tabla|Figura) (\d+)\b", sub, t))
    return salida


class Escritor:
    def __init__(self, doc, ancla, tabla_modelo):
        self.doc = doc
        self.ancla = ancla  # párrafo antes del cual se inserta
        self.tabla_modelo = tabla_modelo
        self.viñeta, self.numerada = numeracion(doc)
        self.n_lista = None

    def _p(self, estilo="Normal"):
        p = self.ancla.insert_paragraph_before(style=estilo)
        return p

    def salto_pagina(self):
        self._p().add_run().add_break(WD_BREAK.PAGE)

    def titulo(self, nivel: int, texto: str, sin_numero=False):
        texto = re.sub(r"^(\d+(\.\d+)*\.?)\s+", "", texto.strip())
        if nivel == 1:
            self.salto_pagina()
        estilo = "Título 1 sin numerar" if sin_numero else f"Heading {nivel}"
        p = self._p(estilo); p.add_run(texto)

    def parrafo(self, texto: str):
        p = self._p(); texto_rico(p, texto)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def item(self, texto: str, numerado: bool):
        p = self._p("List Paragraph"); texto_rico(p, texto)
        if numerado:
            if self.n_lista is None:
                self.n_lista = lista_nueva(self.doc, self.numerada)
            poner_lista(p, self.n_lista)
        else:
            poner_lista(p, self.viñeta)

    def pie(self, texto: str, tipo: str):
        p = self._p("Figuras" if tipo == "Figura" else "TOC Heading")
        p.add_run(texto)

    def fuente(self, texto: str):
        p = self._p(); r = p.add_run(texto); r.font.size = Pt(10); r.italic = True

    def figura(self, fichero: str):
        ruta = FIG / fichero
        p = self._p(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if ruta.exists():
            p.add_run().add_picture(str(ruta), width=Cm(15))
        else:
            r = p.add_run(f"[Figura pendiente: {fichero}]"); r.font.color.rgb = RGBColor(0xC0, 0, 0)

    def tabla(self, filas: list[list[str]]):
        cab, cuerpo = filas[0], filas[1:]
        t = self.doc.add_table(rows=len(filas), cols=len(cab))
        # estilo de la tabla de ejemplo de la plantilla
        tblpr_modelo = self.tabla_modelo._tbl.tblPr
        t._tbl.remove(t._tbl.tblPr); t._tbl.insert(0, copy.deepcopy(tblpr_modelo))
        for i, fila in enumerate(filas):
            for j in range(len(cab)):
                celda = t.cell(i, j)
                txt = fila[j] if j < len(fila) else ""
                p = celda.paragraphs[0]
                texto_rico(p, txt.strip(), negrita_base=(i == 0), tam=Pt(9.5))
                p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
                if i == 0:
                    tcpr = celda._tc.get_or_add_tcPr(); sh = OxmlElement("w:shd")
                    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), "D9E2F3")
                    tcpr.append(sh)
        # anchos proporcionales al texto más largo de cada columna (mín. 8 %, total 16 cm)
        largo = [max(len(re.sub(r"[*`]", "", (f[j] if j < len(f) else ""))) for f in filas) for j in range(len(cab))]
        palabra = [max((len(w_) for f in filas for w_ in re.sub(r"[*`]", "", (f[j] if j < len(f) else "")).split()), default=4)
                   for j in range(len(cab))]
        peso = [max(min(max(l, 6), 60), palabra[j] * 1.6) for j, l in enumerate(largo)]
        tot = sum(peso)
        anchos = [max(Cm(16) * w_ / tot, Cm(16) * 0.08) for w_ in peso]
        esc = Cm(16) / sum(anchos)
        anchos = [int(a * esc) for a in anchos]
        t.autofit = False
        grid = t._tbl.tblGrid
        for j, gc in enumerate(grid.findall(qn("w:gridCol"))):
            gc.set(qn("w:w"), str(int(anchos[j] / 635)))
        for fila in t.rows:
            for j, celda in enumerate(fila.cells):
                celda.width = anchos[j]
        self.ancla._p.addprevious(t._tbl)

    def markdown(self, md: str):
        lineas = md.splitlines()
        i = 0
        while i < len(lineas):
            l = lineas[i].rstrip()
            if not l.strip():
                self.n_lista = None
                i += 1; continue
            m = re.match(r"^(#{1,4})\s+(.*)", l)
            if m:
                self.titulo(len(m.group(1)), m.group(2)); i += 1; continue
            m = re.match(r"^\*\*((Tabla|Figura) \d+\..*)\*\*$", l.strip())
            if m:
                self.pie(m.group(1), m.group(2)); i += 1; continue
            m = re.match(r"^\[FIGURA:\s*(.+?)\]$", l.strip())
            if m:
                self.figura(m.group(1)); i += 1; continue
            if l.strip().startswith("Fuente:"):
                self.fuente(l.strip()); i += 1; continue
            if l.lstrip().startswith("|"):
                filas = []
                while i < len(lineas) and lineas[i].lstrip().startswith("|"):
                    celdas = [c.strip() for c in lineas[i].strip().strip("|").split("|")]
                    if not all(re.fullmatch(r":?-{3,}:?", c) for c in celdas):
                        filas.append(celdas)
                    i += 1
                self.tabla(filas); continue
            m = re.match(r"^\s*[-*]\s+(.*)", l)
            if m:
                self.item(m.group(1), False); i += 1; continue
            m = re.match(r"^\s*\d+\.\s+(.*)", l)
            if m:
                self.item(m.group(1), True); i += 1; continue
            # párrafo (une líneas consecutivas)
            buf = [l.strip()]; i += 1
            while i < len(lineas) and lineas[i].strip() and not re.match(r"^(#|\||\s*[-*]\s|\s*\d+\.\s|\*\*(Tabla|Figura)|\[FIGURA|Fuente:)", lineas[i]):
                buf.append(lineas[i].strip()); i += 1
            self.parrafo(" ".join(buf))


def construir(plantilla: str, salida: str):
    pre = yaml.safe_load((AQUI / "00_preliminares.yaml").read_text(encoding="utf-8"))
    doc = Document(plantilla)
    P = doc.paragraphs

    # --- portada (se eliminan 6 párrafos vacíos para que quepa en una página) ---
    vacios_portada = [P[i] for i in (14, 15, 16, 17, 18, 19) if not P[i].text.strip()]
    fijar_texto(P[12], pre["titulo_es"])
    fijar_texto(P[13], pre["titulo_en"])
    for r in P[13].runs:
        r.italic = True
    fijar_texto(P[22], f"Autor: {pre['autor']}")
    fijar_texto(P[23], f"Tutor: {pre['tutor']}")
    fijar_texto(P[27], pre["curso"])
    # --- resumen / abstract ---
    fijar_texto(P[29], pre["resumen"]); P[29].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    P[31].clear(); r = P[31].add_run("Palabras clave: "); r.bold = True; P[31].add_run(pre["palabras_clave"])
    fijar_texto(P[36], pre["abstract"]); P[36].alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    P[38].clear(); r = P[38].add_run("Keywords: "); r.bold = True; P[38].add_run(pre["keywords"])

    for p in vacios_portada:
        borrar(p._p)
    P = doc.paragraphs
    idx = {p.text.strip(): i for i, p in enumerate(P)}
    i_toc = next(i for i, p in enumerate(P) if p.style.name == "toc 1")
    i_fig = next(i for i, p in enumerate(P) if p.text.startswith("Figura 1"))
    i_tab = next(i for i, p in enumerate(P) if p.style.name == "table of figures")
    # --- índices: sustituir las entradas de ejemplo por campos ---
    toc, figs, tabs = P[i_toc], P[i_fig], P[i_tab]
    for p in P[i_toc + 1:i_fig - 1] + P[i_fig + 1:i_tab - 1]:
        borrar(p._p)
    for p in (toc, figs, tabs):
        for r in list(p._p):
            if r.tag != qn("w:pPr"):
                p._p.remove(r)
    campo_toc(toc, 'TOC \\o "1-3" \\h \\z \\u \\t "Título 1 sin numerar,1;Anexo,1"',
              "Haga clic derecho y elija «Actualizar campo» para generar el índice.")
    campo_toc(figs, 'TOC \\h \\z \\t "Figuras,1"', "Actualice el campo para generar el índice de figuras.")
    campo_toc(tabs, 'TOC \\h \\z \\t "TOC Heading,1"', "Actualice el campo para generar el índice de tablas.")

    # --- borrar el contenido de ejemplo y preparar el ancla ---
    P = doc.paragraphs
    inicio = next(i for i, p in enumerate(P) if p.style.name == "TOC Heading" and not p.text.strip())
    tabla_modelo = doc.tables[1]
    ancla = doc.add_paragraph()  # al final del cuerpo, antes de sectPr
    tbl_modelo_xml = copy.deepcopy(tabla_modelo._tbl)
    for p in P[inicio:]:
        borrar(p._p)
    borrar(tabla_modelo._tbl)
    from docx.table import Table
    modelo = Table(tbl_modelo_xml, doc._body)

    w = Escritor(doc, ancla, modelo)
    caps = [(c.name, c.read_text(encoding="utf-8")) for c in sorted(AQUI.glob("0[1-9]_*.md"))]
    anx_f = AQUI / "anexos.md"
    if anx_f.exists():
        caps.append(("anexos.md", anx_f.read_text(encoding="utf-8")))
    textos = renumerar(caps)
    anexos_txt = textos.pop() if anx_f.exists() else None
    for t in textos:
        w.markdown(t)

    # --- referencias ---
    ref = AQUI / "referencias.md"
    w.salto_pagina()
    p = w._p("Título 1 sin numerar"); p.add_run("Referencias bibliográficas")
    if ref.exists():
        for l in ref.read_text(encoding="utf-8").splitlines():
            l = l.strip()
            if not l or l.startswith("#") or l.lower().startswith(("verificad", "url de verificación", ">")):
                continue
            l = re.sub(r"^[-*]\s+", "", l)
            l = re.sub(r"\s*\[?(Verificad[oa]|Verificación)[^\]]*\]?\s*$", "", l, flags=re.I)
            p = w._p("Referencias bibliográficas"); texto_rico(p, l)

    # --- anexos ---
    if anexos_txt:
        for bloque in re.split(r"(?m)^# ", anexos_txt):
            if not bloque.strip():
                continue
            cab, _, cuerpo = bloque.partition("\n")
            w.salto_pagina()
            p = w._p("Anexo"); p.add_run(re.sub(r"^Anexo [A-Z]\.\s*", "", cab.strip()))
            w.markdown(cuerpo)

    borrar(ancla._p)
    # pedir a Word que actualice los campos al abrir
    st = doc.settings.element
    uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"), "true"); st.append(uf)
    doc.save(salida)
    print("ok ->", salida)


if __name__ == "__main__":
    construir(sys.argv[1], sys.argv[2])
