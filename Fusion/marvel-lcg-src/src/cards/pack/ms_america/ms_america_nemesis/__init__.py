from cards.pack import *
# Les cartes du set nemesis ont leur PROPRE `from . import *` (ce fichier),
# distinct de celui du pack heros (ms_america/ms_america/__init__.py) : sans
# cet import explicite, toute aide partagee part en NameError (lecon
# iron_lad).
from cards.pack.ms_america.ms_america import (
    NOM_MS_AMERICA, NOM_AMERICA_CHAVEZ, NOM_CATALINA,
    SommeDesModificateurs,
)

# ===========================================================================
# Set nemesis de MS. AMERICA — contenu custom de « jakxin ».
#
# Composition du `nemesis_set` (data/nemesis/ms_america_nemesis.json) :
# ma018 Catalina Chavez (le sbire nemesis), ma019 Search for the Cure
# (manigance annexe), ma020 et ma021 Star Lightning (deux exemplaires
# physiques de la meme trahison) — QUATRE cartes. Le pack fourni par l'auteur
# n'en compte pas cinq, contrairement a un set nemesis officiel : c'est le
# materiel livre, on n'invente pas la cinquieme.
#
# ⚠ ma017 Edges Syndrome n'est PAS ici : c'est l'obligation du set
# `Ms. America`, donc dans ms_america/ms_america/ma017.py, et elle vit dans
# la cle `obligations` du deck de depart.
#
# ---------------------------------------------------------------------------
# LE FIL ROUGE DU SET : LA SŒUR
#
# Catalina Chavez frappe, et les deux Star Lightning la font frapper
# (« Catalina Chavez attacks you. »). Brique exacte du moteur :
# `enemy.DoAttackYou(player, effect, if_no_attack_was_made=...,
# if_this_attack_deals_damage=...)` (enemy.py:74-86), modeles `02040` Tail
# Sweep, `22031` Old Rivals et `pt021` Bulldozing Charge.
#
# ---------------------------------------------------------------------------
# ⚠ ma018 : `HP: "4"` SANS ETOILE, DELIBEREMENT — NE PAS « CORRIGER »
#
# Le scan imprime une etoile sur les TROIS stats. Dans le moteur, l'etoile
# n'a pas le meme sens selon l'attribut : `FormatPlayerNumValue`
# (has_attribute.py:17) transforme un `HP: "4*"` en 4 x nb_joueurs, alors
# qu'un `ATK: "1*"` vaut « 1 degat consecutif » (can_attack.py:47). Sur ce
# pack l'etoile imprimee renvoie a la CAPACITE ETOILEE, pas a un par-joueur —
# le marqueur par-joueur de ce pack est l'icone PERSONNAGE, visible sur
# ma019. D'ou `HP: "4"` nu dans cards.json. Point clos.
#
# ---------------------------------------------------------------------------
# ⚠ ma019 : L'ICONE A ETE VERIFIEE PAR DECOUPE D'IMAGE, NE PAS RE-LITIGER
#
# Contre trois temoins : `ag011` (qui declare Crisis ET Acceleration),
# `hd022` (Hazard, carte-plus NUE) et `hd026` (Acceleration, carte-plus
# SOULIGNEE). C'est la version NUE, donc `Hazard`, et rien d'autre. A vue on
# aurait dit Acceleration. `Hazard` est lu NATIVEMENT dans `desc`
# (`HasHazard`) : aucun module a ecrire pour lui, et coder une capacite
# fantome serait une faute. Fiche : docs/reference/mots-cles/hazard.md.
#
# Idem `Quickstrike "1"` sur ma018 et `Boost` partout : lus nativement.
# Fiches : mots-cles/quickstrike.md, mots-cles/surge.md.
# ===========================================================================

# `NOM_MS_AMERICA` et `NOM_AMERICA_CHAVEZ` sont importes pour rester
# disponibles au set (meme convention que `patriot_nemesis`) ; la cible du
# sbire passe par `desc.Nemesis`, lu nativement.
Unused(NOM_MS_AMERICA, NOM_AMERICA_CHAVEZ)
