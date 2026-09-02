from cards.pack import *

# ===========================================================================
# Pack VIV VISION — contenu custom de « Rainy ». Set 147, prefixe `vv`.
#
# Vivian, la fille synthezoide de Vision, membre des Champions. Un seul set,
# `Viv Vision` (vv001a-vv011, dossier viv_vision/viv_vision/). 12 card_id :
# 2 faces d'identite, 9 cartes signature distinctes en 15 exemplaires, et
# 1 obligation.
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : L'ENERGIE EST LA MONNAIE, LE MOT-CLE `Requirement`
# EST LE MOTEUR
#
#   vv001a Density Manipulation -> 1 energie -> +2 a un pouvoir de base
#   vv001b Recharge             -> repeche une carte a ENERGIE IMPRIMEE
#   vv008 Computer Mind         -> pioche autant que le `Requirement` paye
#   vv010 Viv's Solar Gem       -> genere de l'energie, se redresse chaque
#                                  fin de phase du vilain
#   vv002/vv004/vv005/vv009     -> portent `Requirement`, donc nourrissent
#                                  vv008 a chaque fois
#
# Stats volontairement basses (THW 1 / ATK 1 / DEF 1, 10 PV, REC 3) : tout le
# kit existe pour les compenser.
#
# ---------------------------------------------------------------------------
# ⚠ DEUX POINTS QUE LE ZIP NE TRANCHE PAS, ARBITRES PAR L'UTILISATEUR LE
# 02/09/2026 (questions posees AVANT d'ecrire la premiere ligne) :
#
#  1. Le mot-cle maison **`breakthrough`** (vv003 Just a Phase) n'est defini
#     nulle part : le zip ne contient aucun insert de regles, contrairement
#     au pack Spider-Man 2099 du meme auteur qui definit son mot-cle `Seek`
#     noir sur blanc. Definition retenue puis confirmee par la liste
#     communautaire « Marvel Champions Home Brew Master List » : le miroir
#     d'`overkill`, valable pour les degats ET pour la menace. Fiche
#     complete : docs/reference/mots-cles/breakthrough.md.
#
#  2. Le pack n'a **AUCUNE carte nemesis**. La critique BGG du pack rapporte
#     que Rainy recommande le modulaire officiel **Zzzax** (Ironheart,
#     29036-29040) a cette place : c'est exactement la forme d'un set nemesis
#     (1 sbire + 1 manigance + 3 cartes), et son theme — attaquer les
#     ressources energie — mord precisement sur l'economie de Viv. C'est donc
#     lui qui remplit `nemesis_set` dans deck/starter/viv_vision.json.
#     ⚠ Consequence a connaitre : si le joueur choisit AUSSI Zzzax comme
#     modulaire du scenario, les cinq cartes existent en double.
#
# Le sous-dossier « Vivian alt cards » du zip a ete ECARTE (decision du
# 02/09/2026). Ce n'est pas de l'art alternatif malgre son nom : l'illustration
# est identique et c'est le TEXTE qui change (identite renommee « Vivian »,
# trait CIVILIAN ajoute a l'alter-ego, et surtout limite « once per POWER per
# round » au lieu de « once per round », soit trois activations au lieu d'une).
# Une variante de regles se declarerait en `metadata.hero_alts` (§5.3 du
# GUIDE-CREATION-CONTENU, precedent The Thing Guardian), pas ici.
#
# ---------------------------------------------------------------------------
# ⚠ HOMONYMES PREEXISTANTS, verifies dans data/cards.json le 02/09/2026 :
#  - « Solar Beam » (vv005) : 26008, carte signature du VISION officiel
#    (desc.Class = "Hero", set_name « Vision »), plus la traitrise 57051 ;
#  - « Superdense Strike » (vv006) : 26009, idem cote Vision, plus 57052 ;
#  - « Grounded » (vv011) : obligation 47023 (Jubilee) et environnement wd041
#    (Electro) — aucun risque fonctionnel, les trois sont dans des sets
#    differents ;
#  - « Viv's Solar Gem » (vv010) : a ne pas confondre avec « * Solar Gem »
#    57047, attachement du scenario Synthezoid qui vise le Vision officiel.
# Les deux premiers sont des cartes de classe « Hero » appartenant a un AUTRE
# heros : le controle « jamais une signature d'un autre heros dans un deck »
# (PROCESSUS-HEROS etape 10) doit rester vert, et le deck de depart le
# documente dans son `collision_note`.
#
# `set_name` retenu : « Viv Vision », verifie libre — « Vision » est pris par
# le heros officiel 26001a, et `IsDeckBuildingClass` compare les `set_name`
# litteralement.
# ===========================================================================
