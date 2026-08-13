from . import *

# Thorn in Their Side

def GetAbilities() -> Sequence['Ability']:

    def thorn_in_their_side(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()

        this.RemoveThreatFromSchemes(effect.targets, 2, effect)

        # « you MAY take up to 5 damage » : 0 est un choix legitime, la
        # declaration de nombre suffit donc a porter le « may ».
        voulu = initiator.DeclareNumber(0, 5)
        avant = hero.health
        hero.TakeDamage(this, voulu, effect)
        pris = avant - hero.health
        if pris > 0:
            RepartirLeRetraitDeMenace(this, initiator, pris, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            thorn_in_their_side
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
