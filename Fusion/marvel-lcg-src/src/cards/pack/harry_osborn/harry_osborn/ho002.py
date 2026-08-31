from . import *

# * Spider-Man (Peter Parker) — allie signature. EARTH-6160. WEB-WARRIOR.
# Cout 4 / PV 3 / THW 2* / ATK 2*
# Response: After Spider-Man enters play, place a total of 2 stun status
#   cards on up to 2 enemies.
#
# Cartes de reference : 01083 * Mockingbird (« After Mockingbird enters play,
# stun an enemy »), meme montage `AfterCardEnterPlay(Response, "This", ...)`
# + `Faces.GiveStatus(..., "Stunned", ...)`, et 14006 Speed Cyclone pour la
# cible multiple `SetTarget(Enemy, range=...)`.
#
# ⚠ « a TOTAL of 2 ... on UP TO 2 enemies » : la repartition est libre —
# 1 cible choisie = elle recoit les 2 stun, 2 cibles = 1 stun chacune. Les
# stuns s'empilent sur le vilain, c'est le sens meme du « total ».

def GetAbilities() -> Sequence['Ability']:

    def spider_man(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        cibles = [t for t in effect.targets if t is not None]
        if not cibles:
            return
        if len(cibles) == 1:
            Faces.GiveStatus(cibles, "Stunned", effect)
            Faces.GiveStatus(cibles, "Stunned", effect)
        else:
            Faces.GiveStatus(cibles[:2], "Stunned", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            spider_man
        ).SetTarget(Enemy, range=(1, 2), canbe_stunned=True)
    ]
