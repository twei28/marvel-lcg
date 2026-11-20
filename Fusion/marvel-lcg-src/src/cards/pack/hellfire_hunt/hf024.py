from . import *

# * Wolfsbane (Rahne Sinclair) : allie RECRUITED, cout 1, PV 2, THW 1*, ATK 1*. [star] Response.
# Response: After Wolfsbane enters play, she gets +2 ATK until the end of the round.
#
# Cartes de reference : rm002 (`AfterCardEnterPlay`/`GainUntilPhaseEnd`), `GainUntilRoundEnd(effect, attack=2)` (face_action.py:440).
def GetAbilities() -> Sequence['Ability']:
    def wolfsbane(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        this.GainUntilRoundEnd(effect, attack=2)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            wolfsbane,
        ),
    ]
