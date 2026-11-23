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


# Variante calculada más próxima a la definición publicada por cada entidad
BASE_ENTIDAD = {("sabadell", "roe"): "roe_fondos_propios"}  # Sabadell: fondos propios sin OCI


def cargar_publicados() -> pd.DataFrame:
    pub = pd.read_csv(RAIZ / "data/published/ratios_publicados.csv")
    pub["entidad"] = pub["entidad"].map(lambda e: CLAVE.get(e, e))
    return pub


def referencia(pub: pd.DataFrame, entidad: str, ratio: str, ejercicio: int):
    p = pub[(pub.entidad == entidad) & (pub.ratio == ratio) & (pub.ejercicio == ejercicio)]
    p = p[~p.variante.fillna("").str.contains("proxy")]  # las aproximaciones no validan
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
    valor = {(r.entidad, r.ratio, r.ejercicio): r.valor_pct for r in calc.itertuples()}
    filas = []
    for c in calc.itertuples():
        if c.ratio == "roe_fondos_propios":
            continue
        r = referencia(pub, c.entidad, c.ratio, c.ejercicio)
        if r is None:
            continue
        base = BASE_ENTIDAD.get((c.entidad, c.ratio), c.ratio)
        calc_v = valor.get((c.entidad, base, c.ejercicio))
        dif = None if calc_v is None or pd.isna(calc_v) else round(calc_v - r.valor_pct, 2)
        filas.append({
            "entidad": c.entidad, "ratio": c.ratio, "ejercicio": c.ejercicio,
            "base_calculada": base, "calculado_pct": calc_v, "publicado_pct": r.valor_pct,
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
          f"diferencia absoluta mediana = {v.diferencia_pp.abs().median():.2f} p.p.")


if __name__ == "__main__":
    main()
