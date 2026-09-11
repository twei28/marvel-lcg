"""Verifie data/translate_fr.json contre les phrases que le moteur emet vraiment.

Le moteur traduit par correspondance EXACTE de la chaine (TransText, dans
src/engine/lib/translate.py) : une cle qui ne correspond a aucun litteral du
code ne traduit rien, en silence. C'est arrive : « {trigger} is being attack
by {attacker} » (sans -ed) laissait « Spider-Man is being attacked by Klaw »
en anglais dans une partie en francais (capture de l'utilisateur, 11/09/2026).

Ce qui ECHOUE : une cle orpheline (aucun litteral du code ne la porte).
Ce qui s'AFFICHE seulement : les litteraux du code sans traduction, pour
savoir ou en est la couverture.

Usage : python3 tools/verifier_traductions_fr.py   (depuis Fusion/marvel-lcg-src)
"""
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE = os.path.join(RACINE, "data", "translate_fr.json")
SRC = os.path.join(RACINE, "src")

MOTIF = re.compile(r'TransText\(\s*(f?)"((?:[^"\\]|\\.)*)"')


def litteraux_du_code() -> set:
    trouves = set()
    for dossier, _, fichiers in os.walk(SRC):
        for nom in fichiers:
            if not nom.endswith(".py"):
                continue
            with open(os.path.join(dossier, nom), encoding="utf-8", errors="ignore") as f:
                source = f.read()
            for prefixe, brut in MOTIF.findall(source):
                if prefixe == "f":
                    continue  # une f-string n'est pas une cle de traduction
                # Le litteral Python contient des sequences d'echappement
                # (« \n ») ; la cle JSON contient le vrai saut de ligne.
                trouves.add(brut.encode("utf-8").decode("unicode_escape"))
    return trouves


def main() -> int:
    with open(TABLE, encoding="utf-8") as f:
        cles = set(json.load(f).keys())
    litteraux = litteraux_du_code()
    orphelines = sorted(c for c in cles if c not in litteraux)
    manquantes = sorted(l for l in litteraux if l not in cles and l.strip())

    for cle in orphelines:
        print("  ORPHELINE  " + repr(cle))
    print("cles FR : %d | litteraux moteur : %d | sans traduction : %d"
          % (len(cles), len(litteraux), len(manquantes)))
    if "--tout" in sys.argv:
        for l in manquantes:
            print("  sans traduction  " + repr(l))
    if orphelines:
        print("ECHEC : %d cle(s) orpheline(s), elles ne traduisent rien." % len(orphelines))
        return 1
    print("OK : aucune cle orpheline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
