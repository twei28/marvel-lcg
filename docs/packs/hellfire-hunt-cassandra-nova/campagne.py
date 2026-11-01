#!/usr/bin/env python3
"""Ecrit (idempotent) l'entree du scenario 5 « Cassandra Nova » dans `data/campagnes/hellfire_hunt.json` : resume, enjeu (FR et EN), `final`, `defaite`
(champ DEJA lu par ui-app/src/board/campagne/defaite-campagne.ts : precedent mut_gen / trors, voir docs/rapports/CAMPAGNES.md). Ne touche AUCUNE autre entree.
Lecture-modification-ecriture sous flock `/tmp/cards_json.lock`. Usage : python3 campagne.py <racine_du_depot>"""
import fcntl
import io
import json
import os
import sys

CHEMIN = os.path.join(sys.argv[1], "Fusion", "marvel-lcg-src", "data", "campagnes", "hellfire_hunt.json")

CHAMPS = {
    "resume": "Cassandra Nova, la sœur jumelle maléfique de Charles Xavier, lance son plan d'extinction des mutants avec les moyens du Hellfire Club, des mutants captifs et de la technologie volée.",
    "enjeu": ("Dernier scénario : Cassandra Nova pose des compteurs de Contrôle sur votre identité ; à 3, Cassandra Domination vous force à choisir. "
              "Xavier's Institute quitte le jeu ; les survivants se rallient autour de Rally the Survivors. En expert, une défaite fait perdre toute la campagne ; "
              "la victoire la gagne."),
    "resume_en": "Cassandra Nova, Charles Xavier's evil twin sister, launches her plan for mutant extinction with the resources of the Hellfire Club, captured mutants and stolen technology.",
    "enjeu_en": ("Final scenario: Cassandra Nova places Cassandra Controls counters on your identity; at 3, Cassandra Domination forces a choice. Xavier's Institute leaves play; "
                 "the survivors rally around Rally the Survivors. In expert, a defeat loses the whole campaign; victory wins it."),
    "final": True,
}


def main() -> None:
    with open("/tmp/cards_json.lock", "w") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX)
        with io.open(CHEMIN, encoding="utf-8", newline="") as f:
            data = json.load(f)
        scenario = next(s for s in data["scenarios"] if s["id"] == "hellfire_cassandra_nova")
        scenario.update(CHAMPS)
        scenario["defaite"] = {"quand": "partie_perdue", "expert_seulement": True,
                               "texte": "Cassandra Nova élimine tous les mutants : la campagne est perdue."}
        with io.open(CHEMIN, "w", encoding="utf-8", newline="") as f:
            f.write(json.dumps(data, indent=1, ensure_ascii=False))
    print("ok")


main()
