from . import *

# Psychic Aegis (ATTACHEMENT PSIONIC). Setup. « Attach to the villain. Attached character cannot be confused. Attached character cannot take damage
# from a player while that player is confused. Action : Spend [mental][mental] resources -> discard this card. [star] Boost : Reveal this card. »
# Cartes de reference : 16149 Power Stone (Setup + `AttachToFaceWhenPutIntoPlay(Villain)`), mt012 (`UnitCannotBeConfused`), sk147 Distracted (Cost("BB")
# + `PlayerActionToDiscardThis`), `PlayersCannotDamageUnit` (player.py), hf110 (boost `RevealThisCard`).
# ⚠ « Action » (pas Hero Action) : jouable aussi en alter-ego ; [mental] = icone « noeuds » (verifie contre hf110 : RES = B) ; « confused » : l'ETAT
# du joueur (son identite), lu au moment des degats.


def GetAbilities() -> Sequence['Ability']:
    def joueur_confus(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        joueur = message.by_effect.initiator
        return Player.IsType(joueur) and joueur.GetIdentity().IsConfused()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.UnitCannotBeConfused("AttachedCharacter"),
        AbilityFactory.PlayersCannotDamageUnit("AnyPlayer", "AttachedCharacter", conditions=[joueur_confus]),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.Action).SetCost(Cost("BB")),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
