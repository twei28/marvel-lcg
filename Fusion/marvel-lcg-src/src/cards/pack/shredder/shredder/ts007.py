from . import *

# * Kuro Kabuto — ATTACHEMENT UNIQUE. ARMOR. FOOT CLAN. RELIC. MNG +1, etoile de boost.
# Attach to Shredder.
# Shredder gains steady.
# Forced Response: After the villain phase ends, cloak Shredder.
# Hero Action: Discard 2 cards from your hand -> discard this card.
# [star] Boost: Attach Kuro Kabuto to Shredder.
#
# Cartes de reference :
#  - `01100` / `ts006` : `AttachToFaceWhenPutIntoPlay`, `PlayerActionToDiscardThis` ;
#  - `gmw nebula/__init__` : « boost : attach this card to the villain » =
#    `message.AfterThisActivation(effect, op)` puis `this.AttachTo2(villain,
#    effect)` (une carte de boost est rangee APRES sa resolution : attacher
#    tout de suite serait ecrase) ;
#  - `ra026` / `mf003` : `CostFunc.Discard("YourHandCards", range=(2, 2))` pour
#    « discard 2 cards from your hand ».
#
# Mots-pieges : « Shredder gains STEADY » (Steady, pas Stalwart) ; « after the
# VILLAIN phase ends » ; le boost attache, il ne se contente pas de reveler.


def GetAbilities() -> Sequence['Ability']:

    def fin_de_phase(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        Cloak(effect, TrouverShredder(effect))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Attachment)

        def attacher() -> None:
            shredder = TrouverShredder(effect)
            if shredder:
                this.AttachTo2(shredder, effect)

        message.AfterThisActivation(effect, attacher)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(card_ids=IDS_SHREDDER)),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(card_ids=IDS_SHREDDER), steady=1),
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Villain", fin_de_phase),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(2, 2))),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
