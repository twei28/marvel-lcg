from . import *

# Vault Breakout — MANIGANCE SECONDAIRE de nemesis (2/5). 3 menaces PAR
# JOUEUR, boost 2, icone de CRISE.
# When Revealed: Each player searches the encounter deck for a minion and puts
#   it into play engaged with them. Shuffle the encounter deck.
#
# ⚠ L'ICONE DE CRISE est une BASE NATIVE, `desc.Crisis` : tant que cette
# manigance est en jeu, on ne peut pas retirer de menace du complot principal.
# Un sbire par joueur ET le complot verrouille : c'est la carte qui fait
# basculer une partie.
#
# CARTE DE REFERENCE
#  - `Search.EncounterCard(effect, joueur, include_discard_pile=False,
#    card_type=Minion)` (search.py:47), qui remelange le deck fouille toute
#    seule — c'est la phrase « Shuffle the encounter deck ».
#  - `04077` * Absorbing Man : `Players.ForEachPlayer`.
#
# TEXTE CONTRE CODE
#  ⚠ « EACH player searches » : chacun fouille POUR LUI et engage le sbire avec
#    LUI. En solo cela ne se voit pas ; a quatre, cela fait quatre sbires.
#  ⚠ « the ENCOUNTER DECK », pas la defausse : `include_discard_pile=False`.
#  ⚠ Deck de rencontre sans sbire : ce joueur n'en met aucun, sans erreur.


def GetAbilities() -> Sequence['Ability']:

    def evasion(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(effect.this, message)

        def chercher(joueur: 'Player') -> None:
            sbire = Search.EncounterCard(
                effect, joueur, include_discard_pile=False, card_type=Minion)
            if sbire is not None:
                sbire.PutIntoPlay(joueur, effect)

        Players.ForEachPlayer(effect, chercher)

    return [
        AbilityFactory.WhenThisRevealed(None, evasion),
    ]
