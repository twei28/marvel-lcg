from . import *

# Dark Magic

def GetAbilities() -> Sequence['Ability']:

    def dark_magic(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        deck = initiator.player_deck
        deck.Shuffle(effect)

        voulu = initiator.DeclareNumber(0, 3)
        retirees = []
        for _ in range(voulu):
            face = deck.GetTopCard()
            if face is None:
                break
            Faces.RemoveAllFromGame([face], effect)
            retirees.append(face)

        Drain(this, effect.targets, 2 * len(retirees), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            dark_magic
        ).SetPlay(only_if_your_identity_has_trait="MYSTIC")
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
