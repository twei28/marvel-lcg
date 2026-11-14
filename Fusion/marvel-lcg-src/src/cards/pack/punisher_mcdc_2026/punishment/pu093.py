from . import *

# Punisher's Assault Rifle — ATTACHEMENT. ARMAMENT. WEAPON. ATQ +1★, Boost 1, Uses (2 ammo par joueur).
# Attach to Punisher. Uses (2[per hero] ammo counters).
# When Revealed : Discard each other ARMAMENT card in play.
# ★ Punisher's attacks gain overkill. His overkill damage on minions is dealt to the TARGETED villain.
# ★ Forced Response : After Punisher attacks, remove 1 ammo counter from here.
#
# Cartes de reference : punishers_armory/pu115.py (`AttacherPunisherSinonVilain`, `DefausserLesAutresArmements`),
# `UnitAttackGainKeyword("AttachedCharacter", overkill=True)`. L'exces d'un coup sur un sbire va au vilain cible : branche
# `overkill_to` de `PunisherAttaque` (__init__.py) pour les attaques de Punisher sur un ennemi.
# ⚠ « After Punisher attacks » : toute attaque (sur un joueur, un ennemi ou un allie).

from ..punishers_armory import DefausserLesAutresArmements

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.RemoveCountersOn([effect.this], 1, 'ammo', effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Punisher", card_type=Villain)),
        AbilityFactory.WhenThisRevealed(None, DefausserLesAutresArmements),
        AbilityFactory.UnitAttackGainKeyword("AttachedCharacter", overkill=True),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "AttachedCharacter", None, apres_attaque),
    ]
