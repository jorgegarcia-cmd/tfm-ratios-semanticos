"""Nivel 6: las cifras citadas en la memoria siguen saliendo del prototipo."""
import pandas as pd

from conftest import RAIZ
import pytest

from tfm_ratios.comparacion import comparar

CALC = pd.read_csv(RAIZ / "data/results/ratios_calculados.csv").set_index(["entidad", "ratio", "ejercicio"]).valor_pct

# (entidad, ratio, ejercicio): valor citado en la memoria (capítulos 3 y 4)
MEMORIA = {
    ("bbva", "roe", 2025): 18.60, ("bbva", "roe_fondos_propios", 2025): 14.10,
    ("caixabank", "roe", 2025): 15.64, ("caixabank", "roe_fondos_propios", 2025): 15.42,
    ("santander", "roe", 2025): 13.98, ("santander", "roe_fondos_propios", 2025): 10.21,
    ("sabadell", "roe", 2025): 12.23, ("sabadell", "roe_fondos_propios", 2025): 11.83,
    ("bbva", "roa", 2025): 1.36, ("caixabank", "roa", 2025): 0.91, ("santander", "roa", 2025): 0.84, ("sabadell", "roa", 2025): 0.73,
    ("bbva", "eficiencia", 2025): 38.81, ("caixabank", "eficiencia", 2025): 39.43,
    ("santander", "eficiencia", 2025): 42.12, ("sabadell", "eficiencia", 2025): 46.74,
    ("bbva", "nim", 2025): 3.22, ("caixabank", "nim", 2025): 1.65, ("santander", "nim", 2025): 2.29, ("sabadell", "nim", 2025): 1.46,
    ("bbva", "ltd", 2025): 92.76, ("caixabank", "ltd", 2025): 83.81, ("sabadell", "ltd", 2025): 89.79,
    ("mapfre", "roe", 2025): 12.38, ("linea_directa", "roe", 2025): 22.47,
    ("mapfre", "ratio_combinado", 2025): 84.42, ("linea_directa", "ratio_combinado", 2025): 91.49,
    ("mapfre", "siniestralidad", 2025): 59.62,
}


@pytest.mark.parametrize("clave,valor", MEMORIA.items(), ids=lambda x: "-".join(map(str, x)) if isinstance(x, tuple) else str(x))
def test_valor_citado(clave, valor):
    assert CALC[clave] == pytest.approx(valor, abs=0.005)


def test_resultados_de_la_validacion():
    d = comparar().dropna(subset=["diferencia_pp"])
    assert len(d) == 37 and int(d.coincide.astype(bool).sum()) == 23
    assert round(d.diferencia_pp.abs().median(), 2) == 0.22


def test_diferencia_maxima_de_bases_del_roe():
    """«La base de patrimonio cambia el ROE hasta 4,5 puntos» (figura 2)."""
    difs = [CALC[(b, "roe", 2025)] - CALC[(b, "roe_fondos_propios", 2025)] for b in ("bbva", "caixabank", "santander", "sabadell")]
    assert round(max(difs), 1) == 4.5
