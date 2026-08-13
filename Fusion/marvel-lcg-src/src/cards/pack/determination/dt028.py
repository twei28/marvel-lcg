from . import *

# Pay It Forward

def GetAbilities() -> Sequence['Ability']:

    def pay_it_forward(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()

        # X est ce que le heros ENCAISSE, pas ce qu'on lui inflige : une armure
        # qui previent une partie des degats reduit d'autant l'effet.
        voulu = initiator.DeclareNumber(0, 3)
        avant = hero.health
        hero.TakeDamage(this, voulu, effect)
        pris = avant - hero.health
        if pris <= 0:
            return

        ennemis = [x for x in Worlds.FindCardsOnField(effect, card_type=Enemy)
                   if not x.IsDefeated()]
        if ennemis:
            initiator.AssignDamage(ennemis, this, pris, effect)

        RepartirLeRetraitDeMenace(this, initiator, pris, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            pay_it_forward
        ).SetPlay().SetLabel('attack', 'thwart'),
    ]
