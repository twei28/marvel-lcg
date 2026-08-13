from . import *

# Whatever it Takes

def GetAbilities() -> Sequence['Ability']:

    # « Alliance » ne fait rien par lui-meme : il nomme ce que le texte demande
    # deja (un X-MEN et un X-FORCE).
    def whatever_it_takes(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        total = 0
        for cible in effect.targets:
            voulu = initiator.DeclareNumber(0, 3)
            avant = cible.CastTo(CanHealth).health
            this.DealDamage([cible], voulu, effect)
            total += avant - cible.CastTo(CanHealth).health

        if total <= 0:
            return
        RepartirLeRetraitDeMenace(this, initiator, total, effect)
        ennemis = [x for x in Worlds.FindCardsOnField(effect, card_type=Enemy)
                   if not x.IsDefeated()]
        if ennemis:
            initiator.AssignDamage(ennemis, this, total, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            whatever_it_takes
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget(CardFinder(trait="X-MEN", card_type=Unit2), range=(1, 1))
        .SetTarget2(CardFinder(trait="X-FORCE", card_type=Unit2), range=(1, 1)),
    ]
