from . import *

# Power Surge (2A)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        # « Exhaust each friendly TECH support and upgrade. »
        materiel = Worlds.FindCardsOnField(effect, trait="TECH", card_type=Support)
        materiel += Worlds.FindCardsOnField(effect, trait="TECH", card_type=Upgrade)
        if materiel:
            Faces.ExhaustAll(materiel, effect)

        def par_joueur(joueur: 'Player') -> None:
            # « Each player discards cards from the encounter deck until they
            # discard an A.I.M. minion, then reveals that minion. »
            sbire = Worlds.DiscardEncounterCardsUntil(
                effect,
                trait="A.I.M",
                card_type=Minion,
            )
            if sbire:
                sbire.Reveal(joueur, effect)

            # « Each player searches their deck and discard pile for a card with
            # a printed [energy] resource and adds it to their hand. »
            trouvee = Search.SearchForCard(
                effect,
                joueur,
                include_player_deck=True,
                include_player_discard_pile=True,
                has_printed_res='Y',
            )
            if trouvee:
                Faces.AddToHand([trouvee], joueur, effect)

        Players.ForEachPlayer(effect, par_joueur)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
