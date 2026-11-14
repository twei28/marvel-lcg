from . import *

# * Kree Leader (I) — MECHANT, stade 1, face A (HIDDEN). KREE. PV 15[per_hero]. SCH 2. ATK : etoile (non chiffree,
#   la moitie attaque de HIDDEN remplace toute attaque, voir mots-cles/hidden.md).
# The villain cannot be affected by player cards. Attachments attached to the villain cannot be discarded.
# [star] Forced Interrupt: When the villain would attack you, deal yourself a facedown encounter card instead.
#
# Cartes de reference :
#  - « cannot be affected by player cards » : brique commune du 20/10/2026, deja codee
#    (`AbilityFactory.CannotBeAffectedByPlayerCards`, mots-cles/immunite-cartes-joueur.md).
#  - « Attachments attached to the villain cannot be discarded » : `WhenCardWouldDiscard` + `SetBeInstead`,
#    modele `skrull_menace/paibok/__init__.py` (`RegleDesPouvoirs`).
#  - « the villain would attack you ... deal yourself a facedown encounter card instead » : mecanique NEUVE,
#    fiche `docs/reference/mots-cles/hidden.md`. `Message.WhenUnitWouldAttack` + `message.SetBeInstead(effect)`
#    (modele `AbilityFactoryEnemy.EnemyCannotActivate`) + `Player.DealEncounterCards` (modele ar012 Ares,
#    sk248 Skrull Elite War Skrull).
#
# ⚠ Mots-pieges : « the villain » = This (une seule face active a la fois) ; « would attack YOU » = un
# joueur precis (`against_player`), jamais un allie ; l'ATK de la face HIDDEN n'est jamais utilisee (etoile
# non chiffree, aucune attaque ne va au bout tant que HIDDEN est present).


def GetAbilities() -> Sequence['Ability']:
    return CapacitesKreeLeader()
