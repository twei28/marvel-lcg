from . import *

# Zombie Colossus — METAZOMBIE (Fallen Heroes, modulaire du scenario The Hunger Core). X-MEN. SCH 0. ATK 3.
# PV 7. Guard. Toughness. Boost 3.
# Guard. Toughness.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[guard]] (mots-cles/guard.md) : BASE NATIVE, `desc.Guard` = "1". Aucun script requis.
# - [[toughness]] (mots-cles/toughness.md) : BASE NATIVE, `desc.Toughness` = "1" (verifie dans
#   `data/cards_custom.json`, hg069 porte bien la cle). Lu directement par le moteur
#   (`HasToughness`/`CanStatus`, `can_status.py`) : la carte entre en jeu avec une carte Tough, sans que le
#   script n'ait besoin de la poser lui-meme.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Carte « Guard. Toughness. » pure, sans aucune autre phrase imprimee : modele exact `cd017` Inner Demon
#   (meme texte imprime mot pour mot, `data/cards.json` : `"text": "Guard. Toughness."`), carte OFFICIELLE
#   dont AUCUN fichier `.py` n'existe dans tout le depot (`find src/cards -iname "cd017.py"` : aucun resultat)
#   -- confirmation directe que ces deux mots-cles, pris seuls sans texte imprime supplementaire, ne requierent
#   structurellement RIEN cote script : `database.py` (`CardsDB.FindAbilities`) renvoie `GetAbilities() -> []`
#   par defaut pour toute carte sans module, et c'est exactement le comportement vise ici.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Guard. Toughness. » -> les DEUX mots-cles sont des bases automatiques lues depuis `desc` (PROCESSUS-CARTE
#   §3 : « Toughness et Restricted sont lus par le moteur directement dans desc, aucun module n'est
#   necessaire pour eux » -- Guard suit la meme regle, confirme par `cd017` ci-dessus et par hg059/hg061/
#   hg062/hg063 du meme set Fallen Heroes qui ne codent ni l'un ni l'autre). Aucune ligne de texte restante a
#   coder sur cette carte : le fichier existe pour la tracabilite du processus (etapes 1-6), mais
#   `GetAbilities()` est intentionnellement vide.
#
# Bloc nombres texte <-> code : aucune valeur numerique a verifier en dehors de `desc` (SCH 0 / ATK 3 / PV 7 /
#   Guard 1 / Toughness 1 / Boost 3), toutes deja conformes a `data/cards_custom.json` ; aucune valeur
#   numerique dans ce script puisqu'il n'y a aucune capacite a coder.


def GetAbilities() -> Sequence['Ability']:

    return []
