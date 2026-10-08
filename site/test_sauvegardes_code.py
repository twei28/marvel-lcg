"""Les sauvegardes du code (08/10/2026) : la liste, la plus recente en tete.

    python3 site/test_sauvegardes_code.py
"""

import os
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import orchestrateur as o  # noqa: E402

echecs = []


def cas(nom, obtenu, attendu):
    if obtenu == attendu:
        print("  ok    %s" % nom)
    else:
        echecs.append(nom)
        print("  ECHEC %s : attendu %r, obtenu %r" % (nom, attendu, obtenu))


with tempfile.TemporaryDirectory() as dossier:
    for nom in ("code-20261007-2100-aaaa.zip", "code-20261008-0830-bbbb.zip", "autre.zip",
                "code-20261006-1200-cccc.zip", "notes.txt"):
        open(os.path.join(dossier, nom), "w").close()
    cas("seuls les zips de sauvegarde, le plus recent en tete",
        o.sauvegardes_du_code(dossier),
        ["code-20261008-0830-bbbb.zip", "code-20261007-2100-aaaa.zip", "code-20261006-1200-cccc.zip"])
cas("dossier absent : liste vide", o.sauvegardes_du_code("/n/existe/pas"), [])

print("\n%s" % ("TOUT EST VERT" if not echecs else "%d ECHEC(S)" % len(echecs)))
sys.exit(1 if echecs else 0)
