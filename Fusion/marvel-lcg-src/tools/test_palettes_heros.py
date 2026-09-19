"""Les corrections de palettes se posent PAR-DESSUS le relevé généré.

`outils/palettes-heros.py` réécrit `data/palettes-heros.json` en entier à
chaque passe : une couleur corrigée à la main dedans serait effacée à la
première régénération. Elle vit donc dans un fichier à part, et c'est ce
recouvrement que ce test tient.

La garde de l'écriture (403 pour qui n'est pas l'administrateur du site, assis
au siège 0) n'est pas rejouée ici : `/save_palette_heros` emprunte la même
`_est_administrateur` que `/save_images_cartes`, déjà en place.

Usage: RELEASE=1 python3.10 tools/test_palettes_heros.py
"""
import json
import os
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))
os.environ.setdefault("RELEASE", "1")

from cards.palettes_heros import (  # noqa: E402
    PALETTES_CORRECTIONS_FILE, PALETTES_HEROS_FILE, PalettesHeros)

ROUGE = [140, 41, 31]
BLEU = [32, 43, 114]
BLANC = [219, 220, 222]
VERT = [30, 163, 83]

echecs = []


def verifier(nom, condition, detail=""):
    if condition:
        print(f"  ok   {nom}")
    else:
        print(f"  ECHEC {nom} : {detail}")
        echecs.append(nom)


def ecrire(chemin, palettes):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump({"version": 1, "palettes": palettes}, f)


def main():
    with tempfile.TemporaryDirectory() as dossier:
        genere = os.path.join(dossier, "palettes-heros.json")
        corrections = os.path.join(dossier, "corrections.json")
        PALETTES_HEROS_FILE.value = genere
        PALETTES_CORRECTIONS_FILE.value = corrections

        ecrire(genere, {"01001a": [ROUGE, BLEU, BLANC], "01001b": [ROUGE, BLEU, BLANC],
                        "dd001a": [VERT]})

        # 1. Sans corrections, le relevé généré passe tel quel.
        PalettesHeros.Recharger()
        toutes = PalettesHeros.Toutes()
        verifier("sans correction, le relevé généré passe tel quel",
                 toutes.get("01001a") == [ROUGE, BLEU, BLANC], toutes.get("01001a"))
        verifier("sans correction, la liste des corrections est vide",
                 PalettesHeros.Corrections() == {}, PalettesHeros.Corrections())

        # 2. Une correction RECOUVRE la couleur générée, pour cette carte seule.
        ecrire(corrections, {"01001a": [VERT], "01001b": [VERT]})
        PalettesHeros.Recharger()
        toutes = PalettesHeros.Toutes()
        verifier("la correction recouvre la couleur générée",
                 toutes.get("01001a") == [VERT], toutes.get("01001a"))
        verifier("les deux faces suivent",
                 toutes.get("01001b") == [VERT], toutes.get("01001b"))
        verifier("une identité non corrigée n'est pas touchée",
                 toutes.get("dd001a") == [VERT] and toutes["dd001a"] is not toutes["01001a"],
                 toutes.get("dd001a"))
        verifier("le relevé GÉNÉRÉ reste lisible à part",
                 PalettesHeros.Generees().get("01001a") == [ROUGE, BLEU, BLANC],
                 PalettesHeros.Generees().get("01001a"))
        verifier("les corrections se lisent seules",
                 PalettesHeros.Corrections() == {"01001a": [VERT], "01001b": [VERT]},
                 PalettesHeros.Corrections())

        # 3. Une REGÉNÉRATION du relevé n'efface pas les corrections. C'est
        #    toute la raison d'être du fichier séparé.
        ecrire(genere, {"01001a": [BLEU], "01001b": [BLEU], "dd001a": [VERT]})
        PalettesHeros.Recharger()
        toutes = PalettesHeros.Toutes()
        verifier("une régénération n'efface pas la correction",
                 toutes.get("01001a") == [VERT], toutes.get("01001a"))
        verifier("une régénération est vue là où rien n'est corrigé",
                 toutes.get("dd001a") == [VERT], toutes.get("dd001a"))

        # 4. Fichier de corrections absent = aucune correction, jamais d'erreur.
        os.remove(corrections)
        PalettesHeros.Recharger()
        verifier("corrections absentes : le relevé généré suffit",
                 PalettesHeros.Toutes().get("01001a") == [BLEU],
                 PalettesHeros.Toutes().get("01001a"))

        # 5. Fichier abîmé : on ne casse pas la table pour une couleur.
        with open(corrections, "w", encoding="utf-8") as f:
            f.write("{ ceci n'est pas du JSON")
        PalettesHeros.Recharger()
        verifier("corrections illisibles : aucune teinte corrigée, aucune erreur",
                 PalettesHeros.Toutes().get("01001a") == [BLEU],
                 PalettesHeros.Toutes().get("01001a"))

        # 6. Une couleur mal formée dans le fichier est ignorée, pas propagée.
        ecrire(corrections, {"01001a": [[1, 2], [3, 4, 5]], "01001b": "pas une liste"})
        PalettesHeros.Recharger()
        toutes = PalettesHeros.Toutes()
        verifier("une couleur mal formée est ignorée",
                 toutes.get("01001a") == [[3, 4, 5]], toutes.get("01001a"))
        verifier("une entrée qui n'est pas une liste est ignorée",
                 toutes.get("01001b") == [BLEU], toutes.get("01001b"))

    print()
    if echecs:
        print(f"BILAN : {len(echecs)} echec(s) — " + " ; ".join(echecs))
        return 1
    print("BILAN : tout est vert")
    return 0


if __name__ == "__main__":
    sys.exit(main())
