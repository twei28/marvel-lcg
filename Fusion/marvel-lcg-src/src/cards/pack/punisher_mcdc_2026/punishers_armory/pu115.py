from . import *

# Punisher's Shotgun — ATTACHEMENT. ARMAMENT. WEAPON. ATQ +1★, Boost 1, Uses (2 ammo par joueur).
# Attach to Punisher. Otherwise, attach to the villain. Uses (2[per hero] ammo counters).
# When Revealed : Discard each other ARMAMENT card in play.
# ★ Forced Response : After attached character attacks, remove 1 ammo counter from here and stun the attack's target.
#
# Cartes de reference : jigsaw/pu058.py, gs083 (attache), 27174a (`Faces.RemoveCountersOn`), pu064 (`GiveStatus
# "Stunned"`). Uses et ATK+ : natifs (`desc`, fiche mots-cles/uses.md).
# ⚠ « the attack's TARGET » : le defenseur s'il y en a un, sinon la cible ; tout ce qui est attaque, pas seulement
# contre un joueur ; la carte part d'elle-meme quand le dernier compteur est retire.

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this
        Faces.RemoveCountersOn([this], 1, 'ammo', effect)
        cible = message.defender or message.attacked
        Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AttacherPunisherSinonVilain(),
        AbilityFactory.WhenThisRevealed(None, DefausserLesAutresArmements),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "AttachedCharacter", None, apres_attaque),
    ]
