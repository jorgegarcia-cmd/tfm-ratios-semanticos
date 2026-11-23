"""Nivel 2: reglas del motor de ratios sobre hechos sintéticos."""
import pandas as pd
import pytest

from tfm_ratios import motor

LEI = "LEI0000000000000TEST"


def hechos(filas):
    base = {"lei": LEI, "etiqueta_extension": "", "unidad": "EUR", "decimales": "-6", "dimensiones": "", "id_hecho": "f"}
    return pd.DataFrame([{**base, **f} for f in filas])


def inst(prefijo, concepto, anio, valor, i="x"):
    return {"prefijo": prefijo, "concepto": concepto, "valor": valor, "periodo_tipo": "instante",
            "fecha_inicio": "", "fecha_fin": f"{anio}-12-31", "id_hecho": i}


def dur(prefijo, concepto, anio, valor, i="y"):
    return {"prefijo": prefijo, "concepto": concepto, "valor": valor, "periodo_tipo": "duracion",
            "fecha_inicio": f"{anio}-01-01", "fecha_fin": f"{anio}-12-31", "id_hecho": i}


@pytest.fixture
def entidad(tmp_path, monkeypatch):
    def crear(filas, nombre="bbva", mapeo=None):
        hechos(filas).to_csv(tmp_path / f"{LEI}-2025-12-31_facts.csv", index=False)
        monkeypatch.setattr(motor, "HECHOS", tmp_path)
        return motor.Entidad(nombre, LEI, mapeo or MAPEO)
    return crear


MAPEO = {
    "patrimonio_atribuido": {"_todas": {"resta": ["ifrs-full:Equity", "ifrs-full:NoncontrollingInterests"]}},
    "activo_total": {"_todas": ["ifrs-full:Assets"]},
    "prestamos_clientela": {"bbva": ["ifrs-full:A", "ifrs-full:B"], "santander": {"no_disponible": "sin etiqueta"}},
}


def test_suma_de_etiquetas(entidad):
    e = entidad([inst("ifrs-full", "A", 2025, 10), inst("ifrs-full", "B", 2025, 5)])
    v = e.valor("prestamos_clientela", 2025, "instante")
    assert v.valor == 15 and len(v.hechos) == 2


def test_no_disponible_con_motivo(entidad):
    e = entidad([inst("ifrs-full", "A", 2025, 10)], nombre="santander")
    v = e.valor("prestamos_clientela", 2025, "instante")
    assert v.valor is None and v.motivo == "sin etiqueta"


def test_resta_con_minoritarios(entidad):
    e = entidad([inst("ifrs-full", "Equity", 2025, 100), inst("ifrs-full", "NoncontrollingInterests", 2025, 10)])
    v = e.valor("patrimonio_atribuido", 2025, "instante")
    assert v.valor == 90 and v.regla == "resta"


def test_resta_sin_minoritarios_avisa(entidad):
    e = entidad([inst("ifrs-full", "Equity", 2025, 100)])
    v = e.valor("patrimonio_atribuido", 2025, "instante")
    assert v.valor == 100 and "sin ifrs-full:NoncontrollingInterests" in v.regla


def test_media_y_saldo_de_cierre(entidad):
    e = entidad([inst("ifrs-full", "Assets", 2024, 100), inst("ifrs-full", "Assets", 2025, 200)])
    v, nota = e.media("activo_total", 2025)
    assert v.valor == 150 and "media" in nota
    v, nota = e.media("activo_total", 2024)  # falta 2023
    assert v.valor == 100 and "cierre" in nota


def test_flujo_requiere_ejercicio_completo(entidad):
    e = entidad([dur("ifrs-full", "Assets", 2025, 7) | {"fecha_inicio": "2025-07-01"}])
    assert e.valor("activo_total", 2025, "duracion").valor is None


def test_concepto_sin_regla(entidad):
    e = entidad([inst("ifrs-full", "Assets", 2025, 1)])
    assert e.valor("concepto_inexistente", 2025, "instante").motivo
