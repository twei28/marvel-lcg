from . import *

# Multiverse Shenanigans

def GetAbilities() -> Sequence['Ability']:

    # APPROXIMATION ECRITE, et c'est la plus large de l'aspect.
    #
    # La carte dit « choisissez 3 cartes d'aspect non-Determination DE VOTRE
    # COLLECTION ». Une collection n'existe pas dans le moteur : il ne connait
    # que les cartes du deck et celles du scenario. Les trois cartes mises de
    # cote sont donc prises DANS VOTRE DECK, ce qui garde l'esprit (piocher
    # hors du hasard, une fois par partie) sans inventer une zone que le jeu
    # n'a pas.
    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        if player is None:
            return
        for _ in range(3):
            face = Search.PlayerCard(
                effect, player,
                include_player_deck=True,
                include_discard_pile=False,
                may=True,
                finder=CardFinder(non_card_class="Determination"),
            )
            if face is None:
                break
            this.TuckCardUnderHere(face, effect)

    def multiverse_shenanigans(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        mises_de_cote = list(this.GetPlacedCardArea().Get())
        if player is None or not mises_de_cote:
            return
        face = player.MayChooseOneText(mises_de_cote)
        if face:
            player.GainCard(face, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenGameBeginSetup(mise_en_place).NoOutOfPlayLimit(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            multiverse_shenanigans
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealPlayerEncounterCard(1, "Initiator")),
    ]
