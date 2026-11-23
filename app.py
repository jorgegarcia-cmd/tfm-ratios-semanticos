"""Interfaz de demostración del prototipo.

    pip install -r requirements.txt
    streamlit run app.py
"""
import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / "src"))
from tfm_ratios.consulta import NOMBRE_RATIO, NOMBRES, consultar, interpretar, redactar  # noqa: E402

RAIZ = Path(__file__).parent
st.set_page_config(page_title="Ratios con contexto semántico", layout="wide")
st.title("Ratios financieros con contexto semántico")
st.caption("Banca y seguros cotizados en España · informes ESEF 2025 (con comparativo 2024)")

pestanas = st.tabs(["Pregunta", "Tabla de ratios", "Traza de un ratio"])

with pestanas[0]:
    pregunta = st.text_input("Pregunta", "¿Cuál fue el ROE de Santander y de BBVA en 2025?")
    if pregunta:
        q = interpretar(pregunta)
        st.write(f"Interpretación: entidades = {q['entidades']}, ratio = {q['ratio']}, ejercicio = {q['ejercicio']}")
        for e in q["entidades"]:
            if q["ratio"]:
                r = consultar(e, q["ratio"], q["ejercicio"])
                st.markdown("---")
                st.text(redactar(r))
                with st.expander("Respuesta estructurada (lo que recibe el LLM)"):
                    st.json(r)

with pestanas[1]:
    calc = pd.read_csv(RAIZ / "data/results/ratios_calculados.csv")
    ej = st.radio("Ejercicio", [2025, 2024], horizontal=True)
    for grupo in ("banca", "seguros"):
        t = calc[(calc.ejercicio == ej) & (calc.grupo == grupo)].pivot_table(
            index="ratio", columns="entidad", values="valor_pct")
        t.index = [NOMBRE_RATIO.get(i, i) for i in t.index]
        t.columns = [NOMBRES[c] for c in t.columns]
        st.subheader(grupo.capitalize())
        st.dataframe(t.map(lambda v: "n/d" if pd.isna(v) else f"{v:.2f} %"), use_container_width=True)

with pestanas[2]:
    trazas = json.loads((RAIZ / "data/results/trazas.json").read_text(encoding="utf-8"))
    c1, c2, c3 = st.columns(3)
    ent = c1.selectbox("Entidad", list(NOMBRES), format_func=NOMBRES.get)
    opciones = sorted({t["ratio"] for t in trazas if t["entidad"] == ent})
    rat = c2.selectbox("Ratio", opciones, format_func=lambda r: NOMBRE_RATIO.get(r, r))
    eje = c3.selectbox("Ejercicio", [2025, 2024])
    t = next((t for t in trazas if t["entidad"] == ent and t["ratio"] == rat and t["ejercicio"] == eje), None)
    if t:
        st.metric("Valor", "n/d" if t["valor_pct"] is None else f"{t['valor_pct']:.2f} %")
        for parte in ("numerador", "denominador"):
            st.markdown(f"**{parte.capitalize()}: {t[parte]['concepto']}** · regla: `{t[parte]['regla']}`")
            if t[parte]["hechos"]:
                st.table(pd.DataFrame(t[parte]["hechos"]))
            if t[parte]["motivo"]:
                st.warning(t[parte]["motivo"])
