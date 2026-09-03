from cards.pack import *

# ===========================================================================
# Pack IRON MAN (MODEL 42) — contenu custom de « Rainy ». Set 151, prefixe `im`.
#
# Un seul set, `Iron Man (Model 42)` (im001a-im014, dossier
# iron_man_model_42/iron_man_model_42/). 15 card_id : 2 faces d'identite,
# 12 cartes signature distinctes en 15 exemplaires, 1 obligation.
#
# ⚠ `set_name` = « Iron Man (Model 42) », et surtout PAS « Iron Man » : ce nom
# est pris par le heros OFFICIEL 01029a, et « Superior Iron Man » par le pack
# maison `si`. `IsDeckBuildingClass` compare les set_name litteralement
# (leçon wolverine_x23). `FileManager.CleanName` rend `iron_man_model_42` :
# c'est le nom du dossier, verifie avant d'ecrire une ligne (leçon bt019).
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : UN COMPTEUR, ET DIX CARTES QUI LE LISENT
#
# `reactor` est un compteur MAISON, ajoute a l'enum `COUNTER`
# (src/game/card/face/card_face.py) pour ce pack : sans lui, `IsCounter`
# refuse le nom et toute carte qui en pose tombe des la creation de la partie.
#
#   POSENT des compteurs        im001a Reactor Cores (X ressources energie
#                               IMPRIMEES), im004 Take Flight (si deja AERIAL),
#                               im006 Tony's Workshop, im009 Repulsor Core One
#   EN DEPENSENT                im002 (+3 degats), im003 (+3 menaces),
#                               im007 (previent 2), im008 (+2 degats),
#                               im009 (redresse), im013 (+2 menaces, ignore
#                               Patrouille), im011 (annule une traitrise),
#                               im014 l'obligation (en retire 2 de force)
#
# 10 PV seulement : le compteur est la ressource centrale ET la reserve de
# survie, et l'obligation vient piocher dedans.
#
# ---------------------------------------------------------------------------
# ⚠ « SPEND X **PRINTED** [energy] RESOURCES » (im001a). ARBITRAGE DE
# L'UTILISATEUR (03/09/2026) : lecture LITTERALE. Seules les cartes dont
# l'icone IMPRIMEE est [energy] chargent le reacteur. Une ressource GENEREE
# n'y donne pas droit — im005 Stark Tower, qui genere un wild, ne peut donc
# PAS charger le reacteur, ni 01088 Energy qui en genere deux.
# Le moteur sait lire ca nativement, et deux chemins existent :
#   - `FacesCounter.GetPrintedResourcesCount(faces, "Y")` (modele 01174
#     Electromagnetic Backlash, 23013 * Captain Marvel) ;
#   - le selecteur `SetTarget(has_printed_res="Y", ...)` (modele 29038
#     Haywire).
#
# ---------------------------------------------------------------------------
# ⚠ LE TRAIT AERIAL EST LA SECONDE BOUCLE. im010 Rocket Boots le donne en
# permanence, im004 Take Flight pour le round. Il debloque la REPARTITION
# LIBRE des degats (im002) et de la menace (im003), et rend im004 auto-nourri.
#
# ---------------------------------------------------------------------------
# ⚠ im011 Save The Day et im012 Hulkbuster Armor portent TOUTES DEUX le
# numero imprime 14/15 : l'auteur donne la seconde comme « alternative
# replacement » de la premiere. Ce n'est PAS un cumul, c'est un choix de
# deckbuilding. Decision de l'utilisateur (03/09/2026) : les DEUX cartes
# existent, avec deux card_id distincts, et c'est im011 qui part dans le deck
# de depart livre.
#
# ---------------------------------------------------------------------------
# ⚠ HOMONYMES, verifies dans data/cards.json le 03/09/2026 :
#  - « Iron Man » : le heros OFFICIEL 01029a, l'allie 09039, le sbire de
#    plusieurs sets. Notre face heros porte le meme nom : c'est le set_name
#    qui differe, et le controle de PROCESSUS-HEROS etape 10 doit rester vert ;
#  - « Tony Stark » : l'alter-ego officiel 01029b, et `si016` * Tony Stark
#    A.I., sbire nemesis du pack maison superior_iron_man — dont le
#    `desc.Nemesis` vaut justement « Tony Stark ».
#
# SET NEMESIS : le zip n'en fournit aucun. Sur decision de l'utilisateur
# (03/09/2026), le deck emprunte celui de l'IRON MAN OFFICIEL : 01171 Imminent
# Overload, 01172 * Whiplash, 01173 Electric Whip Attack x2, 01174
# Electromagnetic Backlash. Emprunt rendu jouable par le correctif `IsNemesis`
# du 02/09 (commit 89b9a45).
# ===========================================================================

# ⚠ Les helpers partages du set vivent dans le `__init__.py` DU SET, pas ici :
# les modules font `from . import *`, qui importe le `__init__` du dossier du
# set. Un helper defini ici leve un NameError avale par le moteur (paye sur
# hk005 le 02/09/2026).
