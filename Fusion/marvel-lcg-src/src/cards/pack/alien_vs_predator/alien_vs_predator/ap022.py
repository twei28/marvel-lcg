from . import *

# Chestburster — ATTACHEMENT. CONDITION. ATK +2. Boost 2.
# Attach to a [[XENOMORPH]] minion. Otherwise attach to the active villain.
# [star] Forced Interrupt: When attached enemy attacks, this attack gains piercing. At the end of this attack, stun your identity and discard
#   this card.
#
# Cartes de reference :
#  - « Attach to X. Otherwise attach to Y » : `AttachToFaceWhenPutIntoPlay(.., otherwise_attach_to=)` ; ATK +2 natif ;
#  - « this attack gains piercing » : `UnitAttackGainKeyword("AttachedEnemy", piercing=True)` (27059) ;
#  - « At the end of this attack » : `AfterUnitAttackEnd(ForcedResponse, "AttachedEnemy")` ; « stun your identity » : `GiveStatus("Stunned")`.
#
# ⚠ Mots-pieges :
#  - « YOUR identity » : le joueur attaque (celui de l'allie si un allie est vise) ;
#  - « Otherwise attach to the ACTIVE villain » (pas « the villain ») ; aucune cible : la carte reste sans hote (defaussee) ;
#  - une seule attaque : la carte part a la fin de la premiere.


def GetAbilities() -> Sequence['Ability']:

    def fin_d_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this
        joueur = None
        atk = getattr(message, "would_atk_message", None)
        if atk is not None and atk.property is not None:
            joueur = atk.property.against_player
        if not Player.IsType(joueur):
            joueur = JoueurDuMessage(message, effect)
        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Minion, trait="XENOMORPH"),
                                                   otherwise_attach_to=Select.From(CardFinder(card_type=Villain,
                                                                                             check_face_fn=lambda f: f.IsActive()))),
        AbilityFactory.UnitAttackGainKeyword("AttachedEnemy", piercing=True),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "AttachedEnemy", fin_d_attaque),
    ]
