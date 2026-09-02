from . import *

# * Gorr the God Butcher (III) — VILAIN, stade III. NECROVERSE.
# SCH 2 / ATQ 3 — 19 PV par joueur.
#
# When Revealed: Advance the main scheme to stage 3A. Discard the top 5 cards
#   of each player's deck.
# Forced Response: After a player's deck runs out of cards, Gorr the God
#   Butcher activates against them.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Advance the main scheme to stage 3A » : 50088b (Batroc) fait
#   `this.Advance("3A", effect)` depuis le complot lui-meme. Ici c'est le
#   VILAIN qui pousse le complot : on recupere d'abord le complot principal en
#   jeu (`Worlds.GetMainSchemes`), puis on appelle `Advance` dessus. La cible
#   « 3A » est resolue par `main_schemes_deck.FindCard(stage=3)`
#   (world.py:916-919), d'ou l'importance du `desc.Stage` des faces.
# - « Discard the top 5 cards of each player's deck » : 01145 (Rage of Ultron),
#   `player.DiscardDeckTopCards(n, effect)`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « ADVANCE the main scheme TO STAGE 3A » -> saut explicite vers le stade 3,
#   pas un simple « stade suivant » : le vilain III peut arriver alors que le
#   complot est encore au stade 1B (jeu en expert), et le texte impose 3A.
# « EACH player's deck » -> tous les joueurs.
# « top 5 CARDS » -> 5, pas 5 par joueur : aucune icone joueur imprimee.
# Ordre : l'avancement du complot D'ABORD, la defausse ENSUITE.


def GetAbilities() -> Sequence['Ability']:

    def est_un_deck_de_joueur(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> bool:
        Unused(effect)
        return message.deck.flags.is_player_deck

    def gorr_active_contre_lui(effect: 'Effect', message: 'Message.AfterDeckRunOut') -> None:
        this = effect.this.CastTo(Villain)

        joueur = message.deck.GetOwner()
        if isinstance(joueur, Player):
            this.DoActivate(joueur, effect)

    def bienvenue_dans_les_tenebres(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this, message)

        principaux = Worlds.GetMainSchemes(effect)
        if principaux:
            principaux[0].Advance("3A", effect)

        Players.ForEachPlayer(effect, lambda joueur: joueur.DiscardDeckTopCards(5, effect))

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            bienvenue_dans_les_tenebres,
        ),
        Ability(
            AbilityType.ForcedResponse,
            Message.AfterDeckRunOut,
            [est_un_deck_de_joueur],
            gorr_active_contre_lui,
        ).SetName("Deicide"),
    ]
