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

# L'archive des images, fabriquee a la volee.
import io, tarfile, types  # noqa: E402
with tempfile.TemporaryDirectory() as racine:
    assets = os.path.join(racine, "assets")
    os.makedirs(os.path.join(assets, "pics-fr"))
    open(os.path.join(assets, "pics-fr", "fr_61002.jpg"), "wb").write(b"jpg")
    o.DOSSIER_ASSETS = assets
    faux = types.SimpleNamespace(wfile=io.BytesIO(), entetes=[], close_connection=False)
    faux.send_response = lambda code: faux.entetes.append(("code", code))
    faux.send_header = lambda n, v: faux.entetes.append((n, v))
    faux.end_headers = lambda: None
    o.Handler._servir_images(faux)
    faux.wfile.seek(0)
    noms = tarfile.open(fileobj=faux.wfile).getnames()
    cas("l'archive des images contient assets/ et ses scans", "assets/pics-fr/fr_61002.jpg" in noms, True)
    cas("elle part en piece jointe", any(n == "Content-Disposition" for n, _ in faux.entetes), True)

# Les parties terminees des joueurs (onglet Parties > A revoir).
with tempfile.TemporaryDirectory() as dossier:
    os.makedirs(os.path.join(dossier, "yarro"))
    os.makedirs(os.path.join(dossier, "vide"))
    for nom in ("partie-20261007-2000-Rhino.marvelreplay", "partie-20261008-0900-Klaw.marvelreplay", "notes.txt"):
        open(os.path.join(dossier, "yarro", nom), "w").close()
    cas("par joueur, la plus recente en tete, sans les dossiers vides",
        o.parties_des_joueurs(dossier),
        {"yarro": ["partie-20261008-0900-Klaw.marvelreplay", "partie-20261007-2000-Rhino.marvelreplay"]})

print("\n%s" % ("TOUT EST VERT" if not echecs else "%d ECHEC(S)" % len(echecs)))
sys.exit(1 if echecs else 0)
