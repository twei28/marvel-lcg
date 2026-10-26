from . import *

def GetAbilities() -> Sequence['Ability']:
    def exige(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> bool:
        """« a card with the requirement keyword » : la carte jouee imprime un Requirement."""
        Unused(effect)
        exigence = getattr(message.played_face, "requirement", None)
        return exigence is not None and exigence.val > 0

    def maitre_de_tous_les_metiers(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        Unused(message)
        PlusUneTailleDeMain(effect, IdentiteDe(effect))

    return [
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.Interrupt,
            "You",
            None,
            maitre_de_tous_les_metiers,
            conditions=[exige],
        ).SetName("Master of All Trades")
        .LimitOncePerPhase(),
    ]
