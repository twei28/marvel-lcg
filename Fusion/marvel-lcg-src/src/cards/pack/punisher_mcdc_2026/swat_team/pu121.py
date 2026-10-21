from . import *

# Riot Police — SBIRE x2. POLICE. SCH 1★, ATQ 0, 6 PV, Boost 1, Guard, Retaliate 2, Toughness.
# Guard. Retaliate 2. Toughness.
# ★ When Riot Police schemes, place that threat on SWAT, if able.
# Hero Action : Spend 1 resource of any type and discard an ally you control → discard Riot Police and remove 2 threat
#   from SWAT.
#
# Cartes de reference : `MenaceSurSwat()`, jigsaw/pu058.py (`PlayerActionToDiscardThis`), magneto/49019.py
# (`CostFunc.Discard("YourAlly")`), rainy/rescue_rainy/90123.py (`CostFunc.Spend(Cost("1"))`).
# ⚠ « 1 resource of ANY type » : `Cost("1")` ; « discard an ALLY you control » : cout (allie en jeu) ; « remove 2 threat
# FROM SWAT » : meme sans « vaincre » SWAT (Permanent) ; Guard, Retaliate, Toughness : natifs.

def GetAbilities() -> Sequence['Ability']:

    def retirer_deux(effect: 'Effect', message: 'Message2') -> None:
        from game.card.face.attribute.can_place_token import CanPlaceToken
        swat = TrouverSwat(effect)
        if swat is not None and swat.threat > 0:
            CanPlaceToken.RemoveTokensInternal(swat, min(2, swat.threat), 'threat', effect, forced=True)

    return [
        MenaceSurSwat(),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction, ex_operation=retirer_deux)
        .SetCostFunc(CostFunc.Spend(Cost("1")))
        .SetCostFunc(CostFunc.Discard("YourAlly")),
    ]
