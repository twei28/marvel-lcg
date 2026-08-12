from . import *

# Guard Protocol — custom « Kajislav »
# Hero Action: Until the end of the round Albert gains retaliate 1 while in
# hero form. Give Albert a tough status card. If he already has a tough
# status card, resolve Albert's "Initiate Protocol" ability.

def GetAbilities() -> Sequence['Ability']:

    def guard_protocol(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()

        already_tough = hero.IsTough()

        hero.GainUntilRoundEnd(
            effect,
            retaliate=1,
        )
        Faces.GiveStatus([hero], "Tough", effect)

        if already_tough:
            ResolveInitiateProtocol(effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            guard_protocol
        ).SetPlay().SetLabel(),
    ]
