from . import *

# hs199 In Hiding (Experience Cost 2)
# Hero Interrupt : quand un ennemi t'attaquerait, defausse In Hiding -> il manigance
# a la place, sans carte boost pour cette activation.

def GetAbilities() -> Sequence['Ability']:

    def cacher(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        from game.card.face.attribute.can_scheme import SchemeProperty
        joueur = effect.GetInitiator()
        message.SetBeInstead(effect)
        ennemi = message.attacker
        if Enemy.IsType(ennemi):
            ennemi.CastTo(Enemy).DoSchemes(joueur, effect,
                                           property=SchemeProperty(against_player=joueur, do_not_give_boost=True))

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.HeroInterrupt, Enemy, cacher, against_player="You")
        .SetCostFunc(CostFunc.Discard("This")),
    ]
