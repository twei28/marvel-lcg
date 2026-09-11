"""Les faces d'identite CROISEES dans les scans HD, detectees par comparaison.

POURQUOI (11/09/2026, « a la selection de perso, il montre des fois l'alter
ego en grand a la place de la carte heros, par exemple avec Wolverine et
Storm »)
---------------------------------------------------------------------------
Le moteur nomme la face HEROS `NNNNNa` et l'alter ego `NNNNNb`. Les serveurs
d'images, eux, suivent la lettre IMPRIMEE au coin de la carte, et sur dix
identites officielles FFG a imprime l'alter ego en « 1A » : Groot, Rocket
(Galaxy's Most Wanted) et toute la vague X-Men (Colossus, Shadowcat, Cyclops,
Phoenix, Wolverine, Storm, Gambit, Rogue). Pour celles-la, le scan HD
telecharge sous `a` est l'alter ego, et la scene de l'assistant montre Logan
au lieu de Wolverine. Mesure sur les 170 identites : 160 conformes, 10
croisees, distance 0 (le fichier `a` HD EST le scan `b`, au pixel pres).

CE QUE FAIT CE MODULE
---------------------
Il ne connait aucune liste de packs : il COMPARE. Le scan habituel de
`assets/pics/` est la reference (il suit la convention du moteur, verifie a
l'oeil sur Wolverine, Logan et Storm). Pour chaque paire `a`/`b` presente des
deux cotes, on reduit les quatre images en petites empreintes grises ; si le
`a` HD ressemble plus au `b` de reference qu'au `a`, ET reciproquement, les
deux fichiers HD sont echanges. Une liste de packs aurait ete fausse a la
prochaine extension ; une comparaison ne l'est jamais.

⚠ AUCUN IMPORT DU MOTEUR ICI : ce module est aussi charge par
`tools/telecharger_scans_hd.py`, qui tourne sur le serveur a chaque
deploiement, par son chemin de fichier et sans `launch.json`.

Appelants : `tools/telecharger_scans_hd.py` (apres telechargement, et
`--redresser` seul) et `engine/file/cache.py` (`Cache.TelechargerHD`, apres
un telechargement a la demande).
"""
import os
from typing import Iterable, List, Sequence, Tuple

# Petite, mais pas trop : 24x32 garde la silhouette et les bandeaux de la
# carte, et la distance entre deux faces d'une meme identite depasse 20 la
# ou une copie exacte donne 0.
TAILLE_EMPREINTE = (24, 32)
# En dessous, on tient l'image pour identique. Mesure : 0 pour une copie,
# 21 a 36 entre un heros et son alter ego.
SEUIL_IDENTIQUE = 5.0


def empreinte(chemin: str) -> List[int]:
    from PIL import Image
    with Image.open(chemin) as im:
        return list(im.convert("L").resize(TAILLE_EMPREINTE).getdata())


def distance(a: Sequence[int], b: Sequence[int]) -> float:
    return sum(abs(x - y) for x, y in zip(a, b)) / max(1, len(a))


def paires_croisees(dossier_hd: str, dossier_ref: str,
                    identifiants_heros: Iterable[str]) -> List[Tuple[str, str]]:
    """Les paires (a, b) dont les fichiers HD sont croises, sans rien changer.

    `identifiants_heros` : les identifiants de FACE HEROS (« 35001a »). Une
    paire n'est examinee que si ses quatre fichiers existent (a et b, HD et
    reference) : un scan absent n'est ni croise ni conforme, il est ignore.
    """
    croisees: List[Tuple[str, str]] = []
    for a in sorted(set(identifiants_heros)):
        if not a.endswith("a"):
            continue
        b = a[:-1] + "b"
        chemins = [os.path.join(dossier_hd, a + ".jpg"), os.path.join(dossier_hd, b + ".jpg"),
                   os.path.join(dossier_ref, a + ".jpg"), os.path.join(dossier_ref, b + ".jpg")]
        if not all(os.path.exists(c) for c in chemins):
            continue
        hd_a, hd_b, ref_a, ref_b = (empreinte(c) for c in chemins)
        a_est_b = distance(hd_a, ref_b) < distance(hd_a, ref_a)
        b_est_a = distance(hd_b, ref_a) < distance(hd_b, ref_b)
        # Les DEUX sens, sinon ce n'est pas un croisement mais un scan
        # divergent (art alternatif, recadrage), qu'on ne touche pas.
        if a_est_b and b_est_a:
            croisees.append((a, b))
    return croisees


def redresser(dossier_hd: str, dossier_ref: str,
              identifiants_heros: Iterable[str]) -> List[Tuple[str, str]]:
    """Echange les fichiers HD de chaque paire croisee. Rend les paires echangees."""
    echangees = paires_croisees(dossier_hd, dossier_ref, identifiants_heros)
    for a, b in echangees:
        chemin_a, chemin_b = os.path.join(dossier_hd, a + ".jpg"), os.path.join(dossier_hd, b + ".jpg")
        provisoire = os.path.join(dossier_hd, a + ".echange.tmp")
        os.replace(chemin_a, provisoire)
        os.replace(chemin_b, chemin_a)
        os.replace(provisoire, chemin_b)
    return echangees


def identifiants_heros_de(cartes_json: str) -> List[str]:
    """Les faces heros officielles (« NNNNNa ») lues dans cards.json."""
    import json
    import re
    officiel = re.compile(r"^\d{5}a$")
    with open(cartes_json, encoding="utf-8") as f:
        packs = json.load(f)
    vus = set()
    for cartes in packs.values():
        if not isinstance(cartes, list):
            continue
        for carte in cartes:
            if not isinstance(carte, dict) or carte.get("type") != "Hero":
                continue
            pic = str(carte.get("pic_id") or carte.get("card_id") or "")
            if officiel.match(pic):
                vus.add(pic)
    return sorted(vus)
