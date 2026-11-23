"""Niveles 8 y 10: API de la versión web (deploy/main.py)."""
import importlib.util
import json
import sys
import time

import pytest
from fastapi.testclient import TestClient

from conftest import RAIZ


@pytest.fixture(scope="module")
def cliente():
    dep = RAIZ / "deploy"
    sys.path.insert(0, str(dep / "src"))
    sys.modules.pop("tfm_ratios.consulta", None)  # usar la copia del paquete de despliegue
    spec = importlib.util.spec_from_file_location("deploy_main", dep / "main.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    yield TestClient(m.app)
    sys.path.remove(str(dep / "src"))
    sys.modules.pop("tfm_ratios.consulta", None)


def test_pagina(cliente):
    r = cliente.get("/")
    assert r.status_code == 200 and "Ratios de banca y seguros" in r.text


@pytest.mark.parametrize("ruta", ["/api/ratios", "/api/comparacion", "/api/traza?entidad=bbva&ratio=roe&ejercicio=2025"])
def test_endpoints_json_validos(cliente, ruta):
    r = cliente.get(ruta)
    assert r.status_code == 200
    json.loads(r.text, parse_constant=lambda c: pytest.fail(f"valor no JSON: {c}"))  # sin NaN/Infinity


def test_pregunta(cliente):
    j = cliente.get("/api/pregunta", params={"q": "ROE de Santander y BBVA 2025"}).json()
    assert len(j["respuestas"]) == 2
    assert {x["estructurada"]["calculado"]["valor_pct"] for x in j["respuestas"]} == {13.98, 18.6}


@pytest.mark.parametrize("q", ["", "hola", "<script>alert(1)</script> ROE de BBVA", "ROE ' OR 1=1 -- de Mapfre", "ñáéíóú 2099"])
def test_entradas_raras_sin_errores(cliente, q):
    r = cliente.get("/api/pregunta", params={"q": q})
    assert r.status_code in (200, 422)


def test_pregunta_demasiado_larga(cliente):
    assert cliente.get("/api/pregunta", params={"q": "x" * 301}).status_code == 422


def test_traza_inexistente(cliente):
    assert cliente.get("/api/traza?entidad=bbva&ratio=solvencia_ii&ejercicio=2025").json() == {"error": "sin traza"}


def test_latencia(cliente):
    t0 = time.perf_counter()
    for _ in range(10):
        cliente.get("/api/pregunta", params={"q": "eficiencia de Sabadell 2025"})
    assert (time.perf_counter() - t0) / 10 < 1.0
