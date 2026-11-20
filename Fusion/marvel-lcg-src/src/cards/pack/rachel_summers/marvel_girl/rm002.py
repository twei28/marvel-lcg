from . import *

# * Captain Britain (Betsy Braddock) — ALLIE, cout 2, PV 3, ATK 1*, THW 1*. PSIONIC. X-FORCE.
# Response: After your turn begins, Captain Britain gets +1 ATK and +1 THW until the end of the phase.
#
# CARTES DE REFERENCE : `22001a` (`AfterPlayerTurnBegin(Response, "You", ..)`), `03003` (`GainUntilPhaseEnd`).
def GetAbilities() -> Sequence['Ability']:
    def captain_britain(effect: 'Effect', message: 'Message.AfterPlayerTurnBegin') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.GainUntilPhaseEnd(effect, attack=1, thwart=1)

    return [
        AbilityFactory.AfterPlayerTurnBegin(
            AbilityType.Response,
            "You",
            captain_britain,
        ),
    ]
