from . import *

# Punisher's Sniper Rifle — ATTACHEMENT. ARMAMENT. WEAPON. ATQ +2★, Boost 2, Uses (1+1 par joueur compteurs).
# Attach to Punisher. Otherwise, attach to the villain. Uses (1+1[per hero] ammo counters).
# When Revealed : Discard each other ARMAMENT card in play.
# ★ Attached character's attacks gain piercing and ranged.
# ★ Forced Response : After attached character attacks, remove 1 counter from here.
#
# Cartes de reference : gs083 (`UnitAttackGainKeyword("AttachedCharacter", piercing=True, ranged=True)`), pu115.

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.RemoveCountersOn([effect.this], 1, 'ammo', effect)

    return [
        AttacherPunisherSinonVilain(),
        AbilityFactory.WhenThisRevealed(None, DefausserLesAutresArmements),
        AbilityFactory.UnitAttackGainKeyword("AttachedCharacter", piercing=True, ranged=True),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "AttachedCharacter", None, apres_attaque),
    ]
