from . import *

# Unwavering — ATTACHEMENT (Accuser Corps). CONDITION. ATK +3[star]. 1 etoile + 1 icone de boost. 2 exemplaires.
# Attach to an enemy.
# [star] Forced Response: After attached enemy attacks and damages a character, discard this card.
# [star] Boost: Attach to an enemy.
#
# Cartes de reference :
#  - « Attach to an enemy » : `AttachToFaceWhenPutIntoPlay(Enemy)`, modele courant (ex. hood 24038).
#  - « After attached enemy attacks and damages a character, discard this card » :
#    `AfterUnitAttackAndDamageUnit(ForcedResponse, "AttachedEnemy", "Character", ...)`, modele gs076 Kree
#    Sentry (meme pack) adapte a « AttachedEnemy » plutot que « This ».
#  - « Boost: Attach to an enemy » : `message.activating_enemy` + `AttachTo2`, modele gs157 (meme pack).
#
# ⚠ Mots-pieges : « attacks AND DAMAGES » (aucun degat = rien) ; le badge « ATK +3 » est une bonification
# statique de l'ennemi porteur, lue native (`desc.ATK+`), pas un module.


def GetAbilities() -> Sequence['Ability']:

    def defausser(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Unused(message)
        Faces.DiscardAll([effect.this], effect)

    def booster(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        ennemi = message.activating_enemy
        if ennemi is not None:
            effect.this.CastTo(Attachment).AttachTo2(ennemi, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Enemy),
        AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, "AttachedEnemy", "Character", defausser),
        AbilityFactory.WhenCardBecomeBoost("This", booster),
    ]
