"""Niveles 5 y 10: pipeline completo sobre los informes ESEF reales, coherencia contable y rendimiento."""
import time

import pandas as pd
import pytest
import yaml

from conftest import ESEF, requiere_esef, requiere_hechos
from tfm_ratios import motor
from tfm_ratios.ixbrl_parser import extraer_hechos

ESPERADO = {"5493006QMFDDMYWIAM13": 1725, "K8MS7FD7N5Z2WQ51AZ71": 1634, "SI5RG2M0WQQLZCXKRM20": 1217,
            "7CUNS533WID6K7DGFI87": 1088, "95980020140005693107": 713, "95980079E2NBJT967T79": 458}


@requiere_esef
def test_lectura_de_los_seis_informes_y_rendimiento():
    t0 = time.perf_counter()
    totales = {p.stem[:20]: len(extraer_hechos(p)) for p in sorted(ESEF.glob("*.xbri"))}
    dur = time.perf_counter() - t0
    assert totales == ESPERADO and sum(totales.values()) == 6835
    assert dur < 30, f"lectura demasiado lenta: {dur:.1f} s"


@requiere_hechos
def test_pipeline_completo():
    df, trazas = motor.calcular()
    assert len(df) == 72 and df.valor_pct.notna().sum() == 64 and len(trazas) == 72
    faltan = df[df.valor_pct.isna()]
    assert faltan.no_calculable.notna().all(), "todo dato ausente debe llevar motivo"


def _hechos(lei):
    d = pd.read_csv(next(motor.HECHOS.glob(f"{lei}-*_facts.csv")), dtype=str, keep_default_na=False)
    d["valor"] = d.valor.astype(float)
    return d[d.dimensiones == ""]


@requiere_hechos
@pytest.mark.parametrize("nombre,lei", yaml.safe_load(open(motor.DICCIONARIO))["lei"].items())
def test_identidades_contables(nombre, lei):
    h = _hechos(lei)
    for anio in ("2024-12-31", "2025-12-31"):
        def v(c):
            s = h[(h.concepto == c) & (h.fecha_fin == anio) & (h.periodo_tipo == "instante")].valor
            return s.iloc[0] if len(s) else None
        activo, pn, pasivo, total = v("Assets"), v("Equity"), v("Liabilities"), v("EquityAndLiabilities")
        if activo is None:
            continue
        if total is not None:
            assert abs(activo - total) < 1e6, f"{nombre} {anio}: activo ≠ pasivo + patrimonio"
        if pn is not None and pasivo is not None:
            assert abs(activo - pasivo - pn) < 1e6, f"{nombre} {anio}: activo − pasivo ≠ patrimonio"
        e = motor.Entidad(nombre, lei, yaml.safe_load(open(motor.DICCIONARIO))["mapeo"])
        pa = e.valor("patrimonio_atribuido", int(anio[:4]), "instante")
        if pa.ok and pn is not None:
            assert pa.valor <= pn + 1, f"{nombre} {anio}: patrimonio atribuido > patrimonio total"


@requiere_hechos
def test_resultado_atribuido_no_supera_resultado_total():
    df, _ = motor.calcular()
    for e in df.entidad.unique():
        for a in (2024, 2025):
            roe = df[(df.entidad == e) & (df.ejercicio == a) & (df.ratio == "roe")].iloc[0]
            roa = df[(df.entidad == e) & (df.ejercicio == a) & (df.ratio == "roa")].iloc[0]
            assert roe.numerador_meur <= roa.numerador_meur + 0.5
