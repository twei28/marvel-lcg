from . import *

# Shi'ar Crest — ATTACHEMENT (Majestrix's Verdict). ITEM. Badge +1 SCH/THW. 1 icone de boost.
# Attach to Deathbird.
# Attached character gains steady.
# Response: After Lilandra attacks Deathbird, spend a [mental] resource → attach this card to Lilandra.
# [star] Boost: Give the activating enemy a tough status card.
#
# Cartes de reference :
#  - badge « +1 SCH/THW » : BASES AUTOMATIQUES `desc.SCH+` et `desc.THW+` (`has_modify.py` ->
#    `GiveKeywordToAttached(scheme=1, thwart=1)`) : +1 MNG porte par Deathbird, +1 CTR porte par Lilandra.
#  - « Attached character gains steady » : `GiveKeywordToAttached("Character", steady=1)` (fiche steady.md).
#  - Response : helper `AttacherALilandra("B")`, modele 07035.
#  - Boost : `Faces.GiveStatus([message.activating_enemy], "Tough")`, modele OFFICIEL 52037 Growing Strong.
#  - icone [mental] (noeuds relies) : verifiee par decoupe contre sk003 / sk148 (meme auteur).
#
# ⚠ Mots-pieges : « the ACTIVATING enemy » (le sbire ou le mechant qui recoit ce boost, pas forcement Deathbird).


def GetAbilities() -> Sequence['Ability']:

    def robuste(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        ennemi = getattr(message, "activating_enemy", None)
        if ennemi is not None:
            Faces.GiveStatus([ennemi], "Tough", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name=DEATHBIRD, card_type=Villain)),
        *AbilityFactory.GiveKeywordToAttached("Character", steady=1),
        AttacherALilandra("B"),
        AbilityFactory.WhenCardBecomeBoost("This", robuste),
    ]
