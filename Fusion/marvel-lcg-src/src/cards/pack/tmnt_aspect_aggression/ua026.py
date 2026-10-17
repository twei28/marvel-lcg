from . import *

# * Leatherhead — ALLIE 4 [physical], ATK 3 (2 degats consecutifs), THW 1 (1), PV 4. ALLIGATOR. MUTANIMAL.
# Response: After Leatherhead attacks and defeats a minion, heal 2 damage from him.
#
# CARTE DE REFERENCE : `01051` * Tigra (« After Tigra attacks and defeats a minion, heal 1 damage from her ») =
#   `AfterUnitAttackAndDefeatUnit(Response, "This", Minion, ...)` + `.SetTarget("This", canbe_heal=True)`.
#   Ici 2 au lieu de 1.
# ⚠ ORDRE MOTEUR (ability_type.py, TimingPriority) : les degats CONSECUTIFS sont la DERNIERE etape, apres les
#   Reponses. Leatherhead soigne donc les degats qu'il portait AVANT l'attaque, puis prend ses 2 consecutifs,
#   exactement comme Tigra. Mesure : cas `[ua] ua026` (2 degats prealables -> 2 a la fin, et non 4). Un
#   Leatherhead intact ne se voit pas proposer la Reponse (rien a soigner a ce moment).
# TEXTE CONTRE CODE
#  ⚠ « a MINION » (pas le vilain) ; « attacks AND defeats » ; « heal 2 damage from HIM » (Leatherhead).


def GetAbilities() -> Sequence['Ability']:

    def leatherhead(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.HealthUnits([effect.this], 2, effect)

    return [
        AbilityFactory.AfterUnitAttackAndDefeatUnit(
            AbilityType.Response,
            "This",
            Minion,
            leatherhead,
        ).SetTarget("This", canbe_heal=True),
    ]
