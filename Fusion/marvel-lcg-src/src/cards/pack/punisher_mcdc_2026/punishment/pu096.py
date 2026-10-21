from . import *

# Mexican Standoff — ATTACHEMENT. CONFRONTATION. Boost 1. Attach to Punisher.
# Forced Response : After you attack Punisher, he activates. Then, the TARGETED villain activates against you. Do not give
#   either character a boost card for these activations. Discard this card.
#
# Cartes de reference : `Enemy.DoActivate(joueur, effect, do_not_give_boost=True)` (enemy.py),
# `AfterUnitAttackUnit(ForcedResponse, "You", "AttachedCharacter")` (pu086a pour le cote joueur).
# ⚠ « After YOU attack Punisher » : le joueur qui l'a attaque ; Punisher s'active contre ce joueur ; PUIS le vilain cible
# s'active contre lui aussi ; AUCUNE carte de boost pour ces deux activations ; la carte est ensuite defaussee.

def GetAbilities() -> Sequence['Ability']:

    def face_a_face(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this
        joueur = message.trigger.GetControlByPlayer() or Worlds.GetFirstPlayer(effect)
        punisher = Punisher(effect)
        cible = VilainCible(effect)
        if punisher is not None:
            punisher.CastTo(Enemy).DoActivate(joueur, effect, do_not_give_boost=True)
        if cible is not None:
            cible.CastTo(Enemy).DoActivate(joueur, effect, do_not_give_boost=True)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Punisher", card_type=Villain)),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "You", "AttachedCharacter", face_a_face),
    ]
