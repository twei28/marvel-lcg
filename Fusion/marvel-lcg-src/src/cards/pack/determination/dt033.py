from . import *

# Sustenance

def GetAbilities() -> Sequence['Ability']:

    def sustenance(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        identity = effect.GetInitiator().GetIdentity()
        villain = Worlds.FindVillain(effect)
        # « X = le numero d'etape du vilain » : c'est `printed_stage` (02029).
        supplement = villain.printed_stage if villain else 0
        this.HealthUnits([identity], 1 + supplement, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sustenance
        ).SetPlay(only_if_your_identity_has_trait="AVENGER"),
    ]
