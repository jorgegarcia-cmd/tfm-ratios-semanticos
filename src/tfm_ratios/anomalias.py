"""Detector de anomalías de etiquetado en los informes ESEF.

Comprobaciones deterministas que señalan cifras cuyo etiquetado merece revisión antes de usarlas:
  A1  identidad contable: activo = pasivo + patrimonio
  A2  patrimonio "atribuido" mayor que el patrimonio total (elemento usado para otra magnitud)
  A3  elemento pensado para empresas industriales usado por una entidad financiera
  A4  extensión sin anclaje ESEF (incumple el requisito de anclaje)
  A5  mismo elemento y contexto con valores distintos en el documento
  A6  elemento NIIF específico disponible en la taxonomía pero no usado, en favor de otro más genérico

    PYTHONPATH=src python -m tfm_ratios.anomalias
Genera data/results/anomalias.csv
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[2]
DIC = yaml.safe_load((RAIZ / "config/diccionario_semantico.yaml").read_text(encoding="utf-8"))
GRUPO = {"santander": "banca", "bbva": "banca", "caixabank": "banca", "sabadell": "banca",
         "mapfre": "seguros", "linea_directa": "seguros"}
INDUSTRIALES = {"GrossProfit": "beneficio bruto (ventas − coste de ventas)", "CostOfSales": "coste de ventas",
                "Revenue": "ingresos ordinarios por ventas"}
ESPECIFICOS = {  # elemento específico esperado -> alternativa genérica que se usa en su lugar
    "InterestIncomeExpenseNet": "InterestRevenueExpense",
}


def _hechos(lei: str) -> pd.DataFrame:
    d = pd.read_csv(next((RAIZ / "data/processed").glob(f"{lei}-*_facts.csv")), dtype=str, keep_default_na=False)
    d["valor"] = d.valor.astype(float)
    return d


def detectar() -> pd.DataFrame:
    anc = pd.read_csv(RAIZ / "data/processed/anclajes.csv", dtype=str)
    filas = []

    def add(ent, codigo, gravedad, detalle):
        filas.append({"entidad": ent, "codigo": codigo, "gravedad": gravedad, "detalle": detalle})

    for ent, lei in DIC["lei"].items():
        todos = _hechos(lei)
        h = todos[todos.dimensiones == ""]

        def v(concepto, fecha):
            s = h[(h.prefijo == "ifrs-full") & (h.concepto == concepto) & (h.fecha_fin == fecha) & (h.periodo_tipo == "instante")].valor
            return s.iloc[0] if len(s) else None

        for fecha in ("2024-12-31", "2025-12-31"):
            a, p, e = v("Assets", fecha), v("Liabilities", fecha), v("Equity", fecha)
            if None not in (a, p, e) and abs(a - p - e) > 1e6:
                add(ent, "A1", "alta", f"{fecha}: activo − pasivo − patrimonio = {(a - p - e) / 1e6:,.0f} M€")
            at = v("EquityAttributableToOwnersOfParent", fecha)
            if at is not None and e is not None and at > e + 1e6:
                add(ent, "A2", "alta", f"{fecha}: EquityAttributableToOwnersOfParent ({at / 1e6:,.0f} M€) > Equity ({e / 1e6:,.0f} M€)")

        usados = set(h[h.prefijo == "ifrs-full"].concepto)
        for el, sentido in INDUSTRIALES.items():
            if el in usados:
                add(ent, "A3", "media", f"usa ifrs-full:{el} (pensado para {sentido}) en una entidad financiera")
        for especifico, generico in ESPECIFICOS.items():
            if GRUPO[ent] == "banca" and especifico not in usados and generico in usados:
                add(ent, "A6", "baja", f"usa ifrs-full:{generico} en lugar de ifrs-full:{especifico}")

        ext = set((todos[todos.prefijo != "ifrs-full"].prefijo + ":" + todos[todos.prefijo != "ifrs-full"].concepto))
        sin_ancla = sorted(ext - set(anc[anc.lei == lei].extension))
        if sin_ancla:
            add(ent, "A4", "media", f"{len(sin_ancla)} de {len(ext)} extensiones sin anclaje, p. ej. {', '.join(sin_ancla[:3])}")

        clave = ["prefijo", "concepto", "fecha_inicio", "fecha_fin", "dimensiones", "unidad"]
        dup = todos.groupby(clave).valor.nunique()
        dup = dup[dup > 1]
        for k in dup.index[:5]:
            add(ent, "A5", "alta", f"{k[0]}:{k[1]} a {k[3]} con {dup[k]} valores distintos")
        if len(dup) > 5:
            add(ent, "A5", "alta", f"… y {len(dup) - 5} casos más")
    return pd.DataFrame(filas)


def main():
    df = detectar()
    df.to_csv(RAIZ / "data/results/anomalias.csv", index=False)
    print(df.pivot_table(index="entidad", columns="codigo", values="detalle", aggfunc="count", fill_value=0).to_string())
    print()
    for r in df[df.codigo.isin(["A1", "A2", "A5"])].itertuples():
        print(f"[{r.codigo}] {r.entidad}: {r.detalle}")


if __name__ == "__main__":
    main()
