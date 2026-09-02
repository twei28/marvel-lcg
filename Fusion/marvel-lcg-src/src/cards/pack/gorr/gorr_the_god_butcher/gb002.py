from . import *

# * Gorr the God Butcher (II) — VILAIN, stade II. NECROVERSE.
# SCH 2 / ATQ 2 — 16 PV par joueur.
#
# When Revealed: Deal each player 1 facedown encounter card.
# Forced Response: After a player's deck runs out of cards, Gorr the God
#   Butcher activates against them.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Deal each player 1 facedown encounter card » : 24001 (The Hood) passe par
#   `player.DealEncounterCard` ; ici la formulation est la forme standard sans
#   filtre, donc `player.DealEncounterCards(1, effect)`
#   (player/action/player_action.py:54), avec `Players.ForEachPlayer` pour le
#   « each player » (modele hood/the_hood/__init__.py:19-25).
# - La Reponse Obligatoire est celle de gb001, mot pour mot : meme montage,
#   meme condition. Elle n'est PAS factorisee dans le `__init__` du set a
#   dessein : les trois stades sont trois cartes distinctes, et un helper
#   partage masquerait qu'un stade puisse un jour diverger.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « EACH player » -> tous les joueurs, pas le joueur actif seul.
# « FACEDOWN » -> c'est le comportement par defaut de `DealEncounterCards` :
#   la carte est distribuee face cachee et se revelera a la phase du vilain.
# « When Revealed » sur un VILAIN -> se declenche quand ce stade est revele,
#   donc a la mise en place ou a l'avancement, pas a chaque tour.


def GetAbilities() -> Sequence['Ability']:

    def est_un_deck_de_joueur(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> bool:
        Unused(effect)
        return message.deck.flags.is_player_deck

    def gorr_active_contre_lui(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> None:
        this = effect.this.CastTo(Villain)

        joueur = message.deck.GetOwner()
        if isinstance(joueur, Player):
            this.DoActivate(joueur, effect)

    def une_carte_rencontre_chacun(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this, message)

        Players.ForEachPlayer(effect, lambda joueur: joueur.DealEncounterCards(1, effect))

    return [
        # `None` = aucune condition de forme (la fabrique n'accepte que
        # "Alter-Ego", "Hero", None ou un predicat : reveal.py:118-127).
        AbilityFactory.WhenThisRevealed(
            None,
            une_carte_rencontre_chacun,
        ),
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterDeckRunOut,
            [est_un_deck_de_joueur],
            gorr_active_contre_lui,
        ).SetName("Deicide"),
    ]
