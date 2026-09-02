from cards.pack import *

# ===========================================================================
# Pack HULK — contenu custom de « Rainy ». Set 148, prefixe `hk`.
#
# Bruce Banner et son autre lui. Un seul set, `Hulk (Rainy)`
# (hk001a-hk013, dossier hulk_rainy/hulk_rainy/). 14 card_id : 2 faces
# d'identite, 11 cartes signature distinctes en 15 exemplaires, 1 obligation.
#
# ⚠ `set_name` = « Hulk (Rainy) », et surtout PAS « Hulk » : ce nom est pris
# par le heros OFFICIEL 10001a, et `IsDeckBuildingClass` compare les
# `set_name` litteralement (leçon `wolverine_x23`). Modele du nommage :
# « Thor (Jane Foster) », deja dans le depot pour la meme raison.
# ⚠ `FileManager.CleanName("Hulk (Rainy)")` rend `hulk_rainy` : c'est bien le
# nom du dossier de modules, et c'est ce dossier-la que `database.py:197`
# cherchera. Verifie avant d'ecrire une ligne (leçon bt019, dont le module
# n'etait jamais charge, en silence).
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : ENCAISSER PAIE, ET LA COULEUR DU PAIEMENT COMPTE
#
#   hk001a Anger          -> chaque degat subi rend 1 degat
#   hk006 Reckless Charge -> se blesser pour frapper plus fort
#   hk005 Interception    -> encaisser 2 pour annuler une traitrise
#   hk010 Intimidating Roar -> etre frappe retire de la menace
#
# CTR 0 en forme heros : la menee passe entierement par Bruce Banner
# (hk003 Brilliant Mind, Alter-Ego Action) et par hk009 The Other Guy, qui
# recompense chaque changement de forme.
#
# ---------------------------------------------------------------------------
# LA PROVENANCE DU PAIEMENT, TROIS TOURNURES DISTINCTES
#
# Rien de neuf a construire : le moteur sait deja tout faire, et 306 cartes
# officielles portent ce genre de phrase.
#
#   « using ONLY [mental] »       -> `effect.GetPaidResources().OnlyHasColor("B")`
#                                    hk003, modele 10004 Sub-Orbital Leap
#   « using A [physical] »        -> `effect.GetPaidResources().HasColor("R")`
#                                    hk006, modele 01053 Relentless Assault
#   « OVERPAID with [energy] or
#     [physical] »                -> `SurpaiementEnergieOuPhysique` ci-dessous
#                                    hk005, modele 58005 Starstruck
#
# Les trois se ressemblent et ne veulent PAS dire la meme chose : « only »
# exige que TOUT le paiement soit de cette couleur, « a » qu'au moins une
# ressource le soit, « overpaid » que la couleur ait servi AU-DELA du cout
# imprime.
#
# ---------------------------------------------------------------------------
# ⚠ HOMONYMES PREEXISTANTS, verifies dans data/cards.json le 02/09/2026 :
#  - « Hulk Smash » (hk004) : 10003, carte signature du HULK OFFICIEL
#    (desc.Class = "Hero", set_name « Hulk ») ;
#  - « Limitless Strength » (hk012) : 10007, idem — et c'est une RESSOURCE
#    la-bas, une amelioration ici ;
#  - « Hulk » : le heros officiel 10001a, l'allie 01050, le sbire th014,
#    l'allie 62020 ;
#  - « Bruce Banner » : l'alter-ego officiel 10001b ;
#  - « Black Widow » (hk002) : six homonymes, dont l'allie officiel 01075 —
#    stats DIFFERENTES, ce sont deux cartes distinctes de meme nom.
# Les deux premiers sont de classe « Hero » et appartiennent a un AUTRE
# heros : le controle « jamais une signature d'un autre heros dans un deck »
# (PROCESSUS-HEROS etape 10) doit rester vert, et le deck de depart le
# documente dans son `collision_note`.
#
# ---------------------------------------------------------------------------
# SET NEMESIS : le zip n'en fournit AUCUN — son dossier s'appelle pourtant
# « Nemesis & Obligation » et ne contient que l'obligation. Sur decision de
# l'utilisateur (02/09/2026), le deck emprunte le set nemesis du HULK
# OFFICIEL : 10026 * Abomination, 10027 Total Destruction, 10028 Clash of the
# Titans x3.
# ⚠ Cet emprunt n'etait PAS jouable avant le correctif moteur du meme jour :
# `IsNemesis` comparait des noms de set, et « Hulk Nemesis » ne correspond pas
# a « Hulk (Rainy) » — `01190` Shadow of the Past n'aurait jamais mis
# Abomination en jeu. Les cartes du `nemesis_set` sont desormais MARQUEES a la
# mise en place avec leur joueur (player_setup.py, etape 5).
# ===========================================================================

# ⚠ Les helpers partages du set vivent dans `hulk_rainy/hulk_rainy/__init__.py`,
# PAS ici : les modules de cartes font `from . import *`, qui importe le
# `__init__` du SET (dossier du `set_name` nettoye), jamais celui du pack.
# Paye le 02/09/2026 : `SurpaiementEnergieOuPhysique` defini ici levait un
# `NameError` avale par le moteur, et hk005 Interception annulait bien la
# traitrise mais ne retirait JAMAIS ses 2 menaces. Seul son cas de test l'a vu.
