"""API web del prototipo (despliegue en Vercel). Reutiliza src/tfm_ratios/consulta.py sin cambios."""
import json
import sys
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

RAIZ = Path(__file__).parent
sys.path.insert(0, str(RAIZ / "src"))
from tfm_ratios.consulta import NOMBRE_RATIO, NOMBRES, consultar, interpretar, redactar  # noqa: E402

app = FastAPI(title="Ratios con contexto semántico")
CALC = pd.read_csv(RAIZ / "data/results/ratios_calculados.csv")
TRAZAS = json.loads((RAIZ / "data/results/trazas.json").read_text(encoding="utf-8"))
COMP = pd.read_csv(RAIZ / "data/results/comparacion.csv")


@app.get("/", response_class=HTMLResponse)
def inicio():
    return (RAIZ / "index.html").read_text(encoding="utf-8")


@app.get("/api/pregunta")
def pregunta(q: str = Query(..., max_length=300)):
    i = interpretar(q)
    respuestas = []
    for e in i["entidades"]:
        for r in i["ratios"]:
            for a in i["ejercicios"]:
                res = consultar(e, r, a)
                respuestas.append({"estructurada": res, "texto": redactar(res)})
    return {"interpretacion": i, "respuestas": respuestas}


@app.get("/api/ratios")
def ratios():
    filas = CALC.astype(object).where(pd.notna(CALC), None).to_dict(orient="records")
    return {"filas": filas, "nombres": NOMBRES, "ratios": NOMBRE_RATIO}


@app.get("/api/traza")
def traza(entidad: str, ratio: str, ejercicio: int):
    t = next((t for t in TRAZAS if t["entidad"] == entidad and t["ratio"] == ratio and t["ejercicio"] == ejercicio), None)
    return t or {"error": "sin traza"}


@app.get("/api/comparacion")
def comparacion():
    return {"filas": COMP.astype(object).where(pd.notna(COMP), None).to_dict(orient="records")}
