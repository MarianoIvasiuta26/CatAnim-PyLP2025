"""
Conversor simple: CSV de reglas (exportado desde RapidMiner con "Tree to Rules")
a archivo Prolog con hechos regla/2.

Esperado: un CSV con columnas: rule_id,label,conditions
- label: categoría predicha (número o átomo)
- conditions: lista de condiciones con formato `atributo = 1 AND otro = 0 ...`
"""

import csv
import re
import sys
from pathlib import Path

def to_atom(s):
    return (
        s.strip()
        .lower()
        .replace(" ", "_")
        .replace("ñ","n")
        .replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    )

def parse_conditions(cond_str):
    # Divide por AND/OR (asumimos AND para reglas de árbol)
    parts = re.split(r"\s+AND\s+|\s*&\s*", cond_str, flags=re.I)
    lits = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # Aceptamos formatos: attr = 1, attr = 0, attr = true/false
        m = re.match(r"([^=<>]+)=\s*([01]|true|false)", p, flags=re.I)
        if not m:
            # fallback para expresiones tipo attr IS TRUE
            m = re.match(r"([^ ]+)\s+IS\s+(TRUE|FALSE)", p, flags=re.I)
        if m:
            attr = to_atom(m.group(1))
            val = m.group(2).lower()
            val = "1" if val in ("1","true") else "0"
            if val == "1":
                lits.append(f"tiene(X, {attr})")
            else:
                lits.append(f"\\+ tiene(X, {attr})")
    return lits

def main(in_csv, out_pl):
    rows = list(csv.DictReader(open(in_csv, newline='', encoding='utf-8')))
    out = []
    out.append("% reglas(auto) generadas desde " + Path(in_csv).name)
    out.append("% regla(Label, CondicionesComoLista).")
    for i, r in enumerate(rows, 1):
        label = to_atom(str(r.get("label", f"cat{i}")))
        conds = parse_conditions(r.get("conditions",""))
        conds_list = ", ".join(conds) if conds else "true"
        out.append(f"regla({label}, [{conds_list}]).")
    Path(out_pl).write_text("\n".join(out), encoding="utf-8")
    print("OK ->", out_pl)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python csv_reglas_a_prolog.py reglas_rapidminer.csv salida.pl")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
