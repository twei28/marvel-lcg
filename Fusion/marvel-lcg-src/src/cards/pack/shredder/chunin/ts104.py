from . import *

# Doroppuin (x2) — TRAITRISE (set Chunin). 1 icone de boost + etoile.
# When Revealed: Reveal the topmost minion in the encounter discard pile.
#   Otherwise, this gains surge.
# [star] Boost: If this activation is an attack, it gains piercing.
#
# Cartes de reference : `cw 56108` (`GetEncounterDiscardPile().FindTopmost`),
# `01188` (`ThisCardGainSurge` pour « otherwise, this gains surge ») ;
# `wd110` Tiger pour « if this activation is an attack, it gains piercing ».
#
# Mots-pieges : « the topmost MINION » (n'importe quel sbire, pas seulement FOOT
# CLAN) ; « Otherwise » = la defausse n'a aucun sbire ; boost : seulement si
# l'activation EST une attaque (`during_attack=True`).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if RevelerLePlusHautDeLaDefausse(effect, joueur, CardFinder(card_type=Minion)) is None:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.would_atk_message.GainPiercing(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True),
    ]
