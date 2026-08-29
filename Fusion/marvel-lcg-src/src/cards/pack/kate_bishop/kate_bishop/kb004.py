from . import *

# Infiltrate
# Interrupt: When any amount of threat would be placed on a scheme, prevent 2
#   of that threat (4 instead if you are in alter-ego form).
#
# Modele du declencheur : Jennifer Walters (core/she_hulk/01019b.py),
# `AbilityFactory.WhenThreatWouldBePlacedOn(..., None, ...)` (None = « a
# scheme », pas seulement la manigance principale) + `message.PreventThreat`.


def GetAbilities() -> Sequence['Ability']:

    def infiltrate(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        valeur = 4 if initiator and initiator.IsAlterEgo() else 2
        message.PreventThreat(valeur, effect)

    return [
        AbilityFactory.WhenThreatWouldBePlacedOn(
            AbilityType.Interrupt,
            None,
            infiltrate,
        ).SetPlay(),
    ]
