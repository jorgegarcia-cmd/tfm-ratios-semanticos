"""Nivel 1: lector de Inline XBRL."""
from decimal import Decimal

import pytest

from tfm_ratios.ixbrl_parser import _normalizar_numero, extraer_hechos


@pytest.mark.parametrize("texto,formato,esperado", [
    ("1.234,56", "ixt:num-comma-decimal", Decimal("1234.56")),
    ("1,234.56", "ixt:num-dot-decimal", Decimal("1234.56")),
    ("1 234 567", "ixt:num-dot-decimal", Decimal("1234567")),
    ("-", "ixt:fixed-zero", Decimal(0)),
    ("—", None, Decimal(0)),
    ("(1.000)", "ixt4:num-comma-decimal", Decimal("1000")),  # el signo va en el atributo sign, no en el texto
    ("abc", None, None),
])
def test_normalizar_numero(texto, formato, esperado):
    assert _normalizar_numero(texto, formato) == esperado


def test_extraccion_paquete_sintetico(paquete_sintetico):
    df = extraer_hechos(paquete_sintetico)
    hechos = {(r.concepto, r.dimensiones): r for r in df.itertuples()}
    # escala 6 con coma decimal, deduplicado
    assert (df.concepto == "Assets").sum() == 1
    assert hechos[("Assets", "")].valor == pytest.approx(1_234_500_000)
    # escala 3, punto decimal y signo negativo
    assert hechos[("ProfitLoss", "")].valor == pytest.approx(-2_500_250)
    assert hechos[("ProfitLoss", "")].fecha_inicio == "2025-01-01"
    # guion como cero y etiqueta de extensión en español
    assert hechos[("FondosPropios", "")].valor == 0
    assert hechos[("FondosPropios", "")].etiqueta_extension == "Fondos propios"
    # dimensiones conservadas
    assert hechos[("Equity", "SegmentsAxis=VidaMember")].valor == 77
    # hechos nulos descartados
    assert "Goodwill" not in set(df.concepto)
    assert set(df.lei) == {"LEI0000000000000TEST"}
