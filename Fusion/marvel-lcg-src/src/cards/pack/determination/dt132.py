from . import *

# Enraged Energy

def GetAbilities() -> Sequence['Ability']:

    # `DoubleResourcesThisGenerates` ne prend pas de condition : on ecrit donc
    # la fonction de ressources a la main, sur le modele de ce que cette
    # fabrique produit (resources.py:36).
    def enraged_energy(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        this = effect.this.CastTo(Resource)

        res = this.printed_resource
        hero = effect.GetInitiator().GetHero()
        if hero is not None and hero.health < hero.starting_health/2:
            res *= 2
        return res

    return [
        AbilityFactory.CheckThisCanDropPay(
            enraged_energy,
        ),
    ]
