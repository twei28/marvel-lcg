from . import *

# Zombie Luke Cage — METAZOMBIE (Fallen Heroes, modulaire). DEFENDER. SCH 1. ATK 2. HP 6.
# Guard. Toughness.
#
# Cartes de reference :
#  - « Guard » (mot-cle officiel, fiche mots-cles/guard.md) : cle native `desc.Guard` (`"Guard": "1"` dans
#    `data/cards_custom.json`), lue par `HasGuard` (`has_guard.py`) et appliquee par
#    `Villain.CanBeAttackBy()` -- AUCUN script requis, modele `01101` Hydra Mercenary (meme mot-cle seul,
#    pas de fichier `.py`).
#  - « Toughness » (mot-cle officiel, fiche mots-cles/toughness.md) : cle native `desc.Toughness`
#    (`"Toughness": "1"`), lue par `HasToughness` (`has_toughness.py`), pose le statut Tough a l'entree en
#    jeu -- AUCUN script requis, modele `01076` * Luke Cage (meme mot-cle seul, pas de fichier `.py`).
#
# ⚠ Mots-pieges :
#  - Les DEUX mots-cles imprimes sur cette carte sont des « bases automatiques » du guide
#    (PROCESSUS-CARTE.md, fin de l'etape 5) : rien dans `data/cards.json`/`cards_custom.json` au-dela des
#    cles `Guard`/`Toughness` deja renseignees, rien a coder en script.
#  - Aucune autre ligne de texte sur la carte (pas de « When Revealed », pas de capacite annexe) : a la
#    difference de `11041` Deathunt 9000 (Villainous + capacite [star] Boost propre), rien ne justifie un
#    fichier non vide ici.
#  - Trait METAZOMBIE verifie DIRECTEMENT dans `data/cards_custom.json` (`"traits": ["METAZOMBIE",
#    "DEFENDER"]`), pas suppose : cette carte est un Minion (pas un Villain comme hg007-hg015, le Horde
#    deck) qui porte NEANMOINS le trait METAZOMBIE -- voir la note de synthese du rapport sur la portee de
#    `commun.Metazombies()` (qui ne liste QUE les Villain) et sur hg064, qui en depend.
#
# Bloc nombres texte <-> code : SCH 1 / ATK 2 / HP 6 / Guard 1 / Toughness 1 -> tous dans `desc` de
# `data/cards_custom.json`, aucune valeur numerique dans ce script (il n'y en a pas a coder).


def GetAbilities() -> Sequence['Ability']:

    return []
