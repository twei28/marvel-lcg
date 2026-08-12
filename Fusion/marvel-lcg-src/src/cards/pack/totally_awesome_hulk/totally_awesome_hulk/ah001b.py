from . import *

# * Amadeus Cho — custom « DesignHacker »
# Reverse Engineer — Action: Discard a hero-specific card from your hand →
#   draw X cards, where X is the printed cost of the card you discarded this
#   way. (Limit once per round.)


def GetAbilities() -> Sequence['Ability']:

    def reverse_engineer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        initiator = effect.GetInitiator()

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=False,
            include_player_hand_cards=True,
            card_class="IdentitySpecific",
        )
        if face is None:
            return

        # Le coût IMPRIMÉ, lu avant la défausse.
        value = FacesCounter.GetTotalCost([face])
        Faces.DiscardAll([face], effect)
        if value > 0:
            initiator.DrawUp(value, effect)

    return [
        # « Losing Control » de la face ah001a doit AUSSI valoir ici : c'est en
        # quittant l'alter-ego que le moteur propose les deux formes heros.
        LosingControlGuard(),
        # « The Trunk » (Setup) est UNE carte a deux faces mise de cote : elle
        # se declare "ah012a,ah012b" dans le deck et arrive en jeu par ici, sur
        # le modele de Vision (26002a/b) et de Phoenix (34002a/b). La cle
        # `Setup` de cards.json ne conviendrait pas : ProcessSetup ne parcourt
        # que le deck du joueur, jamais les cartes mises de cote.
        AbilityFactory.SetupPutIntoPlay(
            ["ah012a,ah012b"],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            reverse_engineer,
        ).SetName("Reverse Engineer")
        .LimitOncePerRound(),
    ]
