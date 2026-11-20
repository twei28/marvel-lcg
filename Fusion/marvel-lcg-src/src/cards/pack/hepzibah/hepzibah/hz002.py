from . import *
# * Corsair (Christopher Summers), allie, cout 3, ATQ 2*, CTR 2*, 3 PV, joker.
#
# [star] Hero Response: After Corsair uses a basic power, resolve the "Special" ability on a card in your hand.
#
# Carte de reference : 50002 Nick Fury (`AfterUnitUseBasicPower(.., "This", ..)`), zeus/ze002 Hera pour le Special en main.
# « Hero Response » : sous-type dedie `AbilityType.HeroResponse` (jamais la Response nue), donc le heros doit etre en forme heros.
def GetAbilities() -> Sequence['Ability']:
    def corsair(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        ResoudreUnSpecialEnMain(effect.GetInitiator(), effect)
    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "This",
            corsair,
            conditions=[UnSpecialEnMain],
        ),
    ]
