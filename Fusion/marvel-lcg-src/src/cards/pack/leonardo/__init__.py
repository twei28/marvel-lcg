from cards.pack import *

# ===========================================================================
# Pack LEONARDO (Tortues Ninja) — contenu custom de « Inkwire » (TMNT Heroes).
# Prefixe `tl`, set 164. PHASE A (construction) : AUCUNE carte validee.
#
# DEUX sets dans ce pack :
#   - `Leonardo`          (tl001a-tl013, dossier leonardo/leonardo/)
#   - `Leonardo Nemesis`  (tl014-tl016, dossier leonardo/leonardo_nemesis/)
# 17 card_id : 2 faces d'identite, 11 cartes signature distinctes en 15
# exemplaires, 1 obligation, 3 cartes nemesis distinctes en 5 exemplaires
# (Foot Soldiers x3).
#
# ⚠ `FileManager.CleanName` rend `leonardo` et `leonardo_nemesis` : ce sont
# les noms des deux dossiers de modules (lecon bt019).
#
# LE PACK EN UNE PHRASE : DEUX KATANA, ET TOUT LE KIT LES INCLINE / REDRESSE.
#   tl011 / tl012 sont les seules cartes [[KATANA]] ; elles sont Restricted ;
#   tl001b (Leo) les met en jeu inclinees ; tl001a, tl004, tl005, tl008,
#   tl009, tl010 les redressent ou les inclinent ; tl011 en fait des sources de
#   ressource.
#
# ⚠ BASES AUTOMATIQUES (aucun script) : `Restricted` (tl011, tl012) via
#   `desc.Restricted`.
# ⚠ MOT-CLE MAISON : « Cloak » (tl015, tl016) = poser la carte d'etat Cloaked —
#   voir docs/reference/mots-cles/cloak.md, cloaked.md et
#   `leonardo_nemesis/__init__.py`.
# ===========================================================================
