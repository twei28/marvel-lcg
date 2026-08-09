from . import *

# Mental Gymnastics — custom « DesignHacker » (coût X)
# Hero Action (attack): Deal 2 + X damage to an enemy. Then, if you have no
# cards remaining in your hand, confuse that enemy.

def GetAbilities() -> Sequence['Ability']:

    def mental_gymnastics(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        this.DealDamage(effect.targets, 2 + effect.GetCostX(), effect)

        initiator = effect.GetInitiator()
        if len(list(initiator.hand_cards.Get())) > 0:
            return

        cibles = [x for x in effect.targets if x.IsInPlay()]
        if cibles:
            Faces.GiveStatus(cibles, "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            mental_gymnastics
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
