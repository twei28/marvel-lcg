from . import *

# * Ghost Rider

def GetAbilities() -> Sequence['Ability']:

    def ghost_rider(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()

        # X est ce que le heros ENCAISSE : « for each damage your hero took
        # this way ».
        voulu = initiator.DeclareNumber(0, 3)
        avant = hero.health
        this.DealDamage([hero], voulu, effect)
        pris = avant - hero.health
        if pris > 0:
            this.GainForThisActive(effect, message, attack=pris)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            "This",
            ghost_rider
        ),
    ]
