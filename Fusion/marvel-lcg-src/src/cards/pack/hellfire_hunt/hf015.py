from . import *

# * Dazzler (Alison Blaire) : allie RECRUITED, cout 2, PV 2, THW 1*, ATK 1*.
# Response: After Dazzler enters play, confuse up to 2 minions.
#
# Carte de reference : 01083 Mockingbird (`AfterCardEnterPlay(Response, "This")` + `SetTarget(Enemy, canbe_stunned=True)` + `Faces.GiveStatus`).
# ⚠ « up to 2 MINIONS » : sbires seulement (pas le vilain), de 0 a 2 cibles.
def GetAbilities() -> Sequence['Ability']:
    def dazzler(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Faces.GiveStatus(effect.targets, "Confused", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            dazzler,
        ).SetTarget(Minion, range=(0, 2), canbe_confused=True),
    ]
