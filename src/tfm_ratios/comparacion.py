"""Validación: ratios calculados por el motor frente a los publicados por cada entidad.

    PYTHONPATH=src python -m tfm_ratios.comparacion
Genera data/results/comparacion.csv
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
CLAVE = {"Santander": "santander", "BBVA": "bbva", "CaixaBank": "caixabank", "Sabadell": "sabadell",
         "Mapfre": "mapfre", "Línea Directa": "linea_directa"}
# Variante publicada que se usa como referencia cuando hay varias
PREFERIDA = {"roa": ("RoA", "ROA"), "solvencia_ii": ("tras dividendo", "diciembre 2024", "septiembre 2025"),
             "siniestralidad": ("tabla",), "ratio_gastos": ("tabla",), "cet1": ("phased-in",)}


def cargar_publicados() -> pd.DataFrame:
    pub = pd.read_csv(RAIZ / "data/published/ratios_publicados.csv")
    pub["entidad"] = pub["entidad"].map(lambda e: CLAVE.get(e, e))
    return pub


def referencia(pub: pd.DataFrame, entidad: str, ratio: str, ejercicio: int):
    p = pub[(pub.entidad == entidad) & (pub.ratio == ratio) & (pub.ejercicio == ejercicio)]
    if p.empty:
        return None
    for clave in PREFERIDA.get(ratio, ()):
        q = p[p.variante.fillna("").str.contains(clave, regex=False)]
        if not q.empty:
            return q.iloc[0]
    return p.iloc[0]


def comparar() -> pd.DataFrame:
    calc = pd.read_csv(RAIZ / "data/results/ratios_calculados.csv")
    pub = cargar_publicados()
    filas = []
    for c in calc.itertuples():
        r = referencia(pub, c.entidad, c.ratio, c.ejercicio)
        if r is None:
            continue
        dif = None if pd.isna(c.valor_pct) else round(c.valor_pct - r.valor_pct, 2)
        filas.append({
            "entidad": c.entidad, "ratio": c.ratio, "ejercicio": c.ejercicio,
            "calculado_pct": c.valor_pct, "publicado_pct": r.valor_pct,
            "variante_publicada": r.variante if isinstance(r.variante, str) else "",
            "diferencia_pp": dif,
            "coincide": None if dif is None else abs(dif) < 0.5,
            "definicion_entidad": r.definicion_entidad,
        })
    return pd.DataFrame(filas)


def main():
    df = comparar()
    df.to_csv(RAIZ / "data/results/comparacion.csv", index=False)
    with pd.option_context("display.width", 200, "display.max_rows", 100):
        print(df[["entidad", "ratio", "ejercicio", "calculado_pct", "publicado_pct", "variante_publicada",
                  "diferencia_pp"]].to_string(index=False))
    v = df.dropna(subset=["diferencia_pp"])
    print(f"\n{len(v)} pares comparables; {int(v.coincide.astype(bool).sum())} coinciden (|dif| < 0,5 p.p.); "
          f"mediana |dif| = {v.diferencia_pp.abs().median():.2f} p.p.")


if __name__ == "__main__":
    main()
