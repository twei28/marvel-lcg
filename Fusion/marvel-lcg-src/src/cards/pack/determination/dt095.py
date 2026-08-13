from . import *

# Last Legs

def GetAbilities() -> Sequence['Ability']:

    def last_legs(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        allies = [a for a in initiator.GetAllies() if a.HasTrait("X-MEN")]
        if not allies:
            return
        valeur = sum(a.CastTo(CanHealth).health for a in allies)
        Faces.DiscardAll(allies, effect)
        if valeur <= 0:
            return

        RepartirLeRetraitDeMenace(this, initiator, valeur, effect)

        ennemis = [x for x in Worlds.FindCardsOnField(effect, card_type=Enemy)
                   if not x.IsDefeated()]
        if ennemis:
            initiator.AssignDamage(ennemis, this, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            last_legs
        ).SetPlay(only_if_your_identity_has_trait="X-MEN")
        .SetLabel('attack', 'thwart'),
    ]
