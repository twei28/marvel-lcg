from . import *

# Big Reach — custom « DesignHacker »
# Hero Action (attack): Deal 3 damage to the villain. Then, deal X damage to
# an enemy, where X is the number of cards remaining in your hand.

def GetAbilities() -> Sequence['Ability']:

    def big_reach(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        villain = Worlds.FindVillain(effect)
        if villain:
            this.DealDamage([villain], 3, effect)

        initiator = effect.GetInitiator()
        valeur = len(list(initiator.hand_cards.Get()))
        if valeur <= 0:
            return

        cibles = [x for x in effect.targets if x.IsInPlay()]
        if cibles:
            this.DealDamage(cibles, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            big_reach
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
