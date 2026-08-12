"""Le nommage des cartes tient-il encore ?

Quatre silences que ce verificateur refuse. Chacun s'est deja produit :

1. UN card_id EN DOUBLE. Deux cartes sous le meme identifiant : la seconde
   ecrase la premiere, sans un mot.
2. UN PREFIXE FAN-MADE NON DECLARE. Le contenu fan-made prend un prefixe de
   deux LETTRES, declare dans tools/prefixes_fanmade.json. Un prefixe qui
   apparait sans y etre est un ajout qui n'a pas lu la regle.
3. UN card_id FAN-MADE QUI EMPRUNTE UN NUMERO. C'est exactement ce qui a
   bloque le projet : les sets officiels vont jusqu'a 60, et le fan-made
   occupait 61 a 79, la place des prochaines sorties de FFG.
4. UN NUMERO DE SET EN DOUBLE dans sets_info.json. Le numero sert de rang de
   tri a la galerie : deux sets au meme rang s'ordonnent au hasard. Trois
   doublons ont vecu la sans que personne ne les voie (108, 109, 110).

Il ne verifie PAS que les prefixes officiels sont justes : la numerotation de
FFG n'est pas la notre, et nous n'avons pas a la juger.

Usage: python3.10 tools/verifier_prefixes.py
"""
import json
import io
import os
import re
import sys
import collections

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARTES = os.path.join(RACINE, "data", "cards.json")
SETS = os.path.join(RACINE, "data", "sets_info.json")
REGISTRE = os.path.join(RACINE, "tools", "prefixes_fanmade.json")

# Un card_id officiel : cinq chiffres, plus une lettre de face.
OFFICIEL = re.compile(r"^\d{5}[a-z]?$")
# Un card_id fan-made : deux lettres, trois chiffres, plus une lettre de face.
FANMADE = re.compile(r"^([a-z]{2})\d{3}[a-z]?$")


def lire(chemin):
    return json.load(io.open(chemin, encoding="utf-8", newline=""))


def main():
    defauts = []
    cartes = lire(CARTES)
    registre = lire(REGISTRE)["prefixes"]

    # --- 1. Un card_id en double -------------------------------------------
    vus = collections.defaultdict(list)
    for pack, liste in cartes.items():
        if not isinstance(liste, list):
            continue
        for c in liste:
            if isinstance(c, dict) and c.get("card_id"):
                vus[str(c["card_id"])].append(pack)
    for cid, packs in sorted(vus.items()):
        if len(packs) > 1:
            defauts.append("card_id en double : %r dans %s" % (cid, packs))

    # --- 2 et 3. Les prefixes ----------------------------------------------
    # Les identifiants purement alphabetiques (« minion », « wild »,
    # « aav_traitor_minion ») sont hors format et laisses tranquilles : ils
    # designent des cartes techniques, pas des cartes de collection.
    hors_format = 0
    prefixes_vus = collections.Counter()
    for cid, packs in sorted(vus.items()):
        if OFFICIEL.match(cid):
            continue
        m = FANMADE.match(cid)
        if not m:
            hors_format += 1
            continue
        pref = m.group(1)
        prefixes_vus[pref] += 1
        if pref not in registre:
            defauts.append(
                "prefixe non declare : %r (carte %s, pack %s). "
                "L'ajouter a tools/prefixes_fanmade.json." % (pref, cid, packs[0])
            )

    # Un pack declare fan-made ne doit plus porter de numero.
    packs_fanmade = {v["pack"] for v in registre.values()}
    for pack in sorted(packs_fanmade):
        for c in cartes.get(pack, []):
            if not (isinstance(c, dict) and c.get("card_id")):
                continue
            cid = str(c["card_id"])
            if OFFICIEL.match(cid):
                defauts.append(
                    "card_id fan-made numerote : %s (pack %s). Les numeros sont "
                    "l'espace de FFG ; le fan-made prend deux lettres." % (cid, pack)
                )

    # --- 4. Un numero de set en double -------------------------------------
    sets = lire(SETS)
    numeros = collections.defaultdict(list)
    for cle in sets:
        m = re.match(r"^(\d+)\.", str(cle))
        if m:
            numeros[int(m.group(1))].append(cle)
    for n, cles in sorted(numeros.items()):
        if len(cles) > 1:
            defauts.append("numero de set en double : %d -> %s" % (n, cles))

    # --- Rapport ------------------------------------------------------------
    print("cartes            : %d" % len(vus))
    print("prefixes declares : %d" % len(registre))
    print("cartes fan-made   : %d" % sum(prefixes_vus.values()))
    print("hors format       : %d (identifiants techniques, ignores)" % hors_format)
    non_utilises = sorted(set(registre) - set(prefixes_vus))
    if non_utilises:
        print("prefixes declares mais inutilises : %s" % non_utilises)
    print()
    if defauts:
        print("DEFAUTS : %d" % len(defauts))
        for d in defauts:
            print("  - %s" % d)
        return 1
    print("OK : aucun doublon, aucun prefixe non declare, aucun numero emprunte.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
