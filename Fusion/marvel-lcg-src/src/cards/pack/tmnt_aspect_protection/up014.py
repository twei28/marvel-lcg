from . import *

# * Grotto (bandeau « Iron Fist ») — ALLIE 4 [physical], aspect Protection (TMNT Aspects, Inkwire).
# DIMENSION X. NOVA POSSE. THW 1 (1), ATK 2 (1), PV 3.
# Grotto enters play with 2 brute counters on him.
# Interrupt: When Grotto attacks an enemy, remove 1 brute counter from him -> stun that enemy and deal 1
#   damage to it.
#
# Texte de `09014` Iron Fist au nom du COMPTEUR pres (« brute » au lieu de « mystic ») : le module de
# 09014 ecrit 'mystic' en dur, un ability_link poserait des compteurs mystic. Script propre, copie de 09014.
#
# CARTE DE REFERENCE : `09014` Iron Fist (copie ligne a ligne, seul le nom du compteur change).
#
# TEXTE CONTRE CODE
#  ⚠ « 2 BRUTE counters » ; « remove 1 brute counter » = cout ; « stun THAT enemy and deal 1 damage TO IT » :
#    la cible de l'attaque, les deux effets.


def GetAbilities() -> Sequence['Ability']:

    def grotto(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Ally)
        Faces.GiveStatus(effect.targets, "Stunned", effect)
        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'brute'),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.Interrupt,
            "This",
            Enemy,
            grotto,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'brute'))
        .SetTarget("Targets", range="All"),
    ]
