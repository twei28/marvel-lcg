"""Insere (ou remplace) les 24 cartes du scenario Super-Skrull et du set Kree-Skrull War dans
Fusion/marvel-lcg-src/data/cards.json (cle `skrull_menace`), met a jour data/sets_info.json
(« 143. Custom (Skrull Menace) ») et recalcule les checksums.

IDEMPOTENT : une carte deja presente (meme card_id) est remplacee, jamais dupliquee ; relancer
le script apres une fusion donne le meme resultat. Usage (depuis n'importe ou) :
    python3 .planning/skrull-menace/defs/inserer_super_skrull.py
Le python du depot n'est necessaire que pour le recalcul des checksums (le script utilise
l'interpreteur courant : lancer avec le python du depot).
"""
import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
sys.path.insert(0, ICI)
from super_skrull_cards import CARDS  # noqa: E402

CLE_PACK = "skrull_menace"
CLE_SET = "143. Custom (Skrull Menace)"
SCENARIOS = ["sk_super_skrull"]
ENCOUNTERS = ["sk_kree_skrull_war"]


def numero(card_id: str) -> int:
    return int(re.match(r"sk(\d+)", card_id).group(1))


def charger(chemin):
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def ecrire(chemin, donnees):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=1, ensure_ascii=False)  # le fichier d'origine n'a pas de retour final


def main():
    chemin_cartes = os.path.join(MOTEUR, "data", "cards.json")
    cartes = charger(chemin_cartes)
    pack = cartes[CLE_PACK]
    nouveaux = {c["card_id"]: c for c in CARDS}
    pack[:] = [c for c in pack if c["card_id"] not in nouveaux]
    # Chaque carte va avant la premiere carte « sk » de numero superieur (le pack n'est pas
    # trie en bloc : `skrull_minion`, carte technique, garde sa place) ; sinon en fin de liste.
    for carte in nouveaux.values():
        cle = (numero(carte["card_id"]), carte["card_id"])
        place = len(pack)
        for i, autre in enumerate(pack):
            if re.match(r"sk\d+", autre["card_id"]) and (numero(autre["card_id"]), autre["card_id"]) > cle:
                place = i
                break
        pack.insert(place, carte)
    ecrire(chemin_cartes, cartes)

    chemin_sets = os.path.join(MOTEUR, "data", "sets_info.json")
    sets = charger(chemin_sets)
    fiche = sets[CLE_SET]
    for nom in SCENARIOS:
        if nom not in fiche["scenarios"]:
            fiche["scenarios"].append(nom)
    for nom in ENCOUNTERS:
        if nom not in fiche["encounters"]:
            fiche["encounters"].append(nom)
    plus_grand = max(numero(c["card_id"]) for c in pack if re.match(r"sk\d+", c["card_id"]))
    fiche["max_id"] = "sk%03d" % plus_grand
    ecrire(chemin_sets, sets)

    env = dict(os.environ, PYTHONPATH=os.path.join(MOTEUR, "src"), RELEASE="1")
    subprocess.run([sys.executable, os.path.join(MOTEUR, "tools", "recalculer_checksums.py"), MOTEUR,
                    "data/cards.json", "data/sets_info.json"], check=True, env=env, cwd=MOTEUR)
    print("OK : %d cartes Super-Skrull / Kree-Skrull War (re)inserees, max_id sk%03d" % (len(nouveaux), plus_grand))


if __name__ == "__main__":
    main()
