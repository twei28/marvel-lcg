from . import *

# Spider-Sense — custom « Rainy »
# Hero Interrupt: When the villain or a villainous minion initiates an attack
#   against you, draw 1 card.
# Hero Interrupt: When a boost card is turned faceup during an attack against
#   you, discard 1 card from your hand -> cancel that boost card's boost
#   ability.

def GetAbilities() -> Sequence['Ability']:

    def pioche(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)

    def vilain_ou_villainous(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        attaquant = message.attacker
        if Villain.IsType(attaquant):
            return True
        if Minion.IsType(attaquant) and HasVillainous.IsType(attaquant):
            return attaquant.IsVillainous()
        return False

    def annule_boost(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        message.CancelBoostAbility(effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            pioche,
            against_player="You",
            conditions=[vilain_ou_villainous],
        ).SetName("Spider-Sense (draw)"),

        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.HeroInterrupt,
            "Ability",
            annule_boost,
            while_attack=True,
            activate_target="You",
        ).SetName("Spider-Sense (cancel boost)")
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
