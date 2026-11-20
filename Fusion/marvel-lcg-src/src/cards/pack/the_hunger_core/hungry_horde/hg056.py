from . import *

# Hungry Zombie — SBIRE (set partage « Hungry Horde », module du scenario « The Hunger Core »). Trait ZOMBIE
# (PAS METAZOMBIE : verifie directement dans data/cards_custom.json, "traits": ["ZOMBIE"] -- les sbires de ce
# set ne sont pas des Metazombies, a la difference des neuf vilains hg007-hg015 du Horde deck qui, eux, portent
# TRAIT_METAZOMBIE dans commun.py).
# SCH 0. ATK 1. PV 3. Guard 1. [star] Boost: 1.
# Guard.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - [[guard]] (docs/reference/mots-cles/guard.md) : « Guard. » -> base automatique du moteur, cle `desc.Guard`
#   deja renseignee dans cards_custom.json ("Guard": "1"), lue nativement par `HasGuard`
#   (src/game/card/face/attribute/has_guard.py) et appliquee par `Villain.CanBeAttackBy()`. La fiche le dit
#   explicitement : « Aucun script requis pour ce mot-cle ».
# - [star] Boost (icone) : badge natif (`desc.Boost`), meme regle que documentee sur hg046 (ce pack) : aucun
#   script requis (docs/reference/mots-cles/boost.md, section « icones = base automatique »).
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Carte sans capacite propre, texte imprime limite a « Guard. » : modele exact `01101` Hydra Mercenary
#   (pack `core`), cite nommement par guard.md : « Aucun fichier 01101.py trouve dans src/cards/pack : cette
#   carte n'a pas de capacite imprimee distincte necessitant un script. » Hungry Zombie est dans le meme cas :
#   SCH/ATK/HP/Guard/Boost sont tous des cles `desc` natives, zero mot-cle maison, zero declencheur a coder.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE (etape 5)
#
# Le texte imprime se limite a « Guard. » : aucun mot-piege de la liste de PROCESSUS-CARTE.md ne s'applique
# (pas de « each », pas de « you control », pas de « unless »/« instead », pas de declencheur Forced/When
# Revealed/Response/Interrupt a coder).
#
# ---------------------------------------------------------------------------
# NOMBRES TEXTE <-> CODE (etape 6)
#
# cards_custom.json hg056 : {"SCH": "0", "ATK": "1", "HP": "3", "Guard": "1", "Boost": "1"} -- toutes ces
# valeurs sont natives (lues directement depuis `desc` par le moteur) : rien a comparer cote script, puisqu'il
# n'y a aucune ligne de script portant un chiffre.
#
# ---------------------------------------------------------------------------
# A CONFIRMER
#
# Ce fichier ne contient volontairement AUCUNE Ability : par coherence avec le precedent `01101` (guard.md),
# une carte dont le SEUL texte imprime est « Guard. » n'a besoin d'aucun script, le moteur lit tout depuis
# `desc`. `GetAbilities` est quand meme fourni ici (liste vide) parce que ce fichier `hg056.py` a ete demande
# nommement comme livrable de cette tache. A CONFIRMER avec l'utilisateur si la lecture la plus stricte de la
# convention du projet (ne pas ecrire de fichier du tout pour une carte purement native, comme `01101`) doit
# prevaloir ici -- dans le doute, le fichier existe mais n'ajoute rien a ce que `desc` fait deja seul, et ne
# peut donc rien casser.


def GetAbilities() -> Sequence['Ability']:
    return []
