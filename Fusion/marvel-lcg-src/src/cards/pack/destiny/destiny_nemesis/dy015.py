from . import *

# Destiny's Warning : COMPLOT ANNEXE, menace 3[per_hero], boost 0 + [star], Incite 2. Nemesis de Destiny.
# When Revealed: Remove 1[per_hero] threat from the main scheme.
# [star] Boost: Put Destiny's Warning into play.
#
# CARTES DE REFERENCE
#  - `02027` Goblin Nation : `WhenCardBecomeBoost("This", PutThisIntoPlay)` pour « [star] Boost: Put X into play » ; fiche `boost.md` (l'etoile n'existe que par la capacite).
#  - `mt` / `hf` : `RemoveThreatFromSchemes("MainScheme", "1*", effect)` pour « 1[per_hero] threat from the main scheme ».
#  - `incite.md` : `Incite 2` lu NATIVEMENT dans `desc`.
#
# TEXTE CONTRE CODE
#  « Remove 1[per_hero] threat FROM THE MAIN SCHEME » : le complot principal, 1 par joueur (`"1*"`). « [star] Boost: PUT INTO PLAY » : comme carte de boost, le complot entre en jeu SANS « When Revealed » ni Incite.
#  Chiffres : menace 3*, boost 0, Incite 2.


def GetAbilities() -> Sequence['Ability']:

    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        this.RemoveThreatFromSchemes("MainScheme", "1*", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            when_revealed,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            PutThisIntoPlay,
        ),
    ]
