from . import *

# * Honey Badger: Gabby Kinney
# Hero Response: After Honey Badger takes any amount of damage, ready
#   Wolverine.
#
# Copie de Honey Badger (43003). Meme substitution de cible que wx002 : le
# « Wolverine » du texte est celui qui controle Gabby.


def GetAbilities() -> Sequence['Ability']:

    def honey_badger(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            "This",
            honey_badger
        ).SetTarget("YourIdentity", canbe_ready=True),
    ]
