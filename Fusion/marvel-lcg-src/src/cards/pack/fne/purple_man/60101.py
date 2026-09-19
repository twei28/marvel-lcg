from . import *

# Firefighter (CIVILIAN, INFLUENCED) — Vulnerable : base.
# [star] Firefighter's attacks gain piercing.
# When Defeated: Discard the highest-cost support or upgrade from play.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        cartes = Worlds.FindCardsOnField(effect, card_type=Support|Upgrade)
        cible = Filter.One(cartes, effect, highest_cost=True)
        if cible:
            Faces.DiscardAll([cible], effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
