"""Motor de ratios con trazabilidad.

Para cada entidad y ejercicio:
  1. resuelve cada concepto canónico con las reglas de `mapeo` del diccionario semántico,
  2. calcula los ratios de forma determinista,
  3. guarda, junto a cada ratio, la traza completa: regla aplicada, etiquetas XBRL,
     valores, fechas e identificadores de los hechos en el documento ESEF.

Uso:
    PYTHONPATH=src python -m tfm_ratios.motor
Genera data/results/ratios_calculados.csv y data/results/trazas.json
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd
import yaml

RAIZ = Path(__file__).resolve().parents[2]
DICCIONARIO = RAIZ / "config" / "diccionario_semantico.yaml"
HECHOS = RAIZ / "data" / "processed"
SALIDA = RAIZ / "data" / "results"

GRUPO = {
    "santander": "banca", "bbva": "banca", "caixabank": "banca", "sabadell": "banca",
    "mapfre": "seguros", "linea_directa": "seguros",
}
EJERCICIOS = [2024, 2025]


@dataclass
class Valor:
    """Valor de un concepto con su procedencia."""
    concepto: str
    valor: float | None
    regla: str
    hechos: list[dict] = field(default_factory=list)
    motivo: str | None = None  # por qué no está disponible

    @property
    def ok(self) -> bool:
        return self.valor is not None


class Entidad:
    def __init__(self, nombre: str, lei: str, mapeo: dict):
        self.nombre = nombre
        self.grupo = GRUPO[nombre]
        self.mapeo = mapeo
        ficheros = list(HECHOS.glob(f"{lei}-*_facts.csv"))
        if not ficheros:
            raise FileNotFoundError(f"No hay hechos para {nombre} ({lei})")
        df = pd.read_csv(ficheros[0], dtype=str, keep_default_na=False)
        df["valor"] = df["valor"].astype(float)
        self.hechos = df[df["dimensiones"] == ""]  # solo cifras sin desglose dimensional

    # -- resolución de reglas ---------------------------------------------------
    def _regla(self, concepto: str):
        reglas = self.mapeo.get(concepto, {})
        for clave in (self.nombre, f"_{self.grupo}", "_todas"):
            if clave in reglas:
                return reglas[clave]
        return {"no_disponible": "concepto sin regla para esta entidad"}

    def _hecho(self, etiqueta: str, ejercicio: int, tipo: str) -> dict | None:
        prefijo, local = etiqueta.split(":")
        h = self.hechos[(self.hechos["prefijo"] == prefijo) & (self.hechos["concepto"] == local)]
        fin = f"{ejercicio}-12-31"
        if tipo == "duracion":
            h = h[(h["fecha_fin"] == fin) & (h["fecha_inicio"] == f"{ejercicio}-01-01")]
        else:
            h = h[(h["fecha_fin"] == fin) & (h["periodo_tipo"] == "instante")]
        if h.empty:
            return None
        r = h.iloc[0]
        return {"etiqueta": etiqueta, "valor": r["valor"], "fecha_fin": fin, "id_hecho": r["id_hecho"]}

    def valor(self, concepto: str, ejercicio: int, tipo: str) -> Valor:
        regla = self._regla(concepto)
        if isinstance(regla, dict) and "no_disponible" in regla:
            return Valor(concepto, None, "no_disponible", motivo=regla["no_disponible"])
        if isinstance(regla, dict) and "resta" in regla:
            a, b = (self._hecho(e, ejercicio, tipo) for e in regla["resta"])
            if a is None:
                return Valor(concepto, None, "resta", motivo=f"falta {regla['resta'][0]} en {ejercicio}")
            hechos = [a] + ([b] if b else [])
            return Valor(concepto, a["valor"] - (b["valor"] if b else 0.0), "resta", hechos)
        hechos = [self._hecho(e, ejercicio, tipo) for e in regla]
        encontrados = [h for h in hechos if h]
        if not encontrados:
            return Valor(concepto, None, "suma", motivo=f"sin hechos para {regla} en {ejercicio}")
        return Valor(concepto, sum(h["valor"] for h in encontrados), "suma", encontrados)

    def media(self, concepto: str, ejercicio: int) -> tuple[Valor, str]:
        """Media de saldos inicial y final; si falta el inicial, saldo de cierre."""
        fin = self.valor(concepto, ejercicio, "instante")
        ini = self.valor(concepto, ejercicio - 1, "instante")
        if fin.ok and ini.ok:
            return Valor(concepto, (fin.valor + ini.valor) / 2, f"media({fin.regla})",
                         ini.hechos + fin.hechos), "media de saldos inicial y final"
        return fin, "saldo de cierre (saldo inicial no etiquetado)"


# ---------------------------------------------------------------------------
# Definición de ratios: (id, grupos, numerador, denominador, base_denominador)
#   base: "flujo" (dato del periodo), "saldo" (cierre), "media" (media de saldos)
# ---------------------------------------------------------------------------
RATIOS = [
    ("roe", {"banca", "seguros"}, ("resultado_atribuido", "flujo"), ("patrimonio_atribuido", "media")),
    ("roe_fondos_propios", {"banca", "seguros"}, ("resultado_atribuido", "flujo"), ("fondos_propios", "media")),
    ("roa", {"banca", "seguros"}, ("resultado_ejercicio", "flujo"), ("activo_total", "media")),
    ("eficiencia", {"banca"}, ("gastos_explotacion_banca", "flujo"), ("margen_bruto", "flujo")),
    ("nim", {"banca"}, ("margen_intereses", "flujo"), ("activo_total", "media")),
    ("ltd", {"banca"}, ("prestamos_clientela", "saldo"), ("depositos_clientela", "saldo")),
    ("siniestralidad", {"seguros"}, ("siniestralidad_neta", "flujo"), ("ingresos_seguros", "flujo")),
    ("ratio_gastos", {"seguros"}, ("gastos_no_siniestros", "flujo"), ("ingresos_seguros", "flujo")),
    ("ratio_combinado", {"seguros"}, ("gastos_servicio_seguro", "flujo"), ("ingresos_seguros", "flujo")),
]
TIPO = {"flujo": "duracion", "saldo": "instante"}


def _componente(ent: Entidad, concepto: str, base: str, ejercicio: int) -> tuple[Valor, str]:
    if concepto == "gastos_no_siniestros":  # derivado: gastos del servicio de seguro - siniestralidad
        total = ent.valor("gastos_servicio_seguro", ejercicio, "duracion")
        sin = ent.valor("siniestralidad_neta", ejercicio, "duracion")
        if not (total.ok and sin.ok):
            return Valor(concepto, None, "derivado", motivo=sin.motivo or total.motivo), ""
        return Valor(concepto, total.valor - sin.valor, "derivado: gastos_servicio_seguro - siniestralidad_neta",
                     total.hechos + sin.hechos), ""
    if base == "media":
        return ent.media(concepto, ejercicio)
    return ent.valor(concepto, ejercicio, TIPO[base]), ""


def calcular() -> tuple[pd.DataFrame, list[dict]]:
    dic = yaml.safe_load(DICCIONARIO.read_text(encoding="utf-8"))
    filas, trazas = [], []
    for nombre, lei in dic["lei"].items():
        ent = Entidad(nombre, lei, dic["mapeo"])
        for ej in EJERCICIOS:
            for rid, grupos, (cn, bn), (cd, bd) in RATIOS:
                if ent.grupo not in grupos:
                    continue
                num, nota_n = _componente(ent, cn, bn, ej)
                den, nota_d = _componente(ent, cd, bd, ej)
                valor = None
                if num.ok and den.ok and den.valor:
                    valor = round(100 * num.valor / den.valor, 2)
                motivo = None if valor is not None else (num.motivo or den.motivo or "denominador nulo")
                nota = "; ".join(n for n in (nota_n, nota_d) if n)
                filas.append({
                    "entidad": nombre, "grupo": ent.grupo, "ejercicio": ej, "ratio": rid,
                    "valor_pct": valor, "numerador_meur": _m(num), "denominador_meur": _m(den),
                    "formula": f"{cn} / {'media(' + cd + ')' if bd == 'media' else cd}",
                    "nota": nota, "no_calculable": motivo,
                })
                trazas.append({
                    "entidad": nombre, "ejercicio": ej, "ratio": rid, "valor_pct": valor,
                    "numerador": num.__dict__, "denominador": den.__dict__, "nota": nota,
                })
    return pd.DataFrame(filas), trazas


def _m(v: Valor):
    return None if v.valor is None else round(v.valor / 1e6, 1)


def main() -> None:
    SALIDA.mkdir(parents=True, exist_ok=True)
    df, trazas = calcular()
    df.to_csv(SALIDA / "ratios_calculados.csv", index=False)
    (SALIDA / "trazas.json").write_text(json.dumps(trazas, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    tabla = df.pivot_table(index=["ratio"], columns=["entidad", "ejercicio"], values="valor_pct")
    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print(tabla.round(2))
    print(f"\n{df['valor_pct'].notna().sum()} ratios calculados; {df['valor_pct'].isna().sum()} no calculables")


if __name__ == "__main__":
    main()
