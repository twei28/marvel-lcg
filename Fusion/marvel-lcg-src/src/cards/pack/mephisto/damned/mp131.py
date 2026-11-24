from . import *

# Hell's Legions — MANIGANCE ANNEXE. Boost 2, Assault 1, menace de depart 3[per_hero] (natifs, `desc`).
# Each MYSTIC minion gains toughness. [star] Boost : Reveal this card.
#
# Cartes de reference : sm/guerrilla_tactics/27142 (`GiveKeywordToInPlayWhenApplyThis(.., toughness=1)`), `Card.Reveal(joueur, effect)` (find.md).
# ⚠ Mots-pieges : « EACH MYSTIC minion » (comme mp130) ; Boost « REVEAL this card » : la carte est revelee comme une carte de rencontre normale (Assault et When Revealed
# d'une manigance annexe jouent), par le joueur vise par l'activation.


def GetAbilities() -> Sequence['Ability']:
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetAgainstPlayer()
        if joueur is not None:
            effect.this.Reveal(joueur, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("MYSTIC", Minion), toughness=1),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
