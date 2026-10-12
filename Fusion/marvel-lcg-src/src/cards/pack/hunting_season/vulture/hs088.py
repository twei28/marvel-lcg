from . import *

# hs088 Wing Harness
# Attach to Vulture. * Forced Interrupt : Vulture attaque un personnage AERIAL, +1 ATK.
# Hero Action : epuisez votre heros, defaussez 2 cartes -> defaussez ceci, Vulture perd AERIAL jusqu'a la fin du tour.

def GetAbilities() -> Sequence['Ability']:

    def cible_aerial(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return PorteurEstAttaquant(effect, message) and any(t.HasTrait("AERIAL") for t in message.attacked_targets)

    def plus_un(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainATKForThisAttack(1, effect)

    return [
        AttacherALaRevelation(),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Villain, plus_un, conditions=[cible_aerial]),
        ActionPerdreAerial(None, CostFunc.Exhaust("YourHero"), CostFunc.Discard("YourHandCards", range=(2, 2))),
    ]
