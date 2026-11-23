import sys
import zipfile
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
ESEF = RAIZ / "data" / "raw" / "esef"
PROCESADOS = RAIZ / "data" / "processed"

requiere_esef = pytest.mark.skipif(not list(ESEF.glob("*.xbri")), reason="paquetes ESEF no disponibles en data/raw/esef")
requiere_hechos = pytest.mark.skipif(not list(PROCESADOS.glob("*_facts.csv")), reason="hechos no extraídos")

XHTML = """<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:ix="http://www.xbrl.org/2013/inlineXBRL"
 xmlns:xbrli="http://www.xbrl.org/2003/instance" xmlns:xbrldi="http://xbrl.org/2006/xbrldi"
 xmlns:ifrs-full="https://xbrl.ifrs.org/taxonomy/2024-03-27/ifrs-full" xmlns:tst="http://test"
 xmlns:ixt="http://www.xbrl.org/inlineXBRL/transformation/2020-02-12"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<body><div style="display:none"><ix:header><ix:resources>
 <xbrli:context id="c25"><xbrli:entity><xbrli:identifier scheme="http://standards.iso.org/iso/17442">LEI0000000000000TEST</xbrli:identifier></xbrli:entity>
  <xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period></xbrli:context>
 <xbrli:context id="d25"><xbrli:entity><xbrli:identifier scheme="http://standards.iso.org/iso/17442">LEI0000000000000TEST</xbrli:identifier></xbrli:entity>
  <xbrli:period><xbrli:startDate>2025-01-01</xbrli:startDate><xbrli:endDate>2025-12-31</xbrli:endDate></xbrli:period></xbrli:context>
 <xbrli:context id="c25seg"><xbrli:entity><xbrli:identifier scheme="http://standards.iso.org/iso/17442">LEI0000000000000TEST</xbrli:identifier>
  <xbrli:segment><xbrldi:explicitMember dimension="ifrs-full:SegmentsAxis">tst:VidaMember</xbrldi:explicitMember></xbrli:segment></xbrli:entity>
  <xbrli:period><xbrli:instant>2025-12-31</xbrli:instant></xbrli:period></xbrli:context>
</ix:resources></ix:header></div>
<p><ix:nonFraction name="ifrs-full:Assets" contextRef="c25" unitRef="EUR" decimals="-6" scale="6" format="ixt:num-comma-decimal">1.234,5</ix:nonFraction></p>
<p><ix:nonFraction name="ifrs-full:Assets" contextRef="c25" unitRef="EUR" decimals="-6" scale="6" format="ixt:num-comma-decimal">1.234,5</ix:nonFraction></p>
<p><ix:nonFraction name="ifrs-full:ProfitLoss" contextRef="d25" unitRef="EUR" decimals="-3" scale="3" sign="-" format="ixt:num-dot-decimal">2,500.25</ix:nonFraction></p>
<p><ix:nonFraction name="tst:FondosPropios" contextRef="c25" unitRef="EUR" decimals="0" format="ixt:fixed-zero">-</ix:nonFraction></p>
<p><ix:nonFraction name="ifrs-full:Equity" contextRef="c25seg" unitRef="EUR" decimals="0" format="ixt:num-dot-decimal">77</ix:nonFraction></p>
<p><ix:nonFraction name="ifrs-full:Goodwill" contextRef="c25" unitRef="EUR" xsi:nil="true"/></p>
</body></html>"""

LABELS = """<?xml version="1.0" encoding="utf-8"?>
<link:linkbase xmlns:link="http://www.xbrl.org/2003/linkbase" xmlns:xlink="http://www.w3.org/1999/xlink">
<link:labelLink xlink:type="extended" xlink:role="http://www.xbrl.org/2003/role/link">
 <link:loc xlink:type="locator" xlink:href="tst.xsd#tst_FondosPropios" xlink:label="loc1"/>
 <link:label xlink:type="resource" xlink:label="lab1" xlink:role="http://www.xbrl.org/2003/role/label" xml:lang="es">Fondos propios</link:label>
 <link:labelArc xlink:type="arc" xlink:arcrole="http://www.xbrl.org/2003/arcrole/concept-label" xlink:from="loc1" xlink:to="lab1"/>
</link:labelLink></link:linkbase>"""


@pytest.fixture
def paquete_sintetico(tmp_path):
    ruta = tmp_path / "TEST-2025-12-31.xbri"
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr("TEST/reports/test.xhtml", XHTML)
        z.writestr("TEST/www.test.com/tst_lab-es.xml", LABELS)
    return ruta
