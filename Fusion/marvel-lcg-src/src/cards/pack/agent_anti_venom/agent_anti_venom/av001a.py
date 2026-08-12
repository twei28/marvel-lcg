from . import *

# * Agent Anti-Venom — custom « DesignHacker »
# [star] Ten Out of Ten! — While Agent Anti-Venom has exactly 10 hit points
#   remaining, he gets +1 THW, +1 ATK, +1 DEF, and his attacks gain piercing.

def GetAbilities() -> Sequence['Ability']:

    def dix_sur_dix(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Hero)
        return 1 if this.health == TEN else 0

    return [
        AbilityFactory.ThisGainKeyword(
            dix_sur_dix,
            thwart=1,
            attack=1,
            defense=1,
            change_on_event=OnEvent.Health("This"),
        ).SetName("Ten Out of Ten!"),

        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
            conditions=[
                lambda effect, message:
                    effect.this.CastTo(Hero).health == TEN
            ],
        ).SetName("Ten Out of Ten!"),
    ]
