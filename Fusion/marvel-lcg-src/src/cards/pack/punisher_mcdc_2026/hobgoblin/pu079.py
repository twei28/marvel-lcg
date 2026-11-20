from . import *

# Designs on Crimes — COMPLOT ANNEXE. Menace de depart 3 par joueur, Boost 1, Hazard 1.
# When Revealed : Discard 3[per hero] cards from the encounter deck.
# When Defeated : In player order, each player resolves the "Pumpkin Bomb" ability.
#
# Cartes de reference : jigsaw/pu065.py (`WhenSchemeBeDefeated(WhenDefeated, "This")`),
# `Worlds.DiscardEncounterCards("3*", effect)` (nombre par joueur). Hazard : natif.
#
# ⚠ « 3 PAR JOUEUR » : 3 cartes en solo, 6 a deux, etc. ; « each player resolves » : une Pumpkin Bomb PAR joueur, dans
# l'ordre des joueurs, chacune avec son joueur (celui qui prend les degats indirects).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Worlds.DiscardEncounterCards("3*", effect)

    def vaincu(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        for joueur in list(Worlds.GetPlayers(effect)):
            ResoudrePumpkinBomb(effect, joueur, 1)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
