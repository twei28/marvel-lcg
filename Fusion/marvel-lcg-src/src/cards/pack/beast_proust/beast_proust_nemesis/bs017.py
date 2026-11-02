from . import *

# High-Tech Glasses : ATTACHEMENT, boost 3, ATQ +1, SCH +1.
# Attach this card to Black Beast. If you cannot, attach it to the villain.
# Hero Action: Discard an upgrade you control -> discard this attachment.
#
# CARTES DE REFERENCE
#  - `ar013` : `AttachToFaceWhenPutIntoPlay(CardFinder(..), if_cannot_attach_to=Villain)` ; `01099` Charge / `01141` Program Transmitter : `desc` `ATK+` / `SCH+` lus NATIVEMENT.
#  - `01100` Enhanced Ivory Horn : `Hero Action` de defausse de l'attachement ; `tc001a` : `CostFunc.Discard("YouControlCards", card_type=Upgrade)`.
#
# TEXTE CONTRE CODE
#  « Attach to BLACK BEAST. If you cannot, attach it to the VILLAIN » : Black Beast s'il est en jeu, sinon le vilain. « Discard AN upgrade YOU CONTROL → discard this attachment » : n'importe quelle amelioration du joueur
#    (cout), l'attachement part. Le bonus +1 ATQ / +1 SCH est dans `desc` (aucun script). « Hero Action » : forme heros.
#  Chiffres : boost 3, ATQ +1, SCH +1.


def GetAbilities() -> Sequence['Ability']:

    def lunettes(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(message)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_BLACK_BEAST),
            if_cannot_attach_to=Villain,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lunettes,
        ).SetCostFunc(CostFunc.Discard("YouControlCards", card_type=Upgrade)),
    ]
