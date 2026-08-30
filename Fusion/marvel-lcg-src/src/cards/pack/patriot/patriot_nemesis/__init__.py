from cards.pack import *
# Les cartes du set nemesis ont leur PROPRE `from . import *` (ce fichier),
# distinct de celui du pack heros (patriot/patriot/__init__.py) : sans cet
# import explicite, toute aide partagee part en NameError (lecon iron_lad).
from cards.pack.patriot.patriot import (
    NOM_PATRIOT, NOM_ELIJAH, NOM_MR_HYDE, NOM_MGH_DRUG,
)

# ===========================================================================
# Set nemesis de PATRIOT — contenu custom de CptScorp.
#
# Composition du `nemesis_set` (data/nemesis/patriot_nemesis.json) : pt018
# Mr. Hyde's Lab (manigance annexe), pt019 Mr. Hyde (le sbire nemesis,
# Toughness 1 + ELITE), pt020 MGH Drug (attachement), pt021 et pt022
# Bulldozing Charge (deux exemplaires physiques de la meme trahison) — CINQ
# cartes, comme tout set nemesis officiel.
#
# ⚠ pt017 MGH Addiction n'est PAS ici : c'est l'obligation du set `Patriot`
# (numerotee sans mention nemesis sur le scan), donc dans
# patriot/patriot/pt017.py, et elle vit dans la cle `obligations` du deck de
# depart.
#
# ---------------------------------------------------------------------------
# LE FIL ROUGE DU SET : MR. HYDE FRAPPE, OU RIEN NE SE PASSE
#
# Trois des cinq cartes impriment « Mr. Hyde attacks you. If no attack was
# made this way, ... » (pt018 en When Defeated, pt021 et pt022 en When
# Revealed). Le moteur a la brique exacte :
# `enemy.DoAttackYou(player, effect, if_no_attack_was_made=action)`, employee
# par `02040` Tail Sweep, `22031` Old Rivals et `19029` « I Will Destroy
# You! ». Le repli part aussi quand Mr. Hyde n'est PAS en jeu du tout, cas
# que `02040` traite explicitement par un `else: action()`.
#
# ---------------------------------------------------------------------------
# ⚠ COLLISION DE NOM : « Mr. Hyde » vs « Mister Hyde »
#
# Le jeu contient DEJA `24035` « Mister Hyde » (set `Mister Hyde`, pack
# `hood`). C'est le meme personnage Marvel, mais la CHAINE est differente :
# aucune collision moteur, aucune recherche croisee. On ne corrige RIEN cote
# `hood`.
#
# Le nom est ecrit SANS l'etoile d'unicite (`cards/paper.py:45-46` la
# retire) : la constante `NOM_MR_HYDE` vaut « Mr. Hyde », pas « * Mr. Hyde ».
# ===========================================================================

# `NOM_PATRIOT` et `NOM_ELIJAH` sont importes pour rester disponibles au set,
# comme chez `speed_nemesis` ; aucune carte nemesis ne les emploie
# aujourd'hui (la cible du sbire passe par `desc.Nemesis`, lu nativement).
Unused(NOM_PATRIOT, NOM_ELIJAH)
