"""Les parties en cours (bandeau « Continuer la partie ») : garde, purge, reprise sans doublon, fin de partie.

    python3 tools/test_en_cours.py        (depuis Fusion/marvel-lcg-src, sans moteur ni reseau)

Ce que ce test couvre : la logique de `src/engine/en_cours.py` sur un dossier temporaire. La sauvegarde de la vraie scene et les
routes `/en_cours_*` sont prouvees en jeu (ui-check, 18/11/2026) : liste, reprise sans doublon, suppression a la fin de partie.
"""
import json
import os
import sys
import tempfile
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))
from engine import en_cours  # noqa: E402

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom + ("" if condition else " | " + str(detail)))
    if not condition:
        echecs.append(nom)


tmp = tempfile.mkdtemp(prefix="en-cours-")
en_cours.dossier = lambda: tmp  # type: ignore[assignment]


def ecrire(nom, graine, age=0):
    chemin = os.path.join(tmp, nom + ".json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump({"metadata": {"seed": graine}}, f)
    t = time.time() - age
    os.utime(chemin, (t, t))
    return chemin


# 1. La commentaire porte la manche ; sans lui, zero.
verifier("manche et phase relues du commentaire", en_cours.manche_et_phase("en-cours|4|Player 1 Turn") == {"round": 4, "phase": "Player 1 Turn"})
verifier("un commentaire etranger ne donne rien", en_cours.manche_et_phase("autre chose") == {"round": 0, "phase": ""})

# 2. Cinq gardees, la plus recente d'abord.
for i in range(7):
    ecrire(f"p{i}", 1000 + i, age=100 - i * 10)
liste = en_cours.fichiers()
verifier("la liste ne rend que 5 parties", len(liste) == 5, len(liste))
verifier("la plus recente est en tete", os.path.basename(liste[0]) == "p6.json", liste[:1])
en_cours._purger()
verifier("la purge supprime les plus anciennes", sorted(os.listdir(tmp)) == [f"p{i}.json" for i in range(2, 7)], sorted(os.listdir(tmp)))

# 3. Reprise sans doublon : le fichier repris part quand la meme partie (meme graine) se sauvegarde sous un autre nom.
verifier("on ne reprend pas un fichier hors liste", en_cours.noter_reprise("/ailleurs/x.json") is False)
repris = os.path.join(tmp, "p3.json")
verifier("on retient le fichier repris", en_cours.noter_reprise(repris) is True)
nouveau = ecrire("p3-bis", 1003)  # la partie reprise, rangee sous un nouvel identifiant
en_cours.remplacer_reprise(nouveau)
verifier("l'ancienne entree de la partie reprise a disparu", not os.path.exists(repris))
verifier("la nouvelle entree reste", os.path.exists(nouveau))

# 4. Fin de partie : sa propre entree part ; celle d'une AUTRE partie reprise ne bouge pas.
ancien = os.path.join(tmp, "p5.json")
en_cours.noter_reprise(ancien)
en_cours.supprimer("p4", graine=999999)           # une autre partie finit
verifier("l'entree de la partie finie est retiree", not os.path.exists(os.path.join(tmp, "p4.json")))
verifier("une autre partie reprise n'est pas touchee", os.path.exists(ancien))
en_cours.supprimer("zz", graine=1005)              # la partie reprise finit avant son premier rangement
verifier("la partie reprise qui finit emporte son fichier d'origine", not os.path.exists(ancien))

print("\nBILAN :", "tout est vert" if not echecs else f"{len(echecs)} echec(s)")
sys.exit(1 if echecs else 0)
