from . import *

# Shielded Drop
# Play only if Red Guardian's Shield is in your hand.
# Hero Action (thwart): Remove 5 threat from a scheme.
#
# Modele : To the Rescue! (10019), au chiffre et a la condition de jeu pres.
# Le bouclier reste en main — la carte se contente de le lire.


def GetAbilities() -> Sequence['Ability']:

    def shielded_drop(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        this.RemoveThreatFromSchemes(list(effect.targets), 5, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            shielded_drop,
            conditions=[BouclierEstEnMain],
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
