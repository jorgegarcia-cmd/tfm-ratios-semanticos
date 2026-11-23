"""Nivel 4: reglas de la validación calculado/publicado."""
import pandas as pd

from tfm_ratios.comparacion import BASE_ENTIDAD, cargar_publicados, comparar, referencia


def test_variante_preferida_roa_frente_a_rorwa():
    r = referencia(cargar_publicados(), "santander", "roa", 2025)
    assert r.variante == "RoA" and r.valor_pct == 0.84


def test_aproximaciones_excluidas():
    assert referencia(cargar_publicados(), "caixabank", "nim", 2025) is None


def test_base_comparable_sabadell():
    d = comparar()
    fila = d[(d.entidad == "sabadell") & (d.ratio == "roe") & (d.ejercicio == 2025)].iloc[0]
    assert fila.base_calculada == BASE_ENTIDAD[("sabadell", "roe")] == "roe_fondos_propios"


def test_umbral_estricto():
    d = comparar().dropna(subset=["diferencia_pp"])
    assert (d.coincide == (d.diferencia_pp.abs() < 0.5)).all()
    frontera = d[(d.entidad == "sabadell") & (d.ratio == "nim") & (d.ejercicio == 2024)].iloc[0]
    assert frontera.diferencia_pp == -0.5 and not frontera.coincide


def test_variante_fondos_propios_no_se_compara_aparte():
    assert "roe_fondos_propios" not in set(comparar().ratio)
