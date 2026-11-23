"""Genera anexos.md y las respuestas del prototipo a partir de los ficheros del proyecto."""
from pathlib import Path
import sys
import pandas as pd
import yaml

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "src"))
from tfm_ratios.consulta import interpretar, responder  # noqa: E402

d = yaml.safe_load((R / "config/diccionario_semantico.yaml").read_text(encoding="utf-8"))
q = pd.read_csv(R / "docs/evaluacion/preguntas.csv")
fuente = {"esef": "Calculado (ESEF)", "publicado": "Publicado por la entidad"}
o = ["# Anexo A. Diccionario semántico", "",
     "El diccionario completo está en `config/diccionario_semantico.yaml` del repositorio. Este anexo resume el catálogo de ratios; las reglas de mapeo por entidad se resumen en el apartado 3.4.2 y se recogen completas, con el motivo de cada excepción, en la sección `mapeo` del fichero.", "",
     "**Tabla 1. Catálogo de ratios del diccionario semántico**", "", "| Ratio | Aplica a | Fórmula | Fuente |", "|---|---|---|---|"]
for k, r in d["ratios"].items():
    o.append(f"| {r['nombre']} | {', '.join(r['aplica_a'])} | `{r['formula']}` | {fuente[r['fuente']]} |")
o += ["", "Fuente: Elaboración propia.", "", "# Anexo B. Preguntas de evaluación", "",
      "**Tabla 2. Preguntas de evaluación y respuestas de referencia**", "",
      "| Id | Tipo | Pregunta | Respuesta de referencia |", "|---|---|---|---|"]
for r in q.itertuples():
    o.append(f"| {r.id} | {r.tipo.replace('_', ' ')} | {r.pregunta} | {r.respuesta_referencia} |")
o += ["", "Fuente: Elaboración propia a partir del motor de ratios y de los informes de las entidades.", "",
      "# Anexo C. Repositorio y estructura del código", "",
      "El código, los datos derivados y esta memoria están en el repositorio privado https://github.com/jorgegarcia-cmd/tfm-ratios-semanticos, al que el autor dará acceso al tutor y al tribunal. La demostración del prototipo está publicada en https://tfm-ratios-semanticos.vercel.app.", "",
      "- `src/tfm_ratios/ixbrl_parser.py`: lector de Inline XBRL sin taxonomías externas.",
      "- `config/diccionario_semantico.yaml`: diccionario semántico (conceptos, ratios y reglas de mapeo).",
      "- `src/tfm_ratios/motor.py`: motor de ratios con trazabilidad.",
      "- `src/tfm_ratios/comparacion.py`: validación frente a los ratios publicados.",
      "- `src/tfm_ratios/consulta.py`: capa de consulta y esquema de la herramienta para un modelo de lenguaje.",
      "- `app.py`: interfaz de demostración en Streamlit.",
      "- `deploy/`: versión web (API FastAPI y página) desplegada en Vercel.",
      "- `data/published/`: ratios publicados por las entidades, con su definición y una cita verificable.",
      "- `data/results/`: ratios calculados, trazas y comparación.",
      "- `docs/evaluacion/`: preguntas, respuestas y rúbrica de la evaluación.", ""]
(R / "docs/memoria/anexos.md").write_text("\n".join(o), encoding="utf-8")

out = ["# Respuestas del prototipo (capa semántica con intérprete por reglas)\n", "Generado con `tfm_ratios.consulta.responder`.\n"]
for r in q.itertuples():
    i = interpretar(r.pregunta)
    out.append(f"## {r.id} · {r.pregunta}\n\nInterpretación: entidades={i['entidades']}, ratios={i['ratios']}, ejercicios={i['ejercicios']}\n\n```\n{responder(r.pregunta)}\n```\n")
(R / "docs/evaluacion/respuestas_prototipo.md").write_text("\n".join(out), encoding="utf-8")
print("anexos y respuestas regenerados")
