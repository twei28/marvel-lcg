from . import *

# * Koya — SBIRE UNIQUE (Foot Goon Squad). AERIAL. FALCON. FOOT CLAN.
# MNG 2 / ATQ 1 / PV 2, etoile de boost. Incite 1. Quickstrike.
# When Revealed: Heal 2 damage from the villain.
# [star] Boost: Place 1 threat on the main scheme and heal 2 damage from the villain.
#
# Cartes de reference : `aoa four_horsemen` (`this.HealthUnits([villain], 2,
# effect)`), `hs160` / `ts004b` (`PlaceThreatOnSchemes("MainScheme", 1, effect)`) ;
# Incite et Quickstrike lus dans `desc`.
#
# Mots-pieges : « heal 2 damage FROM THE VILLAIN » (pas d'elle-meme) ; « place 1
# threat ON THE MAIN SCHEME » ; les deux effets du boost, dans cet ordre.


def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect') -> None:
        villain = Worlds.FindVillain(effect)
        if villain:
            effect.this.HealthUnits([villain], 2, effect)

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        soigner(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        effect.this.PlaceThreatOnSchemes("MainScheme", 1, effect)
        soigner(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
