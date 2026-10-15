from . import *

# * Emperor Dorrek I — MECHANT, stade 3 (Skrull Empire). SKRULL. Sans PV
# (desc HP « INF ») : l'environnement Skrull Empire encaisse a sa place.
# Retaliate 2.
# ★ Emperor Dorrek I's attacks gain ranged.
#
# Carte de reference : **`41002b`** Psi-Katana / `sk032` (meme coffret) :
# `UnitAttackGainKeyword("This", ranged=True)`. Retaliate : desc, natif.
# ⚠ « attacks gain ranged » : TOUTES ses attaques (pas « basic »). Le ★ renvoie
# au texte (convention validee le 15/10/2026), aucune valeur a ajouter.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", ranged=True),
    ]
