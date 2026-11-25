"""Tareas fuera de línea: anclajes ESEF, detector de anomalías y propuesta de reglas."""
import pandas as pd

from conftest import ESEF, requiere_esef, requiere_hechos
from tfm_ratios.anclaje import extraer_anclajes


@requiere_esef
def test_anclajes_de_los_seis_paquetes():
    d = pd.concat([extraer_anclajes(p) for p in sorted(ESEF.glob("*.xbri"))])
    assert len(d) == 595 and d.extension.nunique() == 560
    assert not d.extension.str.startswith("ifrs-full:").any()
    fp = d[d.extension == "bbva:FondosPropios"]
    assert list(fp.ancla) == ["ifrs-full:Equity"] and fp.sentido.iloc[0] == "la extensión es más estrecha"


@requiere_hechos
def test_detector_encuentra_los_hallazgos_conocidos():
    from tfm_ratios.anomalias import detectar
    d = detectar()
    caixa_a2 = d[(d.entidad == "caixabank") & (d.codigo == "A2")]
    assert len(caixa_a2) == 2  # atribuido > total en 2024 y 2025
    assert set(d[d.codigo == "A3"].entidad) == {"santander", "bbva", "caixabank", "sabadell"}  # GrossProfit
    assert set(d[d.codigo == "A6"].entidad) == {"santander", "bbva", "caixabank", "sabadell"}
    assert set(d[d.codigo == "A4"].entidad) == {"mapfre", "linea_directa"}
    assert d[d.codigo.isin(["A1", "A5"])].empty  # identidades contables y sin duplicados contradictorios


@requiere_hechos
def test_oro_y_metodos_deterministas():
    from tfm_ratios.proponer_reglas import evaluar, metodo_anclaje, metodo_literal, oro
    ref = oro()
    assert len(ref) == 58
    assert ref[("bbva", "patrimonio_atribuido")]["tipo"] == "resta"
    lit, anc = evaluar(metodo_literal(), "literal"), evaluar(metodo_anclaje(), "anclaje")
    assert int(lit.equivalente.sum()) == 33 and int(anc.equivalente.sum()) == 34
    # el anclaje propone para Santander los fondos propios (sin OCI) como patrimonio atribuido: semánticamente erróneo
    fila = anc[(anc.entidad == "santander") & (anc.concepto == "patrimonio_atribuido")].iloc[0]
    assert not fila.equivalente and fila.propuesta["elementos"][0].startswith("san:")
