from . import *

# Silence the City (2A) — MANIGANCE PRINCIPALE.
# When Revealed : Deal each player an encounter card.
# (In campaign mode, record the location where the final LEAD card was added to the victory display.)
#
# Cartes de reference : `player.DealEncounterCards(1, effect)` (gmw/16118, ar012), gs161a (`WhenThisRevealed`).
# ⚠ « each player » : chacun des joueurs (pas le seul premier) ; la parenthese de campagne (noter le lieu de la derniere piste) ecrit le
# carnet (`campaign.py` : `NoterLeLieuDeLaDernierePiste`) et n'a aucun effet hors campagne. « the final LEAD card » = la derniere ajoutee a la
# pile de victoire : le DESSUS de la pile (`Get(True)[0]`), prouve par un cas a deux pistes.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        for joueur in TousLesJoueurs(effect):
            joueur.DealEncounterCards(1, effect)
        # (In campaign mode, record the location where the final LEAD card was added to the victory display.)
        pistes = PistesEnVictoire(effect)
        NoterLeLieuDeLaDernierePiste(effect, pistes[0] if pistes else None)

    return [AbilityFactory.WhenThisRevealed(None, revele)]
