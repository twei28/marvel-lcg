from . import *

# Inner Strength — EVENEMENT, cout 1, RES [physical]. ATTACK.
# Hero Action (attack): Deal damage to an enemy equal to your ATK and THW
#   combined.
#
# CARTES DE REFERENCE
#  - `25018` Quick Strike : « deal damage to an enemy equal to your ATK ».
#  - `29017` Go All Out : la somme de plusieurs caracteristiques du heros.
#
# TEXTE CONTRE CODE
#  ⚠ Jumelle exacte de vz010, l'autre bout de la paire : celle-ci frappe avec
#    ATQ+CTR, celle-la contre avec CTR+DEF. Le CTR est dans les deux.
def GetAbilities() -> Sequence['Ability']:

    def inner_strength(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        heros = effect.GetInitiator().GetHero()
        this.DealDamage(effect.targets, heros.attack + heros.thwart, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            inner_strength
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
