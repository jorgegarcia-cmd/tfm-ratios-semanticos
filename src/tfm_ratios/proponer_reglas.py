"""Propuesta automática de reglas del diccionario y evaluación frente al mapeo manual.

Tres métodos, de menos a más contexto:
  1. literal  - el elemento NIIF esperado para el concepto, si la entidad lo etiqueta
  2. anclaje  - literal; si no existe, la extensión de la entidad anclada a ese elemento
  3. llm      - propuesta de un modelo de lenguaje a ciegas (sin ver el diccionario manual),
                leída de data/processed/propuestas_llm.json

La referencia (oro) es la sección `mapeo` del diccionario, revisada a mano.
Una propuesta es "exacta" si usa el mismo conjunto de elementos, y "equivalente" si,
con otros elementos, da el mismo valor a 31/12/2025 (±0,5 %).

    PYTHONPATH=src python -m tfm_ratios.proponer_reglas            # evalúa
    PYTHONPATH=src python -m tfm_ratios.proponer_reglas --brief    # prepara el material para el LLM
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import yaml

from tfm_ratios.motor import GRUPO, Entidad

RAIZ = Path(__file__).resolve().parents[2]
DIC = yaml.safe_load((RAIZ / "config/diccionario_semantico.yaml").read_text(encoding="utf-8"))
ANCLAJES = RAIZ / "data/processed/anclajes.csv"
PROPUESTAS_LLM = RAIZ / "data/processed/propuestas_llm.json"

# Conceptos evaluados y grupo al que aplican
CONCEPTOS = {
    "resultado_atribuido": {"banca", "seguros"}, "resultado_ejercicio": {"banca", "seguros"},
    "activo_total": {"banca", "seguros"}, "patrimonio_atribuido": {"banca", "seguros"},
    "fondos_propios": {"banca", "seguros"}, "margen_intereses": {"banca"}, "margen_bruto": {"banca"},
    "gastos_explotacion_banca": {"banca"}, "prestamos_clientela": {"banca"}, "depositos_clientela": {"banca"},
    "ingresos_seguros": {"seguros"}, "gastos_servicio_seguro": {"seguros"},
    "siniestralidad_neta": {"seguros"}, "gastos_adquisicion_seguro": {"seguros"},
}
# Elemento NIIF "esperado" para cada concepto (lo que usaría un mapeo literal)
ESPERADO = {
    "resultado_atribuido": ["ifrs-full:ProfitLossAttributableToOwnersOfParent"],
    "resultado_ejercicio": ["ifrs-full:ProfitLoss"], "activo_total": ["ifrs-full:Assets"],
    "patrimonio_atribuido": ["ifrs-full:EquityAttributableToOwnersOfParent"],
    "fondos_propios": ["ifrs-full:EquityAttributableToOwnersOfParent"],
    "margen_intereses": ["ifrs-full:InterestIncomeExpenseNet"], "margen_bruto": ["ifrs-full:Revenue"],
    "gastos_explotacion_banca": ["ifrs-full:AdministrativeExpense", "ifrs-full:DepreciationAndAmortisationExpense"],
    "prestamos_clientela": ["ifrs-full:LoansAndAdvancesToCustomers"], "depositos_clientela": ["ifrs-full:DepositsFromCustomers"],
    "ingresos_seguros": ["ifrs-full:InsuranceRevenue"],
    "gastos_servicio_seguro": ["ifrs-full:InsuranceServiceExpensesFromInsuranceContractsIssued"],
    "siniestralidad_neta": ["ifrs-full:InsuranceServiceExpensesFromInsuranceContractsIssued"],
    "gastos_adquisicion_seguro": ["ifrs-full:InsuranceServiceExpensesFromInsuranceContractsIssued"],
}
DESCRIPCION = {
    "resultado_atribuido": "Resultado del ejercicio atribuido a los propietarios de la dominante (flujo anual).",
    "resultado_ejercicio": "Resultado consolidado total del ejercicio, incluidos los minoritarios (flujo anual).",
    "activo_total": "Total del activo del balance consolidado (saldo a 31/12).",
    "patrimonio_atribuido": "Patrimonio neto atribuido a la dominante, INCLUIDO el otro resultado global acumulado (saldo).",
    "fondos_propios": "Fondos propios de la dominante: capital, reservas y resultado, SIN el otro resultado global acumulado (saldo).",
    "margen_intereses": "Margen de intereses de un banco: ingresos menos gastos por intereses (flujo anual).",
    "margen_bruto": "Margen bruto de un banco: total de ingresos ordinarios netos (intereses, comisiones, otros) (flujo anual).",
    "gastos_explotacion_banca": "Gastos de administración más amortizaciones de un banco (flujo anual).",
    "prestamos_clientela": "Préstamos y anticipos a la clientela, netos, en el balance (saldo).",
    "depositos_clientela": "Depósitos de la clientela en el balance (saldo).",
    "ingresos_seguros": "Ingresos por contratos de seguro según NIIF 17 (flujo anual).",
    "gastos_servicio_seguro": "Gastos totales del servicio de seguro según NIIF 17 (flujo anual).",
    "siniestralidad_neta": "Siniestros incurridos y otros gastos directos del servicio de seguro, sin gastos de adquisición (flujo anual).",
    "gastos_adquisicion_seguro": "Gastos de adquisición atribuibles a contratos de seguro (flujo anual).",
}
TIPO = {c: ("instante" if c in {"activo_total", "patrimonio_atribuido", "fondos_propios", "prestamos_clientela", "depositos_clientela"} else "duracion") for c in CONCEPTOS}


def _entidades():
    return {n: Entidad(n, lei, DIC["mapeo"]) for n, lei in DIC["lei"].items()}


def _pares():
    for n, g in GRUPO.items():
        for c, gs in CONCEPTOS.items():
            if g in gs:
                yield n, c


def _normalizar(regla) -> dict:
    """Regla del diccionario -> {'tipo': suma|resta|no_disponible, 'elementos': [...]}."""
    if isinstance(regla, dict) and "no_disponible" in regla:
        return {"tipo": "no_disponible", "elementos": []}
    if isinstance(regla, dict) and "resta" in regla:
        return {"tipo": "resta", "elementos": list(regla["resta"])}
    return {"tipo": "suma", "elementos": sorted(regla)}


def oro() -> dict:
    ents = _entidades()
    return {(n, c): _normalizar(ents[n]._regla(c)) for n, c in _pares()}


def _valor(ent: Entidad, propuesta: dict, concepto: str):
    if propuesta["tipo"] == "no_disponible" or not propuesta["elementos"]:
        return None
    vals = [ent._hecho(e, 2025, TIPO[concepto]) for e in propuesta["elementos"]]
    if propuesta["tipo"] == "resta":
        if vals[0] is None:
            return None
        return vals[0]["valor"] - (vals[1]["valor"] if len(vals) > 1 and vals[1] else 0)
    vals = [v for v in vals if v]
    return sum(v["valor"] for v in vals) if vals else None


def metodo_literal() -> dict:
    ents = _entidades()
    res = {}
    for n, c in _pares():
        presentes = [e for e in ESPERADO[c] if ents[n]._hecho(e, 2025, TIPO[c])]
        res[(n, c)] = {"tipo": "suma", "elementos": sorted(presentes)} if presentes else {"tipo": "no_disponible", "elementos": []}
    return res


def metodo_anclaje() -> dict:
    ents, anc = _entidades(), pd.read_csv(ANCLAJES, dtype=str)
    res = metodo_literal()
    for (n, c), p in res.items():
        if p["tipo"] != "no_disponible":
            continue
        lei = DIC["lei"][n]
        cand = anc[(anc.lei == lei) & anc.ancla.isin(ESPERADO[c]) & (anc.sentido == "la extensión es más estrecha")]
        con_dato = [e for e in cand.extension if ents[n]._hecho(e, 2025, TIPO[c])]
        if len(con_dato) == 1:  # solo si el anclaje es inequívoco
            res[(n, c)] = {"tipo": "suma", "elementos": con_dato}
    return res


def metodo_llm() -> dict | None:
    if not PROPUESTAS_LLM.exists():
        return None
    datos = json.loads(PROPUESTAS_LLM.read_text(encoding="utf-8"))
    res = {}
    for p in datos:
        tipo = p.get("tipo", "suma")
        el = p.get("elementos", [])
        res[(p["entidad"], p["concepto"])] = {"tipo": tipo, "elementos": el if tipo == "resta" else sorted(el)}
    return res


def evaluar(propuestas: dict, nombre: str) -> pd.DataFrame:
    ents, ref = _entidades(), oro()
    filas = []
    for (n, c), g in ref.items():
        p = propuestas.get((n, c), {"tipo": "no_disponible", "elementos": []})
        exacta = p["tipo"] == g["tipo"] and (p["elementos"] == g["elementos"] if g["tipo"] == "resta" else sorted(p["elementos"]) == g["elementos"])
        vg, vp = _valor(ents[n], g, c), _valor(ents[n], p, c)
        if vg is None and vp is None:
            equivalente = True
        elif vg is None or vp is None:
            equivalente = False
        else:
            equivalente = abs(vp - vg) <= 0.005 * max(abs(vg), 1)
        filas.append({"metodo": nombre, "entidad": n, "concepto": c, "oro": g, "propuesta": p,
                      "exacta": exacta, "equivalente": exacta or equivalente})
    return pd.DataFrame(filas)


def brief():
    """Material para el LLM: hechos de 2025 sin dimensiones, con etiqueta y anclaje. No incluye el diccionario."""
    anc = pd.read_csv(ANCLAJES, dtype=str)
    salida = RAIZ / "data/processed/brief_llm"
    salida.mkdir(parents=True, exist_ok=True)
    for n, lei in DIC["lei"].items():
        d = pd.read_csv(next((RAIZ / "data/processed").glob(f"{lei}-*_facts.csv")), dtype=str, keep_default_na=False)
        d["valor"] = d.valor.astype(float)
        d = d[(d.dimensiones == "") & (d.fecha_fin == "2025-12-31")]
        d = d[(d.periodo_tipo == "instante") | (d.fecha_inicio == "2025-01-01")]
        d["elemento"] = d.prefijo + ":" + d.concepto
        a = anc[anc.lei == lei].groupby("extension").ancla.apply(lambda s: "; ".join(sorted(set(s))))
        d["anclaje"] = d.elemento.map(a).fillna("")
        d["valor_meur"] = (d.valor / 1e6).round(1)
        d[["elemento", "etiqueta_extension", "periodo_tipo", "valor_meur", "anclaje"]].drop_duplicates("elemento").to_csv(salida / f"{n}.csv", index=False)
    conceptos = [{"concepto": c, "aplica_a": sorted(g), "tipo": TIPO[c], "descripcion": DESCRIPCION[c]} for c, g in CONCEPTOS.items()]
    (salida / "conceptos.json").write_text(json.dumps({"entidades": GRUPO, "conceptos": conceptos}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"brief en {salida}")


def main():
    if "--brief" in sys.argv:
        brief()
        return
    tablas = [evaluar(metodo_literal(), "literal"), evaluar(metodo_anclaje(), "anclaje")]
    llm = metodo_llm()
    if llm:
        tablas.append(evaluar(llm, "llm"))
    df = pd.concat(tablas)
    df.assign(oro=df.oro.map(json.dumps), propuesta=df.propuesta.map(json.dumps)).to_csv(RAIZ / "data/results/propuesta_reglas.csv", index=False)
    resumen = df.groupby("metodo", sort=False).agg(pares=("exacta", "size"), exactas=("exacta", "sum"), equivalentes=("equivalente", "sum"))
    resumen["% equivalentes"] = (100 * resumen.equivalentes / resumen.pares).round(1)
    print(resumen.to_string())


if __name__ == "__main__":
    main()
