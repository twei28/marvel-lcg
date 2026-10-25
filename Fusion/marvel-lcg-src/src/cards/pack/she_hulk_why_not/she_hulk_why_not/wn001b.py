from . import *

# * Jennifer Walters (variante Why Not, Merlin)
# "I Object!" — Interrupt: When threat would be placed on a scheme, prevent 1
# of that threat. (Limit once per PHASE.)
#
# Modele 01019b, a la limite pres : l'auteur a remplace « round » par « phase ».


def GetAbilities() -> Sequence['Ability']:

    def jennifer_walters(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        message.PreventThreat(1, effect)

    return [
        AbilityFactory.WhenThreatWouldBePlacedOn(
            AbilityType.Interrupt,
            None,
            jennifer_walters
        ).SetName('"I Object!"')
        .LimitOncePerPhase(),
    ]
