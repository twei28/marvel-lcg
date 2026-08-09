"""Quote les annotations forward-ref (types) dans les fichiers indiqués.

Quote toute expression d'annotation (après ': ' ou '-> ') qui ressemble à un
type (commence par une majuscule, ou est un accès attribut Type.Sub), pour
neutraliser les NameError des closures non évaluées au boot. Ne touche pas
aux annotations déjà quotées.

Usage: python3.10 quote_forward_refs.py <fichier.py> [<fichier.py> ...]
"""
import sys, re

def annotation_spans(line):
    spans, i = [], 0
    while i < len(line):
        m = re.match(r"(:\s*|->\s*)", line[i:])
        if not m or (line[i] == ':' and i + len(m.group(0)) >= len(line.rstrip('\n'))):
            i += 1
            continue
        start = i + len(m.group(0))
        j, depth = start, 0
        while j < len(line):
            c = line[j]
            if c in "([{":
                depth += 1
            elif c in ")]}":
                if depth == 0:
                    break
                depth -= 1
            elif depth == 0 and c in ",=:":
                break
            j += 1
        if j > start:
            spans.append((start, j))
        i = j if j > i else i + 1
    return spans

# un type : commence par une lettre majuscule, contient identifiants/./[]/|/espaces
TYPE_RE = re.compile(r"^[A-Z][\w\.\[\]\| ,']*$")

def process(path):
    lines = open(path).readlines()
    n = 0
    for idx, line in enumerate(lines):
        # ne quote que les lignes qui sont des 'def ' (signatures)
        if not re.match(r"\s*def ", line):
            continue
        for start, end in reversed(annotation_spans(line)):
            expr = line[start:end].strip()
            if "'" in expr or '"' in expr:
                continue
            if TYPE_RE.match(expr):
                line = line[:start] + f"'{expr}'" + line[end:]
                n += 1
        lines[idx] = line
    open(path, "w").writelines(lines)
    return n

total = 0
for p in sys.argv[1:]:
    c = process(p)
    total += c
    print(f"{c:3d} annotations quotées dans {p}")
print("total:", total)
