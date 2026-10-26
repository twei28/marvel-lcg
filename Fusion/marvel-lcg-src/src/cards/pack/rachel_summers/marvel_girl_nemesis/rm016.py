from . import *

# Hound Clothes (x3) — ATTACHEMENT (nemesis), boost 1 + [star]. WEAPON. « Max 1 per identity. »
# Attach to your identity. Otherwise, this card gains surge.
# You get -1 hand size.
# Hero Action: Exhaust your identity -> discard this card.
# [star] Boost: Discard 1 card at random from your hand.
#
# CARTES DE REFERENCE : `32150` Wrapped in Metal (`desc.MaxPerUnit` + `AttachToFaceWhenPutIntoPlay("YourIdentity")` +
# `PlayerActionToDiscardThis(..).SetCostFunc(CostFunc.Exhaust("YourIdentity"))`), `01163` / `rz019`
# (`if_cannot_gain_surge=True`), `27154` (boost : `message.GetToPlayer().DiscardRandomHandCards(n, effect)`).
#
# MOTS-PIEGES : « Max 1 PER IDENTITY » (un second exemplaire ne s'attache pas : il gagne Renfort) ; « -1 hand size » vaut
# pour l'identite portant la carte ; la Hero Action n'est jouable qu'en forme heros.
def GetAbilities() -> Sequence['Ability']:
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(effect.this)
        message.GetToPlayer().DiscardRandomHandCards(1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            hand_size=-1,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
