from cards.pack import *

# ===========================================================================
# Pack ALOPEX (Tortues Ninja) — contenu custom de « Inkwire » (TMNT Heroes,
# zip « Alopex v3 »). Prefixe `ta`, set 183.
#
# DEUX sets dans ce pack :
#   - `Alopex`          (ta001a-ta012, dossier alopex/alopex/)
#   - `Alopex Nemesis`  (ta013-ta015, dossier alopex/alopex_nemesis/)
# 16 card_id : 2 faces d'identite, 9 cartes signature distinctes en 15
# exemplaires, Prey (16e carte du deck, mise de cote au Setup), 1 obligation,
# 3 cartes nemesis distinctes en 5 exemplaires (Curse of Nine Tales x3).
#
# ⚠ `FileManager.CleanName` rend `alopex` et `alopex_nemesis` : ce sont les
# noms des deux dossiers de modules (lecon bt019).
#
# LE PACK EN UNE PHRASE : UNE PROIE, ET TOUT LE KIT S'EN NOURRIT.
#   ta001a (Matagi) attache `Prey` (ta011) a l'ennemi qu'elle attaque ou a la
#   manigance qu'elle contre ; Prey donne +1 degat / +1 menace retiree et
#   REVIENT de cote quand elle quitte le jeu ; ta002 / ta008 / ta009 y
#   reagissent ; ta010 (Other Kama) et ta009 (Kama) accordent leur capacite a
#   toute amelioration [[KAMA]].
#
# ⚠ BASES AUTOMATIQUES (aucun script) : `Restricted` (ta009, ta010), `Boost`,
#   `Hazard 1` (ta013), `Acceleration 2` (ta012), `StartingThreat 2*` (ta013),
#   `Nemesis` (ta014), `GiveTo` (ta012).
# ⚠ MOTS-CLES MAISON : « Cloak » (ta001..: pose la carte d'etat Cloaked, fiche
#   mots-cles/cloak.md) et « Daze » (pose la carte d'etat Dazed, fiches
#   mots-cles/daze.md et dazed.md).
# ===========================================================================
