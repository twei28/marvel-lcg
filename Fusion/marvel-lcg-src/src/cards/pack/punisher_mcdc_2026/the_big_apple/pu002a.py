from . import *

# Silence the City (2A) — MANIGANCE PRINCIPALE.
# When Revealed : Deal each player an encounter card.
# (In campaign mode, record the location where the final LEAD card was added to the victory display.)
#
# Cartes de reference : `player.DealEncounterCards(1, effect)` (gmw/16118, ar012), gs161a (`WhenThisRevealed`).
# ⚠ « each player » : chacun des joueurs (pas le seul premier) ; la parenthese de campagne (noter le lieu de la derniere piste) est une
# ecriture du carnet de campagne : a brancher en PU-9 (mode campagne), PAS ici ; hors campagne elle n'a aucun effet.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        for joueur in TousLesJoueurs(effect):
            joueur.DealEncounterCards(1, effect)

    return [AbilityFactory.WhenThisRevealed(None, revele)]
