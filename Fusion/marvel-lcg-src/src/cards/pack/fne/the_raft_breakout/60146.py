from . import *

# * Drang (BADOON, ELITE, PRISONER) — Villainous : base.
# [star] Forced Response: After Drang attacks you, place 1 barrage counter on
#   him. Then, take 1 indirect damage for each barrage counter on Drang.

def GetAbilities() -> Sequence['Ability']:

    def barrage(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)
        Faces.PlaceCountersOn([this], 1, 'barrage', effect)
        joueur = message.GetAgainstPlayer()  # ⚠ pas d'attribut `attacked_you` sur AfterUnitAttackEnd
        if joueur is not None:
            joueur.GetIdentity().TakeIndirectDamage(this, this.GetCounters('barrage'), effect)

    return [
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "This", barrage),
    ]
