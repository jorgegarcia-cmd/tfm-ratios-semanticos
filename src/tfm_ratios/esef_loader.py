"""Extracción de hechos XBRL de un paquete ESEF (.zip) a una tabla plana.

Uso:
    python -m tfm_ratios.esef_loader data/raw/esef/bankinter_2024.zip

Genera data/processed/<nombre>_facts.csv con una fila por hecho XBRL:
    concepto, prefijo, valor, unidad, decimales, periodo_tipo, fecha_inicio, fecha_fin, dimensiones

Nota: Arelle descarga las taxonomías ESMA/IFRS la primera vez (requiere internet)
y las guarda en caché local.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from arelle import Cntlr


def extraer_hechos(ruta_zip: str | Path) -> pd.DataFrame:
    cntlr = Cntlr.Cntlr(logFileName="logToPrint")
    modelo = cntlr.modelManager.load(str(ruta_zip))
    if modelo is None:
        raise RuntimeError(f"No se pudo cargar {ruta_zip}")

    filas = []
    for hecho in modelo.facts:
        if hecho.isNil or not hecho.isNumeric:
            continue  # en esta fase solo interesan las cifras
        ctx = hecho.context
        instantaneo = ctx.isInstantPeriod
        filas.append(
            {
                "concepto": hecho.qname.localName,
                "prefijo": hecho.qname.prefix,
                "valor": float(hecho.xValue) if hecho.xValue is not None else None,
                "unidad": hecho.unit.id if hecho.unit is not None else None,
                "decimales": hecho.decimals,
                "periodo_tipo": "instante" if instantaneo else "duracion",
                "fecha_inicio": None if instantaneo else ctx.startDatetime.date().isoformat(),
                # Arelle devuelve el fin de periodo como el día siguiente a medianoche
                "fecha_fin": (
                    (ctx.instantDatetime if instantaneo else ctx.endDatetime) - pd.Timedelta(days=1)
                ).date().isoformat(),
                "dimensiones": ";".join(
                    f"{dim.localName}={mem.memberQname.localName if mem.isExplicit else mem.typedMember}"
                    for dim, mem in sorted(ctx.qnameDims.items(), key=lambda x: str(x[0]))
                ),
            }
        )
    cntlr.modelManager.close()
    return pd.DataFrame(filas)


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    ruta = Path(sys.argv[1])
    df = extraer_hechos(ruta)
    salida = Path("data/processed") / f"{ruta.stem}_facts.csv"
    salida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(salida, index=False)
    sin_dims = df[df["dimensiones"] == ""]
    print(f"{len(df)} hechos numéricos ({len(sin_dims)} sin dimensiones) -> {salida}")
    print("Prefijos:", df["prefijo"].value_counts().to_dict())


if __name__ == "__main__":
    main()
