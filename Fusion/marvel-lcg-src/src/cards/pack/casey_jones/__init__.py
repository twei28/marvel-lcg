from cards.pack import *

# ===========================================================================
# Pack CASEY JONES (TMNT Heroes v3, auteur Inkwire). Prefixe `tc`.
#
# DEUX sets dans ce pack :
#   - `Casey Jones`          (tc001a-tc014, dossier casey_jones/casey_jones/)
#   - `Casey Jones Nemesis`  (tc015-tc017, dossier casey_jones/casey_jones_nemesis/)
# 18 card_id : 2 faces d'identite, 12 cartes signature distinctes (16
# exemplaires), 1 obligation, 3 cartes nemesis distinctes (5 exemplaires,
# Purple Dragon Goons x3).
#
# ⚠ `FileManager.CleanName` rend `casey_jones` et `casey_jones_nemesis` : ce
# sont les noms des deux dossiers de modules (lecon bt019).
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : CINQ ARMES (WEAPON, Restricted) ET UN SAC.
#   tc001a  Overswing : defausse une arme Restricted -> 3 ressources WILD, pour
#           un evenement ATTACK / THWART / DEFENSE (une fois par phase) ;
#   tc001b  Setup : le Sac (tc013) entre en jeu ; Response : ramene une arme ;
#   tc013   Casey's Bag : on peut JOUER les cartes rangees dessous (« tuck »,
#           mots-cles/tuck.md), et le Sac range la plus basse arme de la
#           defausse ;
#   tc006   Anything Goes : echange une arme en jeu et une arme rangee ;
#   tc002   Clap Back : confond un ennemi si une arme de Casey a ete defaussee
#           pour le payer (donc par Overswing).
#
# ⚠ BASES AUTOMATIQUES, AUCUN SCRIPT POUR ELLES (desc) : `Restricted` (tc007,
# tc009-tc012), `Permanent` (tc013), `Requirement` (tc005), `Toughness` (tc016),
# `Guard` / `Patrol` (tc017), `Incite` et `Crisis` (tc015), `Boost` (icones).
# Les recoder ferait doubler leur effet.
#
# ⚠ HOMONYME : « Casey Jones » est AUSSI l'allie unique de Raphael (`tr002`,
# pack raphael). Aucun module du pack ne cherche par le NOM ; le filtre est le
# type (Hero/AlterEgo/identite), le card_id ou l'ensemble. Voir
# `deck/starter/casey_jones.json` (`collision_note`).
#
# ⚠ Traits : tous deja au depot (VIGILANTE, CIVILIAN, WEAPON, ARMOR, ITEM,
# SKILL, BRUTE) sauf PURPLE DRAGONS (nom propre, laisse en anglais). Aucun
# fichier moteur partage n'est touche par ce pack.
#
# ⚠ NOMS DE CARTES UNIQUES : s'ecrivent SANS l'etoile dans `CardFinder(name=...)`
# (RECETTES-MOTEUR §6) ; ce pack n'en a pas besoin.
# ===========================================================================
