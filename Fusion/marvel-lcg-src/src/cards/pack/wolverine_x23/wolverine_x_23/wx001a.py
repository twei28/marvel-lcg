from . import *

# * Wolverine
# Living Weapon — Response: After Wolverine takes any amount of damage,
#   ready Wolverine. (Limit once per phase.)
#
# Copie de X-23 (43001a). Aucun ciblage par nom ici : « This » designe la
# carte elle-meme, donc rien a borner.


def GetAbilities() -> Sequence['Ability']:

    def wolverine(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "This",
            wolverine
        ).SetName("Living Weapon")
        .SetTarget("This", canbe_ready=True)
        .LimitOncePerPhase(),
    ]
