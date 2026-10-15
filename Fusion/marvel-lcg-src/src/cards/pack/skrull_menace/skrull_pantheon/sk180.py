from . import *

# Strengthen the Faith (x2, 180) — COMPLOT ANNEXE. Menace 2[per_hero], 1 icone Y + etoile de boost.
# Forced Response: After a SKRULL minion enters play, place 1 faith counter on the villain.
# ★ Boost: Place 1 faith counter on the villain.
#
# Cartes de reference : **`hunting_season/hs222`** (`AfterCardEnterPlay(ForcedResponse, CardFinder(trait=...,
# card_type=Minion), op)`) ; boost : `WhenCardBecomeBoost("This", op)` (modele sk113).
#
# ⚠ Mots-pieges : « a SKRULL MINION » (trait SKRULL ET type sbire : ni le mechant, ni un allie) ; « AFTER ...
# enters play » (Reponse) ; « on the VILLAIN » ; une copie par exemplaire en jeu (deux copies = deux jetons) ;
# le sbire qui entre peut etre Nogor lui-meme.


def GetAbilities() -> Sequence['Ability']:

    def entree(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        PoserFoi(effect, 1)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        PoserFoi(effect, 1)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, CardFinder(trait="SKRULL", card_type=Minion), entree),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
