from . import *

# In the Crosshairs — ATTACHEMENT. TARGETED. Setup. Permanent.
# Attached character gets +5[per hero] hit points, gains the TARGETED trait, and cannot be affected by player cards.
# If attached character's current stage is defeated, the players lose the game.
#
# Cartes de reference : `AbilityFactory.GiveKeywordToAttached(finder, health=..., trait=...)` (asset.py),
# `AbilityFactory.CannotBeAffectedByPlayerCards("AttachedCharacter")` (brique commune §15.2), `AttachToFaceWhenPutIntoPlay`,
# `WhenUnitBeDefeated(WhenDefeated, ...)` (sk167), `Worlds.SetGameOver(False, effect)`.
# ⚠ « current stage is DEFEATED » : n'importe quel stade du sous-fifre (I, II...), pas seulement le dernier ; « +5 PAR joueur » :
# 5 x nombre de joueurs ; l'attache vise le vilain UNDERLING (la mise en place de pu090a la met en jeu).

def GetAbilities() -> Sequence['Ability']:

    def pv_supplementaires(effect: 'Effect') -> int:
        return 5 * len(list(Worlds.GetPlayers(effect)))

    def defaite_des_joueurs(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Worlds.SetGameOver(False, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Villain, trait="UNDERLING")),
        *AbilityFactory.GiveKeywordToAttached(Villain, health=pv_supplementaires, trait="TARGETED"),
        AbilityFactory.CannotBeAffectedByPlayerCards("AttachedCharacter"),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "AttachedCharacter", defaite_des_joueurs),
    ]
