from . import *

# Hand Blademaster — SBIRE, HAND. PV 3, ATQ 1*, MAN 1*, 1 icone de boost. Nemesis 4/5.
# [star] +1 MAN et +1 ATQ s'il y a un AUTRE sbire HAND en jeu. When Defeated : se melange dans le paquet de rencontre.
#
# CARTES DE REFERENCE : `hs160` / `hs163` (`ThisGainKeyword(check, ..., change_on_event=OnEvent.CardInPlay(...))`), `50098`.
# ⚠ « ANOTHER HAND minion » : lui-meme ne compte pas. Le bonus vaut +1, pas +1 par sbire.


def GetAbilities() -> Sequence['Ability']:

    def autre_main(effect: 'Effect', ui: List['CardFace']) -> int:
        autres = [f for f in Worlds.FindCardsOnField(effect, trait=TRAIT_MAIN, card_type=Minion) if f != effect.this]
        ui.extend(autres)
        return 1 if autres else 0

    return [
        AbilityFactory.ThisGainKeyword(autre_main, scheme=1, attack=1,
                                       change_on_event=OnEvent.CardInPlay(CardFinder(trait=TRAIT_MAIN))),
        MelangerQuandVaincu(),
    ]
