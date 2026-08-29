from . import *

# * Ayo
# Response: After Ayo enters play, all other DORA MILAJE allies you control
#   get +1 THW until the end of the phase.
#
# Modele : ok002 (Aneka), meme structure, THW au lieu d'ATK.


def GetAbilities() -> Sequence['Ability']:

    def ayo(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)

        autres = [f for f in Worlds.FindCardsOnField(effect, trait="DORA MILAJE", card_type=Ally) if f is not this]
        for face in autres:
            face.GainUntilPhaseEnd(effect, thwart=1)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            ayo,
        ),
    ]
