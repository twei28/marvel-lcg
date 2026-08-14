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
        # ⚠ Le texte dit « thwarts and REMOVES THREAT », pas « removes the LAST
        # threat » : le premier jet avait pris la fabrique du dernier pion, et la
        # carte ne se declenchait qu'en achevant une manigance.
        AbilityFactory.AfterUnitThwartScheme(
            AbilityType.Response,
            "YourHero",
            Scheme2,
            fuir,
            remove_threat=True,
        ).SetPlay(),
    ]
