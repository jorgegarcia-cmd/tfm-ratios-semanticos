"""Capa de consulta: responde preguntas sobre ratios con cifras trazables y contexto.

Arquitectura (ver memoria, cap. 3):
  pregunta en lenguaje natural
    -> interpretación (LLM con la herramienta `consultar_ratio`, o el parser por reglas de este módulo)
    -> consultar()  [determinista: nunca inventa cifras]
    -> respuesta redactada (LLM o plantilla) citando fórmula, fuente y avisos de comparabilidad

Uso sin LLM (demo):
    PYTHONPATH=src python -m tfm_ratios.consulta "¿Cuál fue el ROE de BBVA en 2025?"
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[2]
CALCULADOS = RAIZ / "data" / "results" / "ratios_calculados.csv"
PUBLICADOS = RAIZ / "data" / "published" / "ratios_publicados.csv"
DICCIONARIO = RAIZ / "config" / "diccionario_semantico.yaml"

NOMBRES = {
    "santander": "Banco Santander", "bbva": "BBVA", "caixabank": "CaixaBank",
    "sabadell": "Banco Sabadell", "mapfre": "Mapfre", "linea_directa": "Línea Directa",
}
NOMBRE_RATIO = {
    "roe": "ROE", "roe_fondos_propios": "ROE sobre fondos propios", "roa": "ROA",
    "eficiencia": "ratio de eficiencia", "nim": "margen de intereses sobre activos medios (NIM)",
    "ltd": "ratio préstamos/depósitos", "siniestralidad": "ratio de siniestralidad",
    "ratio_gastos": "ratio de gastos", "ratio_combinado": "ratio combinado",
    "morosidad": "tasa de morosidad", "cobertura": "tasa de cobertura", "cet1": "ratio CET1",
    "solvencia_ii": "ratio de Solvencia II", "rote": "RoTE",
}

# Esquema de la herramienta para un LLM con llamada a funciones (tool use)
HERRAMIENTA = {
    "name": "consultar_ratio",
    "description": (
        "Devuelve el valor de un ratio financiero de una entidad y ejercicio, calculado de forma "
        "determinista desde su informe ESEF, con la fórmula, las cifras de origen, el valor publicado "
        "por la propia entidad si existe, los comparables del sector y avisos de comparabilidad. "
        "Úsala SIEMPRE para cualquier cifra; no calcules ni recuerdes cifras por tu cuenta."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "entidad": {"type": "string", "enum": list(NOMBRES)},
            "ratio": {"type": "string", "enum": list(NOMBRE_RATIO)},
            "ejercicio": {"type": "integer", "enum": [2024, 2025]},
        },
        "required": ["entidad", "ratio", "ejercicio"],
    },
}


def _cargar():
    calc = pd.read_csv(CALCULADOS)
    pub = pd.read_csv(PUBLICADOS) if PUBLICADOS.exists() else pd.DataFrame(
        columns=["entidad", "ratio", "variante", "ejercicio", "valor_pct", "definicion_entidad", "fuente", "cita"])
    dic = yaml.safe_load(DICCIONARIO.read_text(encoding="utf-8"))
    return calc, pub, dic


def consultar(entidad: str, ratio: str, ejercicio: int) -> dict:
    """Respuesta estructurada y trazable. Es lo único que el LLM puede usar como fuente de cifras."""
    calc, pub, dic = _cargar()
    fila = calc[(calc.entidad == entidad) & (calc.ratio == ratio) & (calc.ejercicio == ejercicio)]
    p = pub[(pub.entidad == entidad) & (pub.ratio == ratio) & (pub.ejercicio == ejercicio)]
    base = ratio.replace("_fondos_propios", "")
    def_ratio = dic["ratios"].get(base, {})

    res: dict = {
        "entidad": NOMBRES.get(entidad, entidad), "ratio": NOMBRE_RATIO.get(ratio, ratio),
        "ejercicio": ejercicio, "calculado": None, "publicado": [], "comparables": [], "avisos": [],
        "interpretacion": def_ratio.get("interpretacion"), "variantes_conocidas": def_ratio.get("variantes", []),
    }
    if not fila.empty:
        f = fila.iloc[0]
        if pd.notna(f.valor_pct):
            res["calculado"] = {
                "valor_pct": float(f.valor_pct), "formula": f.formula,
                "numerador_meur": f.numerador_meur, "denominador_meur": f.denominador_meur,
                "fuente": "Informe financiero anual consolidado 2025 en formato ESEF (cifras XBRL sin dimensiones)",
            }
            if isinstance(f.nota, str) and f.nota:
                res["avisos"].append(f"Base del denominador: {f.nota}.")
            grupo = calc[(calc.ratio == ratio) & (calc.ejercicio == ejercicio) & (calc.grupo == f.grupo)
                         & calc.valor_pct.notna()].sort_values("valor_pct", ascending=False)
            res["comparables"] = [
                {"entidad": NOMBRES[r.entidad], "valor_pct": float(r.valor_pct)} for r in grupo.itertuples()]
        else:
            res["avisos"].append(f"No calculable desde ESEF: {f.no_calculable}.")
    for r in p.itertuples():
        res["publicado"].append({
            "valor_pct": float(r.valor_pct), "variante": r.variante if isinstance(r.variante, str) else "",
            "definicion_entidad": r.definicion_entidad, "fuente": r.fuente,
        })
    if res["calculado"] and res["publicado"]:
        dif = res["calculado"]["valor_pct"] - res["publicado"][0]["valor_pct"]
        if abs(dif) >= 0.5:
            res["avisos"].append(
                f"El valor calculado difiere {dif:+.2f} p.p. del publicado por la entidad: las definiciones "
                "no coinciden (ver definición de la entidad).")
    if ratio in ("roe", "roe_fondos_propios"):
        res["avisos"].append(
            "El ROE depende de la base de patrimonio: con patrimonio total atribuido (incluye otro resultado "
            "global acumulado) o con fondos propios. Compare siempre la misma definición entre entidades.")
    return res


# ---------------------------------------------------------------------------
# Parser por reglas (sustituible por el LLM) y redacción por plantilla
# ---------------------------------------------------------------------------
def _norm(t: str) -> str:
    return unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()


PATRONES_ENTIDAD = {
    "santander": r"santander", "bbva": r"bbva", "caixabank": r"caixa", "sabadell": r"sabadell",
    "mapfre": r"mapfre", "linea_directa": r"linea directa",
}
PATRONES_RATIO = [  # orden: de más a menos específico
    ("roe_fondos_propios", r"roe.*fondos propios"), ("rote", r"rote|tangible"), ("roe", r"\broe\b|rentabilidad sobre (recursos|fondos) propios"),
    ("roa", r"\broa\b|rentabilidad sobre activos"), ("eficiencia", r"eficiencia|cost.to.income"),
    ("nim", r"\bnim\b|margen de intereses"), ("ltd", r"prestamos.*depositos|loan.to.deposit|\bltd\b"),
    ("morosidad", r"morosidad|\bnpl\b|dudosos"), ("cobertura", r"cobertura"), ("cet1", r"cet ?1|capital"),
    ("ratio_combinado", r"combinado"), ("siniestralidad", r"siniestralidad"), ("ratio_gastos", r"ratio de gastos"),
    ("solvencia_ii", r"solvencia"),
]


def interpretar(pregunta: str) -> dict:
    t = _norm(pregunta)
    entidades = [e for e, p in PATRONES_ENTIDAD.items() if re.search(p, t)]
    ratio = next((r for r, p in PATRONES_RATIO if re.search(p, t)), None)
    ratios = [ratio] if ratio else []
    if ratio == "roe_fondos_propios" and "patrimonio" in t:  # pide ambas definiciones
        ratios.append("roe")
    anios = sorted({int(a) for a in re.findall(r"20(?:24|25)", t)}) or [2025]
    return {"entidades": entidades, "ratio": ratio, "ratios": ratios,
            "ejercicio": anios[-1], "ejercicios": anios}


def redactar(r: dict) -> str:
    partes = [f"{r['ratio'][0].upper() + r['ratio'][1:]} de {r['entidad']} en {r['ejercicio']}:"]
    if r["calculado"]:
        c = r["calculado"]
        partes.append(f"{c['valor_pct']:.2f} % calculado ({c['formula']}; {c['numerador_meur']:,.0f} / "
                      f"{c['denominador_meur']:,.0f} M€).")
    for p in r["publicado"]:
        var = f" ({p['variante']})" if p["variante"] else ""
        partes.append(f"La entidad publica {p['valor_pct']:.2f} %{var}: {p['definicion_entidad']}")
    if not r["calculado"] and not r["publicado"]:
        partes.append("No hay dato disponible.")
    if r["comparables"] and len(r["comparables"]) > 1:
        comp = ", ".join(f"{x['entidad']} {x['valor_pct']:.2f} %" for x in r["comparables"])
        partes.append(f"Comparables del mismo grupo y definición: {comp}.")
    partes += r["avisos"]
    if r["interpretacion"]:
        partes.append(f"Interpretación: {r['interpretacion']}")
    return "\n".join(partes)


def responder(pregunta: str) -> str:
    q = interpretar(pregunta)
    if not q["entidades"] or not q["ratio"]:
        return "No he identificado entidad o ratio en la pregunta."
    return "\n\n".join(redactar(consultar(e, r, a))
                       for e in q["entidades"] for r in q["ratios"] for a in q["ejercicios"])


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--herramienta":
        print(json.dumps(HERRAMIENTA, ensure_ascii=False, indent=2))
    else:
        print(responder(" ".join(sys.argv[1:]) or "¿Cuál fue el ROE de BBVA en 2025?"))
