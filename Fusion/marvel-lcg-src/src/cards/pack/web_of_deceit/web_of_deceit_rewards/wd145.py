from . import *

# Flee the Scene

def GetAbilities() -> Sequence['Ability']:

    def fuir(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        # « Response: After your hero thwarts and removes threat from a scheme,
        # take 1 damage → ready your hero. »
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        this.DealDamage([joueur.GetIdentity()], 1, effect)
        Faces.ReadyAll([joueur.GetIdentity()], effect)

    return [
        AbilityFactory.AfterUnitThwartAndRemoveLastThreat(
            AbilityType.Response,
            "YourHero",
            fuir
        ).SetPlay(),
    ]
