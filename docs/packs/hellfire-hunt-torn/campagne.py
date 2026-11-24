#!/usr/bin/env python3
"""Met a jour l'entree du scenario 4 « Torn » (`id: hellfire_torn`) de `data/campagnes/hellfire_hunt.json` (resume, enjeu).
Lecture-modification-ecriture sous flock /tmp/cards_json.lock : SEULE l'entree `hellfire_torn` est touchee. Idempotent.
Usage : python3 campagne.py <racine du moteur Fusion/marvel-lcg-src>
Les etapes de mise en place / de victoire sont dans le code (`cards.pack.hellfire_hunt.campaign` + `hf503a`, `ReleveTorn`) ; le carnet n'a AUCUNE cle propre au
scenario 4 (allies Recruited, manigances POTENTIAL ALLY retirees, PV restants en expert : cles communes de `victoire_commune`).
"""
import fcntl
import io
import json
import sys

RESUME = "Emma Frost, déchirée, est devenue le jouet de Cassandra Nova : elle ne peut pas être vaincue, il faut briser l'emprise psychique qui la tient."
ENJEU = ("Emma Frost a quatre faces : vaincue, elle se retourne (PV infinis) jusqu'à la fin de la phase du méchant, puis revient à ses PV imprimés. On gagne en retirant toute la menace "
         "de Nova's Psychic Puppetry (face Fragment). Le deck Hellfire regroupe les sbires ÉLITE HELLFIRE, avec sa propre défausse. "
         "À la victoire, les alliés Recruited gagnés sont notés ; en expert, les PV restants aussi.")


def main():
    chemin = sys.argv[1].rstrip("/") + "/data/campagnes/hellfire_hunt.json"
    with open("/tmp/cards_json.lock", "w") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX)
        d = json.load(io.open(chemin, encoding="utf-8"))
        n = 0
        for sc in d["scenarios"]:
            if sc["id"] == "hellfire_torn":
                sc["resume"], sc["enjeu"] = RESUME, ENJEU
                n += 1
        assert n == 1
        with io.open(chemin, "w", encoding="utf-8", newline="") as f:
            f.write(json.dumps(d, indent=1, ensure_ascii=False))
    print("hellfire_torn mis a jour")


main()
