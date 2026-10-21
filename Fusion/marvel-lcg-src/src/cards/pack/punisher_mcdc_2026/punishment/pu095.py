from . import *

# Punisher's M1911s — ATTACHEMENT. ARMAMENT. WEAPON. ATQ +1★, Boost 2, Uses (2 ammo par joueur).
# Attach to Punisher. Uses (2[per hero] ammo counters).
# When Revealed : Discard each other ARMAMENT card in play.
# ★ Punisher's attacks gain ranged.
# ★ Forced Response : After Punisher attacks, remove 1 ammo counter from here.
#
# Cartes de reference : pu093, hobgoblin/pu071a (`UnitAttackGainKeyword("This"/"AttachedCharacter", ranged=True)`).

from ..punishers_armory import DefausserLesAutresArmements

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.RemoveCountersOn([effect.this], 1, 'ammo', effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Punisher", card_type=Villain)),
        AbilityFactory.WhenThisRevealed(None, DefausserLesAutresArmements),
        AbilityFactory.UnitAttackGainKeyword("AttachedCharacter", ranged=True),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "AttachedCharacter", None, apres_attaque),
    ]
