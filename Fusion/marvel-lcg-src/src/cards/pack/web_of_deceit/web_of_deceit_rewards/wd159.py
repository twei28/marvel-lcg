from . import *

# Web Swing!

def GetAbilities() -> Sequence['Ability']:

    def elan(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Hero Action: Ready your hero. Your identity gets +1 to each of its
        # basic powers until the end of the round. »
        joueur = effect.GetInitiator()
        identite = joueur.GetIdentity()
        Faces.ReadyAll([identite], effect)
        identite.GainUntilRoundEnd(
            effect, attack=1, thwart=1, defense=1, recover=1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            elan
        ).SetPlay(),
    ]
