from . import *

# * Skar — SBIRE (New Revengers). REVENGER. PV 4, MNG 1, ATQ 3 (etoile), 2 boosts.
# [star] Skar's attacks gain overkill.
# When Revealed: Exhaust a character you control.
#
# Cartes de reference :
#  - Overkill : **`mts 21145`** * Nidhogg (« [star] Nidhogg's attacks gain overkill ») /
#    `UnitAttackGainKeyword("This", overkill=True)` (modele `sk070`, meme coffret, pour `ranged`).
#  - « Exhaust a character you control » : **`trors 04136`** Bitter Rival / **`mut_gen 32073`** Avalanche :
#    `player.ChooseAbilities(effect, ForChoiceAbility(...).SetTarget("YouControlUnit", canbe_exhaust=True))`.
#
# ⚠ Mots-pieges : « a character YOU control » : le joueur qui revele CHOISIT parmi ses personnages
# (identite et allies) ; « attacks gain overkill » : toutes ses attaques ; `canbe_exhaust=True` : un
# personnage deja incline n'est pas ciblable (le joueur dont tout est incline ne perd rien).


def GetAbilities() -> Sequence['Ability']:

    def epuise(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        message.GetToPlayer().ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("", lambda cibles: Faces.ExhaustAll(cibles, effect))
            .SetTarget("YouControlUnit", canbe_exhaust=True),
        )

    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        AbilityFactory.WhenThisRevealed(None, epuise),
    ]
