"""L'essai « Nouvelle phase du méchant » se coche par compte (10/10/2026).

Vérifie, sur une base jetable :
  1. un compte neuf n'a pas l'essai, et sa table n'en reçoit pas la clé ;
  2. le basculer depuis /admin l'active, et la configuration de SA table porte
     `essai_phase_mechant` ; un autre compte n'est pas touché ;
  3. un second basculement le coupe ;
  4. une base d'avant la colonne la reçoit au démarrage (migration).

Usage : python3 site/test_essai_phase.py
"""
import json
import os
import sqlite3
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
dossier = tempfile.mkdtemp(prefix="essai-phase-")
os.environ["BASE"] = os.path.join(dossier, "narwhal.db")
sys.path.insert(0, ICI)

import orchestrateur as o  # noqa: E402

# ⚠ LA TABLE D'ESSAI S'ECRIT DANS LE DOSSIER JETABLE : `_config_partie` cree les
# dossiers de sa place et son `launch-N.json` sous RACINE_JEU.
import shutil  # noqa: E402
jeu = os.path.join(dossier, "jeu")
os.makedirs(jeu)
shutil.copy(os.path.join(o.RACINE_JEU, "launch.json"), os.path.join(jeu, "launch.json"))
o.RACINE_JEU = jeu

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


# 4. Une base d'AVANT la colonne : la migration l'ajoute.
with sqlite3.connect(os.environ["BASE"]) as cx:
    cx.execute("CREATE TABLE comptes (pseudo TEXT PRIMARY KEY, email TEXT UNIQUE, sel TEXT NOT NULL,"
               " empreinte TEXT NOT NULL, statut TEXT NOT NULL DEFAULT 'attente', cree TEXT NOT NULL,"
               " derniere_connexion TEXT)")
    cx.execute("INSERT INTO comptes (pseudo, email, sel, empreinte, statut, cree)"
               " VALUES ('yarro', 'y@x.be', 's', 'e', 'valide', '2026-10-10')")
    cx.execute("INSERT INTO comptes (pseudo, email, sel, empreinte, statut, cree)"
               " VALUES ('autre', 'a@x.be', 's', 'e', 'valide', '2026-10-10')")
o.initialiser_base()
with sqlite3.connect(os.environ["BASE"]) as cx:
    colonnes = {r[1] for r in cx.execute("PRAGMA table_info(comptes)")}
verifier("migration : la colonne essai_phase est ajoutée", "essai_phase" in colonnes)

# 1. Par défaut, pas d'essai.
verifier("compte neuf : pas d'essai", o.essai_phase_de("yarro") is False)


class Partie:
    def __init__(self, code):
        self.code = code
        self.mot_de_passe = "m"
        self.cles_sieges = ["", "", "", ""]
        self.jeton_site = "j"


def config_de(code):
    chemin = o._config_partie(9, Partie(code))
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


verifier("table sans essai : pas de clé", "essai_phase_mechant" not in config_de("yarro"))

# 2. Basculer l'active pour CE compte seulement.
o.basculer_essai_phase("Yarro ")
verifier("basculé : essai actif", o.essai_phase_de("yarro") is True)
verifier("sa table reçoit la clé", config_de("yarro").get("essai_phase_mechant") is True)
verifier("un autre compte n'est pas touché", o.essai_phase_de("autre") is False)
verifier("la table d'un autre compte n'a pas la clé", "essai_phase_mechant" not in config_de("autre"))

# 3. Un second basculement le coupe.
o.basculer_essai_phase("yarro")
verifier("rebasculé : essai coupé", o.essai_phase_de("yarro") is False)

# La page d'administration montre l'interrupteur.
source = open(os.path.join(ICI, "orchestrateur.py"), encoding="utf-8").read()
verifier("l'admin propose l'interrupteur", 'value="essai_phase"' in source and 'action == "essai_phase"' in source)
shutil.rmtree(dossier, ignore_errors=True)

print("\n%s" % ("TOUT EST BON" if not echecs else "%d ECHEC(S)" % len(echecs)))
sys.exit(1 if echecs else 0)
