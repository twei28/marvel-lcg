from . import *


def GetAbilities() -> Sequence['Ability']:
    def revealed_identity(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.against_player        # l'initiateur de l'effet est le MECHANT qui s'active
        mechant = message.trigger
        message.SetBeInstead(effect)
        mechant.DoAttackYou(joueur, effect)
        this.PlaceThreatOnSchemes("MainScheme", 2, effect)     # « after that attack »

    def se_defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.ForcedInterrupt,
            Villain,
            revealed_identity,
            against_player="You",
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            se_defausser,
            conditions=[ActionPayable("2", avec_firepower=False)],
        ).SetCost(Cost("2")),
    ]
