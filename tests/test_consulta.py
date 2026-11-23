"""Nivel 3: capa de consulta (sobre los resultados reales del motor)."""
import pandas as pd

from conftest import RAIZ
import pytest

from tfm_ratios.consulta import HERRAMIENTA, consultar, interpretar, responder

CALC = pd.read_csv(RAIZ / "data/results/ratios_calculados.csv")


@pytest.mark.parametrize("pregunta,entidades,ratios,anios", [
    ("¿Cuál fue el ROE de BBVA en 2025?", ["bbva"], ["roe"], [2025]),
    ("eficiencia de CaixaBank", ["caixabank"], ["eficiencia"], [2025]),
    ("Morosidad de Sabadell en 2025 respecto a 2024", ["sabadell"], ["morosidad"], [2024, 2025]),
    ("ROE de Santander sobre fondos propios y patrimonio", ["santander"], ["roe_fondos_propios", "roe"], [2025]),
    ("ratio combinado de Línea Directa y Mapfre", ["mapfre", "linea_directa"], ["ratio_combinado"], [2025]),
    ("préstamos sobre depósitos de Santander", ["santander"], ["ltd"], [2025]),
    ("CET1 de La Caixa", ["caixabank"], ["cet1"], [2025]),
])
def test_interpretacion(pregunta, entidades, ratios, anios):
    q = interpretar(pregunta)
    assert sorted(q["entidades"]) == sorted(entidades)
    assert q["ratios"] == ratios and q["ejercicios"] == anios


def test_cifra_solo_del_motor():
    """La cifra calculada que devuelve la consulta es exactamente la del motor, para todos los casos."""
    for f in CALC.itertuples():
        r = consultar(f.entidad, f.ratio, f.ejercicio)
        if pd.isna(f.valor_pct):
            assert r["calculado"] is None and any("No calculable" in a for a in r["avisos"])
        else:
            assert r["calculado"]["valor_pct"] == f.valor_pct


def test_aviso_no_publicado():
    r = consultar("bbva", "nim", 2025)
    assert r["publicado"] == [] and any("no publica" in a for a in r["avisos"])


def test_aviso_diferencia_con_publicado():
    r = consultar("sabadell", "eficiencia", 2025)
    assert any("difiere" in a for a in r["avisos"])


def test_aviso_base_roe():
    assert any("base de patrimonio" in a for a in consultar("santander", "roe", 2025)["avisos"])


def test_dato_no_disponible_sin_inventar():
    texto = responder("préstamos sobre depósitos de Santander 2025")
    assert "No calculable desde ESEF" in texto and "calculado (" not in texto


def test_pregunta_no_reconocida():
    assert responder("¿qué tiempo hace hoy?").startswith("No he identificado")


def test_esquema_herramienta_cerrado():
    props = HERRAMIENTA["input_schema"]["properties"]
    assert set(props["ejercicio"]["enum"]) == {2024, 2025}
    assert "bbva" in props["entidad"]["enum"] and "roe" in props["ratio"]["enum"]
