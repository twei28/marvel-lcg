from . import *

# Demon Amalgam — SBIRE MYSTIC. PV 1, ATK 3, SCH 0, Boost 2, Toughness 1, Vulnerable 1, Teamwork (MYSTIC) (natifs, `desc`).
# [star] Demon Amalgam gets +1 hit point for each damned counter on it.
# When Revealed : Place X damned counters on Demon Amalgam, where X is equal to the number of MYSTIC minions in the encounter discard pile.
#
# Cartes de reference : skrull_pantheon/sk178 (`ThisGainKeyword(.., health=1, change_on_event=OnEvent.Counter(..))`), compteur `damned` (card_face.py).
# ⚠ Mots-pieges : « MYSTIC MINIONS in the ENCOUNTER DISCARD PILE » (defausse de rencontre, trait MYSTIC, sbires seulement) ; « +1 hit point for EACH counter » : PV
# supplementaires qui suivent le nombre de compteurs ; le texte etoile est constant.


def GetAbilities() -> Sequence['Ability']:
    def compteurs(effect: 'Effect', ui: List['CardFace']) -> int:
        Unused(ui)
        return effect.this.CastTo(Minion).GetCounters('damned')

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        x = len([f for f in Worlds.GetEncounterDiscardPileCards(effect) if Minion.IsType(f) and f.HasTrait("MYSTIC")])
        if x > 0:
            Faces.PlaceCountersOn([effect.this.CastTo(Minion)], x, 'damned', effect)

    return [
        AbilityFactory.ThisGainKeyword(compteurs, health=1, change_on_event=OnEvent.Counter("This", "damned")),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
