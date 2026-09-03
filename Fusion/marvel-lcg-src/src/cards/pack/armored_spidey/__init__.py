from cards.pack import *

# ===========================================================================
# Pack ARMORED SPIDEY — contenu custom de « Kajislav ». Set 152, prefixe `as`.
#
# DEUX sets dans ce pack :
#   - `Armored Spidey`        (as001a-as022, dossier armored_spidey/armored_spidey/)
#   - `Armored Spidey Nemesis`(as023-as026, dossier armored_spidey/armored_spidey_nemesis/)
# 28 card_id : 2 faces d'identite, 2 faces d'amelioration PERMANENTE,
# 11 cartes signature distinctes (16 exemplaires), 1 obligation,
# 6 cartes d'aspect PROTECTION, 2 cartes BASIC, 4 cartes nemesis.
#
# ⚠ `FileManager.CleanName` rend `armored_spidey` et `armored_spidey_nemesis` :
# ce sont bien les noms des deux dossiers de modules, et c'est eux que
# `database.py:197` cherchera (leçon bt019, dont le module n'etait jamais
# charge, en silence).
# ⚠ `set_name` = « Armored Spidey », verifie LIBRE le 03/09/2026 : aucun set
# ni aucune carte officielle ne porte ce nom.
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : UNE ARMURE A DEUX FACES, ET DOUZE CARTES QUI LA LISENT
#
# `as002a/as002b` Spider Armor est une amelioration PERMANENTE RECTO-VERSO,
# posee au Setup par `as001b` avec 3 compteurs `metal` dessus. Elle est le
# centre de gravite du pack :
#
#   POSENT du metal      as002a (3 a chaque retour sur la face OPERATIONAL),
#                        as013 Vibranium Enhancement (1, max 3)
#   EN DEPENSENT         as001a (previent 2 degats), as004 (1 degat a chaque
#                        ennemi par compteur), as006 (etourdit), as007 (2
#                        cartes par compteur), as008 (degat/menace par icone
#                        de boost), as009 (desoriente)
#   LISENT la face       as003 (retourne sur OPERATIONAL), as012 (+1 CTR et
#                        ignore Garde/Patrouille), as013 (Riposte 1 + Stoique)
#   REAGISSENT au retrait as005 Embrace It! (redresse l'identite)
#
# Le dernier compteur retire RETOURNE la carte sur `as002b` DESTROYED, ou le
# heros perd 1 ATQ et 1 DEF jusqu'a ce qu'il paie 3 ressources en forme civile
# (ou defausse as003 Spider-Bot). Depenser du metal est donc toujours un pari.
#
# Trois compteurs MAISON ajoutes a l'enum `COUNTER`
# (src/game/card/face/card_face.py) pour ce pack : `metal` (Spider Armor),
# `sense` (as015 Scarlet Spider), `article` (as019 The Daily Bugle). Sans eux,
# `IsCounter` refuse le nom et la carte tombe des la creation de la partie.
# Deux traits MAISON ajoutes a l'enum `TRAITS` : `OPERATIONAL` et `DESTROYED`,
# les deux faces de l'armure. Un trait maison non declare fait tomber la carte
# a la CONSTRUCTION, pas en jeu.
#
# ---------------------------------------------------------------------------
# ⚠ PREMIER PACK DE LA SERIE A FOURNIR SA DECKLIST. Kajislav donne le deck de
# depart carte par carte, aspect PROTECTION : aucune question d'aspect n'a
# donc ete posee, contrairement a hulk_rainy, lady_sif et iron_man_model_42.
# Les six cartes d'aspect du pack (as015-as020) sont de classe Protection et
# portent le `set_name` « Armored Spidey » (decision de l'utilisateur,
# 03/09/2026) : elles restent donc reperables comme contenu du pack, tout en
# etant jouables par n'importe quel heros de Protection.
#
# ---------------------------------------------------------------------------
# ⚠ HOMONYMES, verifies dans data/cards.json le 03/09/2026 :
#  - « * Scarlet Spider » : `as015` (Protection, ce pack) et `mw022`
#    (pack maison madame_web, AUSSI de classe Protection). Deux cartes
#    DISTINCTES, aux capacites differentes, qui peuvent se retrouver dans le
#    meme deck de Protection. C'est le `set_name` qui les separe.
#  - « * Kingpin » : `as023` (sbire nemesis de ce pack) et le sbire officiel
#    du set Kingpin. `desc.Nemesis` vaut « Peter Parker ».
#  - « * Peter Parker » : l'alter-ego officiel `01001b` et trois allies. Notre
#    face civile porte le meme nom, avec le sous-titre « Earth-31198 » : c'est
#    le `set_name` qui differe.
#  - « * Spider-Verse », « * The Daily Bugle », « Double Defense » : verifies
#    libres.
#
# SET NEMESIS : fourni par l'auteur, 4 cartes (as023-as026), autour de
# Kingpin et de son complot annexe « The Kingpin of Crime ».
# ===========================================================================

# ⚠ Les helpers partages du set vivent dans le `__init__.py` DU SET, pas ici :
# les modules font `from . import *`, qui importe le `__init__` du dossier du
# set. Un helper defini ici leve un NameError avale par le moteur (paye sur
# hk005 le 02/09/2026).
