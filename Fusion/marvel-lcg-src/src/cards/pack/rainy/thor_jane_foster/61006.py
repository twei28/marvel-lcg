from . import *

# Stand Fast — custom "Rainy"
# Hero Action: Ready Thor and Mjolnir. If you paid for this card using only
# [energy] resources, give Thor a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def stand_fast(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        to_ready = [identity]
        mjolnir = CardFinder(name="Mjolnir", card_type=Upgrade).Checks(
            initiator.GetControlCards())
        to_ready += list(mjolnir)
        Faces.ReadyAll(to_ready, effect)

        paid = getattr(effect.context, 'paid_this_resources', None)
        if paid and paid.rbyg.OnlyHasColor("Y"):
            Faces.GiveStatus([identity], "Tough", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            stand_fast
        ).SetPlay(hero_form_only=True)
    ]
