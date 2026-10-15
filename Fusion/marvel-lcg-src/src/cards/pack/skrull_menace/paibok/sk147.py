from . import *

# Distracted — ATTACHEMENT x2 (Paibok). CONDITION. Etoile de boost (pas d'icone chiffree).
# Attach to your identity.
# Forced Interrupt: When you thwart, reduce the amount of threat that thwart removes by 1.
# Hero Action: Spend [mental][mental] resources → discard this card.
# [star] Boost: Place 1 threat on the main scheme.
#
# Cartes de reference :
#  - Attache a l'identite : **`27166`** Webbed Up (`AttachToFaceWhenPutIntoPlay("YourIdentity")`).
#  - Retrait de menace moindre : `message.RemoveAdditionalThreat(-1, effect)` sur
#    `WhenUnitWouldThwart` (sender_friend.py:64) ; fenetre de l'attache : `AbilityFactory.WhenUnitWouldThwart`
#    (thwart.py:40), PAS `WhenAttachedPlayerWouldThwart` (do_thwart.py ecoute l'ATTAQUE par erreur de
#    copie dans le moteur d'origine).
#  - Cout 2 mentales : **`gmw 16123`** Obedience Potion / `Cost("BB")` ; defausse : `PlayerActionToDiscardThis`.
#  - Boost : `this.PlaceThreatOnSchemes("MainScheme", 1, effect)` (modele 50134).
#
# ⚠ Mots-pieges : « When YOU thwart » = l'identite attachee (pas un allie) ; « by 1 » est un -1 sur la
# menace retiree (jamais en dessous de 0) ; [mental] = nœuds, `B` (verifie contre sk057 Mister Fantastic,
# meme auteur : RES=B) ; « Hero Action » : jouable en forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def distrait(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        message.RemoveAdditionalThreat(-1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        effect.this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenUnitWouldThwart(AbilityType.ForcedInterrupt, "AttachedIdentity", distrait),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("BB")),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
