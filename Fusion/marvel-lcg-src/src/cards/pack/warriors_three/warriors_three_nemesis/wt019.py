from . import *


def GetAbilities() -> Sequence['Ability']:
    def gleipnir(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        Unused(message)
        message.GetGaveToPlayer().DealEncounterCards(1, effect)

    def libere(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        fenris = en_jeu(effect, "Fenris", Minion)
        if fenris is not None:
            Faces.DiscardAll([fenris], effect)

    def en_renfort(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        # `GetInitiator()` leve une AssertionError quand l'effet vient du vilain (le boost) : on revele au premier joueur.
        effect.this.Reveal(effect.world.GetFirstPlayer(), effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(gleipnir),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, libere)
        .SetCost(Cost('3'))
        .SetCostFunc(CostFunc.Discard("This")),
        AbilityFactory.WhenCardBecomeBoost("This", en_renfort),
    ]
