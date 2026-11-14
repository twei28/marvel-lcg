from . import *

# Welcome to Sunnydale — COMPLOT ANNEXE (nemesis 1/5). Menace 3, Hinder 1[per_hero], boost 1.
# Each VAMPIRE minion gains 1 acceleration icon. [star] Boost: Reveal this card.
#
# CARTES DE REFERENCE
#  - `50085` Mad Science / `30031` Bora : `GiveKeywordToInPlayWhenApplyThis(CardFinder2(trait, Minion), acceleration_icon=1)`.
#  - `16140` Sound the Alarms : `WhenCardBecomeBoost("This", RevealThisCard)` pour « Boost: Reveal this card ».
#
# TEXTE CONTRE CODE
#  « Hinder 1[per_hero] » -> `desc.Hinder = "1*"` (base automatique). « each VAMPIRE minion » -> TOUS les sbires VAMPIRE (de tout joueur).
#  « acceleration icon » -> `acceleration_icon=1`. Le boost de la carte est « 1 » : lu SUR LE SCAN (une icone + l'etoile), a verifier.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder2("VAMPIRE", Minion),
            acceleration_icon=1,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
        ),
    ]
