from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path

from owlready2 import default_world, get_ontology, onto_path
from rdflib.term import Literal, URIRef


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY_FILE = ROOT / "Airbnb.owx"
QUESTIONS_FILE = ROOT / "preguntas.md"
OUTPUT_DIR = ROOT / "resultados_preguntas"
BASE_IRI = "http://www.semanticweb.org/steven/ontologies/2026/2/airbnb#"


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()
    return text[:60] or "consulta"


def parse_queries(markdown: str) -> list[tuple[str, str]]:
    queries: list[tuple[str, str]] = []
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith("## "):
            i += 1
            continue

        title = line[3:].strip()
        i += 1
        query_lines: list[str] | None = None

        while i < len(lines) and not lines[i].startswith("## "):
            if lines[i].startswith("```sparql"):
                i += 1
                query_lines = []
                while i < len(lines) and not lines[i].startswith("```"):
                    query_lines.append(lines[i])
                    i += 1
                break
            i += 1

        if query_lines:
            queries.append((title, "\n".join(query_lines).strip()))

    return queries


def format_cell(value) -> str:
    if isinstance(value, URIRef):
        text = str(value)
        return text.removeprefix(BASE_IRI)
    if isinstance(value, Literal):
        return str(value)
    return str(value)


def write_csv(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)


def main() -> None:
    onto_path.append(str(ROOT))
    get_ontology(ONTOLOGY_FILE.name).load()
    graph = default_world.as_rdflib_graph()

    queries = parse_queries(QUESTIONS_FILE.read_text(encoding="utf-8"))
    OUTPUT_DIR.mkdir(exist_ok=True)

    summary_lines = ["# Resultados de preguntas SPARQL", ""]

    for index, (title, query) in enumerate(queries, start=1):
        result = graph.query(query)
        headers = [str(var) for var in result.vars]
        raw_rows = list(result)
        rows = [[format_cell(cell) for cell in row] for row in raw_rows]

        filename = f"Q{index:02d}_{slugify(title)}.csv"
        write_csv(OUTPUT_DIR / filename, headers, rows)

        summary_lines.append(f"## {title}")
        summary_lines.append(f"- Filas: {len(rows)}")
        summary_lines.append(f"- Archivo: `{filename}`")
        summary_lines.append("")

    (OUTPUT_DIR / "resumen.md").write_text("\n".join(summary_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
